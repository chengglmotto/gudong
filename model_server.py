#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Author  ：chenggl
@Date    ：2024/8/4 09:36
@DESC     ：Qwen2-0.5b的web服务端
'''
from model import Qwen
from flask import Flask,request,session
import logging
import socket
from argparse import ArgumentParser

# prompt = "You are a cv research, get the background knowledge:\n\n1.{0}\n2.{1}\n3.{2}\n\n Please answer follow question use the backward knowledge mentioned above,the question is:\n{3}"
# query = "What tricks are used when trainning pp-yole?"
app = Flask(__name__)

# url = "http://"+str(ip)+":8091/chat"
# headers = {'Content-Type': 'application/json'}

@app.route('/chat',methods=['POST'])
def chat():
    data = request.json.get("message")
    app.logger.info("request",data)
    response = qwen.chat(data)
    app.logger.info("response",response)
    return response

if __name__ == '__main__':
    parser = ArgumentParser("model_server")
    parser.add_argument("--port",type=int,default=8091)
    args = parser.parse_args()


    qwen = Qwen(model_name_path='/RAG/llmmodel/qwen2-0.5b-instruct')
    ip = socket.gethostbyname(socket.getfqdn(socket.gethostname()))
    print(ip)
    app.run(host=ip,port=args.port,debug=True)