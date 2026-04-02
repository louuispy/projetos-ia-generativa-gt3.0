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