from fastapi import FastAPI
from .database import engine
from . import models
from .routers import router

app = FastAPI(
    title='Bank Recommender - CatBoost + Embeddings',
    description='Hybrid recommendation: CatBoost (60%) + Embeddings (20%) + Rules (20%)',
    version='3.0'
)

models.Base.metadata.create_all(bind=engine)

app.include_router(router)

@app.get('/')
def root():
    return {
        'ok': True,
        'service': 'Bank Product Recommender',
        'version': '3.0',
        'architecture': 'CatBoost + Client2Vec/Product2Vec + Rules',
        'features': [
            'CatBoost classifier per product type',
            'Client embeddings from transaction patterns (Word2Vec)',
            'Product embeddings from co-occurrence (Word2Vec)',
            'Cosine similarity between client and product embeddings',
            'Hybrid scoring: CatBoost (60%) + Embeddings (20%) + Rules (20%)',
            '62 features total (structured + embeddings)',
            'Top-3 recommendations with confidence scores'
        ]
    }