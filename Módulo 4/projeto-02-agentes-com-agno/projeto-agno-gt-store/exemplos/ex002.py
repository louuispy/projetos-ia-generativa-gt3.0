# EX002 - Adicionando tools de pesquisa ao nosso agente

from agno.agent import Agent
from agno.models.groq import Groq 
from agno.tools.duckduckgo import DuckDuckGoTools
from dotenv import load_dotenv 

load_dotenv()

instrucoes = """
        Você é um pesquisador especializado e profissional, que responde todas
        as nossas perguntas com respostas completas e precisas, sem viéses ou erros.

        Para responder às pergunas:
        1. Use no máx. 3 sites diferentes para pesquisar informações;
        2. Acesse os sites e leia todo o conteúdo, sem deixar passar nada;
        3. Busque sempre fontes confiáveis e atualizadas;
        4. Sintetize as informações de forma clara e objetiva;
        5. Cite as fontes utilizadas no final da resposta;
        6. Se notar que nas fontes há algum viés, informe na resposta. O objetivo são obter respostas neutras, imparciais e precisas.

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
