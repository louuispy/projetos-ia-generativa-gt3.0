# EX003 - Aprimorando o nosso agente com nossas próprias Tools

## IMPORTS E CARREGANDO API
from agno.agent import Agent
from agno.models.groq import Groq
from agno.db. sqlite import SqliteDb
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
        return f"Pedido {id_pedido}: {pedido['produto']} - {pedido['status']} - aguardando apgamento"
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
Sempre que o cliente perguntar sobre produtos, use a tool 'listar_produtos'. Todos os produtos possuem um # no início. Logo, se um cliente pedir informações sobre o pedido #1044, o id é literalmente #1044, com o #.
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
