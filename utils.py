#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Author  ：chenggl
@Date    ：2024/8/4 15:22 
@DESC     ：工具类,搜索PDF中的标题
'''

import fitz


def extract_titles_from_pdf(pdf_path, thres=1.1):
    doc = fitz.open(pdf_path)
    titles = []

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        blocks = page.get_text("dict")["blocks"]

        # 获取当前页的页码
        page_number = page_num + 1

        # 寻找每一页可能的标题
        page_titles = []
        count = 0
        for block in blocks:
            # 获取文本块的字体大小
            print(count)
            count+=1
            if "lines" not in block:
                continue
            sizes = [span["size"] for line in block["lines"] for span in line["spans"]]
            avg_size = sum(sizes) / max(len(sizes), 1)

            # 判断是否可能是标题
            if avg_size > thres:
                text = " ".join([span["text"] for line in block["lines"] for span in line["spans"]])
                # 排除正文、表格、图片和公式，只保留可能的标题
                if not is_body_text(text) and not is_table(text) and not is_image(text) and not is_formula(text) and possible_title(text):
                    # 将标题、页码添加到结果中
                    page_titles.append((text.strip(), page_number))

        # 将该页的标题添加到结果列表中
        titles += page_titles

    return titles


def is_body_text(text):
    # 根据文本的长度和内容等特征，判断是否为正文
    # 这里可以根据具体的PDF文件的特点来定义规则
    # 以下只是一个示例，可能需要根据实际情况进行调整
    return len(text) > 100 or text.endswith(".") or text.endswith("?") or text.endswith("!")

import re
pattern = "^\d{1}\."
def possible_title(text):
    if re.match(pattern,text) is not None:
        return True

def is_table(text):
    # 根据文本的结构和内容特征，判断是否为表格
    # 这里可以根据表格的特点来定义规则
    # 以下只是一个示例，可能需要根据实际情况进行调整
    return "  " in text or "\t" in text or " | " in text


def is_image(text):
    # 根据文本的特征，判断是否为图像
    # 这里可以根据图像的特点来定义规则
    # 以下只是一个示例，可能需要根据实际情况进行调整
    return text.startswith("Image:") or text.startswith("Figure:")


def is_formula(text):
    # 根据文本的特征，判断是否为公式
    # 这里可以根据公式的特点来定义规则
    # 以下只是一个示例，可能需要根据实际情况进行调整
    return text.startswith("Formula:") or text.startswith("Equation:")

