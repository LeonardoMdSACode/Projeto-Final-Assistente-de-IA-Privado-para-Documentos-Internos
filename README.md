Python 3.13.9

python -m venv .venv

.venv\Scripts\activate

qwen2.5:3b
FastAPI + HTML
ChromaDB

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

Fluxo final:
Pergunta
→ embedding da pergunta
→ ChromaDB semantic search
→ devolve chunks mais similares
→ cada chunk tem metadata source
→ LLM responde usando contexto
→ UI mostra fontes


Neste momento:
RAG local
Ollama
embeddings locais modernos multilíngua (bge-m3)
ChromaDB persistente
retrieval semântico tuning
multi-document retrieval
source attribution
frontend
upload dinâmico
FastAPI backend
overlap retrieval chunking
deduplicação
prompt engineering
memory
follow-up questions
reranking
query rewriting
Router entre histórico vs RAG
