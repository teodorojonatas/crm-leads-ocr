from fastapi import FastAPI, File, UploadFile, HTTPException
import uuid

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "API do Mini CRM ativa e segura!"}

@app.post("/upload-print/")
async def upload_print(file: UploadFile = File(...)):
    # Validação simples de tipo por enquanto
    if file.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(status_code=400, detail="Apenas JPG ou PNG.")
    
    unique_filename = f"{uuid.uuid4()}.png"
    return {"status": "sucesso", "filename": unique_filename}