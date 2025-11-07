from catboost import CatBoostClassifier, Pool
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score
import os
from datetime import datetime
from sqlalchemy.orm import Session
from ..models import Client, Product, Feedback, Response, Transaction, AccountBalance, ClientProduct
from ..classifier import extract_client_features
from .embeddings import EmbeddingsGenerator

MODEL_DIR = '/app/ml_model/saved_models'

class CatBoostRecommender:
    def __init__(self, db: Session):
        self.db = db
        self.models = {}  # product_type -> CatBoost model
        self.embeddings_gen = EmbeddingsGenerator(db, embedding_dim=16)
        self.feature_names = []
        
    def prepare_training_data(self):
        """Extract features + embeddings for training"""
        print("Preparing training data with embeddings...")
        
        # Train embeddings first
        self.embeddings_gen.train_client_embeddings()
        self.embeddings_gen.train_product_embeddings()
        
        # Get all feedback
        feedbacks = self.db.query(Feedback).all()
        if len(feedbacks) < 10:
            print(f"Not enough feedback ({len(feedbacks)}), need at least 10")
            return None
        
        data_rows = []
        
        for fb in feedbacks:
            client = self.db.query(Client).filter(Client.id == fb.client_id).first()
            if not client:
                continue
            
            product = self.db.query(Product).filter(Product.product_id == fb.product_id).first()
            if not product:
                continue
            
            # Client features
            features = extract_client_features(self.db, client.client_id)
            if not features or features.get('months_count', 0) < 2:
                continue
            
            # Build feature vector
            row = self._build_feature_row(client.client_id, product, features)
            row['target'] = 1 if fb.accepted else 0
            row['product_type'] = product.product_type
            
            data_rows.append(row)
        
        if len(data_rows) < 10:
            print(f"Not enough valid samples ({len(data_rows)})")
            return None
        
        df = pd.DataFrame(data_rows)
        print(f"Prepared {len(df)} training samples")
        print(f"Positive: {df['target'].sum()}, Negative: {len(df) - df['target'].sum()}")
        
        return df
    
    def _build_feature_row(self, client_id: str, product: Product, client_features: dict) -> dict:
        """Build feature row with structured features + embeddings"""
        row = {}
        
        # === CLIENT FEATURES (10) ===
        row['avg_income'] = client_features.get('avg_income', 0) / 100000
        row['avg_expense'] = client_features.get('avg_expense', 0) / 100000
        row['savings_rate'] = client_features.get('savings_rate', 0)
        row['balance'] = client_features.get('balance', 0) / 100000
        row['income_stability'] = client_features.get('income_stability', 0)
        row['health_score'] = client_features.get('health_score', 0) / 100
        row['months_count'] = min(12, client_features.get('months_count', 0)) / 12
        row['owned_products_count'] = len(client_features.get('owned_ids', set())) / 5
        row['income_cv'] = client_features.get('income_cv', 0)
        row['expense_exceeds_income'] = 1.0 if client_features.get('avg_expense', 0) > client_features.get('avg_income', 0) * 0.95 else 0.0
        
        # === EXPENSE DISTRIBUTION (7) ===
        for cat in ['food', 'transport', 'housing', 'entertainment', 'salary', 'bonus', 'other']:
            row[f'expense_{cat}'] = client_features.get('expense_dist', {}).get(cat, 0)
        
        # === PRODUCT FEATURES (6) ===
        row['product_type'] = product.product_type  # categorical
        row['interest_rate'] = float(product.interest_rate or 0) / 20
        row['min_amount'] = float(product.min_amount or 0) / 100000
        row['max_amount'] = float(product.max_amount or 0) / 500000
        row['term_months'] = float(product.term_months or 0) / 36
        row['has_min_amount'] = 1.0 if product.min_amount and product.min_amount > 0 else 0.0
        
        # === CLIENT-PRODUCT INTERACTION (5) ===
        if product.min_amount:
            row['can_afford'] = 1.0 if client_features.get('balance', 0) >= float(product.min_amount) else 0.0
        else:
            row['can_afford'] = 1.0
        
        row['owns_same_type'] = client_features.get('owned_types', {}).get(product.product_type, 0) / 3
        
        # Response alignment
        resp = client_features.get('responses', {})
        goal = resp.get('financial_goal', '')
        
        if product.product_type == 'deposit':
            row['goal_match'] = 1.0 if 'накопления' in goal or 'инвестиции' in goal else 0.0
        elif product.product_type == 'loan':
            row['goal_match'] = 1.0 if 'покупка' in goal or 'долг' in goal else 0.0
        elif product.product_type == 'card':
            row['goal_match'] = 1.0 if 'покупка' in goal else 0.5
        else:
            row['goal_match'] = 0.0
        
        # Spending style
        spend = resp.get('spending_style', '')
        if 'всё что зарабатываю' in spend:
            row['spending_style_enc'] = 0.0
        elif '10-20%' in spend:
            row['spending_style_enc'] = 0.33
        elif 'больше 20%' in spend:
            row['spending_style_enc'] = 0.66
        else:
            row['spending_style_enc'] = 0.5
        
        # Risk comfort
        comfort = resp.get('risk_comfort', '')
        if 'надёжность' in comfort:
            row['risk_comfort_enc'] = 0.0
        elif 'гибкость' in comfort:
            row['risk_comfort_enc'] = 0.5
        else:
            row['risk_comfort_enc'] = 1.0
        
        # === EMBEDDINGS SIMILARITY (1) ===
        row['embedding_similarity'] = self.embeddings_gen.cosine_similarity(client_id, product.product_id)
        
        # === CLIENT EMBEDDING FEATURES (16) ===
        client_emb = self.embeddings_gen.get_client_embedding(client_id)
        for i in range(len(client_emb)):
            row[f'client_emb_{i}'] = client_emb[i]
        
        # === PRODUCT EMBEDDING FEATURES (16) ===
        product_emb = self.embeddings_gen.get_product_embedding(product.product_id)
        for i in range(len(product_emb)):
            row[f'product_emb_{i}'] = product_emb[i]
        
        return row
    
    def train_models(self):
        """Train CatBoost models per product type"""
        df = self.prepare_training_data()
        
        if df is None:
            return {'success': False, 'message': 'Not enough training data'}
        
        # Store feature names (exclude target and product_type)
        self.feature_names = [col for col in df.columns if col not in ['target', 'product_type']]
        
        cat_features = ['product_type']
        results = {}
        
        # Train separate model for each product type
        for ptype in ['deposit', 'loan', 'card']:
            df_type = df[df['product_type'] == ptype].copy()
            
            if len(df_type) < 5:
                print(f"Not enough samples for {ptype} ({len(df_type)}), skipping")
                continue
            
            if len(df_type['target'].unique()) < 2:
                print(f"Need both positive and negative samples for {ptype}, skipping")
                continue
            
            X = df_type[self.feature_names]
            y = df_type['target']
            
            # Split data
            if len(X) < 10:
                X_train, y_train = X, y
                X_val, y_val = X, y
            else:
                X_train, X_val, y_train, y_val = train_test_split(
                    X, y, test_size=0.2, random_state=42, stratify=y
                )
            
            # Identify categorical features indices
            cat_indices = [i for i, col in enumerate(self.feature_names) if col in cat_features]
            
            # Train CatBoost
            train_pool = Pool(X_train, y_train, cat_features=cat_indices)
            val_pool = Pool(X_val, y_val, cat_features=cat_indices)
            
            print(f"\nTraining CatBoost for {ptype}...")
            model = CatBoostClassifier(
                iterations=300,
                learning_rate=0.05,
                depth=6,
                eval_metric='AUC',
                verbose=50,
                random_seed=42,
                l2_leaf_reg=3,
                bootstrap_type='Bernoulli',
                subsample=0.8
            )
            
            model.fit(
                train_pool,
                eval_set=val_pool,
                early_stopping_rounds=30,
                verbose=False
            )
            
            # Evaluate
            y_pred = model.predict_proba(X_val)[:, 1]
            try:
                auc = roc_auc_score(y_val, y_pred)
                print(f"AUC for {ptype}: {auc:.4f}")
            except:
                auc = 0.5
            
            # Feature importance
            feat_importance = model.get_feature_importance()
            top_features = sorted(zip(self.feature_names, feat_importance), key=lambda x: x[1], reverse=True)[:5]
            
            self.models[ptype] = model
            results[ptype] = {
                'auc': auc,
                'train_samples': len(X_train),
                'val_samples': len(X_val),
                'top_features': [{'name': name, 'importance': float(imp)} for name, imp in top_features]
            }
        
        # Save models
        self._save_models()
        
        return {
            'success': True,
            'models_trained': list(results.keys()),
            'metrics': results,
            'embedding_dim': self.embeddings_gen.embedding_dim,
            'timestamp': datetime.utcnow().isoformat()
        }
    
    def _save_models(self):
        """Save CatBoost models"""
        os.makedirs(MODEL_DIR, exist_ok=True)
        
        for ptype, model in self.models.items():
            path = os.path.join(MODEL_DIR, f'catboost_{ptype}.cbm')
            model.save_model(path)
            print(f"Saved CatBoost model for {ptype} to {path}")
    
    def load_models(self):
        """Load pre-trained models"""
        # Load embeddings
        emb_loaded = self.embeddings_gen.load_embeddings()
        
        # Load CatBoost models
        for ptype in ['deposit', 'loan', 'card']:
            path = os.path.join(MODEL_DIR, f'catboost_{ptype}.cbm')
            if os.path.exists(path):
                try:
                    model = CatBoostClassifier()
                    model.load_model(path)
                    self.models[ptype] = model
                    print(f"Loaded CatBoost model for {ptype}")
                except Exception as e:
                    print(f"Error loading model for {ptype}: {e}")
        
        return len(self.models) > 0 and emb_loaded
    
    def predict_score(self, client_id: str, product: Product, client_features: dict) -> float:
        """Predict acceptance probability"""
        if product.product_type not in self.models:
            return 0.5
        
        # Build feature row
        row = self._build_feature_row(client_id, product, client_features)
        
        # Remove target and product_type if present
        row = {k: v for k, v in row.items() if k not in ['target', 'product_type']}
        
        # Create DataFrame
        X = pd.DataFrame([row])
        
        # Predict
        model = self.models[product.product_type]
        score = model.predict_proba(X)[0, 1]
        
        return float(score)