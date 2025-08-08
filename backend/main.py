import os
import pickle
from contextlib import asynccontextmanager
import numpy as np
import faiss
from fastapi import FastAPI, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer

# --- Configurações e Carregamento de Dados ---

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Dicionário para armazenar os componentes do RAG (modelo, índice, etc.)
rag_components = {}

# Constantes
FAISS_INDEX_PATH = 'faiss_index.bin'
CHUNKS_PATH = 'chunks.pkl'
MODEL_NAME = 'all-MiniLM-L6-v2'
LM_STUDIO_URL = os.getenv("LM_STUDIO_URL", "http://localhost:1234")
LM_STUDIO_MODEL = os.getenv("LM_STUDIO_MODEL", "local-model")
LM_STUDIO_API_ENDPOINT = os.getenv("LM_STUDIO_API_ENDPOINT", "/v1/chat/completions")

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Gerencia o ciclo de vida da aplicação.
    Carrega o modelo e os dados na inicialização.
    """
    print("Carregando modelo de embeddings, índice FAISS e chunks de texto...")
    try:
        rag_components['model'] = SentenceTransformer(MODEL_NAME)
        rag_components['index'] = faiss.read_index(FAISS_INDEX_PATH)
        with open(CHUNKS_PATH, 'rb') as f:
            rag_components['chunks'] = pickle.load(f)
        print("--- Componentes do RAG carregados com sucesso! ---")
    except FileNotFoundError:
        print("\nAVISO: Arquivos de índice ('faiss_index.bin') ou chunks ('chunks.pkl') não encontrados.")
        print("Execute o script 'ingest.py' primeiro para criar esses arquivos: python ingest.py\n")
        rag_components['model'] = None # Impede a API de funcionar sem os dados
    
    yield
    
    # Limpeza (se necessário)
    rag_components.clear()
    print("Componentes do RAG descarregados.")

# Inicializa o aplicativo FastAPI com o gerenciador de ciclo de vida
app = FastAPI(
    title="Chatbot API",
    description="API para o chatbot com RAG e LM Studio",
    version="0.1.0",
    lifespan=lifespan
)

# --- Configuração do CORS ---
# Adiciona o middleware para permitir requisições de diferentes origens (Cross-Origin Resource Sharing)
# Isso é essencial para que o frontend (HTML/JS) possa se comunicar com a API.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite todas as origens (em produção, restrinja para o seu domínio)
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos os métodos (GET, POST, etc.)
    allow_headers=["*"],  # Permite todos os cabeçalhos
)

# --- Modelos de Dados (Pydantic) ---
class ChatRequest(BaseModel):
    question: str
    session_id: str | None = None

class ChatResponse(BaseModel):
    answer: str
    source: list[str] | None = None

# --- Funções de Apoio (RAG) ---
def search_relevant_chunks(query: str, k: int = 5):
    """Busca os k chunks mais relevantes para uma dada query."""
    if not rag_components.get('model') or not rag_components.get('index'):
        raise HTTPException(status_code=503, detail="Componentes do RAG não estão carregados. Execute o script de ingestão.")

    query_embedding = rag_components['model'].encode([query], convert_to_tensor=False)
    query_embedding = np.array(query_embedding).astype('float32')
    
    distances, indices = rag_components['index'].search(query_embedding, k)
    
    relevant_chunks = [rag_components['chunks'][i] for i in indices[0]]
    return relevant_chunks

def build_prompt(question: str, context_chunks: list[str]):
    """Monta o prompt final para o LLM com o contexto."""
    context = "\n\n---\n\n".join(context_chunks)
    prompt = f"""
Você é um assistente especializado em responder perguntas com base em um contexto fornecido.
Use APENAS as informações do contexto abaixo para formular sua resposta.
Se a resposta não estiver no contexto, diga "Com base nos documentos fornecidos, não encontrei informações sobre isso."

Contexto:
{context}

---

Pergunta do usuário: {question}

Resposta:
"""
    return prompt

# --- Endpoints da API ---

@app.get("/", tags=["Status"])
def read_root():
    """Endpoint raiz para verificar se a API está no ar."""
    return {"status": "API do Chatbot está funcionando!"}

@app.post("/chat", response_model=ChatResponse, tags=["Chat"])
def chat_with_bot(request: ChatRequest = Body(...)):
    """
    Endpoint principal para interagir com o chatbot.
    Recebe uma pergunta, busca em documentos e retorna a resposta gerada.
    """
    print(f"Recebida a pergunta: {request.question}")

    # 1. Buscar chunks relevantes (Retrieval)
    relevant_chunks = search_relevant_chunks(request.question)
    
    # 2. Montar o prompt com o contexto
    prompt = build_prompt(request.question, relevant_chunks)
    
    # 3. Enviar para o LM Studio (Generation)
    try:
        headers = {"Content-Type": "application/json"}
        
        # Adapta o payload e a extração da resposta com base no endpoint configurado
        is_chat_endpoint = "chat/completions" in LM_STUDIO_API_ENDPOINT

        if is_chat_endpoint:
            data = {
                "model": LM_STUDIO_MODEL,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.7,
                "stream": False,
            }
        else: # Assume endpoint de completions legado
            data = {
                "model": LM_STUDIO_MODEL,
                "prompt": prompt,
                "max_tokens": 4096,
                "temperature": 0.7,
                "stream": False,
            }

        full_url = f"{LM_STUDIO_URL}{LM_STUDIO_API_ENDPOINT}"
        print(f"Enviando requisição para: {full_url}") # Log para depuração
        response = requests.post(full_url, headers=headers, json=data)
        response.raise_for_status()

        completion = response.json()
        try:
            if is_chat_endpoint:
                answer = completion['choices'][0]['message']['content'].strip()
            else:
                answer = completion['choices'][0]['text'].strip()
        except (KeyError, IndexError):
            print(f"KeyError/IndexError: A estrutura da resposta do LM Studio é inesperada. Resposta completa: {completion}")
            raise HTTPException(status_code=500, detail="Formato de resposta inesperado do LM Studio.")

        return ChatResponse(answer=answer, source=relevant_chunks)

    except requests.exceptions.RequestException as e:
        print(f"Erro ao conectar com o LM Studio: {e}")
        raise HTTPException(status_code=503, detail="Não foi possível conectar ao servidor do modelo de linguagem (LM Studio).")
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")
        raise HTTPException(status_code=500, detail="Ocorreu um erro interno no servidor.")

# --- Para executar o servidor localmente ---
# No terminal, na pasta 'backend', execute:
# uvicorn main:app --reload