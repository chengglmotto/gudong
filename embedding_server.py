#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Author  ：chenggl
@Date    ：2024/8/4 13:36 
@DESC     ：embedding的服务端
'''
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter
from vector import myVector
from FlagEmbedding import FlagReranker
import os
import utils
import torch

work_dir = 'documents'
# title_dict = ["Introduction","Related Work Method Architecture","Selection of Tricks","Experiment Implementation Details ","Ablation Study","Comparison with Other State-of-the-Art De- tectors","Conclusions"]

class Embedding_Server():

    def __init__(self,file_paths: str,reranker_model_path :str):
        self.vs = self.save_embedding(file_paths[0])
        self.file_path = os.path.join(work_dir,file_paths[0])
        print("file_path",self.file_path)
        self.reranker = FlagReranker(reranker_model_path,use_fp16=True)

    def query(self,query_text: str, top_k: int = 100, score_threshold: float = 1.5):

        results = self.vs.retriver(query_text,top_k=top_k)
        pairs = [(query_text, doc) for doc in results]
        scores = self.reranker.compute_score(pairs)
        print("reranker")
        print(scores)
        return [results[idx] for idx in  torch.topk(torch.tensor(scores),3).indices.data]
        #return [results[i] for i, score in enumerate(scores) if score > 0]

    def save_embedding(self,file_name):
        docs = self.load_pdf_file(file_name)
        chunks = self.split_text(docs)
        return myVector(chunks)
    def load_pdf_file(self,file_name):
        loader = PyPDFLoader(os.path.join(work_dir, file_name))
        docs = loader.load()
        for doc in docs:
            doc.page_content = doc.page_content.replace('\n',' ')
        return docs

    def split_text(self,docs,chunk_size=500,chunk_over_lap=20):
        titles_dict = self.gain_titles()
        text_spliter = CharacterTextSplitter(separator='.', chunk_size=chunk_size, chunk_overlap=chunk_over_lap)
        chunks = []
        for doc in docs:
            spliter_texts = text_spliter.split_text(doc.page_content)
            page_num = doc.metadata["page"]
            if page_num < len(titles_dict):
                title,_ = titles_dict[page_num]
                print(spliter_texts[0])
                print(type(spliter_texts[0]))
                chunks.extend([split_text+" the title of it is:"+title for split_text in spliter_texts])
                chunks.extend([split_text+" the title of it is:"+title for split_text in  self.combine(spliter_texts)])
            else:
                chunks.extend(spliter_texts)
                chunks.extend(self.combine(spliter_texts,chunk_over_lap))
        print('len_chunks',len(chunks))
        return chunks

    def combine(self,texts,chunk_over_lap=10):
        '''
        构建chunk与其上下文的合并
        :param texts:
        :return:
        '''
        combined_texts = []
        for i in range(len(texts)):
            if i < len(texts)-1:
                combined_text = texts[i][:-chunk_over_lap]+texts[i+1]
                combined_texts.append(combined_text)
        return combined_texts

    def gain_titles(self):

        # 调用函数提取标题内容
        titles_with_page_numbers = utils.extract_titles_from_pdf(os.path.join(work_dir,'2007.12099v3.pdf'))

        return [title for title in titles_with_page_numbers]


# app = app = Flask(__name__)
#
# @app.route('/upload_file',methods=['POST'])
# async def query():
#     data = await request.json.get("content")
#     embedding_pipe = embedding_pipe('')
#     app.logger.info("response",response)
#     return response

# if __name__ == '__main__':
#     ip = socket.gethostbyname(socket.getfqdn(socket.gethostname()))
#     print(ip)
#     app.run(host=ip,port='8091')

