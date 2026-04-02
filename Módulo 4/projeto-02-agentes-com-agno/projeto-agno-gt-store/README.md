# 🤖 Agentes com Agno — GT Store

> **Aula:** Módulo 4 — Agentes com IA  
> **Duração:** 8h às 12h  
> **Pré-requisito:** Conhecimento básico de Python e LangChain  

---

## 📚 O que vamos aprender hoje?

Hoje vamos sair do LangChain e conhecer o **Agno**, um framework mais moderno e direto ao ponto para criar **agentes de IA**.

Se você já usou LangChain, vai perceber que o Agno é mais simples e com menos "burocracia". A ideia central é a mesma: um modelo de linguagem (LLM) que pode usar ferramentas (tools) para tomar decisões e agir no mundo real.

### O que é um Agente?

Um **agente** é um programa que usa um LLM para:
1. **Receber** uma pergunta ou tarefa
2. **Pensar** em como resolver (quais ferramentas usar, em qual ordem)
3. **Agir** — executar as ferramentas e usar os resultados
4. **Responder** ao usuário de forma inteligente

> 💡 **Diferença para um chatbot comum:** Um chatbot apenas conversa. Um agente pode *fazer coisas*: pesquisar na internet, consultar um banco de dados, registrar informações, etc.

---

## 🏪 O Projeto: GT Store

Nosso projeto simula o suporte de uma loja fictícia chamada **GT Store** (uma loja de eletrônicos). Ao longo dos exemplos, vamos evoluir o agente de suporte dessa loja, adicionando capacidades uma a uma.

---

## ⚙️ Configuração do Ambiente

Antes de rodar qualquer exemplo, siga estes passos:

### 1. Clone o repositório e acesse a pasta

```bash
cd projeto-agno-gt-store
```

### 2. Instale as dependências com o `uv`

Este projeto usa o [uv](https://github.com/astral-sh/uv) como gerenciador de pacotes (é o moderno substituto do pip). Se não tiver instalado:

```bash
pip install uv
```

Depois, instale as dependências:

```bash
uv sync
```

Isso vai criar um ambiente virtual `.venv` e instalar tudo que está no `pyproject.toml`:

| Pacote | Para que serve |
|---|---|
| `agno` | O framework principal de agentes |
| `groq` | Acesso à API do Groq (LLM rápido e gratuito) |
| `ddgs` | DuckDuckGo Search — para pesquisa na web |
| `python-dotenv` | Carrega variáveis de ambiente do arquivo `.env` |
| `sqlalchemy` | Banco de dados SQL (usado para memória no ex003) |

### 3. Configure sua chave de API

Crie um arquivo `.env` na raiz do projeto (já existe um de exemplo):

```
GROQ_API_KEY="sua_chave_aqui"
```

> 📝 **Como pegar sua chave Groq:** Acesse [console.groq.com](https://console.groq.com), crie uma conta gratuita e gere uma API key.

### 4. Rode os exemplos

```bash
uv run python exemplos/ex001.py
uv run python exemplos/ex002.py
uv run python exemplos/ex003.py
```

---

## 📂 Estrutura do Projeto

```
projeto-agno-gt-store/
│
├── exemplos/
│   ├── ex001.py          ← Agente básico (ponto de partida!)
│   ├── ex002.py          ← Agente com pesquisa na web
│   ├── ex003.py          ← Agente com tools próprias + memória
│   └── ex003-ingles.py   ← Variação do ex003 (instruções em inglês, sem memória)
│
├── .env                  ← Suas chaves de API (não sobe pro Git!)
├── pyproject.toml        ← Dependências do projeto
└── README.md             ← Este arquivo
```

---

---

## 🟢 EX001 — Meu Primeiro Agente

**Arquivo:** `exemplos/ex001.py`  
**Conceito:** Criar um agente simples usando Agno + Groq

### O que esse exemplo faz?

Cria o agente de suporte mais básico possível da GT Store. Sem ferramentas, sem memória — apenas um LLM com uma **instrução de sistema** (system prompt).

### Código completo

```python
# EX001 - Criando nosso primeiro "agente"

from agno.agent import Agent 
from agno.models.groq import Groq 
from dotenv import load_dotenv

load_dotenv()

agent = Agent(
    model=Groq(id="llama-3.3-70b-versatile"),
    instructions="Você é suporte da GT Store, uma loja de eletrônicos",
    markdown=True,
)

agent.print_response(
    "Me conte sobre o que você faz.",
    stream=True
)
```

### Passo a passo explicado

#### 📦 Imports e carregamento do `.env`

```python
from agno.agent import Agent 
from agno.models.groq import Groq 
from dotenv import load_dotenv

load_dotenv()
```

- `Agent` → A classe principal do Agno. É aqui que tudo acontece.
- `Groq` → O modelo de linguagem que vamos usar. O Groq é uma plataforma que oferece acesso gratuito a modelos como o **LLaMA 3** com velocidade altíssima.
- `load_dotenv()` → Lê o arquivo `.env` e carrega as variáveis (como `GROQ_API_KEY`) para o ambiente.

> 💡 **Comparando com LangChain:** No LangChain, você usaria `ChatGroq` ou `ChatOpenAI`. No Agno, o conceito é o mesmo, mas embrulhado no `Groq(...)`.

#### 🤖 Criando o agente

```python
agent = Agent(
    model=Groq(id="llama-3.3-70b-versatile"),
    instructions="Você é suporte da GT Store, uma loja de eletrônicos",
    markdown=True,
)
```

| Parâmetro | O que faz |
|---|---|
| `model` | Qual LLM usar. Aqui usamos o LLaMA 3.3 70B via Groq |
| `instructions` | O **system prompt** — define a personalidade e papel do agente |
| `markdown=True` | Formata a resposta em Markdown (negrito, listas, etc.) |

#### 💬 Fazendo uma pergunta ao agente

```python
agent.print_response(
    "Me conte sobre o que você faz.",
    stream=True
)
```

- `print_response(mensagem)` → Envia uma mensagem e imprime a resposta no terminal.
- `stream=True` → A resposta vai aparecendo letra por letra, como no ChatGPT. Sem isso, ele espera tudo pronto antes de exibir.

### O que acontece por baixo dos panos?

```
Você (código) ──mensagem──▶ Agno Agent ──prompt──▶ Groq (LLaMA) ──resposta──▶ Terminal
```

Simples assim. O Agno monta o prompt (juntando `instructions` + sua mensagem) e manda para o LLM.

### ✅ Experimente mudar

- Troque o `instructions` para outro papel (ex: "Você é um assistente de culinária")
- Envie perguntas diferentes
- Remova o `stream=True` e veja a diferença

---

---

## 🔵 EX002 — Agente com Ferramentas de Pesquisa

**Arquivo:** `exemplos/ex002.py`  
**Conceito:** Adicionar **Tools** ao agente — aqui, uma ferramenta de pesquisa no DuckDuckGo

### O que esse exemplo faz?

Cria um **agente pesquisador** que consegue buscar informações reais na internet usando o DuckDuckGo. Quando você faz uma pergunta, o agente decide sozinho se precisa pesquisar ou não, e quais sites consultar.

### Código completo

```python
# EX002 - Adicionando tools de pesquisa ao nosso agente

from agno.agent import Agent
from agno.models.groq import Groq 
from agno.tools.duckduckgo import DuckDuckGoTools
from dotenv import load_dotenv 

load_dotenv()

instrucoes = """
        Você é um pesquisador especializado e profissional, que responde todas
        as nossas perguntas com respostas completas e precisas, sem viéses ou erros.

        Para responder às perguntas:
        1. Use no máx. 3 sites diferentes para pesquisar informações;
        2. Acesse os sites e leia todo o conteúdo, sem deixar passar nada;
        3. Busque sempre fontes confiáveis e atualizadas;
        4. Sintetize as informações de forma clara e objetiva;
        5. Cite as fontes utilizadas no final da resposta;
        6. Se notar que nas fontes há algum viés, informe na resposta.

        Seja conciso, mas completo e objetivo em suas respostas.
    """

agente_de_pesquisa = Agent(
    model=Groq(id="openai/gpt-oss-20b"),
    instructions=instrucoes,
    tools=[DuckDuckGoTools(fixed_max_results=3)],
    markdown=True,
)

agente_de_pesquisa.print_response(
    "A Meta adquiriu a ManusAI?",
    stream=True
)
```

### Passo a passo explicado

#### 📦 Novo import

```python
from agno.tools.duckduckgo import DuckDuckGoTools
```

O Agno já vem com uma série de ferramentas prontas. `DuckDuckGoTools` é uma delas — ela permite que o agente pesquise na internet sem precisar de chave de API.

#### 📝 Instructions mais detalhadas

```python
instrucoes = """
    Você é um pesquisador especializado...
    1. Use no máx. 3 sites...
    2. Acesse os sites...
    ...
"""
```

Perceba que o `instructions` virou uma string mais longa e detalhada. Quanto mais específico você for nas instruções, mais previsível e útil será o comportamento do agente.

> 💡 **Dica pedagógica:** Pense no `instructions` como o "manual de trabalho" do agente. Quanto mais detalhado, melhor ele se comporta.

#### 🔧 Adicionando a ferramenta

```python
agente_de_pesquisa = Agent(
    model=Groq(id="openai/gpt-oss-20b"),
    instructions=instrucoes,
    tools=[DuckDuckGoTools(fixed_max_results=3)],  # <-- NOVIDADE!
    markdown=True,
)
```

O parâmetro `tools` recebe uma **lista** de ferramentas. Aqui passamos apenas o DuckDuckGo, configurado para retornar no máximo 3 resultados de busca por pesquisa.

### Como o agente usa a ferramenta?

Isso é o que torna um agente especial! O processo é:

```
Você pergunta: "A Meta adquiriu a ManusAI?"
        │
        ▼
  Agente recebe a pergunta
        │
        ▼
  LLM decide: "Eu não sei isso de cor. Vou pesquisar."
        │
        ▼
  Chama DuckDuckGoTools com: "Meta adquiriu ManusAI"
        │
        ▼
  Recebe os resultados da busca (3 sites)
        │
        ▼
  LLM lê os resultados e formula uma resposta completa
        │
        ▼
  Resposta aparece no terminal
```

> 💡 **Comparando com LangChain:** No LangChain, isso seria feito com `AgentExecutor` + `Tool`. No Agno, basta passar no parâmetro `tools=[]`. Muito mais simples!

### ✅ Experimente mudar

- Mude a pergunta para um tema atual (ex: "Quem ganhou o Oscar 2025?")
- Mude `fixed_max_results=3` para `1` ou `5` e veja como a resposta muda
- Adicione mais ferramentas (o Agno tem ferramentas para Wikipedia, YouTube, etc.)

---

---

## 🔴 EX003 — Agente com Tools Próprias e Memória

**Arquivo:** `exemplos/ex003.py`  
**Conceito:** Criar suas **próprias ferramentas** (funções Python) e adicionar **memória persistente** ao agente

### O que esse exemplo faz?

Evoluímos o agente de suporte da GT Store com:
1. **Nossas próprias ferramentas** — funções Python comuns que o agente pode chamar
2. **Memória com SQLite** — o agente lembra do que foi dito na conversa, mesmo entre execuções diferentes

### Código completo

```python
# EX003 - Aprimorando o nosso agente com nossas próprias Tools

## IMPORTS E CARREGANDO API
from agno.agent import Agent
from agno.models.groq import Groq
from agno.db.sqlite import SqliteDb
from dotenv import load_dotenv

load_dotenv()

## CRIANDO AS TOOLS DO NOSSO AGENTE
PEDIDOS = {
    "#1052": {"status": "enviado", "produto": "Fone Bluetooth", "dias": 3},
    "#1053": {
        "status": "aguardando pagamento",
        "produto": "Teclado AULA F75",
        "dias": "a definir",
    },
    "#1054": {"status": "atrasado", "produto": "Playstation 5", "dias": 12},
}

PRODUTOS = [
    "Fone Bluetooth - R$80,00",
    "Teclado AULA F75 - R$299,00",
    "Playstation 5 Slim (Digital) - R$3257,00",
    "Xbox Series X - R$2999,00",
]


def consultar_pedido(id_pedido: str):
    """Consulta o status de um pedido pelo seu id"""
    pedido = PEDIDOS.get(id_pedido)
    if pedido and pedido["status"] != "aguardando pagamento":
        return f"Pedido {id_pedido}: {pedido['produto']} - {pedido['status']} - {pedido['dias']} para entrega"
    elif pedido:
        return f"Pedido {id_pedido}: {pedido['produto']} - {pedido['status']} - aguardando pagamento"
    return f"Pedido {id_pedido}: não encontrado"


def listar_produtos():
    "Lista os produtos disponíveis na loja"
    return "\n".join(PRODUTOS)


def registrar_reclamacao(numero_pedido, descricao_reclamacao):
    return f"""Reclamação registrada para o pedido {numero_pedido}.
      
      --- 

      Protocolo: RCL-{numero_pedido[1:]}-2026. 
      Reclamação: {descricao_reclamacao}. 
      
      ---

      Nossa equipe entrará em contato em até 24h."""


## CRIANDO NOSSO AGENTE COM MEMÓRIA

db = SqliteDb(db_file="exemplos/ex003.db")

instrucoes = """Você é um agente de suporte da GT Store.
Responda sempre com educação e profissionalismo.
Sempre que o cliente perguntar sobre produtos, use a tool 'listar_produtos'.
Todos os pedidos possuem um # no início. Logo, se um cliente pedir informações
sobre o pedido #1044, o id é literalmente #1044, com o #.
Sempre que o cliente perguntar sobre um pedido, use a tool 'consultar_pedido'.
Sempre que o cliente reclamar, use a tool 'registrar_reclamacao'.
"""

agent = Agent(
    model=Groq(id="openai/gpt-oss-20b"),
    instructions=instrucoes,
    tools=[consultar_pedido, listar_produtos, registrar_reclamacao],
    markdown=True,
    db=db,
    store_history_messages=True,
    add_history_to_context=True,
    session_id="ex003",
    stream=True,
)

agent.print_response("Qual o status do pedido #1052?")
agent.print_response("Qual era o produto desse pedido que eu perguntei anteriormente?")
```

### Passo a passo explicado

#### 📦 Novo import: SqliteDb

```python
from agno.db.sqlite import SqliteDb
```

Esse import traz suporte a banco de dados SQLite — um banco leve que fica salvo em um arquivo `.db` local. Usamos isso para guardar o histórico de mensagens.

#### 🗃️ Os dados fictícios da loja

```python
PEDIDOS = {
    "#1052": {"status": "enviado", "produto": "Fone Bluetooth", "dias": 3},
    "#1053": {"status": "aguardando pagamento", "produto": "Teclado AULA F75", ...},
    "#1054": {"status": "atrasado", "produto": "Playstation 5", "dias": 12},
}

PRODUTOS = [
    "Fone Bluetooth - R$80,00",
    ...
]
```

Em um projeto real, esses dados viriam de um banco de dados ou API. Aqui usamos dicionários e listas simples para simular.

#### 🔧 Criando nossas próprias Tools

Esta é a parte mais importante do exemplo! No Agno, **qualquer função Python pode virar uma tool**. Basta passá-la na lista `tools=[]`.

**Tool 1: `consultar_pedido`**

```python
def consultar_pedido(id_pedido: str):
    """Consulta o status de um pedido pelo seu id"""
    pedido = PEDIDOS.get(id_pedido)
    if pedido and pedido["status"] != "aguardando pagamento":
        return f"Pedido {id_pedido}: {pedido['produto']} - {pedido['status']} - {pedido['dias']} para entrega"
    elif pedido:
        return f"Pedido {id_pedido}: {pedido['produto']} - {pedido['status']} - aguardando pagamento"
    return f"Pedido {id_pedido}: não encontrado"
```

> ⚠️ **Atenção ao type hint!** O parâmetro `id_pedido: str` tem o tipo declarado. Isso **não é opcional** no Agno — o framework lê essas anotações para entender o que a função espera receber. Sempre declare os tipos dos parâmetros das suas tools!

> ⚠️ **A docstring também importa!** O texto `"""Consulta o status de um pedido pelo seu id"""` é lido pelo agente para entender *para que serve* essa função. Escreva docstrings claras!

**Tool 2: `listar_produtos`**

```python
def listar_produtos():
    "Lista os produtos disponíveis na loja"
    return "\n".join(PRODUTOS)
```

Sem parâmetros. O agente pode chamá-la a qualquer momento em que o cliente perguntar sobre produtos.

**Tool 3: `registrar_reclamacao`**

```python
def registrar_reclamacao(numero_pedido, descricao_reclamacao):
    return f"""Reclamação registrada para o pedido {numero_pedido}.
      Protocolo: RCL-{numero_pedido[1:]}-2026. 
      Reclamação: {descricao_reclamacao}. 
      Nossa equipe entrará em contato em até 24h."""
```

Esta função recebe dois parâmetros que o agente vai **preencher sozinho** com base na conversa. Ou seja, o agente lê o histórico e decide qual é o número do pedido e qual é a reclamação — sem você precisar extrair essas informações manualmente.

#### 🧠 Adicionando memória com SQLite

```python
db = SqliteDb(db_file="exemplos/ex003.db")
```

Cria (ou abre) um banco SQLite no arquivo `exemplos/ex003.db`. É aqui que o histórico de mensagens será guardado.

#### 🤖 Criando o agente com memória

```python
agent = Agent(
    model=Groq(id="openai/gpt-oss-20b"),
    instructions=instrucoes,
    tools=[consultar_pedido, listar_produtos, registrar_reclamacao],
    markdown=True,
    db=db,                          # ← banco de dados
    store_history_messages=True,    # ← salva cada mensagem no banco
    add_history_to_context=True,    # ← envia o histórico junto com cada nova pergunta
    session_id="ex003",             # ← identificador da sessão (como um "nome de sala")
    stream=True,
)
```

| Parâmetro | O que faz |
|---|---|
| `db` | Conecta o agente ao banco SQLite |
| `store_history_messages` | Grava cada mensagem (pergunta + resposta) no banco |
| `add_history_to_context` | Passa o histórico salvo para o LLM a cada nova mensagem |
| `session_id` | Identifica a sessão. O mesmo ID busca o histórico anterior |

#### 💬 Testando a memória

```python
agent.print_response("Qual o status do pedido #1052?")
agent.print_response("Qual era o produto desse pedido que eu perguntei anteriormente?")
```

A segunda pergunta não menciona o pedido pelo número — ela diz "desse pedido que eu perguntei". O agente consegue responder porque **lembra** da primeira mensagem graças à memória.

### Como o agente decide qual tool usar?

```
Usuário: "Qual o status do pedido #1052?"
         │
         ▼
   LLM lê as tools disponíveis e suas docstrings:
   - consultar_pedido: "Consulta o status de um pedido pelo seu id"  ← Esta!
   - listar_produtos: "Lista os produtos disponíveis na loja"
   - registrar_reclamacao: (sem docstring genérica)
         │
         ▼
   LLM chama: consultar_pedido(id_pedido="#1052")
         │
         ▼
   Função retorna: "Pedido #1052: Fone Bluetooth - enviado - 3 para entrega"
         │
         ▼
   LLM usa esse resultado para formular a resposta final ao cliente
```

### ✅ Experimente mudar

- Adicione um novo pedido em `PEDIDOS` e pergunte sobre ele
- Crie uma nova tool (ex: `cancelar_pedido`) e veja o agente usá-la
- Mude o `session_id` para um novo valor e perceba que a memória reinicia
- Delete o arquivo `ex003.db` e rode novamente — ele volta a ser criado do zero

---

---

## 📎 EX003 (Variação) — ex003-ingles.py

**Arquivo:** `exemplos/ex003-ingles.py`  
**Conceito:** Mesmo agente do ex003, mas com **instruções em inglês** e **sem memória**

### Por que esse arquivo existe?

Serves como uma variação para demonstrar dois pontos importantes:

1. **Idioma das instruções:** As instructions foram escritas em inglês. Isso serve para comparar se o agente se comporta diferente (em geral, modelos são treinados predominantemente em inglês e tendem a seguir melhor instrucões nesse idioma).

2. **Sem memória:** Este agente **não tem** `db`, `store_history_messages` ou `add_history_to_context`. Por isso, ao final ele faz a pergunta:

```python
agent.print_response("Qual era o produto desse pedido que eu perguntei?")
```

E o agente **não consegue responder** corretamente — porque não tem nenhum histórico da conversa anterior. Isso ilustra a importância da memória.

### Comparativo rápido

| Característica | ex003.py | ex003-ingles.py |
|---|---|---|
| Idioma das instruções | Português | Inglês |
| Memória persistente | ✅ Sim (SQLite) | ❌ Não |
| Número de perguntas | 2 | 6 |
| Arquivo de banco | `ex003.db` | Nenhum |

### As 6 perguntas do ex003-ingles

```python
agent.print_response("Quais produtos vocês têm?")         # Usa listar_produtos
agent.print_response("Qual o status do pedido #1052?")    # Usa consultar_pedido
agent.print_response("Qual o status do pedido #1058?")    # Pedido inexistente!
agent.print_response("Esse pedido está muito atrasado, quero reclamar!")  # Usa registrar_reclamacao
agent.print_response("Qual o status do pedido #1052?")    # Repete a pergunta
agent.print_response("Qual era o produto desse pedido que eu perguntei?") # Sem memória → falha
```

> 💡 **Use esse arquivo para mostrar em aula o contraste:** Rode o `ex003.py` (com memória) e depois o `ex003-ingles.py` (sem memória). Os alunos vão ver claramente a diferença!

---

---

## 🗺️ Resumo da Evolução dos Exemplos

```
ex001                           ex002                             ex003
─────────────                  ──────────────────                ────────────────────────────
Agente simples                 Agente com tool pronta            Agente completo
  + system prompt                + DuckDuckGoTools                 + tools próprias
                                 + pesquisa na internet            + memória SQLite
                                                                   + histórico persistente
```

---

## 🧠 Conceitos-Chave para Lembrar

| Conceito | O que é | Onde aparece |
|---|---|---|
| `Agent` | A classe principal do Agno | Todos os exemplos |
| `instructions` | O system prompt do agente | Todos os exemplos |
| `tools` | Lista de ferramentas que o agente pode usar | ex002, ex003 |
| `stream=True` | Exibe a resposta em tempo real | ex001, ex002, ex003 |
| `DuckDuckGoTools` | Tool pronta para busca na web | ex002 |
| Funções como tools | Funções Python viram ferramentas do agente | ex003 |
| Docstrings nas tools | Texto que explica ao agente para que serve a função | ex003 |
| Type hints nas tools | Tipos dos parâmetros que o agente precisa preencher | ex003 |
| `SqliteDb` | Banco de dados para guardar o histórico | ex003 |
| `session_id` | Identificador da sessão de memória | ex003 |

---

## ❓ Dúvidas Frequentes

**P: Qual a diferença entre Agno e LangChain?**  
R: Ambos servem para criar agentes, mas o Agno é mais simples e direto. No LangChain, você monta manualmente o `AgentExecutor`, define `Tool` com `name` e `description`, etc. No Agno, basta passar funções Python no parâmetro `tools=[]` — ele lê os type hints e docstrings automaticamente.

**P: O agente sempre usa as tools?**  
R: Não. O LLM decide quando e se usar uma tool com base na pergunta. Por isso as `instructions` são importantes — você pode instruir o agente a *sempre* usar uma tool específica em determinada situação.

**P: Posso conectar o agente a um banco de dados real?**  
R: Sim! Basta criar uma função que consulta o seu banco (PostgreSQL, MySQL, etc.) e passá-la como tool. No ex003 usamos dicionários por simplicidade.

**P: O que acontece se o agente chamar uma tool errada?**  
R: O LLM recebe o resultado da tool e, se não fizer sentido, pode tentar outra abordagem ou pedir clarificação. É por isso que boas `instructions` e boas `docstrings` são fundamentais.

---

## 📦 Dependências Resumidas

```toml
[project]
requires-python = ">=3.12"
dependencies = [
    "agno>=2.5.12",       # Framework de agentes
    "ddgs>=9.12.0",       # DuckDuckGo Search (ex002)
    "groq>=1.1.2",        # Cliente da API Groq
    "python-dotenv>=1.2.2", # Leitura do .env
    "sqlalchemy>=2.0.48", # ORM para o SQLite (ex003)
]
```

---

*Bons estudos e boa aula! 🚀*
