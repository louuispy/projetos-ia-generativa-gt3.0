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