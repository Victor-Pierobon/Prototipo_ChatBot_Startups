import os
import fitz  # PyMuPDF
from tqdm import tqdm
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import pickle

# --- Configurações ---
DOCUMENTS_PATH = '../src/documentos'
FAISS_INDEX_PATH = 'faiss_index.bin'
CHUNKS_PATH = 'chunks.pkl'
MODEL_NAME = 'all-MiniLM-L6-v2' # Um bom modelo inicial, leve e eficiente

def get_pdf_files(path):
    """Encontra todos os arquivos PDF em um diretório, recursivamente."""
    pdf_files = []
    for root, _, files in os.walk(path):
        for file in files:
            if file.lower().endswith('.pdf'):
                pdf_files.append(os.path.join(root, file))
    return pdf_files

def extract_text_from_pdf(file_path):
    """Extrai o texto de um único arquivo PDF."""
    try:
        doc = fitz.open(file_path)
        text = ""
        for page in doc:
            text += page.get_text()
        return text
    except Exception as e:
        print(f"Erro ao ler o arquivo {file_path}: {e}")
        return None

def chunk_text(text, chunk_size=1000, chunk_overlap=200):
    """Divide o texto em chunks com sobreposição."""
    if not isinstance(text, str):
        return []
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - chunk_overlap
    return chunks

def main():
    """
    Função principal para processar os documentos, gerar embeddings
    e criar o índice FAISS.
    """
    print("Iniciando o processo de ingestão de documentos...")

    # 1. Encontrar e ler os documentos PDF
    pdf_files = get_pdf_files(DOCUMENTS_PATH)
    if not pdf_files:
        print(f"Nenhum arquivo PDF encontrado em '{DOCUMENTS_PATH}'. Verifique o caminho.")
        return

    print(f"Encontrados {len(pdf_files)} arquivos PDF. Extraindo texto...")
    all_texts = [extract_text_from_pdf(pdf) for pdf in tqdm(pdf_files)]

    # 2. Dividir os textos em chunks
    print("Dividindo os textos em chunks...")
    all_chunks = []
    for text in tqdm(all_texts):
        if text:
            all_chunks.extend(chunk_text(text))

    if not all_chunks:
        print("Nenhum texto pôde ser extraído ou dividido em chunks. Abortando.")
        return

    print(f"Total de {len(all_chunks)} chunks de texto criados.")

    # 3. Gerar embeddings para os chunks
    print(f"Carregando o modelo de embeddings '{MODEL_NAME}'...")
    # O modelo será baixado automaticamente na primeira vez
    model = SentenceTransformer(MODEL_NAME)

    print("Gerando embeddings para os chunks de texto (isso pode levar um tempo)...")
    embeddings = model.encode(all_chunks, show_progress_bar=True)
    embeddings = np.array(embeddings).astype('float32')

    # 4. Criar e salvar o índice FAISS
    print("Criando o índice FAISS...")
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)

    print(f"Salvando o índice FAISS em '{FAISS_INDEX_PATH}'...")
    faiss.write_index(index, FAISS_INDEX_PATH)

    # 5. Salvar os chunks de texto correspondentes
    print(f"Salvando os chunks de texto em '{CHUNKS_PATH}'...")
    with open(CHUNKS_PATH, 'wb') as f:
        pickle.dump(all_chunks, f)

    print("\n--- Processo de ingestão concluído com sucesso! ---")
    print(f"Índice FAISS e chunks salvos na pasta 'backend'.")
    print("Agora você pode executar a API principal.")

if __name__ == "__main__":
    main()