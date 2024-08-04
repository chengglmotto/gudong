from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
class myVector():

    def __init__(self,docs):
        embedding = HuggingFaceEmbeddings(model_name='BAAI/bge-small-zh-v1.5')
        self.db = FAISS.from_texts(texts=docs,embedding=embedding)

    def retriver(self,query,top_k=None):
        search_result = [doc.page_content for doc in self.db.similarity_search(query,k=top_k)]
        return search_result


