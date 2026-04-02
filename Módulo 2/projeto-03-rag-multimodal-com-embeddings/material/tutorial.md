# Projeto RAG com Embeddings (PDF, YouTube e Imagem)

---

> ESTE PROJETO FOI CRIADO PARA FINS DIDÁTICOS, COM O OBJETIVO DE EXPLICAR O FUNCIONAMENTO DE EMBEDDINGS E VECTORSTORE AOS ALUNOS DO CURSO DE GENAI DO GERAÇÃO TECH 2026!

> O README ABAIXO APRESENTA O PASSO A PASSO DE COMO CONSTRUIR DO ZERO ESTE PROJETO.

---

Este projeto constrói do zero um sistema de LLM para terminal, com LangChain, que pode fazer a leitura de um PDF, transcrição de um vídeo do YouTube, enxergar uma imagem e responder o usuário com base nesse PDF, vídeo ou imagem enviado.

Exemplo:

- Usuário envia um PDF sobre viagens e o LLM vai responder com base nas informações desse PDF
- Usuário envia um vídeo sobre videogames e então, o sistema faz uma transcrição desse vídeo e responde o usuário com base nessa transcrição
- Se o usuário envia uma foto com uma roupa, o LLM vai responder com base na imagem dessa roupa

Esse projeto vai ser relativamente diferente do que fizemos antes, pois vai ser construído de uma forma mais estruturada, com mais arquivos, e utilizando o sistema de embeddings.


---

# Fluxo do projeto

```bash
Usuário → Envio PDF, URL ou Imagem → Leitura do PDF, Vídeo YT ou Imagem → Resposta final
```

---

# Tecnologias usadas

- Python
- LangChain
- Google Gemini (API)
- Python-dotenv (carregar variáveis de ambiente)
- PyPDF (Leitura de PDFs)
- Youtube_transcript_api (Transcrever vídeos do YouTube)
- GoogleGenerativeAIEmbeddings

---

## Estrutura do projeto

```bash
projeto/
│
├── utils/
│			├── pdf.py             # Código da leitura do PDF
│     ├── youtube.py         # Código de transcrição do vídeo do YT
│     ├── view_image.py      # Código pro LLM ver a imagem
│     ├── text_splitter.py   # Código pra dividir os textos em pedaços menores (chunks)
│     ├── embeddings.py      # Código pra transformar chunks em embeddings e armazená-los
│     └── chatbot.py         # Código que junta todas as funções e passa pro LLM responder
│
├── main.py          # Código que irá rodar o projeto
├── .env             # Chave da API
├── arquivo.pdf      # Arquivo PDF que será lido
├── imagem.png       # Imagem que será lida
└── README.md        # Esse passo a passo
```

---

# ETAPA 01 - PRIMEIROS PASSOS

## Primeiro, vamos criar a pasta do nosso projeto

- Aperta as teclas **`Win + R`** e digite **`CMD`** → Enter
- No terminal, vá até o Desktop usando o comando **`cd Desktop`**
- Após isso, crie a pasta do seu projeto com **`mkdir projeto-connor-ai`** **(pode ser o nome que você quiser)**
- Entre na pasta que você acabou de criar com o comando **`cd`**, igual fizemos com Desktop.
- Agora, dentro dessa pasta no terminal, vamos para as próximas etapas.

## Criando o ambiente virtual

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows

# ou, com uv:

pip install uv     # instalando o uv
uv venv            # criando um ambiente virtual com uv
```

## Instalando as dependências

Instale manualmente as bibliotecas listadas:

```bash
pip install langchain-community
pip install langchain-text-splitters
pip install langchain[google-genai]
pip install pillow
pip install pypdf
pip install python-dotenv
pip install rich
pip install youtube-transcript-api
```

caso queira instalar com *UV*:

```bash
uv add "langchain-community"
uv add "langchain-text-splitters"
uv add "langchain[google-genai]"
uv add "pillow"
uv add "pypdf"
uv add "python-dotenv"
uv add "rich"
uv add "youtube-transcript-api"
```

## Criar arquivo `.env`

No terminal, após ter baixado as dependências, digite **`code .`**

Assim, você irá entrar no VsCode já dentro dessa pasta que você criou.

No VsCode, na raiz do projeto (ou seja, fora, literalmente na raiz), crie:

```
.env
```

Dentro dele, coloque:

```
GOOGLE_API_KEY=SUA_CHAVE_AQUI
```

Essa chave é usada para acessar o modelo Gemini da Google.

Você pode encontrar essa chave no site Google AI Studio.

---

# ETAPA 02 - ORDEM DE CONSTRUÇÃO DO PROJETO

Vamos criar o projeto na seguinte ordem:

1. Criar uma pasta **`utils`**
2. Dentro dessa pasta, vamos criar os arquivos:
    1. **`pdf.py`**
    2. **`youtube.py`**
    3. **`view_image.py`**
    4. **`text_splitter.py`**
    5. **`embeddings.py`**
    6. **`chatbot.pt`**
3. Após criar esses arquivos, vamos para fora da pasta **`utils`** e criaremos o arquivo **`main.py`**

---

## A) Criação do arquivo `pdf.py`

Caminho:

```
utils/pdf.py
```

### Código completo

```python
from langchain_community.document_loaders import PyPDFLoader

def leitura_pdf(pdf):
    loader = PyPDFLoader(pdf)
    lista_documentos = loader.load()

    documento = ''

    for doc in lista_documentos:
        documento += doc.page_content

    return documento
```

### Explicação linha por linha

### Imports

```python
from langchain_community.document_loaders import PyPDFLoader
```

- Importa o carregador de PDF da LangChain
- **`PyPDFLoader`** é responsável por abrir PDF, ler ele, separar por páginas e afins.

### Definição da função

```python
def leitura_pdf(pdf):
```

- Cria função chamada **`leitura_pdf`**
- Recebe como parâmetro o caminho do PDF

### Criando o loader

```python
loader = PyPDFLoader(pdf)
```

- Na prática, nós criamos uma variável, e essa variável recebe o objeto PyPDFLoader, que é o responsável por carregar nosso pdf, ou seja, deixar nosso pdf no ponto pra ser lido posteriormente

### Carregando o conteúdo

```python
lista_documentos = loader.load()
```

- **`.load()`**:
    - Lê o PDF
    - Retorna um lista de objetos Document, ou seja, retorna uma lista com cada pedaço do texto do PDF que ele leu
    - Armazenamos esses textos na variável **`lista_documentos`**

### Inicializando string

```python
documento = ''
```

Cria string vazia para armazenar texto completo.

### Loop

```python
for doc in lista_documentos:
    documento += doc.page_content
```

- Percorre cada página
- Acessa **`page_content`**, ou seja, o conteúdo de cada página que tá armazenado em lista_documentos
- Concatena tudo em uma única string

---

### Retorno

```python
return documento
```

Retorna o texto completo do PDF.

---

## B) Criação do arquivo `youtube.py`

Caminho:

```
utils/pdf.py
```

### Código completo

```python
from langchain_community.document_loaders import YoutubeLoader

def transcricao_youtube(url):
    loader = YoutubeLoader.from_youtube_url(url, language=['pt'])
    lista_documento = loader.load()

    documento = ''

    for doc in lista_documento:
        documento += doc.page_content

    return documento
```

### Explicação

### Imports

```python
from langchain_community.document_loaders import YoutubeLoader
```

Loader que extrai transcrição do YouTube.

### Função

```python
def transcricao_youtube(url):
```

Recebe URL do vídeo.

### Criando loader

```python
YoutubeLoader.from_youtube_url(url, language=['pt'])
```

- Extrai a transcrição de um vídeo a partir da URL, no idioma Português

### Load

```python
lista_documento = loader.load()
```

Retorna lista de documentos (blocos de transcrição).

Mesma lógica de como foi com o PDF

---

### Loop e retorno da função

```python
for doc in lista_documentos:
    documento += doc.page_content
    
return documento
```

- Percorre cada página
- Acessa **`page_content`**, ou seja, o conteúdo de cada página que tá armazenado em lista_documentos
- Concatena tudo em uma única string
- Ao final, retorna o texto completo do PDF.

---

## C) Criação do arquivo `view_image.py`

### Código completo

```python
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage, SystemMessage
from dotenv import load_dotenv
import os
import base64

load_dotenv()

GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY")

llm = init_chat_model(
    "gemini-2.5-flash",
    model_provider="google-genai",
    api_key=GEMINI_API_KEY,
    temperature=0.4
)

def encode_image(imagem):
    with open(imagem, "rb") as img_file:
        imagem_base64 = base64.b64encode(img_file.read()).decode("utf-8")
        return imagem_base64

def passa_imagem_pro_llm(caminho_imagem):
    imagem = caminho_imagem

    image_base64 = encode_image(imagem)

    human_message = HumanMessage(
        content=[
            {
                "type": "text",
                "text": "Descreva detalhadamente o que há nesta imagem"
            },
            {
                "type": "image_url",
                "image_url": f"data:image/png;base64,{image_base64}",
            },
        ]
    )

    system_message = SystemMessage("Você é um assistente que analisa imagens com precisão e as descreve de forma completa, em cada detalhe, e precisa")

    messages = [system_message, human_message]

    resposta_llm = llm.invoke(messages)

    return resposta_llm.text
```

---

### Importações

```python
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage, SystemMessage
from dotenv import load_dotenv
import os
import base64
```

- **`init_chat_model`** : Função usada para inicializar um modelo de chat via LangChain.
- **`HumanMessage e SystemMessage`** : Representam mensagens dentro de uma conversa estruturada (como se fosse um chat com papéis definidos).
- **`load_dotenv`**: Permite carregar variáveis do arquivo **`.env`**.
- **`os`**: Usado para acessar variáveis de ambiente.
- **`base64`**: Biblioteca usada para converter arquivos binários (como imagens) em texto codificado.

---

### Carregando a chave da API

```python
load_dotenv()

GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY")
```

- **`load_dotenv()`**
    
    Lê o arquivo `.env` e carrega as variáveis no ambiente do sistema.
    
- **`os.getenv("GOOGLE_API_KEY")`**
    
    Busca o valor da variável chamada **`GOOGLE_API_KEY`**.
    

Isso evita deixar a chave da API escrita diretamente no código, o que é uma boa prática de segurança.

---

### Inicializando o modelo

```python
llm = init_chat_model(
    "gemini-2.5-flash",
    model_provider="google-genai",
    api_key=GEMINI_API_KEY,
    temperature=0.4
)
```

**Explicação dos parâmetros:**

- **`"gemini-2.5-flash"`**
    
    Nome do modelo que será utilizado.
    
- **`model_provider="google-genai"`**
    
    Define que o provedor do modelo é o Google.
    
- **`api_key=GEMINI_API_KEY`**
    
    Passa a chave para autenticação.
    
- **`temperature=0.4`**
    
    Controla o nível de criatividade do modelo.
    
    Valores menores deixam a resposta mais previsível e controlada.
    

Essa parte configura o modelo que será usado para analisar a imagem.

---

### Função para converter imagem em Base64

```python
def encode_image(imagem):
    with open(imagem, "rb") as img_file:
        imagem_base64 = base64.b64encode(img_file.read()).decode("utf-8")
        return imagem_base64
```

### Linha por linha:

- **`def encode_image(imagem):`**
    
    Define uma função que recebe o caminho de uma imagem.
    
- **`open(imagem, "rb")`**
    
    Abre o arquivo em modo leitura binária.
    
    Imagens são arquivos binários, não texto.
    
- **`as img_file:`**
    
    Atribui o apelido “img_file” à imagem que está sendo lida de forma binária
    
- **`base64.b64encode(img_file.read())`**
    
    Converte os bytes da imagem (img_file) para Base64.
    
- **`.decode("utf-8")`**
    
    Transforma o resultado em string.
    

A função retorna a imagem codificada como texto Base64.

### Por que precisamos converter a imagem para base64?

- Imagens PNG internamente são mais ou menos assim: \x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR…
- O base64 vem com a ideia de transformar qualquer texto binário em texto puro, ideal para ser lido pelos sistemas
- Ou seja, na nossa função, nós abrimos uma imagem em binário, e em seguida, pegamos esse binário da imagem e convertemos para base64, que é um formato de texto puro, com letras maiúsculas, minúsculas, números, sinais, que totalizam 64 caracteres possíveis para usar quando for converter.
- Esse texto então, em base64, pode ser passado em JSON, e consequentemente ser passado para uma IA ler

***Exemplo do que aconteceu na função acima:***

1. A gente leu uma imagem no modo de leitura binário
2. Ou seja, nossa imagem, em PNG, internamente, é assim: 

```python
\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR…
```

1. Após ela ser lida em binário, ficou assim:

```python
01001000 01101001
```

1. Repara como isso não é texto puro? Isso não pode ser passado em um JSON e ser enviado para a IA, porque eles não vão entender esse binário. Eles precisam de texto puro legível.
2. Passamos então o base64 pra transformar esse binário em texto legível. Após converter, fica mais ou menos assim:

```python
iVBORw0KGgoAAAANSUhEUgAA...
```

1. Agora sim, temos a nossa imagem convertida em texto legível, e consequentemente podemos enviar pra IA
2. Quando ela receber essa imagem em base64, ela vai decodificar tudo e reconstruir a imagem original, e a partir disso vai ler a imagem!
3. É a mesma ideia quando uma pessoa manda uma mensagem em código morse e a outra pessoa decodifica para ver a mensagem original!

### Função principal: enviar imagem para o modelo

```python
def passa_imagem_pro_llm(caminho_imagem):
```

Essa função coordena todo o processo.

---

### Codificando a imagem

```python
imagem = caminho_imagem
image_base64 = encode_image(imagem)
```

- Recebe o caminho da imagem.
- Converte a imagem para Base64 usando a função anterior.

### Criando a mensagem do usuário

```python
human_message = HumanMessage(
    content=[
        {
            "type": "text",
            "text": "Descreva detalhadamente o que há nesta imagem"
        },
        {
            "type": "image_url",
            "image_url": f"data:image/png;base64,{image_base64}",
        },
    ]
)
```

Aqui temos algo importante.

O conteúdo da mensagem é uma lista com dois blocos:

1. Um bloco de texto (a instrução).
2. Um bloco de imagem.

### Bloco de texto:

```python
{
    "type": "text",
    "text": "Descreva detalhadamente o que há nesta imagem"
}
```

Esse é o prompt.

### Bloco de imagem:

```python
{
    "type": "image_url",
    "image_url": f"data:image/png;base64,{image_base64}",
}
```

A imagem está sendo enviada no formato:

```
data:image/png;base64,...
```

Esse formato permite embutir a imagem diretamente na requisição.

> ATENÇÃO: só serão permitidas imagens no formato “png”
> 

---

### Criando a System Message

```python
system_message = SystemMessage(
    "Você é um assistente que analisa imagens com precisão e as descreve de forma completa, em cada detalhe, e precisa"
)
```

A **`SystemMessage`** define o comportamento do modelo.

Ela funciona como uma instrução de alto nível que guia o estilo e a postura da resposta.

---

### Montando a conversa

```python
messages = [system_message, human_message]
```

O modelo recebe uma lista de mensagens.

A ordem importa:

1. Primeiro a instrução de sistema.
2. Depois a mensagem do usuário com texto + imagem.

---

### Chamando o modelo

```python
resposta_llm = llm.invoke(messages)
```

Aqui o modelo é realmente executado.

Ele recebe:

- Instrução de comportamento
- Prompt textual
- Imagem codificada

Processa tudo e gera uma resposta.

---

### Retornando apenas o texto

```python
return resposta_llm.text
```

O objeto retornado pelo modelo contém metadados.

Aqui estamos retornando apenas o conteúdo textual da resposta.

---

## D) Criação do arquivo `text_splitter.py`

### Código completo

```python
from langchain_text_splitters import CharacterTextSplitter

def cria_chunks_de_texto(documento):
    text_splitter = CharacterTextSplitter(
        separator="\\n",
        chunk_size=1500,
        chunk_overlap=300,
        length_function=len
    )

    chunks = text_splitter.split_text(documento)

    return chunks
```

### Importação

```python
from langchain_text_splitters import CharacterTextSplitter
```

- **`from langchain_text_splitters import ...`** → Estamos importando algo de uma biblioteca.
- **`langchain_text_splitters`** → Módulo da biblioteca LangChain responsável por dividir textos.
- **`CharacterTextSplitter`** → Classe que permite dividir um texto grande em pedaços menores (chunks).

Em resumo: estamos importando uma ferramenta que serve para dividir texto.

### Definição da função

```python
def cria_chunks_de_texto(documento):
```

- **`def`** → Define uma função.
- **`cria_chunks_de_texto`** → Nome da função.
- **`(documento)`** → Parâmetro que a função recebe.

Essa função:

- Recebe um texto grande (**`documento`)**
- Retorna esse texto dividido em partes menores (chunks)

### Criação do divisor de texto

```python
text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1500,
        chunk_overlap=300,
        length_function=len
    )
```

Aqui estamos criando o divisor do texto e configurando como ele vai cortar o texto.

### **Parâmetro 1: separator**

```python
separator="\n",
```

- **`\n`** significa **quebra de linha**. (ou seja, vai pra linha de baixo)
- Isso indica que o texto será dividido usando quebras de linha como base.

Ou seja:

O splitter tentará dividir o texto respeitando as quebras de linha.

### **Parâmetro 2: chunk_size**

```python
chunk_size=1500,
```

- Define o **tamanho máximo de cada pedaço de text**.
- Aqui cada chunk pode ter até **1500 caracteres**.

Se o texto for maior que isso, ele será dividido.

### **Parâmetro 3: chunk_overlap**

```python
chunk_overlap=300,
```

Significa que o próximo pedaço vai repetir 300 caracteres do pedaço anterior.

Por quê?

- Porque isso evita perder informação no meio.

Exemplo simplificado:

*Texto grande:*

```
A B C D E F G H I J K L M N O P
```

Se cada pedaço fosse de 5 letras com 2 de repetição:

*Chunk 1:*

```
A B C D E
```

*Chunk 2:*

```
D E F G H
```

Percebe que D e E aparecem de novo?

Isso ajuda a IA a manter o contexto.

### Parâmetro 4: length_function

```python
length_function=len
```

- Define como o tamanho será medido.
- **`len`** é a função padrão do Python que conta caracteres.

Ou seja:

O tamanho de 1500 será contado em **quantidade de caracteres**.

### Divisão do texto

```python
chunks = text_splitter.split_text(documento)
```

Aqui acontece a mágica:

- **`split_text()`** → método que divide o texto.
- **`documento`** → texto que foi passado para a função.
- O resultado é uma **lista de pedaços menores**.

Exemplo de retorno:

```python
[
  "Primeiro pedaço do texto...",
  "Segundo pedaço do texto...",
  "Terceiro pedaço..."
]
```

---

### Retorno

```python
return chunks
```

- A função devolve a lista com os pedaços de texto.

Quando chamar essa função, você vai receber os chunks prontos para uso 

---

## E) Criação do arquivo `embeddings.py`

### Código completo

```python
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_core.vectorstores import InMemoryVectorStore
from dotenv import load_dotenv
import os

load_dotenv()

GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY")

def cria_embeddings(chunks):
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001",
        api_key=GEMINI_API_KEY
    )

    vectorstore = InMemoryVectorStore.from_texts(
        chunks,
        embedding=embeddings
    )

    return vectorstore
```

### Explicação

### Importações

```python
from langchain_google_genai import GoogleGenerativeAIEmbeddings
```

- Importa a classe responsável por gerar **embeddings usando a API do Google Gemini**.
- Essa classe conecta seu código ao modelo de embeddings do Google.

```python
from langchain_core.vectorstores import InMemoryVectorStore
```

- Importa uma estrutura de armazenamento vetorial.
- **`InMemoryVectorStore`** guarda os vetores na memória RAM.

```python
from dotenv import load_dotenv
import os
```

- **`dotenv`** permite carregar variáveis de ambiente do arquivo **`.env`**.
- **`os`** permite acessar variáveis do sistema.

### Carregando variáveis de ambiente

```python
load_dotenv()
```

- Lê o arquivo **`.env`**
- Carrega variáveis como **`GOOGLE_API_KEY`** para o ambiente

```
GEMINI_API_KEY=os.getenv("GOOGLE_API_KEY")
```

- Busca a variável **`GOOGLE_API_KEY`**
- Armazena o valor na variável **`GEMINI_API_KEY`**

> Isso evita colocar a chave da API diretamente no código (boa prática de segurança).
> 

### Função Principal

```python
def cria_embeddings(chunks):
```

Essa função:

- Recebe uma lista de textos (**`chunks`**)
- Retorna um vector store com embeddings prontos

### Criando o modelo de embeddings

```python
embeddings = GoogleGenerativeAIEmbeddings(
	model = "models/gemini-embedding-001",
	api_key = GEMINI_API_KEY
)
```

Aqui está o ponto central.

Estamos criando um objeto que:

- Usa o modelo **`"models/gemini-embedding-001"`**
- Se autentica com sua chave de API

### (relembrando) O que é embedding?

Embedding é:

> Uma representação numérica do significado um texto.
> 

Exemplo conceitual:

Texto:

```
"gato"
```

Pode virar algo como:

```
[0.123, -0.981, 0.443, ...]
```

Esse vetor captura significado semântico.

Textos parecidos terão vetores parecidos.

### Criando o Vector Store

```python
vectorstore = InMemoryVectorStore.from_texts(
	chunks,
	embedding = embeddings
)
```

Aqui acontece o processamento real:

1. Cada item da lista **`chunks`** é enviado para o modelo de embeddings.
2. O modelo transforma cada texto em vetor.
3. O **`InMemoryVectorStore`** armazena:
    - O texto original
    - O vetor correspondente

Internamente fica algo como:

| Texto | Vetor |
| --- | --- |
| Chunk 1 | [0.23, 0.88, ...] |
| Chunk 2 | [0.11, 0.45, ...] |

### O que significa `.from_texts`?

É um método que:

- Recebe textos
- Gera embeddings automaticamente
- Cria o vector store já populado

É uma forma simplificada de fazer tudo em uma única chamada.

### Retorno

```python
return vectorstore
```

A função retorna o banco vetorial.

Agora você pode fazer:

```python
vectorstore.similarity_search("pergunta do usuário")
```

E ele buscará os chunks semanticamente mais próximos.

---

# F) Criação do arquivo `chatbot.py`

### Código completo

```python
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from dotenv import load_dotenv
import os

load_dotenv()

GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY")

def monta_contexto(docs):
    textos = ""

    for doc in docs:
        textos += doc.page_content

    return textos

llm = init_chat_model(
    "gemini-2.5-flash",
    model_provider="google-genai",
    api_key=GEMINI_API_KEY,
    temperature=0.4
)

def injeta_contexto_no_llm(vectorstore, pergunta, historico_conversa):

    docs = vectorstore.similarity_search(pergunta, k=3)

    contexto = monta_contexto(docs)

    prompt = f"""
    Você é um assistente...
    Suas respostas serão feitas com base no contexto: {contexto}
    """

    system_message = SystemMessage(prompt)
    human_message = HumanMessage(pergunta)

    mensagens = [system_message] + historico_conversa + [human_message]

    resposta_llm = llm.invoke(mensagens)

    ai_message = AIMessage(resposta_llm.text)

    historico_conversa.append(human_message)
    historico_conversa.append(ai_message)

    return str(resposta_llm.text)
```

---

### Importações

```python
from langchain.chat_models import init_chat_model
```

Importa a função que inicializa o modelo de chat.

---

```python
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
```

Importa os três tipos de mensagens usados na conversa:

- **`SystemMessage`** → define instruções e comportamento
- **`HumanMessage`** → representa o usuário
- **`AIMessage`** → representa a resposta do modelo

---

```python
from dotenv import load_dotenv
import os
```

- **`dotenv`** → carrega variáveis do **`.env`**
- **`os`** → acessa variáveis do sistema

---

### Carregando a API Key

```python
load_dotenv()

GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY")
```

Carrega a chave da API do ambiente.

Boa prática: manter credenciais fora do código.

---

### Função `monta_contexto`

```python
def monta_contexto(docs):
    textos = ""

    for doc in docs:
        textos += doc.page_content

    return textos
```

Essa função recebe uma lista de documentos recuperados do vector store.

### Linha por linha:

- **`textos = ""`**
    
    Inicializa uma string vazia.
    
- **`for doc in docs:`**
    
    Percorre cada documento recuperado.
    
- **`doc.page_content`**
    
    Cada objeto **`doc`** contém o texto original no atributo **`page_content`**.
    
- **`textos += doc.page_content`**
    
    Concatena todos os textos em uma única string.
    
- **`return textos`**
    
    Retorna o contexto completo consolidado.
    

Essa função transforma vários chunks em um único bloco de contexto.

---

### Inicialização do Modelo

```python
llm = init_chat_model(
    "gemini-2.5-flash",
    model_provider="google-genai",
    api_key=GEMINI_API_KEY,
    temperature=0.4
)
```

Configura o modelo:

- Modelo rápido e multimodal.
- Temperatura controlada.
- Autenticação via API Key.

Esse modelo será usado para responder às perguntas.

---

### Função Principal: RAG Conversacional

```python
def injeta_contexto_no_llm(vectorstore, pergunta, historico_conversa):
```

Essa função executa o fluxo completo de pergunta + busca + resposta.

Ela recebe:

- `vectorstore` → banco vetorial já populado
- `pergunta` → pergunta atual do usuário
- `historico_conversa` → lista com mensagens anteriores

---

### Busca semântica

```python
docs = vectorstore.similarity_search(pergunta, k=3)
```

O que acontece aqui:

- A pergunta é transformada em embedding.
- O sistema busca os 3 documentos mais semelhantes (**`k=3`**).
- Retorna uma lista de documentos relevantes.

Isso é a etapa de recuperação (Retrieval).

---

### Montagem do contexto

```python
contexto = monta_contexto(docs)
```

Une os textos recuperados em um único bloco.

Agora temos um contexto consolidado.

### Construção do prompt

```python
prompt = f"""
Você é um assistente de IA extremamente gentil e amigável, expert em tecnologia e 
responde perguntas de forma precisa e eficaz, de maneira didática, passo a passo, 
extremamente fácil de compreender, mas sem usar uma linguagem extremamente infantil. 
Seu nome é Connor.

Suas respostas serão feitas com base no contexto: {contexto}
"""
```

Aqui ocorre a injeção de contexto.

O modelo recebe instruções dizendo que:

- Ele deve se basear no contexto recuperado.
- O contexto está explicitamente inserido no SystemMessage.

Isso caracteriza a etapa de Augmented Generation do RAG.

---

### Criação das mensagens

```python
system_message = SystemMessage(prompt)
human_message = HumanMessage(pergunta)
```

- **`SystemMessage`** contém instruções + contexto.
- **`HumanMessage`** contém a pergunta atual.

---

### Montando a conversa completa

```python
mensagens = [system_message] + historico_conversa + [human_message]
```

Aqui temos algo importante.

A ordem final das mensagens fica:

1. SystemMessage (com contexto)
2. Histórico anterior (perguntas e respostas)
3. Pergunta atual

Isso permite que o modelo:

- Saiba o contexto do documento
- Saiba o que já foi conversado
- Responda de forma coerente

---

### Chamando o modelo

```python
resposta_llm = llm.invoke(mensagens)
```

O modelo processa:

- Instruções
- Contexto recuperado
- Histórico
- Pergunta atual

E gera uma resposta.

---

### Criando a mensagem de resposta

```python
ai_message = AIMessage(resposta_llm.text)
```

Transforma o texto retornado em um objeto de mensagem.

Isso permite manter o padrão estrutural da conversa.

---

### Atualizando o histórico

```python
historico_conversa.append(human_message)
historico_conversa.append(ai_message)
```

Adiciona:

- A pergunta atual
- A resposta do modelo

Assim, nas próximas interações, o modelo terá memória da conversa.

---

### Retorno

```python
return str(resposta_llm.text)
```

Retorna apenas o texto da resposta.

---

# ETAPA 03 - CRIANDO O ORQUESTRADOR DO SISTEMA (`main.py`)

---

## Caminho

```
main.py
```

Esse é o **arquivo principal do projeto**.

Ele é responsável por:

- Controlar o fluxo da aplicação
- Exibir menu interativo
- Decidir qual tipo de entrada será processada
- Conectar todos os módulos:
    - **`pdf.py`**
    - **`youtube.py`**
    - **`text_splitter.py`**
    - **`embeddings.py`**
    - **`chatbot.py`**
    - **`view_image.py`**

Ele é o **orquestrador do sistema RAG**.

---

## Código completo do `main.py`

```python
from utils import chatbot, embeddings, pdf, text_splitter, view_image, youtube
import rich

print("=" * 80)
print(f"{'Olá, meu nome é Connor. Seja bem-vindo(a)!':^80}")
print("=" * 80)

selecao_usuario = """
Digite o número da ação que você deseja:

[1] Conversar com PDFs
[2] Conversar com vídeos do YouTube
[3] Conversar com uma imagem
[4] Sair 

"""

historico_conversa = []

while True:
    input_selecao = str(input(selecao_usuario))

    if input_selecao == "1":
        caminho_pdf = str(input("Digite o caminho do seu PDF: "))
        documento = pdf.leitura_pdf(caminho_pdf)

        chunks_texto = text_splitter.cria_chunks_de_texto(documento)
        vectorstore = embeddings.cria_embeddings(chunks_texto)

        print()
        print("=" * 80)
        print(f"{'PERGUNTA DO USUÁRIO':=^80}")
        print("=" * 80)
        print()

        pergunta_usuario = str(input("Digite a sua pergunta: "))

        resposta = chatbot.injeta_contexto_no_llm(
            vectorstore, pergunta_usuario, historico_conversa
        )

        print()
        print("=" * 80)
        print(f"{'RESPOSTA DA IA':=^80}")
        print("=" * 80)
        print()
        rich.print(resposta)

    elif input_selecao == "2":
        url = str(input("Digite a URL do vídeo do YouTube: "))
        documento = youtube.transcricao_youtube(url)

        chunks_texto = text_splitter.cria_chunks_de_texto(documento)
        vectorstore = embeddings.cria_embeddings(chunks_texto)

        print()
        print("=" * 80)
        print(f"{'PERGUNTA DO USUÁRIO':=^80}")
        print("=" * 80)
        print()

        pergunta_usuario = str(input("Digite a sua pergunta: "))

        resposta = chatbot.injeta_contexto_no_llm(
            vectorstore, pergunta_usuario, historico_conversa
        )

        print()
        print("=" * 80)
        print(f"{'RESPOSTA DA IA':=^80}")
        print("=" * 80)
        print()
        rich.print(resposta)

    elif input_selecao == "3":
        caminho_imagem = str(input("Digite o caminho da sua imagem: "))
        descricao_imagem = view_image.passa_imagem_pro_llm(caminho_imagem)

        chunks_texto = text_splitter.cria_chunks_de_texto(descricao_imagem)
        vectorstore = embeddings.cria_embeddings(chunks_texto)

        print()
        print("=" * 80)
        print(f"{'PERGUNTA DO USUÁRIO':=^80}")
        print("=" * 80)
        print()

        pergunta_usuario = str(input("Digite a sua pergunta: "))

        resposta = chatbot.injeta_contexto_no_llm(
            vectorstore, pergunta_usuario, historico_conversa
        )

        print()
        print("=" * 80)
        print(f"{'RESPOSTA DA IA':=^80}")
        print("=" * 80)
        print()
        rich.print(resposta)

    elif input_selecao == "4":
        print("Saindo...")
        break

    else:
        print("Por favor, digite uma opção válida!")

```

---

### Importações

```python
from utils import chatbot, embeddings, pdf, text_splitter, view_image, youtube
import rich
```

### O que está acontecendo aqui:

- **`from utils import ...`**
    
    Você está importando vários módulos que você mesmo criou dentro da pasta `utils`.
    

Cada um deles tem uma responsabilidade:

- **`chatbot`** → conversa com o LLM
- **`embeddings`** → cria os vetores (vectorstore)
- **`pdf`** → lê PDFs
- **`text_splitter`** → divide texto em chunks
- **`view_image`** → envia imagem para o LLM
- **`youtube`** → transcreve vídeo

Isso é **organização de código**. Cada arquivo faz uma coisa específica.

- **`import rich`**
    
    A biblioteca **`rich`** serve para imprimir textos formatados no terminal (cores, markdown, etc).
    

---

## Mensagem inicial

```python
print("=" * 80)
print(f"{'Olá, meu nome é Connor. Seja bem-vindo(a)!':^80}")
print("=" * 80)
```

### O que isso faz:

- **`"=" * 80`** → cria uma linha com 80 sinais de igual.
- **`:^80`** → centraliza o texto em um espaço de 80 caracteres.

Isso é apenas estética para o terminal.

---

## Menu de opções

```python
selecao_usuario = """
Digite o número da ação que você deseja:

[1] Conversar com PDFs
[2] Conversar com vídeos do YouTube
[3] Conversar com uma imagem
[4] Sair
"""
```

Aqui você define o texto que será mostrado como menu.

---

## Histórico de conversa

```python
historico_conversa = []
```

Você cria uma lista vazia.

Essa lista vai guardar:

- mensagens do usuário
- respostas da IA

Isso permite que o chatbot mantenha contexto ao longo da conversa.

---

## Loop principal

```python
while True:
```

Isso cria um loop infinito.

O programa só para quando o usuário escolher a opção 4.

---

## Captura da escolha do usuário

```python
input_selecao = str(input(selecao_usuario))
```

Aqui:

- Mostra o menu
- Espera o usuário digitar algo
- Converte para string

---

## BLOCO 1 — Conversar com PDF

```python
if input_selecao == "1":
```

Se o usuário escolher 1:

### 1) Pede o caminho do PDF

```python
caminho_pdf = str(input("Digite o caminho do seu PDF: "))
```

---

### 2) Lê o PDF

```python
documento = pdf.leitura_pdf(caminho_pdf)
```

Aqui chama a função que você criou no módulo `pdf`.

Ela retorna o texto completo do PDF.

---

### 3) Divide o texto

```python
chunks_texto = text_splitter.cria_chunks_de_texto(documento)
```

O texto grande vira vários pedaços menores.

---

### 4) Cria embeddings

```python
vectorstore = embeddings.cria_embeddings(chunks_texto)
```

Aqui acontece:

Texto → embeddings → banco vetorial em memória.

Agora você pode fazer busca semântica.

---

### 5) Pede pergunta

```python
pergunta_usuario = str(input("Digite a sua pergunta: "))
```

---

### 6) Injeta contexto no LLM

```python
resposta = chatbot.injeta_contexto_no_llm(
    vectorstore, pergunta_usuario, historico_conversa
)
```

Essa função:

1. Busca os trechos mais relevantes no vectorstore
2. Monta um prompt com contexto
3. Envia para o LLM
4. Atualiza o histórico
5. Retorna a resposta

---

### 7) Exibe resposta

```python
rich.print(resposta)
```

Mostra a resposta formatada.

---

## BLOCO 2 — Conversar com YouTube

```python
elif input_selecao == "2":
```

Fluxo quase idêntico ao PDF.

Diferença principal:

```python
documento = youtube.transcricao_youtube(url)
```

Aqui você transforma o vídeo em texto (transcrição).

Depois o fluxo é igual:

transcrição → chunks → embeddings → pergunta → resposta.

---

## BLOCO 3 — Conversar com imagem

```python
elif input_selecao == "3":
```

Aqui a lógica muda um pouco.

---

### 1) Pega caminho da imagem

```python
caminho_imagem = str(input("Digite o caminho da sua imagem: "))
```

---

### 2) Envia imagem para o LLM

```python
descricao_imagem = view_image.passa_imagem_pro_llm(caminho_imagem)
```

Essa função:

- Converte a imagem em base64
- Envia para o modelo multimodal
- Recebe uma descrição detalhada

Agora você tem **texto descrevendo a imagem**.

---

### 3) Divide a descrição em chunks

```python
chunks_texto = text_splitter.cria_chunks_de_texto(descricao_imagem)
```

---

### 4) Cria embeddings

```python
vectorstore = embeddings.cria_embeddings(chunks_texto)
```

Agora a imagem virou um "documento pesquisável".

---

### 5) Pergunta do usuário

```python
pergunta_usuario = str(input("Digite a sua pergunta: "))
```

---

### 6) Injeta no LLM

Mesmo processo que PDF e YouTube.

---

## BLOCO 4 — Sair

```python
elif input_selecao == "4":
    print("Saindo...")
    break
```

`break` encerra o loop.

---

## Caso opção inválida

```python
else:
    print("Por favor, digite uma opção válida!")
```

Validação básica.

---

# FIM DO PROJETO

---

# Autor

Luís Henrique

ML Engineer | GenAI Teacher @ Geração Tech
