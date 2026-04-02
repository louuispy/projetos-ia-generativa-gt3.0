# 🤖 Geração Tech 3.0 — IA Generativa

Repositório com os projetos práticos desenvolvidos durante o curso de **IA Generativa** do programa **Geração Tech 3.0**. O conteúdo é dividido em quatro módulos, cada um explorando conceitos e tecnologias progressivamente mais avançadas da área de Inteligência Artificial.

---

## 📚 Estrutura do Repositório

```
github/
│
├── Módulo 1/
│   └── projeto-01-sincero-ai/          # Chatbot com API do Google Gemini (Google Colab)
│
├── Módulo 2/
│   ├── projeto-01-turismo-langchain/   # Chatbot com LangChain e detecção de intenções
│   ├── projeto-02-leitura-pdf-llm/     # Chatbot com leitura de PDFs e vídeos do YouTube
│   └── projeto-03-rag-multimodal-com-embeddings/ # RAG multimodal com embeddings
│
├── Módulo 3/
│   ├── Projeto 01 - Automação de RH - GT Systems.json
│   ├── Projeto 02 - Introdução a MCP.json
│   ├── Projeto 03 - Agente de IA com MCP - GT Systems.json
│   ├── Projeto 04 - Automação de estoque - GT Farmácia.json
│   ├── Projeto 05 - Agente de IA de estoque - GT Farmácia.json
│   ├── Projeto 06 - DataLake de ideias de posts - GT Studios.json
│   ├── Projeto 07 - DataLake de ideias de post com Telegram - GT Studios.json
│   ├── Projeto 08 - ETL com dados do IMDB.json
│   └── Projeto 08 - RAG com dados do IMDB.ipynb
│
└── Módulo 4/
    ├── projeto-01-multiagentes-n8n/    # Sistema multiagentes com N8N
    └── projeto-02-agentes-com-agno/    # Agentes de IA com framework Agno
```

---

## 📦 Módulos

### Módulo 1 — Introdução à IA Generativa

Primeiro contato com modelos de linguagem (LLMs) e a **API do Google Gemini**. O projeto foi desenvolvido no Google Colab e explora como configurar e personalizar um chatbot com engenharia de prompts.

| Projeto | Descrição |
|---|---|
| [`projeto-01-sincero-ai`](./Módulo%201/projeto-01-sincero-ai/) | Chatbot "SinceroAI" — uma IA treinada para responder de forma honesta e racional, sem validação excessiva. Usa a API `google-genai` diretamente com histórico de conversa e prompt de sistema personalizado. |

**Tecnologias:** Python, Google Gemini API (`google-genai`), Google Colab, `rich`

---

### Módulo 2 — LangChain, Embeddings e RAG

Módulo com foco em **LangChain** para orquestração de pipelines de IA. Ao longo do módulo, os conceitos evoluem de pipelines simples com detecção de intenção até sistemas de **RAG (Retrieval-Augmented Generation)** com embeddings e suporte multimodal.

| Projeto | Descrição |
|---|---|
| [`projeto-01-turismo-langchain`](./Módulo%202/projeto-01-turismo-langchain/) | TurismoAI — chatbot que classifica a intenção da pergunta do usuário (clima, culinária, guia de viagem etc.) e responde com prompts especializados. |
| [`projeto-02-leitura-pdf-llm`](./Módulo%202/projeto-02-leitura-pdf-llm/) | Chatbot capaz de ler PDFs e transcrições de vídeos do YouTube para responder perguntas com base nesses documentos. |
| [`projeto-03-rag-multimodal-com-embeddings`](./Módulo%202/projeto-03-rag-multimodal-com-embeddings/) | Sistema RAG completo e multimodal: suporta PDFs, vídeos do YouTube e imagens. Utiliza embeddings e divisão de texto em chunks para busca semântica eficiente. |

**Tecnologias:** Python, LangChain, Google Gemini API, PyPDF, YouTube Transcript API, `rich`, `uv`

---

### Módulo 3 — Workflows com IA (n8n)

Módulo focado em **automação de processos com IA** usando a plataforma de low-code **n8n**. Os projetos são exportados como fluxos `.json` prontos para importação no n8n.

> Inclui também introdução ao **MCP (Model Context Protocol)** para integração de ferramentas externas com agentes de IA.

| Projeto | Descrição |
|---|---|
| Projeto 01 — Automação de RH | Fluxo automatizado para processos de recursos humanos na GT Systems. |
| Projeto 02 — Introdução a MCP | Introdução ao Model Context Protocol e como utilizá-lo para expandir capacidades dos agentes. |
| Projeto 03 — Agente com MCP | Agente de IA integrado com ferramentas externas via MCP na GT Systems. |
| Projeto 04 — Automação de Estoque | Fluxo de automação para controle de estoque da GT Farmácia. |
| Projeto 05 — Agente de Estoque | Agente de IA para gerenciamento inteligente do estoque da GT Farmácia. |
| Projeto 06 — DataLake de Posts | Pipeline para geração e armazenamento de ideias de posts para a GT Studios. |
| Projeto 07 — DataLake com Telegram | Extensão do projeto de posts com integração ao Telegram. |
| Projeto 08 — ETL com IMDB | Pipeline de ETL processando dados do IMDB. |
| Projeto 08 — RAG com IMDB | Sistema RAG desenvolvido em notebook com dados do IMDB (`Google Colab`). |

**Tecnologias:** n8n, MCP, Google Gemini, APIs

---

### Módulo 4 — Multiagentes

Módulo avançado sobre sistemas **multiagentes**, cobrindo tanto abordagens low-code (n8n) quanto desenvolvimento direto com o framework **Agno** em Python.

| Projeto | Descrição |
|---|---|
| [`projeto-01-multiagentes-n8n`](./Módulo%204/projeto-01-multiagentes-n8n/) | Arquitetura multiagente implementada com n8n, demonstrando comunicação e colaboração entre agentes para resolução de tarefas complexas. |
| [`projeto-02-agentes-com-agno`](./Módulo%204/projeto-02-agentes-com-agno/) | Agentes de IA desenvolvidos com o framework **Agno** em Python, com foco na construção de agentes autônomos e colaborativos. |

**Tecnologias:** n8n, Python, Agno, Google Gemini API, `uv`

---

## 🚀 Como executar os projetos Python

A maioria dos projetos Python neste repositório utiliza o gerenciador de pacotes **[uv](https://docs.astral.sh/uv/)**.

```bash
# 1. Instale o uv (caso não tenha)
pip install uv

# 2. Entre na pasta do projeto desejado
cd "Módulo 2/projeto-01-turismo-langchain"

# 3. Crie o ambiente virtual e instale as dependências
uv sync

# 4. Ative o ambiente virtual
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate

# 5. Configure suas credenciais no arquivo .env
# Adicione sua chave: GOOGLE_API_KEY="sua_chave_aqui"

# 6. Execute o projeto
python main.py
```

> Para os projetos no **Google Colab** (`.ipynb`), basta abrir o notebook no Colab e executar célula por célula, adicionando sua API Key nas Secrets do Colab.

> Para os projetos **n8n** (`.json`), importe o arquivo no n8n através de `Workflows > Import from file`.

---

## 🔑 Chave de API

Os projetos Python utilizam a **API do Google Gemini** e a **API do Groq**. Você pode obter sua chave gratuitamente em:

👉 [Google AI Studio](https://aistudio.google.com/)

👉 [Groq](https://groq.com/)

Após gerar a chave, adicione-a no arquivo `.env` do projeto:

```
GOOGLE_API_KEY="sua_chave_aqui"
```

---

## 📌 Sobre o Geração Tech 3.0

O **Geração Tech** é um programa de formação em tecnologia com foco em preparar profissionais para atuar na área de IA e desenvolvimento de software. O módulo de IA Generativa abrange desde conceitos fundamentais até a construção de sistemas multiagentes complexos.

---

## Autor 

**Luís Henrique**

AI Developer & Educator
