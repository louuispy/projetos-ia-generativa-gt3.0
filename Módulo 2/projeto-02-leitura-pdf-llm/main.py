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

