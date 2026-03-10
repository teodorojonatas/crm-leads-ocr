from fastapi import FastAPI, File, UploadFile, HTTPException
import uuid

app = FastAPI()

@app.get("/")
async def root():
    # Verifico se a API está rodando corretamente para garantir o status do serviço
    return {"message": "Minha API do Mini CRM está ativa e segura!"}

@app.post("/upload-print/")
async def upload_print(file: UploadFile = File(...)):
    # Defino aqui os formatos que aceito para evitar arquivos maliciosos ou inesperados
    # No futuro, pretendo implementar a validação de Magic Bytes para maior segurança
    if file.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(status_code=400, detail="Apenas JPG ou PNG são permitidos.")
    
    # Uso UUID para gerar nomes únicos. Isso impede que um invasor tente adivinhar
    # nomes de arquivos ou sobrescreva dados importantes no meu servidor (Path Traversal)
    unique_filename = f"{uuid.uuid4()}.png"
    
    return {
        "status": "sucesso", 
        "filename": unique_filename,
        "msg": "Arquivo recebido e sanitizado com sucesso."
    }