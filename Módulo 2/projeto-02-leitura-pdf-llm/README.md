# Projeto de chatbot com leitura de PDFs e transcrições de vídeos do YouTube

**TUTORIAL DO PROJETO EM VÍDEO:**

[[PROJETO 03] - Chatbot com leitura de PDFs e transcrições de vídeos](https://youtu.be/gO4p6DnYbqo?si=q6jYQ-fR6z3UpZyR)

---

Este projeto constrói do zero um sistema de LLM simples, com LangChain, que faz a leitura de um PDF, transcrição de um vídeo do YouTube e responde o usuário com base nesse PDF ou nesse vídeo.

Exemplo:

- Usuário envia um PDF sobre viagens e o LLM vai responder com base nas informações desse PDF
- Usuário envia um vídeo sobre videogames e então, o sistema faz uma transcrição desse vídeo e responde o usuário com base nessa transcrição

---

## O que é RAG?

RAG (Retrieval-Augmented Generation) é uma arquitetura que combina busca semântica com modelos generativos, permitindo que o LLM produza respostas fundamentadas em fontes externas confiáveis.

É baseado nos seguintes princípios:

1. Recuperação (retrieval):
    - Busca informações relevantes em bases externas usando embeddings vetoriais e métricas de similaridade

1. Aumento (augmentation):
    - Aumenta, enriquece o contexto do Prompt do LLM com dados recuperados, ampliando o conhecimento disponível no momento da resposta

1. Geração (generation):
    - O modelo então gera a resposta final utilizando exclusivamente o contexto fornecido, reduzindo alucinações e aumentando a precisão das respostas.

### Embeddings

As máquinas não conseguem compreender linguagem natural, logo, todo algoritmo de aprendizagem de máquina opera exclusivamente sobre números. 

Com isso, para que textos possam ser analisados, é necessário que eles sejam convertidos em representações numéricas.

A partir disso, chegamos na solução desse problema: a vetorização.

Vetorização é o processo de transformar textos em vetores (sequências de números em espaços multidimensionais).

Nesse espaço multidimensional:

- palavras semanticamente parecidas ficam mais próximas
- conceitos relacionados formam regiões
- operações matemáticas passam a representar relações linguísticas

Com isso, chegamos então aos embeddings, que consistem em vetores densos, que utilizam centenas de dimensões, valores contínuos e aprendizado automático de relações semânticas.

- Capturam similaridade semântica
- Generalizam melhor
- Permitem cálculos vetoriais avançados
- São a bases dos sistemas modernos de LLMs e Processamento de Linguagem Natural (PLN/NLP)

### Em resumo

**Como máquinas entendem textos:**

- Computadores não entendem palavras como nós entendemos. Eles só entendem números.
- Por exemplo, para um computador, a palavra “gato” não significa nada, é só uma sequência de letras
- Para que a máquina consiga trabalhar com textos, entendendo o significado e afins, precisamos transformar as palavras em números

**Vetorização**

- A vetorização é esse processo que transforma textos em números, no caso, em uma sequência de números organizada, chamada “vetor”.
    - Exemplo de vetor de palavra: [0.12, -0.87, 0.45, 0.33, ...]
- A partir disso, cada palavra passa a existir em um espaço cheio de dimensões, como um mapa matemático.
- Nesse mapa, as palavras parecidas ficam próximas umas das outras:
    - “gato” fica perto de “cachorro”, por exemplo
- Palavras com significados diferentes ficam distantes:
    - “gato” fica longe de “avião”
- Conceitos parecidos formam grupos (regiões):
    - Imagina que tem uma região chamada “reino”
    - “rei” possui um conceito, um significado relativamente parecido com o de “rainha” e “príncipe”, logo, eles ficam nessa mesma região.

**Embeddings:**

- Embeddings são uma forma moderna e mais inteligente de fazer essa transformação que vimos acima.
- Embeddings são vetores com centenas de dimensões e aprendidos automaticamente por modelos de IA. Ou seja, o modelo aprende sozinho quais palavras devem ficar próximas.
- Eles são importantes porque eles permitem que o computador:
    - Entenda a similaridade de significado das palavras
    - Perceba relações entre palavras
    - Generalize melhor (ou seja, entender algo mesmo que nunca tenha visto exatamente igual)
    - Faça “contas” que representam relações linguísticas
    

### Agora que entendemos a teoria, vamos praticar!

---

## Fluxo do projeto

```python
Usuário → Envio PDF ou URL → Leitura do PDF ou transcrição do vídeo → Resposta final
```

---

## Tecnologias usadas

- Python
- LangChain
- Google Gemini (API)
- Python-dotenv (carregar variáveis de ambiente)
- PyPDF (Leitura de PDFs)
- Youtube_transcript-api (Transcrever vídeos do YouTube)

---

## Estrutura do projeto

```bash
projeto/
│
├── main.py          # Código do projeto
├── .env             # Chave da API
├── arquivo.pdf      # Arquivo PDF que será lido
└── README.md        # Esse passo a passo
```

---

## Configuração do ambiente

### 1 - Criar ambiente virtual (opcional, mas recomendado)

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows

# ou, com uv:

pip install uv     # instalando o uv
uv venv            # criando um ambiente virtual com uv
```

### 2- Instalar dependências

```bash
pip install langchain
pip install langchain-google-genai 
pip install python-dotenv 
pip install rich
pip install langchain-community
pip install youtube_transcript_api
pip install pypdf
```

Ou, você pode instalar usando uv:

```bash
uv add "langchain[google-genai]"
uv add "langchain-community"
uv add "python-dotenv"
uv add "rich"
uv add "youtube_transcript_api"
uv add "pypdf"
```

### 3 - Criar o arquivo `.env`

```
GOOGLE_API_KEY="coloque_sua_chave_aqui"
```

---

## Entendendo o código linha por linha

---

## Imports

```python
from langchain.chat_models import init_chat_model
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_community.document_loaders import PyPDFLoader, YoutubeLoader
import dotenv
import os
import rich
```

### O que acabamos de importar?

- `init_chat_model`: que vai inicializar nosso modelo de chat do LangChain
- `SystemMessage`: o que vai definir o comportamento do modelo
- `HumanMessage`: representa a mensagem do usuário
- `dotenv` : carrega as variáveis de ambiente
- `rich`: o que vai permitir que a gente imprima as respostas de IA, porém, melhor formatadas
- `PyPDFLoader`: é o nosso leitor de PDF, que vai permitir que a gente leia um PDF e faça uma extração do texto dele
- `YoutubeLoader`: parecido com o de PDF. É o que vai fazer uma transcrição de um vídeo do YouTube que enviaremos, a partir de sua URL

---

## Carregando a chave de API

```python
load_dotenv()
GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY")
```

Ao usarmos o `load_dotenv()`, ele vai carregar todas as nossas variáveis de ambiente no nosso código. 

Usamos então o `os.getenv()` para especificar qual variável de ambiente queremos obter. No caso, queremos a nossa chave de API, que definimos como “GOOGLE_API_KEY”. O valor disso é salvo na variável “GEMINI_API_KEY”.

Na prática, é a mesma coisa que acontece quando a gente vai no Colab e executamos:

```python
from google.colab import userdata
GEMINI_API_KEY = userdata.get('Gemini-API')
```

---

## Função de leitura do PDF

```python
def leitura_pdf(caminho_pdf):
    loader = PyPDFLoader(caminho_pdf)
    lista_documentos = loader.load()

    documento = ""
    for doc in lista_documentos:
        documento += doc.page_content

    return documento
```

- Utilizamos o `def` para criar uma função chamada `leitura_pdf`, que recebe como parâmetro o caminho do nosso pdf.
    - O caminho do PDF seria, por exemplo: *“documentos/projeto/arquivo.pdf”*
    - Ou seja, é o caminho, pelas pastas do computador, até chegar no arquivo

- Dentro da função, criamos uma variável `loader` que recebe `PyPDFLoader(caminho_pdf)`
    - Na prática, nós criamos uma variável, e essa variável recebe o objeto PyPDFLoader, que é o responsável por carregar nosso pdf, ou seja, deixar nosso pdf no ponto pra ser lido posteriormente.

- Após isso, criamos uma variável `lista_documentos` que recebe `loader.load()`.
    - Aqui, nós estamos pegando a nossa variável loader, que tinha o pdf pronto pra fazer a leitura, e agora, por meio do método `load()`, pedimos pra ela fazer a leitura do pdf. Diante disso, todo o texto do PDF é armazenado em formato de lista `[]` dentro da variável lista_documentos.

- Feito isso, agora nós vamos criar um laço de repetição `for`, que vai percorrer cada elemento dessa lista, e vai extrair todo o conteúdo, e armazenar em uma string, na variável `documento`
- Essa string, contendo todo o conteúdo do PDF, será passada para o LLM e, com isso, ele irá responder a gente com base nesse conteúdo.

---

## Função de transcrição de vídeo do YouTube

```python
def leitura_transcricao_youtube(url_video):
    loader = YoutubeLoader.from_youtube_url(url_video, language=["pt"])
    lista_documentos = loader.load()

    documento = ""
    for doc in lista_documentos:
        documento += doc.page_content

    return documento
```

- A lógica aqui é a mesma da função de leitura do PDF.
- Criamos uma função, com `def` . Nomeamos essa função como `leitura_transcricao_youtube` e passamos a url do vídeo que queremos transcrever como parâmetro.
- Criamos uma variável `loader`, que recebe `YoutubeLoader`, e acessa o método `from_youtube_url()`, passando a url do vídeo, e o idioma.
    - Com isso, temos uma variável com a transcrição do nosso vídeo, em português, pronta para ser carregada.
- Após isso, criamos uma variável `lista_documentos` que recebe `loader.load()`.
    - Aqui, nós estamos pegando a nossa variável loader e agora, por meio do método `load()`, pedimos pra ela fazer a leitura da transcrição.
    - Diante disso, todo o texto da transcrição é armazenado em formato de lista `[]` dentro da variável lista_documentos.

- Feito isso, agora nós vamos criar um laço de repetição `for`, que vai percorrer cada elemento dessa lista, e vai extrair todo o conteúdo, e armazenar em uma string, na variável `documento`
- Essa string, contendo todo o conteúdo do vídeo, será passada para o LLM e, com isso, ele irá responder a gente com base nesse conteúdo.

---

## Função de resposta do LLM

```python
def resposta_llm(pergunta, documento):
    prompt = f"""
    Você é um assistente extremamente gentil, amigável, expert em tecnologia e produz respostas precisas. Seu nome é Markus.
    Você utiliza as seguintes informações: {documento} para gerar as suas respostas, com base nas perguntas que os usuários enviam.
    """

    system_message = SystemMessage(prompt)
    human_message = HumanMessage(pergunta)

    messages = [system_message, human_message]

    resposta = llm.invoke(messages)

    return resposta.text
```

- Criamos uma função chamada `resposta_llm`.
- Essa função recebe duas coisas:
    - a pergunta do usuário
    - o texto do documento (PDF, vídeo, etc.)
    
- Depois criamos um **texto de instruções** chamado `prompt`.
- Esse texto diz para a IA:
    - quem ela é,
    - como deve responder,
    - e que deve usar o conteúdo do documento para responder.
    
- Em seguida, organizamos a conversa em duas partes:
    - uma mensagem de **instrução para a IA**
    - e a **pergunta do usuário**.
- Essas mensagens são reunidas em uma lista chamada `messages`, que representa a conversa enviada para a IA.
- Depois usamos:

```python
llm.invoke(messages)
```

para enviar a conversa ao modelo de IA e obter uma resposta.

- Por fim, retornamos apenas o texto da resposta gerada pela IA.

---

## Executando nosso código em loop

```python
# LAÇO DE REPETIÇÃO
print("="*80)
print(f"{'BEM-VINDO(A) AO GERAÇÃO TECH AI!':^80}")
print("="*80)

texto_selecao = """
Digite [1] se você quiser conversar com um PDF
Digite [2] se você quiser conversar com um vídeo do YouTube

"""

while True:
    selecao_usuario = str(input(texto_selecao))

    if (selecao_usuario) == '1':
        caminho_pdf = str(input("Digite o caminho do seu PDF: "))
        documento = leitura_pdf(caminho_pdf)
        break

    elif (selecao_usuario) == '2':
        url_youtube = str(input("Digite a URL do vídeo do YouTube: "))
        documento = leitura_transcricao_youtube(url_youtube)
        break 
    
    else:
        print("Por favor, digite uma opção válida!")
        

while True:
    print(f"{'USUÁRIO':=^80}")
    pergunta_usuario = str(input("Digite a sua pergunta ou pressione [Q] para sair da conversa: "))
    print()

    if pergunta_usuario in ["Q", "q"]:
        print("Saindo...")
        break

    else:
        resposta = resposta_llm(pergunta_usuario, documento)
        
        print(f"{'IA':=^80}")
        rich.print(resposta)
        print()

```

### Mensagem inicial

```python
print("="*80)
print(f"{'BEM-VINDO(A) AO GERAÇÃO TECH AI!':^80}")
print("="*80)
```

Aqui mostramos uma mensagem de boas-vindas formatada na tela para o usuário.

```python
Resultado:
================================================================================
                        BEM-VINDO(A) AO GERAÇÃO TECH AI!
================================================================================

```

### Menu de seleção

```python
texto_selecao = """
Digite [1] se você quiser conversar com um PDF
Digite [2] se você quiser conversar com um vídeo do YouTube
"""
```

Esse texto é exibido para o usuário escolher o que deseja usar.

### Programa espera uma escolha válida

```python
while True:
    selecao_usuario = str(input(texto_selecao))

```

Aqui o programa entra em repetição até o usuário escolher uma opção válida.

### Usuário escolhe PDF

```python
if selecao_usuario =='1':
```

O programa:

1. pede o caminho do PDF,
2. lê o arquivo,
3. guarda o texto para a conversa,
4. sai do menu.

---

### Usuário escolhe YouTube

```python
elif selecao_usuario =='2':
```

O programa:

1. pede o link do vídeo,
2. pega a transcrição,
3. guarda o texto,
4. sai do menu.

---

### Caso digite errado

```python
else:print("Por favor, digite uma opção válida!")
```

O programa avisa e pergunta novamente.

## Segunda parte do loop: conversa com a IA

Depois que o  primeiro loop foi executado e o documento (PDF ou Transcrição) já foi carregado, começa a conversa.

### Fazemos uma conversa contínua com outro While True

```python
while True:
```

Aqui o programa permite fazer perguntas sem limite, até o usuário decidir sair.

### Pergunta do usuário

```python
 print(f"{'USUÁRIO':=^80}")
    pergunta_usuario = str(input("Digite a sua pergunta ou pressione [Q] para sair da conversa: "))
    print()

    if pergunta_usuario in ["Q", "q"]:
        print("Saindo...")
        break
```

O usuário digita sua pergunta.

Se digitar **Q** ou **q**, o programa encerra.

### Gerando a resposta da IA

Se não sair, ou seja, se for pro else:

```python
resposta = resposta_llm(pergunta_usuario, documento)
```

A pergunta é enviada para a IA junto com o conteúdo do documento obtido no While True anterior.

Então, usando o rich, mostramos a resposta na tela.

```python
rich.print(resposta)
```

---

## Código final do projeto

```python
# IMPORTS
from langchain.chat_models import init_chat_model
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_community.document_loaders import PyPDFLoader, YoutubeLoader
import dotenv
import os
import rich

# CARREGANDO NOSSA CHAVE DE API
dotenv.load_dotenv()

GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY")

# DEFININDO NOSSO LLM
llm = init_chat_model(
    "gemini-2.5-flash",
    model_provider="google_genai",
    api_key = GEMINI_API_KEY
    )

# CRIANDO FUNÇÕES DO PROJETO
def leitura_pdf(caminho_pdf):
    loader = PyPDFLoader(caminho_pdf)
    lista_documentos = loader.load()

    documento = ""
    for doc in lista_documentos:
        documento += doc.page_content

    return documento

def leitura_transcricao_youtube(url_video):
    loader = YoutubeLoader.from_youtube_url(url_video, language=["pt"])
    lista_documentos = loader.load()

    documento = ""
    for doc in lista_documentos:
        documento += doc.page_content

    return documento

def resposta_llm(pergunta, documento):
    prompt = f"""
    Você é um assistente extremamente gentil, amigável, expert em tecnologia e produz respostas precisas. Seu nome é Markus.
    Você utiliza as seguintes informações: {documento} para gerar as suas respostas, com base nas perguntas que os usuários enviam.
    """

    system_message = SystemMessage(prompt)
    human_message = HumanMessage(pergunta)

    messages = [system_message, human_message]

    resposta = llm.invoke(messages)

    return resposta.text

# LAÇO DE REPETIÇÃO
print("="*80)
print(f"{'BEM-VINDO(A) AO GERAÇÃO TECH AI!':^80}")
print("="*80)

texto_selecao = """
Digite [1] se você quiser conversar com um PDF
Digite [2] se você quiser conversar com um vídeo do YouTube

"""

while True:
    selecao_usuario = str(input(texto_selecao))

    if (selecao_usuario) == '1':
        caminho_pdf = str(input("Digite o caminho do seu PDF: "))
        documento = leitura_pdf(caminho_pdf)
        break

    elif (selecao_usuario) == '2':
        url_youtube = str(input("Digite a URL do vídeo do YouTube: "))
        documento = leitura_transcricao_youtube(url_youtube)
        break 
    
    else:
        print("Por favor, digite uma opção válida!")
        

while True:
    print(f"{'USUÁRIO':=^80}")
    pergunta_usuario = str(input("Digite a sua pergunta ou pressione [Q] para sair da conversa: "))
    print()

    if pergunta_usuario in ["Q", "q"]:
        print("Saindo...")
        break

    else:
        resposta = resposta_llm(pergunta_usuario, documento)
        
        print(f"{'IA':=^80}")
        rich.print(resposta)
        print()

```

---

## FIM DO PROJETO