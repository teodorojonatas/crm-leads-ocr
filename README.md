# Mini CRM - Extrator de Leads via OCR 🚀

Este projeto é um Mini CRM desenvolvido para corretores, focado na extração automática de dados de leads a partir de prints do WhatsApp utilizando OCR (Reconhecimento Óptico de Caracteres).

## 📌 Status do Projeto: Marco 0.2.0 Concluído
- [x] Configuração inicial do ambiente (FastAPI).
- [x] Integração com Tesseract OCR.
- [x] Rota de upload de imagem e extração de texto bruto funcional.
- [ ] Extração de campos específicos (Nome, Telefone) com IA/RegEx.
- [ ] Persistência em Banco de Dados.

## 🛠️ Tecnologias Utilizadas
- **Python 3.13**
- **FastAPI** (Backend)
- **Tesseract OCR** (Motor de leitura)
- **Pillow** (Processamento de imagem)

## 🚀 Como rodar o projeto
1. Ative o ambiente virtual: `source backend/venv/Scripts/activate`
2. Instale as dependências: `pip install -r requirements.txt` (Dica: vamos criar esse arquivo logo!)
3. Inicie o servidor: `uvicorn backend.main:app --reload`
4. Acesse: `http://127.0.0.1:8000/docs`