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
def cria_linha(tamanho: int) -> str:
    print("=" * tamanho)


# INICIANDO NOSSO CHAT MODEL
llm = init_chat_model(
    "gemini-2.5-flash", model_provider="google_genai", temperature=0.1
)


# FUNÇÃO PARA CLASSIFICAR A INTENÇÃO DO USUÁRIO
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


# CONSTRUINDO O PROJETO

cria_linha(80)
print(f'{"BEM-VINDO(A) AO TURISMO-AI!":^80}')
cria_linha(80)

while True:
    print()
    print(f"{'USUÁRIO':=^80}")
    pergunta_usuario = str(input("Digite a sua pergunta ou pressione [Q] para sair: "))
    print()

    if pergunta_usuario in ["Q", "q"]:
        print("Saindo...")
        break

    intencao = classifica_intencao(pergunta_usuario)
    print(f"Intenção da pergunta: {intencao}")
    print()
    resposta = responde_com_base_na_intencao(intencao, pergunta_usuario)

    print(f"{'IA':=^80}")
    rich.print(resposta)
    print()

