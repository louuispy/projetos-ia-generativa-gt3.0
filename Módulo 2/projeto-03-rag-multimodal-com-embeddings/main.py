from utils import chatbot, embeddings, pdf, text_splitter, view_image, youtube
import rich

print("=" * 80)
print(f"{'Olá, meu nome é Connor. Seja bem-vindo(a)!':^80}")
print("=" * 80)


selecao_usuario = """
Digite o número da ação que você deseja:

[1] Conversar com PDFs
[2] Conversar com vídeos do YouTube
[3] Conversar com uma imagem
[4] Sair 

"""

historico_conversa = []

while True:
    input_selecao = str(input(selecao_usuario))

    if input_selecao == "1":
        caminho_pdf = str(input("Digite o caminho do seu PDF: "))
        documento = pdf.leitura_pdf(caminho_pdf)

        chunks_texto = text_splitter.cria_chunks_de_texto(documento)
        vectorstore = embeddings.cria_embeddings(chunks_texto)

        print()
        print("=" * 80)
        print(f"{'PERGUNTA DO USUÁRIO':=^80}")
        print("=" * 80)
        print()

        pergunta_usuario = str(input("Digite a sua pergunta: "))

        resposta = chatbot.injeta_contexto_no_llm(
            vectorstore, pergunta_usuario, historico_conversa
        )

        print()
        print("=" * 80)
        print(f"{'RESPOSTA DA IA':=^80}")
        print("=" * 80)
        print()
        rich.print(resposta)

    elif input_selecao == "2":
        url = str(input("Digite a URL do vídeo do YouTube: "))
        documento = youtube.transcricao_youtube(url)

        chunks_texto = text_splitter.cria_chunks_de_texto(documento)
        vectorstore = embeddings.cria_embeddings(chunks_texto)

        print()
        print("=" * 80)
        print(f"{'PERGUNTA DO USUÁRIO':=^80}")
        print("=" * 80)
        print()

        pergunta_usuario = str(input("Digite a sua pergunta: "))

        resposta = chatbot.injeta_contexto_no_llm(
            vectorstore, pergunta_usuario, historico_conversa
        )

        print()
        print("=" * 80)
        print(f"{'RESPOSTA DA IA':=^80}")
        print("=" * 80)
        print()
        rich.print(resposta)

    elif input_selecao == "3":
        caminho_imagem = str(input("Digite o caminho da sua imagem: "))
        descricao_imagem = view_image.passa_imagem_pro_llm(caminho_imagem)

        chunks_texto = text_splitter.cria_chunks_de_texto(descricao_imagem)
        vectorstore = embeddings.cria_embeddings(chunks_texto)

        print()
        print("=" * 80)
        print(f"{'PERGUNTA DO USUÁRIO':=^80}")
        print("=" * 80)
        print()

        pergunta_usuario = str(input("Digite a sua pergunta: "))

        resposta = chatbot.injeta_contexto_no_llm(
            vectorstore, pergunta_usuario, historico_conversa
        )

        print()
        print("=" * 80)
        print(f"{'RESPOSTA DA IA':=^80}")
        print("=" * 80)
        print()
        rich.print(resposta)

    elif input_selecao == "4":
        print("Saindo...")
        break

    else:
        print("Por favor, digite uma opção válida!")
