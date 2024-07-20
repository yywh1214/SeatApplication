from collections import deque


def dinic_max_weight_matching(graph, source, sink):
    # 初始化容量限制的增广路径
    augmenting_path = []

    # 初始化匹配的权重
    max_weight_matching = 0

    # 添加一个到汇点的边到每个顶点
    for vertex in graph:
        if vertex not in graph[sink]:
            graph[vertex][sink] = 0
        if sink not in graph[vertex]:
            graph[sink][vertex] = float("inf")

    while True:
        # 使用BFS找到一条增广路径
        bfs_queue = deque([source])
        parent = {source: None}
        while bfs_queue:
            u = bfs_queue.popleft()
            for v, capacity in graph[u].items():
                if capacity > 0 and v not in parent:
                    parent[v] = u
                    if v == sink:
                        break
                    bfs_queue.append(v)
            if v == sink:
                break
        if v != sink:
            break

        # 找到增广路径上的最小容量
        min_capacity = float("inf")
        u = sink
        while u != source:
            v = parent[u]
            min_capacity = min(min_capacity, graph[v][u])
            u = v

        # 增加匹配的权重
        max_weight_matching += min_capacity

        # 更新图中的容量
        u = sink
        while u != source:
            v = parent[u]
            graph[v][u] -= min_capacity
            graph[u][v] += min_capacity
            u = v

    return max_weight_matching


# 示例无向图
graph = {
    "A": {"B": 1, "C": 2, "D": 3},
    "B": {"A": 0, "C": 4, "D": 5},
    "C": {"A": 0, "B": 0, "D": 6},
    "D": {"A": 0, "B": 0, "C": 0},
}

# 计算最大权匹配
source = "A"
sink = "D"
max_weight_matching = dinic_max_weight_matching(graph, source, sink)
print(max_weight_matching)
