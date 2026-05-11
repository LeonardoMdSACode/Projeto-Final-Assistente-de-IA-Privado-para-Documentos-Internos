Python 3.13.9

python -m venv .venv

qwen2.5:3b

Fluxo:
Frontend
   ↓
/chat endpoint
   ↓
rag_service.py
   ↓
Ollama + embeddings

Logo evita meter lógica RAG diretamente no app.py

python -m tests.test_chunking
python -m tests.test_embedding
python -m tests.test_loader
python -m tests.test_retrieval

Pergunta do utilizador
        ↓
Embedding da pergunta
        ↓
Comparar com embeddings dos chunks
        ↓
Top-k chunks relevantes
        ↓
Construir prompt
        ↓
Enviar ao Ollama
        ↓
Resposta final

