# Mini CRM - Extrator de Leads via OCR 🚀

Este projeto é um Mini CRM desenvolvido para corretores, focado na extração automática de dados de leads a partir de prints do WhatsApp utilizando OCR (Reconhecimento Óptico de Caracteres) e persistência em banco de dados.

📌 Status do Projeto: Marco 0.5.0 Concluído ✅

- [x] Configuração inicial do ambiente (FastAPI).
- [x] Integração com Tesseract OCR.
- [x] Rota de upload de imagem e extração de texto bruto.
- [x] Inteligência de Extração (Nome, Telefone e Contexto da Mensagem) com RegEx.
- [x] Persistência em Banco de Dados (SQLite).
- [x] Sistema CRUD (Listagem, Edição e Exclusão de Leads).
- [ ] Interface Web (Frontend).

🛠️ Tecnologias Utilizadas
- Python 3.13
- FastAPI (Backend)
- Tesseract OCR (Motor de leitura)
- SQLAlchemy (ORM para Banco de Dados)
- SQLite (Banco de Dados local)
- Pillow (Processamento de imagem)

🚀 Como Executar o Projeto

1. Ative o ambiente virtual:
   source backend/venv/Scripts/activate

2. Inicie o servidor:
   uvicorn backend.main:app --reload

3. Acesse a documentação interativa:
   http://127.0.0.1:8000/docs

💡 Funcionalidades Atuais
- Upload de Prints: O sistema identifica automaticamente o nome do lead (mesmo sem estar nos contatos), o telefone e o interesse principal na conversa.
- Banco de Dados: Todos os leads processados são salvos com data e ID único.
- Gestão de Dados: É possível corrigir nomes lidos incorretamente pelo OCR ou deletar registros via API.