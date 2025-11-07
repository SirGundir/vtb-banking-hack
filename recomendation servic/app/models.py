from sqlalchemy import Column, Integer, String, Float, DateTime, JSON, ForeignKey, Boolean, Numeric
from sqlalchemy.orm import relationship
from .database import Base
from datetime import datetime

class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(String, unique=True, index=True, nullable=False)
    bank = Column(String, index=True)
    product_type = Column(String, index=True)
    product_name = Column(String)
    description = Column(String)
    interest_rate = Column(Numeric(6,2))
    min_amount = Column(Numeric(18,2), nullable=True)
    max_amount = Column(Numeric(18,2), nullable=True)
    term_months = Column(Integer, nullable=True)

class Client(Base):
    __tablename__ = 'clients'
    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(String, unique=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    profile = Column(JSON, default={})

class ClientProduct(Base):
    __tablename__ = 'client_products'
    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey('clients.id'))
    product_id = Column(String, index=True)
    added_at = Column(DateTime, default=datetime.utcnow)
    client = relationship('Client')

class AccountBalance(Base):
    __tablename__ = 'balances'
    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey('clients.id'))
    account_id = Column(String, index=True)
    balance = Column(Numeric(18,2))
    currency = Column(String)
    as_of = Column(DateTime)
    client = relationship('Client')

class Transaction(Base):
    __tablename__ = 'transactions'
    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey('clients.id'))
    account_id = Column(String, index=True)
    transaction_id = Column(String, index=True)
    amount = Column(Numeric(18,2))
    currency = Column(String)
    credit = Column(Boolean)
    status = Column(String)
    booking_dt = Column(DateTime)
    value_dt = Column(DateTime)
    info = Column(String)
    bank_code = Column(String)
    client = relationship('Client')

class Question(Base):
    __tablename__ = 'questions'
    id = Column(Integer, primary_key=True)
    key = Column(String, unique=True)
    text = Column(String)
    product_type_hint = Column(String, nullable=True)

class Response(Base):
    __tablename__ = 'responses'
    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey('clients.id'))
    question_key = Column(String)
    answer = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    client = relationship('Client')

class Feedback(Base):
    __tablename__ = 'feedback'
    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey('clients.id'))
    product_id = Column(String)
    accepted = Column(Boolean)
    created_at = Column(DateTime, default=datetime.utcnow)
    client = relationship('Client')