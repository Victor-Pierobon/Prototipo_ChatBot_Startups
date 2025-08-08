# 📚 Projeto Chatbot Jurídico-Empreendedor — Brasil

**Objetivo:**  
Desenvolver um chatbot especializado em responder dúvidas de empreendedores e startups, baseado em documentos e normas oficiais brasileiras, com foco em segurança jurídica, precisão e atualização constante.

---

## 1. Escopo do Protótipo

- **Modelo:** Mistral Small 7B (open-source, custo-efetivo)
- **Arquitetura:** RAG (Retrieval-Augmented Generation) + Vector DB
- **Fonte de conhecimento:** Leis e regulamentos oficiais federais, estaduais e municipais
- **Público-alvo:** Empreendedores, startups, consultores de negócios
- **Objetivo principal:** Responder dúvidas de forma clara, citar dispositivos legais e fornecer links para fontes oficiais

---

## 2. Lista de Documentos Oficiais

Organizada por prioridade.

### **Prioridade A — Essenciais (qualquer negócio)**
1. Constituição Federal
2. Código Civil (Lei nº 10.406/2002)
3. CLT — Consolidação das Leis do Trabalho (Decreto-Lei 5.452/1943)
4. Código Tributário Nacional (Lei nº 5.172/1966)
5. Lei Complementar 123/2006 — Simples Nacional
6. Legislação do MEI
7. Normas do CNPJ — Receita Federal
8. Normas da NF-e, SPED e eSocial — Receita Federal
9. Código de Defesa do Consumidor (Lei nº 8.078/1990)
10. Lei Geral de Proteção de Dados — LGPD (Lei nº 13.709/2018)
11. Lei das S/A (Lei nº 6.404/1976)
12. Lei de Falências e Recuperação Judicial (Lei nº 11.101/2005)
13. Normas das Juntas Comerciais estaduais

### **Prioridade B — Altamente importantes**
14. ICMS, ISS, IPI, PIS/COFINS — legislação e regulamentações
15. Normas do INSS e legislação previdenciária
16. eSocial — manuais e tabelas
17. Normas ANVISA
18. Normas INPI — marcas e patentes
19. Marco Civil da Internet
20. Leis tributárias estaduais e municipais

### **Prioridade C — Setoriais**
21. Resoluções do Banco Central — fintechs
22. Normas da CVM — captação, crowdfunding
23. Normas ambientais — IBAMA e estaduais
24. ANATEL — telecomunicações
25. MAPA — agro e alimentos
26. Legislação municipal — alvarás, zoneamento
27. Incentivos fiscais e Lei do Bem
28. Leis de e-commerce e proteção ao consumidor digital
29. Regras sobre stock options e benefícios

---

## 3. Fontes Oficiais

- **Planalto** — [https://www.planalto.gov.br/](https://www.planalto.gov.br/)
- **Receita Federal** — [https://www.gov.br/receitafederal](https://www.gov.br/receitafederal)
- **Portal eSocial** — [https://www.gov.br/esocial](https://www.gov.br/esocial)
- **INPI** — [https://www.gov.br/inpi](https://www.gov.br/inpi)
- **ANVISA** — [https://www.gov.br/anvisa](https://www.gov.br/anvisa)
- **ANATEL** — [https://www.gov.br/anatel](https://www.gov.br/anatel)
- **IBAMA** — [https://www.gov.br/ibama](https://www.gov.br/ibama)
- **MAPA** — [https://www.gov.br/agricultura](https://www.gov.br/agricultura)
- **Banco Central** — [https://www.bcb.gov.br/](https://www.bcb.gov.br/)
- **CVM** — [https://www.gov.br/cvm](https://www.gov.br/cvm)
- **Juntas Comerciais Estaduais** — portais específicos
- **Prefeituras Municipais** — legislações locais

---

## 4. Estrutura de Dados (Metadados e Proveniência)

```json
{
  "id": "...",
  "titulo": "Lei X / IN Y",
  "jurisdicao": "Federal/Estado-SP/Município-Rio",
  "tipo": "lei/instrucao-normativa/portaria/manual",
  "texto": "...",
  "url": "...",
  "data_publicacao": "YYYY-MM-DD",
  "data_obtencao": "YYYY-MM-DD",
  "hash": "sha256:...",
  "tags": ["tributario","societario","LGPD"]
}
```

---

## 5. Arquitetura do Protótipo

### Pipeline:

1. Ingestão — download de PDFs/HTMLs de fontes oficiais

2. Normalização — extração de texto, OCR se necessário

3. Indexação — embeddings por parágrafo/artigo

4. Armazenamento — Vector DB (Milvus/Pinecone)

5. Recuperação — top-k trechos relevantes

6. Geração — modelo Mistral Small 7B com prompt template

7. Validação — regras determinísticas para cálculos e citações

8. Resposta — texto claro + citações + links

9. Auditoria — log de fontes, prompt e resposta

## 6. Boas Práticas de Compliance

* Citar dispositivo legal e link oficial sempre

* Indicar jurisdição e data da norma

* Alertar sobre necessidade de consulta profissional

* Garantir LGPD no tratamento de dados dos usuários

* Atualizar base de leis periodicamente

* Manter logs de auditoria por prazo definido

## 7. Estratégia de Treinamento

* RAG para sempre basear respostas em texto oficial

* Instruction-tuning com exemplos validados por advogados

* Separar cálculos em micro-serviços determinísticos

* Revisão humana nas respostas sensíveis

## 8. Roadmap do MVP (8 semanas)
1. S1–S2: Coleta leis prioridade A+B e ingestão

2. S3: Indexação + embeddings

3. S4: Prompt templates + RAG

4. S5: Regras de cálculo básico

5. S6: Interface web + logs

6. S7: Testes com especialistas

7. S8: Lançamento com disclaimer

##  9. Checklist de Implementação

1. Indexar leis e normas prioridade "A"

2. Criar metadados com jurisdição e versão

3. Implementar RAG com Mistral Small 7B

4. Configurar Vector DB

5. Criar prompts com citações automáticas

6. Implantar módulo de cálculos básicos

7. Implementar disclaimers automáticos

8. Garantir LGPD na coleta de dados

9. Pipeline de atualização de base legal

10. Auditoria e logging completo

---
---

## Como Executar o Protótipo

Este projeto é um protótipo de chatbot que utiliza a técnica de **Retrieval-Augmented Generation (RAG)** para responder a perguntas com base em um conjunto de documentos. Ele foi projetado para ser executado localmente com o [LM Studio](https://lmstudio.ai/).

### Pré-requisitos

Antes de começar, garanta que você tenha o seguinte instalado:

*   **Python 3.9+**: [Link para download](https://www.python.org/downloads/)
*   **LM Studio**: [Link para download](https://lmstudio.ai/)
*   Um modelo de linguagem (LLM) baixado e carregado no LM Studio (ex: Llama 3, Mistral, etc.).

### Passo 1: Configurar o Backend

1.  **Navegue até a pasta do backend:**
    ```bash
    cd backend
    ```

2.  **Crie um ambiente virtual (recomendado):**
    ```bash
    python -m venv venv
    ```

3.  **Ative o ambiente virtual:**
    *   No Windows:
        ```bash
        .\venv\Scripts\activate
        ```
    *   No macOS/Linux:
        ```bash
        source venv/bin/activate
        ```

4.  **Instale as dependências do Python:**
    ```bash
    pip install -r requirements.txt
    ```
    *(Isso pode levar alguns minutos, pois fará o download de bibliotecas como PyTorch e Sentence-Transformers).*

### Passo 2: Processar os Documentos (Ingestão)

Este passo só precisa ser executado uma vez (ou sempre que os documentos na pasta `src/documentos` forem alterados).

1.  **Execute o script de ingestão:**
    (Certifique-se de que você ainda está no ambiente virtual ativado e na pasta `backend`)
    ```bash
    python ingest.py
    ```
    *   O script irá ler todos os PDFs, processá-los e criar dois arquivos na pasta `backend`: `faiss_index.bin` e `chunks.pkl`.

### Passo 3: Iniciar o Servidor do Modelo (LM Studio)

1.  Abra o **LM Studio**.
2.  Carregue o modelo de sua preferência.
3.  Vá para a aba **"Local Server"** (ícone `<->`).
4.  Clique em **"Start Server"**. O servidor deve estar rodando em `http://localhost:1234`.

### Passo 4: Iniciar a API do Backend

1.  **Execute o servidor FastAPI:**
    (Com o ambiente virtual ativado e na pasta `backend`)
    ```bash
    uvicorn main:app --reload
    ```
    *   A API estará disponível em `http://localhost:8000`. Você pode abrir este endereço no seu navegador e ver a mensagem `{"status":"API do Chatbot está funcionando!"}`.

### Passo 5: Abrir a Interface do Chat (Frontend)

1.  **Abra o arquivo `frontend/index.html` diretamente no seu navegador.**
    *   Você pode fazer isso clicando duas vezes no arquivo ou usando a extensão "Live Server" no VS Code (clique com o botão direito no arquivo e selecione "Open with Live Server").

Agora você pode interagir com o chatbot! Digite uma pergunta na caixa de texto e pressione "Enviar".