from fastapi import FastAPI, File, UploadFile, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional, List
import pytesseract
from PIL import Image
import uuid
import io
import re

# --- CONFIGURAÇÃO DO BANCO DE DADOS ---
from sqlalchemy import create_engine, Column, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from datetime import datetime

SQLALCHEMY_DATABASE_URL = "sqlite:///./leads.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class LeadDB(Base):
    __tablename__ = "leads"
    id = Column(String, primary_key=True, index=True)
    nome = Column(String)
    telefone = Column(String)
    mensagem = Column(Text)
    data_criacao = Column(DateTime, default=datetime.utcnow)

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- CONFIGURAÇÃO TESSERACT ---
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# AQUI ESTÁ A LINHA QUE O SEU ERRO RECLAMOU:
app = FastAPI()

# --- MODELOS ---
class LeadBase(BaseModel):
    nome: Optional[str] = "Não identificado"
    telefone: Optional[str] = "Não identificado"
    mensagem: Optional[str] = None

class LeadResponse(LeadBase):
    id: str
    data_creation: datetime = datetime.now() # Fallback simples
    class Config:
        from_attributes = True

# --- INTELIGÊNCIA DE LIMPEZA ---
def limpar_dados_ocr(texto):
    padrao_tel = r'(\+?55\s?\d{2}\s?9?\d{4}-?\d{4})'
    tel_match = re.search(padrao_tel, texto)
    telefone = tel_match.group(0) if tel_match else "Não encontrado"

    padrao_nome_til = r'~\s?(\w+)'
    nome_match = re.search(padrao_nome_til, texto)
    if nome_match:
        nome = nome_match.group(1)
    else:
        padrao_contato = r'(\w+)\n+Não está nos seus contatos'
        match_contato = re.search(padrao_contato, texto, re.IGNORECASE)
        nome = match_contato.group(1) if match_contato else "Desconhecido"

    linhas = texto.split('\n')
    mensagens_relevantes = []
    sujeira = ["contatos", "grupos", "iniciada", "compartilhamento", "atividades", "Gerenciar", "saudação", "Instagram", "detalhes"]

    for linha in linhas:
        ln = linha.strip()
        if len(ln) > 10 and not any(s in ln for s in sujeira):
            if telefone not in ln and nome not in ln:
                mensagens_relevantes.append(ln)
    
    contexto = " | ".join(mensagens_relevantes) if mensagens_relevantes else "Sem contexto"
    return nome, telefone, contexto

# --- ROTAS ---
@app.get("/")
async def root():
    return {"status": "Sistema Online"}

@app.post("/upload-print/", response_model=LeadResponse)
async def upload_print(file: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
        texto_extraido = pytesseract.image_to_string(image, lang='por')
        nome, telefone, contexto = limpar_dados_ocr(texto_extraido)

        novo_lead = LeadDB(id=str(uuid.uuid4()), nome=nome, telefone=telefone, mensagem=contexto)
        db.add(novo_lead)
        db.commit()
        db.refresh(novo_lead)
        return novo_lead
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/leads/", response_model=List[LeadResponse])
async def listar_leads(db: Session = Depends(get_db)):
    return db.query(LeadDB).all()

@app.put("/leads/{lead_id}", response_model=LeadResponse)
async def atualizar_lead(lead_id: str, dados: LeadBase, db: Session = Depends(get_db)):
    lead = db.query(LeadDB).filter(LeadDB.id == lead_id).first()
    if not lead: raise HTTPException(status_code=404)
    lead.nome, lead.telefone, lead.mensagem = dados.nome, dados.telefone, dados.mensagem
    db.commit()
    return lead