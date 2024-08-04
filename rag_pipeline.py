#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Author  ：chenggl
@Date    ：2024/8/4 13:55 
@DESC     ：
'''
import aiohttp
import asyncio
import socket
from argparse import ArgumentParser

prompt = "You are a cv researcher, the background knowledge:\n\n1.{0}\n2.{1}\n3.{2}\n\n Please answer follow question use the backward knowledge mentioned above,the question is:\n{3}"
query = "What tricks are used when trainning pp-yole?"
ip = socket.gethostbyname(socket.getfqdn(socket.gethostname()))

url = "http://"+str(ip)+":8091/chat"
headers = {'Content-Type': 'application/json'}
from embedding_server import Embedding_Server


async def llm_client(data):
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=data) as response:
            return await response.text()

async def rag_client(final_query):
    params = {"message":final_query}
    result =  await llm_client(params)
    print(result)

if __name__ == '__main__':

    parser = ArgumentParser("rag_pipeline")
    parser.add_argument("--file_path",type=str,default='2007.12099v3.pdf')

    args = parser.parse_args()

    #建库
    embedding_pipe = Embedding_Server([args.file_path],"BAAI/bge-reranker-large")
    #检索
    page_contents = embedding_pipe.query(query)
    final_query = prompt.format(page_contents[0], page_contents[1], page_contents[2], query)
    #调LLM
    print(final_query)
    asyncio.run(rag_client(final_query))
