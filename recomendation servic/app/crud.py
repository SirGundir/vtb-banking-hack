from sqlalchemy.orm import Session
from . import models
from decimal import Decimal
from datetime import datetime

# Products
def upsert_products(db: Session, products: list):
    created = 0
    for p in products:
        prod = db.query(models.Product).filter(models.Product.product_id == p['productId']).first()
        if not prod:
            prod = models.Product(
                product_id=p['productId'],
                bank=p.get('bank') or p.get('Bank') or p.get('BankName'),
                product_type=p.get('productType'),
                product_name=p.get('productName') or p.get('product_name'),
                description=p.get('description'),
                interest_rate=Decimal(str(p.get('interestRate', 0))) if p.get('interestRate') not in (None, '') else None,
                min_amount=Decimal(str(p.get('minAmount'))) if p.get('minAmount') not in (None, '') else None,
                max_amount=Decimal(str(p.get('maxAmount'))) if p.get('maxAmount') not in (None, '') else None,
                term_months=p.get('termMonths')
            )
            db.add(prod)
            created += 1
        else:
            # update some fields
            prod.product_type = p.get('productType') or prod.product_type
            prod.product_name = p.get('productName') or prod.product_name
            prod.description = p.get('description') or prod.description
            if p.get('interestRate') not in (None, ''):
                prod.interest_rate = Decimal(str(p.get('interestRate')))
            db.add(prod)
    db.commit()
    return {'inserted': created}

# Client
def get_or_create_client(db: Session, client_id: str):
    client = db.query(models.Client).filter(models.Client.client_id == client_id).first()
    if not client:
        client = models.Client(client_id=client_id)
        db.add(client)
        db.commit()
        db.refresh(client)
    return client

# Balances
def upsert_balances(db: Session, client_id: str, balances: list):
    client = get_or_create_client(db, client_id)
    for b in balances:
        # store simple snapshot (no dedupe for brevity)
        bal = models.AccountBalance(
            client_id=client.id,
            account_id=b.get('accountId'),
            balance=b['amount']['amount'] if isinstance(b.get('amount'), dict) else b.get('balance'),
            currency=b['amount']['currency'] if isinstance(b.get('amount'), dict) else b.get('currency'),
            as_of=b.get('dateTime')
        )
        db.add(bal)
    db.commit()
    return {'inserted': len(balances)}

# Transactions
def insert_transactions(db: Session, client_id: str, txs: list):
    client = get_or_create_client(db, client_id)
    inserted = 0
    for t in txs:
        exists = db.query(models.Transaction).filter(models.Transaction.transaction_id == t['transactionId']).first()
        if exists:
            continue
        tr = models.Transaction(
            client_id=client.id,
            account_id=t.get('accountId'),
            transaction_id=t.get('transactionId'),
            amount=t['amount']['amount'] if isinstance(t.get('amount'), dict) else t.get('amount'),
            currency=t['amount']['currency'] if isinstance(t.get('amount'), dict) else t.get('currency'),
            credit=(t.get('creditDebitIndicator','').lower() == 'credit'),
            status=t.get('status'),
            booking_dt=t.get('bookingDateTime'),
            value_dt=t.get('valueDateTime'),
            info=t.get('transactionInformation'),
            bank_code=(t.get('bankTransactionCode') or {}).get('code') if t.get('bankTransactionCode') else None
        )
        db.add(tr)
        inserted += 1
    db.commit()
    return {'inserted': inserted}

# Questions / Responses
def list_questions(db: Session):
    return db.query(models.Question).all()

def upsert_response(db: Session, client_id: str, question_key: str, answer: str):
    client = get_or_create_client(db, client_id)
    resp = models.Response(client_id=client.id, question_key=question_key, answer=answer)
    db.add(resp)
    db.commit()
    return resp

# Feedback
def insert_feedback(db: Session, client_id: str, product_id: str, accepted: bool):
    client = get_or_create_client(db, client_id)
    fb = models.Feedback(client_id=client.id, product_id=product_id, accepted=accepted)
    db.add(fb)
    db.commit()
    return fb