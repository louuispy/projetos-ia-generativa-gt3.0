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
    Você é um assistente de IA extremamente gentil e amigável, expert em tecnologia e responde perguntas de forma precisa e eficaz, de maneira didática, passo a passo, extremamente fácil de compreender, mas sem usar uma linguagem extremamente infantil. Seu nome é Connor.

    Suas respostas serão feitas com base no contexto: {contexto}

    """

    system_message = SystemMessage(prompt)
    human_message = HumanMessage(pergunta)

    # cria uma lista de mensagens da conversa 
    mensagens = [system_message] + historico_conversa + [human_message]

    # responde o usuário
    resposta_llm = llm.invoke(mensagens)

    # cria uma AIMessage para o histórico
    ai_message = AIMessage(resposta_llm.text)

    # atualiza o histórico da conversa
    historico_conversa.append(human_message)
    historico_conversa.append(ai_message)

    return str(resposta_llm.text)