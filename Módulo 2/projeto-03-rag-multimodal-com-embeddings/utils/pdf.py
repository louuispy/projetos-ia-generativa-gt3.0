from langchain_community.document_loaders import PyPDFLoader

def leitura_pdf(pdf):
    loader = PyPDFLoader(pdf)
    lista_documentos = loader.load()

    documento = ''
    
    for doc in lista_documentos:
        documento += doc.page_content

    return documento
