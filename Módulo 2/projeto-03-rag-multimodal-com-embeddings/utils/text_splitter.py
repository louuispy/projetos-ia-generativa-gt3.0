from langchain_text_splitters import CharacterTextSplitter

def cria_chunks_de_texto(documento):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1500,
        chunk_overlap=300,
        length_function=len
    )

    chunks = text_splitter.split_text(documento)

    return chunks
