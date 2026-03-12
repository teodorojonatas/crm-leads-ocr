from fastapi import FastAPI, File, UploadFile, HTTPException
import pytesseract
from PIL import Image
import uuid
import io

# Configuração do caminho do Tesseract (Importante!)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Minha API do Mini CRM está ativa e com OCR configurado!"}

@app.post("/upload-print/")
async def upload_print(file: UploadFile = File(...)):
    # Validação de formato
    if file.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(status_code=400, detail="Apenas JPG ou PNG são permitidos.")

    try:
        # 1. Lê os bytes da imagem enviada
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))

        # 2. Usa o Tesseract para extrair o texto da imagem
        # O parâmetro lang='por' ajuda a ler português (se você instalou o pacote de linguagem)
        extracted_text = pytesseract.image_to_string(image, lang='por')

        # 3. Gera um ID único para o log/processamento
        job_id = str(uuid.uuid4())

        return {
            "job_id": job_id,
            "filename": file.filename,
            "extracted_content": extracted_text.strip(),
            "status": "success"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao processar imagem: {str(e)}")