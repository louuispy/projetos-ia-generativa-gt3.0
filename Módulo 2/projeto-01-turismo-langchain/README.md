# Projeto de chatbot com prompts especializados em LangChain

**TUTORIAL DO PROJETO EM VÍDEO:**

[[PROJETO 02] - TurismoAI - aplicação de IA com detecção de intenções](https://youtu.be/chim7X07TBM?si=yOsQ3W0KeHbpFDWu)

---

Este projeto constrói **do zero** um pipeline de Inteligência Artificial capaz de:

1. Receber um texto do usuário via terminal (CLI)
2. **Entender a intenção** da pergunta usando um LLM
3. Direcionar o texto para um **processamento específico**, de acordo com a intenção
4. Retornar uma resposta **organizada, contextual e útil**

> **Importante**: Este projeto não usa RAG, embeddings, vetores, FAISS, Chroma ou LangGraph. O foco é pensamento em pipeline + engenharia de prompts + orquestração com LangChain.
> 

---

## Objetivo

Este projeto foi pensado para **ensinar conceitos fundamentais de IA aplicada**, especialmente para quem está começando com LangChain.

Ao final, o aluno entenderá:

- O que é um **pipeline de IA**
- Como um LLM pode ser usado para **classificação de intenção**
- Como **encadear prompts** de forma lógica
- Como transformar uma única pergunta em **múltiplos comportamentos inteligentes**
- Como estruturar um projeto de IA **sem complexidade desnecessária**

---

## Visão geral do pipeline

O pipeline segue exatamente esta lógica:

```
Usuário → Classificação de intenção → Prompt especializado → Resposta final
```

Em termos práticos:

1. O usuário digita uma pergunta
2. Um LLM classifica a intenção (ex: clima, culinária, cultura…)
3. O código decide **qual prompt usar**
4. Um novo LLM gera a resposta final

Esse padrão é extremamente comum em **produtos reais de IA**.

---

## Tecnologias usadas

- Python
- LangChain
- Google Gemini (GenAI)
- Terminal (CLI)
- dotenv (para variáveis de ambiente)

---

## Estrutura do projeto

```
projeto/
│
├── main.py          # Código do projeto
├── .env             # Chave da API
└── README.md        # Esse passo a passo
```

---

## Configuração do ambiente

### 1 - Criar ambiente virtual (opcional, mas recomendado)

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows
```

### 2- Instalar dependências

```bash
pip install langchain 
pip install langchain-google-genai 
pip install python-dotenv 
pip install rich
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
from langchain_core.messages import HumanMessage, SystemMessage
from dotenv import load_dotenv
import os
import rich
```

### O que está acontecendo aqui?

- `init_chat_model`: inicializa um modelo de chat do LangChain
- `SystemMessage`: define o **comportamento do modelo**
- `HumanMessage`: representa a mensagem do usuário
- `dotenv`: carrega variáveis sensíveis
- `rich`: imprime respostas bonitas no terminal

---

## Carregando a chave da API

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

## Função para criar linhas no terminal

```python
def cria_linha(tamanho):
    print("=" * tamanho)
```

Função puramente estética.

Basicamente ela vai imprimir isso aqui no terminal:

```bash
===============================================
```

Vai servir pra deixar o nosso código mais organizado e melhor de entender, quando ele for executado.

---

## Inicializando o modelo de IA

```python
llm = init_chat_model(
    "gemini-2.5-flash", model_provider="google_genai", temperature=0.1, api_key=GEMINI_API_KEY
)
```

### Decisões importantes aqui:

- `temperature=0.1` → respostas mais **determinísticas**
- Modelo rápido → ideal para **pipelines interativos**

> Temperaturas altas aqui quebrariam a classificação de intenção.
> 

---

## Classificação de intenção

```python
def classifica_intencao(pergunta_do_usuario):
```

Essa função **não responde o usuário**.

Ela basicamente faz uma leitura da pergunta do usuário e tenta compreender qual a intenção dele na pergunta. Ou seja, busca saber o que o usuário quer. Lendo o prompt abaixo, fica mais fácil de compreender.

---

### Prompt de sistema

```python
system_message = SystemMessage(f"""
        Você é um assistente de inteligência artificial especialista em interpretação,
        contexto e viagens.
        Leia a seguinte pergunta do usuário: {pergunta_do_usuario} e com base no que a
        pergunta pede, defina qual é a intenção dessa pergunta.

        Abaixo, segue a lista de intenções:
            - "guia de viagem",
            - "ideia de local para viajar",
            - "dicas de viagem",
            - "não é sobre viagem"
            - "culinaria",
            - "clima",
            - "cultura",
            - "idioma",

        Você deve responder APENAS e SOMENTE a intenção da pergunta do usuário, com base
        na lista de intenções acima.
        Ou seja, se a pergunta do usuário for sobre a criação de um guia de viagem, você
        deve responder:
        "guia de viagem"

        Responda APENAS a intenção do usuário em sua pergunta.
        Qualquer pergunta que seja fora do assunto de viagens ou que possua uma intenção
        diferente, você deve responder:
        "não é sobre viagem"
    """)
```

Aqui usamos o LLM como um **classificador semântico**.

Ele recebe:

- Uma lista fechada de intenções
- Uma regra clara: **responder apenas uma delas**

Isso transforma o LLM em algo próximo a um **roteador inteligente**.

---

### Envio das mensagens

```python
messages = [system_message, human_message]
llm_intencao_usuario = llm.invoke(messages)
```

O LangChain envia o contexto completo para o modelo.

---

### Retorno tratado

```python
return str(llm_intencao_usuario.text.strip().lower())
```

Padronizamos a saída para evitar erros lógicos depois.

---

### Resultado final da função de detectar emoçoes:

```python
def classifica_intencao(pergunta_do_usuario: str) -> str:

    system_message = SystemMessage(
        f"""
        Você é um assistente de inteligência artificial especialista em interpretação, contexto e viagens.
        Leia a seguinte pergunta do usuário: {pergunta_do_usuario} e com base no que a pergunta pede, defina qual é
        a intenção dessa pergunta.

        Abaixo, segue a lista de intenções:
            - "guia de viagem",
            - "ideia de local para viajar",
            - "dicas de viagem",
            - "não é sobre viagem"
            - "culinaria",
            - "clima",
            - "cultura",
            - "idioma",

        Você deve responder APENAS e SOMENTE a intenção da pergunta do usuário, com base na lista de intenções acima.
        Ou seja, se a pergunta do usuário for sobre a criação de um guia de viagem, você deve responder:
        "guia de viagem"

        Responda APENAS a intenção do usuário em sua pergunta.
        Qualquer pergunta que seja fora do assunto de viagens ou que possua uma intenção
        diferente das que citei acima, você deve responder:
        "não é sobre viagem"
    """
    )

    human_message = HumanMessage(pergunta_do_usuario)

    messages = [system_message, human_message]

    llm_intencao_usuario = llm.invoke(messages)

    return str(llm_intencao_usuario.text.strip().lower())

```

---

## Resposta baseada na intenção

```python
def responde_com_base_na_intencao(intencao, pergunta):
```

Aqui acontece a orquestração do pipeline.

Cada `elif` representa um ramo do fluxo de IA.

---

### Exemplo: Guia de viagem

```python
if "guia de viagem" in intencao:
        prompt_guia_viagem = f"""
        Intenção do usuário: {intencao}
        Você é um guia turístico experiente. Crie um roteiro detalhado dia a dia para 
        o destino pedido pelo usuário: {pergunta_do_usuario}, 
        focando em logística, horários e custos estimados.
        """

        system_message = SystemMessage(prompt_guia_viagem)
        human_message = HumanMessage(pergunta_do_usuario)
        messages = [system_message, human_message]
        resposta_guia_viagem = llm.invoke(messages)

        return resposta_guia_viagem.text
```

- Criamos um prompt altamente especializado
- Mudamos completamente o papel do LLM

O modelo é o mesmo, o comportamento muda via prompt.

---

### Padrão repetido (intencionalmente)

Todos os blocos seguem a mesma estrutura do bloco acima, para cada uma das intenções que temos na nossa lista:

1. Prompt especializado
2. `SystemMessage`
3. `HumanMessage`
4. `llm.invoke()`

---

### Código final da função de responder:

```python
def responde_com_base_na_intencao(intencao: str, pergunta_do_usuario: str) -> str:

    if "guia de viagem" in intencao:
        prompt_guia_viagem = f"""
        Intenção do usuário: {intencao}
        Você é um guia turístico experiente. Crie um roteiro detalhado dia a dia para o destino pedido pelo usuário: {pergunta_do_usuario}, 
        focando em logística, horários e custos estimados.
        """

        system_message = SystemMessage(prompt_guia_viagem)
        human_message = HumanMessage(pergunta_do_usuario)
        messages = [system_message, human_message]
        resposta_guia_viagem = llm.invoke(messages)

        return resposta_guia_viagem.text

    elif "ideia de local para viajar" in intencao:
        prompt_ideia_viagem = f"""
        Intenção do usuário: {intencao}
        Você é um consultor de viagens. Com base no perfil do usuário, na seguinte pergunta {pergunta_do_usuario}, sugira 3 destinos, 
        focando em logística, horários e custos estimados.
        """

        system_message = SystemMessage(prompt_ideia_viagem)
        human_message = HumanMessage(pergunta_do_usuario)
        messages = [system_message, human_message]
        resposta_ideia_viagem = llm.invoke(messages)

        return resposta_ideia_viagem.text

    elif "dicas de viagem" in intencao:
        prompt_dicas_viagem = f"""
        Intenção do usuário: {intencao}
        Você é um viajante 'hackers'. Forneça dicas práticas de segurança, economia e etiqueta local
        com base na seguinte pergunta do usuário: {pergunta_do_usuario}.
        """

        system_message = SystemMessage(prompt_dicas_viagem)
        human_message = HumanMessage(pergunta_do_usuario)
        messages = [system_message, human_message]
        resposta_dicas_viagem = llm.invoke(messages)

        return resposta_dicas_viagem.text

    elif "culinaria" in intencao:
        prompt_culinaria = f"""
        Intenção do usuário: {intencao}
        Você é um chef e crítico gastronômico. Descreva os pratos típicos imperdíveis do local citado
        na pergunta do usuário: {pergunta_do_usuario}.
        Mencione ingredientes e onde encontrar a comida mais autêntica.
        """

        system_message = SystemMessage(prompt_culinaria)
        human_message = HumanMessage(pergunta_do_usuario)
        messages = [system_message, human_message]
        resposta_culinaria = llm.invoke(messages)

        return resposta_culinaria.text

    elif "clima" in intencao:
        prompt_clima = f"""
        Intenção do usuário: {intencao}
        Você é um meteorologista especializado em turismo.
        Analise as variações climáticas relacionadas à seguinte pergunta do usuário: {pergunta_do_usuario}
        e recomende exatamente o que levar na mala.
        """

        system_message = SystemMessage(prompt_clima)
        human_message = HumanMessage(pergunta_do_usuario)
        messages = [system_message, human_message]
        resposta_clima = llm.invoke(messages)

        return resposta_clima.text

    elif "cultura" in intencao:
        prompt_cultura = f"""
        Intenção do usuário: {intencao}
        Você é um historiador e sociólogo.
        Explique os pilares culturais, tradições e comportamentos sociais
        relacionados à pergunta do usuário: {pergunta_do_usuario},
        ajudando a evitar gafes culturais.
        """

        system_message = SystemMessage(prompt_cultura)
        human_message = HumanMessage(pergunta_do_usuario)
        messages = [system_message, human_message]
        resposta_cultura = llm.invoke(messages)

        return resposta_cultura.text

    elif "idioma" in intencao:
        prompt_idioma = f"""
        Intenção do usuário: {intencao}
        Você é um poliglota local.
        Liste frases essenciais relacionadas ao destino mencionado na pergunta do usuário: {pergunta_do_usuario},
        com guia de pronúncia simplificado para sobrevivência no local.
        """

        system_message = SystemMessage(prompt_idioma)
        human_message = HumanMessage(pergunta_do_usuario)
        messages = [system_message, human_message]
        resposta_idioma = llm.invoke(messages)

        return resposta_idioma.text

    else:
        return "Não consegui entender a intenção da sua pergunta. Tente reformular."
```

---

## Loop principal (CLI)

```python
cria_linha(80)
print(f'{"BEM-VINDO(A) AO TURISMO-AI!":^80}')
cria_linha(80)
    
while True:
    print()
    print(f"{'USUÁRIO':=^80}")
    pergunta_usuario = str(input("Digite a sua pergunta ou pressione [Q] para sair:"))
    print()

    if pergunta_usuario in ["Q", "q"]:
        print("Saindo...")
        break
		else:
		    intencao = classifica_intencao(pergunta_usuario)
		    print()
		    print(intencao)
		    
		    print(f"{'IA':=^80}")
		    resposta = responde_com_base_na_intencao(intencao, pergunta_usuario)
		    rich.print(resposta)
```

O programa roda até o usuário sair.

O fluxo fica assim:

1. Recebe input
2. Classifica intenção
3. Gera resposta
4. Exibe no terminal

A gente vai basicamente fazer uma estrutura quase igual ao do nosso projeto “SinceroAI”

A diferença é que aqui, vamos apenas chamar as funções que criamos acima, deixando o loop mais limpo.

---

## Conceitos profissionais que colocamos em prática

Mesmo sendo um projeto um pouquinho complexo, nós construímos ele usando apenas o que aprendemos nas últimas aulas.

Usamos funções, laço de repetição, variáveis, f-strings, langchain…

Não utilizamos TypeHints, LangGraph nem nada do tipo!

Sintam-se livres para modificar o projeto, aplicar ele a outro contexto sem ser o de viagens. O único limite é a imaginação!

---

## Código final do projeto

```python
# IMPORTS
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage, SystemMessage
from dotenv import load_dotenv
import os
import rich

# CARREGANDO NOSSA CHAVE DE API
load_dotenv()

GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY")

# CRIANDO AS FUNÇÕES DO PROJETO

"""
INTENCOES_PERGUNTA_USUARIO = [
    "guia de viagem",
    "ideia de local para viajar",
    "dicas de viagem",
    "culinaria",
    "clima",
    "cultura",
    "idioma",
]
"""

# FUNÇÃO DE CRIAR LINHAS
def cria_linha(tamanho):
    print("=" * tamanho)

# INICIANDO NOSSO CHAT MODEL
llm = init_chat_model(
    "gemini-2.5-flash", model_provider="google_genai", temperature=0.1
)

# FUNÇÃO PARA CLASSIFICAR A INTENÇÃO DO USUÁRIO
def classifica_intencao(pergunta_do_usuario):

    system_message = SystemMessage(
        f"""
        Você é um assistente de inteligência artificial especialista em interpretação, contexto e viagens.
        Leia a seguinte pergunta do usuário: {pergunta_do_usuario} e com base no que a pergunta pede, defina qual é
        a intenção dessa pergunta.

        Abaixo, segue a lista de intenções:
            - "guia de viagem",
            - "ideia de local para viajar",
            - "dicas de viagem",
            - "culinaria",
            - "clima",
            - "cultura",
            - "idioma",

        Você deve responder APENAS e SOMENTE a intenção da pergunta do usuário, com base na lista de intenções acima.
        Ou seja, se a pergunta do usuário for sobre a criação de um guia de viagem, você deve responder:
        "guia de viagem"

        Responda APENAS a intenção do usuário em sua pergunta.
        Qualquer pergunta que seja fora do assunto de viagens ou que possua uma intenção diferente, você deve responder:
        "não é sobre viagem"
    """
    )

    human_message = HumanMessage(pergunta_do_usuario)

    messages = [system_message, human_message]

    llm_intencao_usuario = llm.invoke(messages)

    return str(llm_intencao_usuario.text.strip().lower())

# FUNÇÃO PARA RESPONDER O USUÁRIO COM BASE EM SUA INTENÇÃO
def responde_com_base_na_intencao(intencao, pergunta_do_usuario):

    if "guia de viagem" in intencao:
        prompt_guia_viagem = f"""
        Intenção do usuário: {intencao}
        Você é um guia turístico experiente. Crie um roteiro detalhado dia a dia para o destino pedido pelo usuário: {pergunta_do_usuario}, 
        focando em logística, horários e custos estimados.
        """

        system_message = SystemMessage(prompt_guia_viagem)
        human_message = HumanMessage(pergunta_do_usuario)
        messages = [system_message, human_message]
        resposta_guia_viagem = llm.invoke(messages)

        return resposta_guia_viagem.text

    elif "ideia de local para viajar" in intencao:
        prompt_ideia_viagem = f"""
        Intenção do usuário: {intencao}
        Você é um consultor de viagens. Com base no perfil do usuário, na seguinte pergunta {pergunta_do_usuario}, sugira 3 destinos, 
        focando em logística, horários e custos estimados.
        """

        system_message = SystemMessage(prompt_ideia_viagem)
        human_message = HumanMessage(pergunta_do_usuario)
        messages = [system_message, human_message]
        resposta_ideia_viagem = llm.invoke(messages)

        return resposta_ideia_viagem.text

    elif "dicas de viagem" in intencao:
        prompt_dicas_viagem = f"""
        Intenção do usuário: {intencao}
        Você é um viajante 'hackers'. Forneça dicas práticas de segurança, economia e etiqueta local
        com base na seguinte pergunta do usuário: {pergunta_do_usuario}.
        """

        system_message = SystemMessage(prompt_dicas_viagem)
        human_message = HumanMessage(pergunta_do_usuario)
        messages = [system_message, human_message]
        resposta_dicas_viagem = llm.invoke(messages)

        return resposta_dicas_viagem.text

    elif "culinaria" in intencao:
        prompt_culinaria = f"""
        Intenção do usuário: {intencao}
        Você é um chef e crítico gastronômico. Descreva os pratos típicos imperdíveis do local citado
        na pergunta do usuário: {pergunta_do_usuario}.
        Mencione ingredientes e onde encontrar a comida mais autêntica.
        """

        system_message = SystemMessage(prompt_culinaria)
        human_message = HumanMessage(pergunta_do_usuario)
        messages = [system_message, human_message]
        resposta_culinaria = llm.invoke(messages)

        return resposta_culinaria.text

    elif "clima" in intencao:
        prompt_clima = f"""
        Intenção do usuário: {intencao}
        Você é um meteorologista especializado em turismo.
        Analise as variações climáticas relacionadas à seguinte pergunta do usuário: {pergunta_do_usuario}
        e recomende exatamente o que levar na mala.
        """

        system_message = SystemMessage(prompt_clima)
        human_message = HumanMessage(pergunta_do_usuario)
        messages = [system_message, human_message]
        resposta_clima = llm.invoke(messages)

        return resposta_clima.text

    elif "cultura" in intencao:
        prompt_cultura = f"""
        Intenção do usuário: {intencao}
        Você é um historiador e sociólogo.
        Explique os pilares culturais, tradições e comportamentos sociais
        relacionados à pergunta do usuário: {pergunta_do_usuario},
        ajudando a evitar gafes culturais.
        """

        system_message = SystemMessage(prompt_cultura)
        human_message = HumanMessage(pergunta_do_usuario)
        messages = [system_message, human_message]
        resposta_cultura = llm.invoke(messages)

        return resposta_cultura.text

    elif "idioma" in intencao:
        prompt_idioma = f"""
        Intenção do usuário: {intencao}
        Você é um poliglota local.
        Liste frases essenciais relacionadas ao destino mencionado na pergunta do usuário: {pergunta_do_usuario},
        com guia de pronúncia simplificado para sobrevivência no local.
        """

        system_message = SystemMessage(prompt_idioma)
        human_message = HumanMessage(pergunta_do_usuario)
        messages = [system_message, human_message]
        resposta_idioma = llm.invoke(messages)

        return resposta_idioma.text

    else:
        return "Não consegui entender a intenção da sua pergunta. Tente reformular."

# CONSTRUINDO O PROJETO
cria_linha(80)
print(f'{"BEM-VINDO(A) AO TURISMO-AI!":^80}')
cria_linha(80)
    
while True:
    print()
    print(f"{'USUÁRIO':=^80}")
    pergunta_usuario = str(input("Digite a sua pergunta ou pressione [Q] para sair:"))
    print()

    if pergunta_usuario in ["Q", "q"]:
        print("Saindo...")
        break
		else:
		    intencao = classifica_intencao(pergunta_usuario)
		    print()
		    print(intencao)
		    
		    print(f"{'IA':=^80}")
		    resposta = responde_com_base_na_intencao(intencao, pergunta_usuario)
		    rich.print(resposta)

```

---

# FIM DO PROJETO