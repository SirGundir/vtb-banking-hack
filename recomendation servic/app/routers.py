from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .database import SessionLocal
from . import crud, models
from .classifier import ClassifierService
from typing import List

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post('/products/bulk')
def upload_products(products: List[dict], db: Session = Depends(get_db)):
    res = crud.upsert_products(db, products)
    return res

@router.get('/products')
def list_products(db: Session = Depends(get_db)):
    prods = db.query(models.Product).all()
    return prods

@router.post('/clients/{client_id}/balances')
def upload_balances(client_id: str, payload: dict, db: Session = Depends(get_db)):
    balances = payload.get('data', {}).get('balance', [])
    res = crud.upsert_balances(db, client_id, balances)
    return res

@router.post('/clients/{client_id}/transactions')
def upload_transactions(client_id: str, payload: dict, db: Session = Depends(get_db)):
    txs = payload.get('data', {}).get('transaction', [])
    res = crud.insert_transactions(db, client_id, txs)
    return res

@router.post('/clients/{client_id}/products')
def upload_client_products(client_id: str, payload: dict, db: Session = Depends(get_db)):
    prods = payload.get('products', [])
    client = crud.get_or_create_client(db, client_id)
    inserted = 0
    for pid in prods:
        cp = models.ClientProduct(client_id=client.id, product_id=pid)
        db.add(cp)
        inserted += 1
    db.commit()
    return {"inserted": inserted}

@router.get('/clients/{client_id}/profile')
def get_client_profile(client_id: str, db: Session = Depends(get_db)):
    svc = ClassifierService(db)
    profile = svc.client_profile(client_id)
    if not profile:
        raise HTTPException(status_code=404, detail='Client not found')
    return profile

@router.get('/questions')
def get_questions(db: Session = Depends(get_db)):
    svc = ClassifierService(db)
    return {'questions': svc.questions()}

@router.post('/responses/{client_id}')
def post_response(client_id: str, payload: dict, db: Session = Depends(get_db)):
    key = payload.get('question_key')
    ans = payload.get('answer')
    if not key:
        raise HTTPException(status_code=400, detail='question_key required')
    resp = crud.upsert_response(db, client_id, key, ans)
    return {'ok': True}

@router.post('/recommend/{client_id}')
def recommend(client_id: str, payload: dict = None, db: Session = Depends(get_db)):
    """
    Get top-3 personalized recommendations
    Uses: CatBoost (60%) + Embeddings (20%) + Rules (20%)
    """
    use_ml = True
    top_n = 3
    if payload:
        use_ml = payload.get('use_ml', True)
        top_n = payload.get('top_n', 3)
    
    svc = ClassifierService(db)
    recs = svc.recommend(client_id, top_n=top_n, use_ml=use_ml)
    return {'recommendations': recs}

@router.post('/feedback/{client_id}')
def feedback(client_id: str, payload: dict, db: Session = Depends(get_db)):
    prod = payload.get('product_id')
    accepted = payload.get('accepted', False)
    if not prod:
        raise HTTPException(status_code=400, detail='product_id required')
    fb = crud.insert_feedback(db, client_id, prod, bool(accepted))
    return {'ok': True}

@router.post('/train')
def train_models(db: Session = Depends(get_db)):
    """
    Train CatBoost models + generate embeddings
    Needs at least 10 feedback records
    """
    svc = ClassifierService(db)
    result = svc.train_models()
    return result

@router.get('/model/status')
def model_status(db: Session = Depends(get_db)):
    import os
    MODEL_DIR = '/app/ml_model/saved_models'
    
    models_found = {}
    for ptype in ['deposit', 'loan', 'card']:
        path = os.path.join(MODEL_DIR, f'catboost_{ptype}.cbm')
        models_found[ptype] = os.path.exists(path)
    
    emb_client = os.path.exists(os.path.join(MODEL_DIR, 'client_embeddings.npy'))
    emb_product = os.path.exists(os.path.join(MODEL_DIR, 'product_embeddings.npy'))
    
    feedback_count = db.query(models.Feedback).count()
    
    return {
        'catboost_models': models_found,
        'embeddings_trained': {
            'clients': emb_client,
            'products': emb_product
        },
        'total_feedback': feedback_count,
        'ready_for_training': feedback_count >= 10
    }