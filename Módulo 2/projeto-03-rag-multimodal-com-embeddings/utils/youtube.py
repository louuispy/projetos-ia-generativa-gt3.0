from langchain_community.document_loaders import YoutubeLoader

def transcricao_youtube(url):
    loader = YoutubeLoader.from_youtube_url(url, language=['pt'])
    lista_documento = loader.load()

    documento = ''

    for doc in lista_documento:
        documento += doc.page_content

    return documento
