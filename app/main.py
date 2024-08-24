from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from .db import get_db
from . import db
from .models.cliente import Cliente


app = FastAPI()

# @app.on_event("startup")
# def startup():
#     db.Base.metadata.create_all(bind=db.engine)

@app.post("/clientes/")
def create_cliente(nome: str, email: str, db: Session = Depends(get_db)):
    cliente = Cliente(nome=nome, email=email)
    db.add(cliente)
    db.commit()
    db.refresh(cliente)
    return cliente

@app.get("/clientes/{cliente_id}")
def read_cliente(cliente_id: int, db: Session = Depends(get_db)):
    cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return cliente
