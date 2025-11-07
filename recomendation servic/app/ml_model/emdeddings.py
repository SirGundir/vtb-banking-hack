from sqlalchemy.orm import Session
from . import models
from .ml_model.trainer import CatBoostRecommender
from decimal import Decimal
from collections import defaultdict, Counter
import math

DEFAULT_CLIENT_QUESTIONS = [
    {
        "key": "financial_goal", 
        "text": "Какая ваша основная финансовая цель на ближайший год?", 
        "options": ["накопления", "покупка крупной вещи", "погашение долгов", "инвестиции"],
    },
    {
        "key": "spending_style", 
        "text": "Как вы обычно распоряжаетесь деньгами?", 
        "options": ["трачу всё что зарабатываю", "откладываю 10-20%", "откладываю больше 20%", "непостоянный доход"],
    },
    {
        "key": "risk_comfort", 
        "text": "Что для вас важнее?", 
        "options": ["надёжность и стабильность", "гибкость условий", "максимальная выгода"],
    }
]

CATEGORY_KEYWORDS = {
    'salary': ['зарплат', '💼', 'заработ', 'salary'],
    'food': ['продукт', 'еда', 'магазин', '🏪', '🍏'],
    'transport': ['трансп', 'транспорт', 'такси', 'bus', 'metro', '🚌'],
    'entertainment': ['развлеч', 'кино', 'cinema', '🎬', 'покупки'],
    'housing': ['жкх', 'аренд', '🏠'],
    'bonus': ['подраб', 'бонус', '💰'],
}

def init_default_questions(db: Session):
    existing = db.query(models.Question).count()
    if existing == 0:
        for q in DEFAULT_CLIENT_QUESTIONS:
            question = models.Question(key=q['key'], text=q['text'])
            db.add(question)
        db.commit()

def detect_category(text: str) -> str:
    if not text:
        return 'other'
    txt = text.lower()
    for cat, keys in CATEGORY_KEYWORDS.items():
        for k in keys:
            if k in txt:
                return cat
    return 'other'

def safe_decimal(x):
    try:
        return Decimal(str(x))
    except:
        return Decimal('0')

def extract_client_features(db: Session, client_id: str, months_back: int = 10):
    """Extract client financial features"""
    client = db.query(models.Client).filter(models.Client.client_id == client_id).first()
    if not client:
        return None

    txs = db.query(models.Transaction).filter(models.Transaction.client_id == client.id).all()

    income_by_month = defaultdict(Decimal)
    expense_by_month = defaultdict(Decimal)
    expense_by_cat = defaultdict(Decimal)
    months = set()

    for t in txs:
        if not t.value_dt or t.amount is None:
            continue
        try:
            m = t.value_dt.strftime('%Y-%m')
        except:
            continue
        months.add(m)
        amt = safe_decimal(t.amount)
        if t.credit:
            income_by_month[m] += amt
        else:
            expense_by_month[m] += amt
            cat = detect_category(t.info or '')
            expense_by_cat[cat] += amt

    months = sorted([m for m in months if m != 'unknown'], reverse=True)[:months_back]
    months_count = len(months)

    if months_count > 0:
        avg_income = sum(income_by_month[m] for m in months) / months_count
        avg_expense = sum(expense_by_month[m] for m in months) / months_count
    else:
        avg_income = Decimal('0')
        avg_expense = Decimal('0')

    savings_rate = Decimal('0')
    if avg_income > 0:
        savings_rate = max(Decimal('0'), (avg_income - avg_expense) / avg_income)

    balances = db.query(models.AccountBalance).filter(
        models.AccountBalance.client_id == client.id
    ).order_by(models.AccountBalance.as_of.desc()).all()
    balance_sum = sum((b.balance or 0) for b in balances) if balances else Decimal('0')

    owned = db.query(models.ClientProduct).filter(models.ClientProduct.client_id == client.id).all()
    owned_types = Counter()
    owned_ids = set()
    for op in owned:
        prod = db.query(models.Product).filter(models.Product.product_id == op.product_id).first()
        if prod:
            owned_types[prod.product_type] += 1
            owned_ids.add(prod.product_id)

    responses = db.query(models.Response).filter(models.Response.client_id == client.id).all()
    resp_map = {r.question_key: r.answer for r in responses}

    total_exp = sum(expense_by_cat.values()) if expense_by_cat else Decimal('0')
    exp_dist = {}
    for k, v in expense_by_cat.items():
        exp_dist[k] = float(v / total_exp) if total_exp > 0 else 0.0

    incomes = [float(income_by_month[m]) for m in months]
    income_stability = 0.0
    income_cv = 1.0
    if incomes and len(incomes) > 1:
        mean = sum(incomes) / len(incomes)
        var = sum((x - mean) ** 2 for x in incomes) / len(incomes)
        stdev = math.sqrt(var)
        income_cv = float((stdev / mean) if mean > 0 else 1.0)
        income_stability = max(0, 1.0 - income_cv)

    health_score = 0.0
    if avg_income > 0:
        health_score += min(40, float(savings_rate) * 100)
        health_score += min(30, income_stability * 30)
        balance_ratio = float(balance_sum / avg_income)
        health_score += min(30, balance_ratio * 10)

    return {
        'avg_income': float(avg_income),
        'avg_expense': float(avg_expense),
        'savings_rate': float(savings_rate),
        'balance': float(balance_sum),
        'expense_dist': exp_dist,
        'months_count': months_count,
        'owned_types': dict(owned_types),
        'owned_ids': owned_ids,
        'responses': resp_map,
        'income_stability': income_stability,
        'income_cv': income_cv,
        'health_score': health_score,
    }

def recommend_for_client(db: Session, client_id: str, top_n: int = 3, use_ml: bool = True):
    """
    Hybrid recommendation: CatBoost + Embeddings + Rules
    """
    feats = extract_client_features(db, client_id)
    if feats is None:
        return []

    # Load CatBoost models
    catboost_rec = None
    if use_ml:
        catboost_rec = CatBoostRecommender(db)
        models_loaded = catboost_rec.load_models()
        if not models_loaded:
            print("No CatBoost models found, using rules only")
            catboost_rec = None

    # Score products
    prod_list = db.query(models.Product).all()
    scored = []
    
    for p in prod_list:
        if p.product_id in feats.get('owned_ids', set()):
            continue

        reasons = []
        
        # === CATBOOST + EMBEDDINGS SCORE (0-1) ===
        ml_score = 0.5
        embedding_sim = 0.0
        
        if catboost_rec and p.product_type in catboost_rec.models:
            ml_score = catboost_rec.predict_score(client_id, p, feats)
            embedding_sim = catboost_rec.embeddings_gen.cosine_similarity(client_id, p.product_id)
            reasons.append(f'ML: {ml_score:.2f}')
            if embedding_sim > 0.3:
                reasons.append(f'Similarity: {embedding_sim:.2f}')
        
        # === RULE-BASED BOOST ===
        rule_score = 0.0
        
        if p.product_type == 'deposit':
            if p.interest_rate:
                rule_score += float(p.interest_rate) * 2
            if feats['savings_rate'] > 0.15:
                rule_score += 20
                reasons.append(f'Накопления {feats["savings_rate"]*100:.0f}%')
            if 'накопления' in feats['responses'].get('financial_goal', ''):
                rule_score += 25
                reasons.append('Цель: накопления')
                
        elif p.product_type == 'loan':
            if p.interest_rate:
                rule_score += max(0, 20 - float(p.interest_rate))
            if feats['avg_expense'] > feats['avg_income'] * 0.95:
                rule_score += 20
            if 'покупка' in feats['responses'].get('financial_goal', ''):
                rule_score += 30
                reasons.append('Цель: покупка')
                
        elif p.product_type == 'card':
            if feats['avg_expense'] > 20000:
                rule_score += 15
            if 'кэшбэк' in (p.description or '').lower():
                food = feats.get('expense_dist', {}).get('food', 0)
                if food > 0.15:
                    rule_score += 20
                    reasons.append('Кэшбэк выгоден')

        # === FINAL SCORE ===
        # CatBoost (60%) + Embeddings (20%) + Rules (20%)
        if catboost_rec:
            final_score = (ml_score * 100 * 0.6) + (embedding_sim * 100 * 0.2) + (rule_score * 0.2)
            confidence = 0.85
        else:
            final_score = rule_score
            confidence = 0.6

        scored.append({
            'product_id': p.product_id,
            'product_name': p.product_name,
            'bank': p.bank,
            'product_type': p.product_type,
            'score': round(final_score, 2),
            'ml_score': round(ml_score, 3) if catboost_rec else None,
            'embedding_similarity': round(embedding_sim, 3) if catboost_rec else None,
            'rule_score': round(rule_score, 2),
            'confidence': round(confidence, 2),
            'reason': ' | '.join(reasons) if reasons else 'Базовое соответствие'
        })

    scored = sorted(scored, key=lambda x: x['score'], reverse=True)
    return scored[:top_n]

class ClassifierService:
    def __init__(self, db: Session):
        self.db = db
        init_default_questions(db)

    def recommend(self, client_id: str, top_n: int = 3, use_ml: bool = True):
        return recommend_for_client(self.db, client_id, top_n=top_n, use_ml=use_ml)

    def train_models(self):
        """Train CatBoost + Embeddings"""
        trainer = CatBoostRecommender(self.db)
        result = trainer.train_models()
        return result

    def questions(self):
        qs = self.db.query(models.Question).all()
        if not qs:
            init_default_questions(self.db)
            qs = self.db.query(models.Question).all()
        
        result = []
        for q in qs:
            opts = []
            for dq in DEFAULT_CLIENT_QUESTIONS:
                if dq['key'] == q.key:
                    opts = dq.get('options', [])
                    break
            result.append({'key': q.key, 'text': q.text, 'options': opts})
        return result
    
    def client_profile(self, client_id: str):
        features = extract_client_features(self.db, client_id)
        if not features:
            return None
        
        owned_products = []
        for pid in features.get('owned_ids', set()):
            p = self.db.query(models.Product).filter(models.Product.product_id == pid).first()
            if p:
                owned_products.append({
                    'product_id': p.product_id,
                    'product_name': p.product_name,
                    'product_type': p.product_type,
                    'bank': p.bank
                })
        
        return {
            'client_id': client_id,
            'financial_summary': {
                'avg_income': features['avg_income'],
                'avg_expense': features['avg_expense'],
                'savings_rate': f"{features['savings_rate']*100:.1f}%",
                'current_balance': features['balance'],
                'health_score': f"{features['health_score']:.0f}/100",
                'income_stability': f"{features['income_stability']*100:.0f}%"
            },
            'spending_categories': features['expense_dist'],
            'owned_products': owned_products,
            'responses': features['responses'],
            'data_months': features['months_count']
        }