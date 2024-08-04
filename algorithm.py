#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Author  ：chenggl
@Date    ：2024/8/3 17:51
@DESC    ：算法题解法
'''

import math
from collections import defaultdict


#是否在范围内
def calculate_distance(x1, y1, x2, y2):
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


#走迷宫
def dfs(node, visited, graph):
    count = 1
    visited.add(node)
    for neighbor in graph[node]:
        if neighbor not in visited:
            count += dfs(neighbor, visited, graph)
    return count


def maxBombTimes(bombs):
    n = len(bombs)
    graph = defaultdict(list)

    # 构建可达关系
    for i in range(n):
        for j in range(i + 1, n):
            x1, y1, r1 = bombs[i]
            x2, y2, r2 = bombs[j]
            if calculate_distance(x1, y1, x2, y2) <= r1 + r2:
                graph[i].append(j)
                graph[j].append(i)

                # 对每个炸弹执行DFS,求最大
    max_times = 0
    for i in range(n):
        visited = set()
        max_times = max(max_times, dfs(i, visited, graph))

    return max_times


# 示例输入
bombs = [[1,2,3],[2,3,1],[3,4,2],[4,5,3],[5,6,4]]
# 输出结果
print(maxBombTimes(bombs))  # 输出：5

