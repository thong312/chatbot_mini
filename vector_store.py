import os
from langchain_community.vectorstores import Chroma
# from langchain_community.embeddings import HuggingFaceEmbeddings

persist_dir = "./chroma_db"
from langchain_huggingface import HuggingFaceEmbeddings

embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")


def get_vector_store():
    if not os.path.exists(persist_dir):
        texts = [
            "Hello, how are you?",
            "HaNoi is the capital of Vietnam",
            "Python is famous for its simplicity",
            "LangChain helps build LLM applications",
            "ChromaDB is a vector database",
        ]
        metadatas = [{"source": "wiki1"}, {"source": "wiki2"}, {"source": "wiki3"}]
        db = Chroma.from_texts(texts, embeddings, metadatas=metadatas, persist_directory=persist_dir)
        db.persist()
    else:
        db = Chroma(persist_directory=persist_dir, embedding_function=embeddings)
    return db
