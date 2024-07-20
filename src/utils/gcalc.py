from typing import List, Dict

from utils.constants import *
from utils.logger import get_log


class DSU:
    """The DSU class."""

    def __init__(self, n: int):
        """Create a DSU
        Args:
            n (int): The number of students.
        """
        log = get_log()
        log.debug(f"Creating DSU with n: {n}")
        self.parent = list(range(n))
        self.size = [1] * n

    def find(self, x: int) -> int:
        """Find the parent of the student x.
        Args:
            x (int): The student you want to find the parent of.
        Returns:
            int: The parent of the student x.
        """
        log = get_log()
        log.debug(f"Finding parent of {x}")
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        log.debug(f"Parent of {x} is {self.parent[x]}")
        return self.parent[x]

    def union(self, x: int, y: int):
        """Union the parent of the student x and the parent of the student y.
        Args:
            x (int): The student you want to union with.
            y (int): The student you want to union with.
        """
        log = get_log()
        log.debug(f"Unioning {x} and {y}")
        x = self.find(x)
        y = self.find(y)
        if x != y:
            if self.size[x] < self.size[y]:
                x, y = y, x
            self.parent[y] = x
            self.size[x] += self.size[y]
        log.debug(f"Union of {x} and {y} completed")


class DirectedGraph:
    """The DirectedGraph class."""

    def __init__(self, n: int):
        """Initialize the graph

        Args:
            n (int): The number of students
        """
        self.graph: Dict[int, List[int]] = {}
        self.weight: List[List[int]] = []
        self.dep: List[int] = []
        self.out_angle: List[int] = []
        self.in_angle: List[int] = []
        for i in range(n):
            self.dep.append(0)
            self.out_angle.append(0)
            self.in_angle.append(0)
            self.weight.append([])
            for _ in range(n):
                self.weight[i].append(0)

    def add_edge(self, x: int, y: int, w: int):
        """
        Adds a directional edge from x to y in the graph.
        Args:
            x (int): The index of the first node.
            y (int): The index of the second node.
            w (int): The weight of the edge.
        """
        log = get_log()
        log.debug(f"Adding directional edge {x} and {y}, weight {w}")
        if x not in self.graph:
            self.graph[x] = []
        self.graph[x].append(y)
        self.weight[x][y] += w
        self.out_angle[x] += 1
        self.in_angle[y] += 1

    def bfs(self, s: int, t: int) -> bool:
        """Do BFS to divide the graph by depth
        Args:
            s (int): the starting point
            t (int): the ending point
        Returns:
            bool: if there is a path
        """
        log = get_log()
        log.info("Start BFS...")
        log.debug(f"s: {s}, t: {t}")
        log.debug(f"weight: {self.weight}")
        self.dep = [0] * len(self.graph)
        self.dep[s] = 1
        queue = [s]
        while queue:
            x = queue.pop(0)
            log.debug(f"BFS: {x}")
            for y in self.graph[x]:
                if self.dep[y] == 0 and self.weight[x][y] != 0:
                    self.dep[y] = self.dep[x] + 1
                    queue.append(y)
                    if y == t:
                        log.debug(f"Found t: {t}")
                        return True
        log.warning(f"No path from {s} to {t}")
        return False

    def dfs(self, u: int, t: int, flow: int, cur: List[int]) -> int:
        """Get and sum up all the routes from u to t
        Args:
            u (int): the current point in dfs
            t (int): the destination
            flow (int): the max flow of this edge
            cur (List[int]): the first node of u
        Returns:
            int: the max flow
        """
        log = get_log()
        log.info("Start DFS...")
        log.debug(f"u: {u}, flow: {flow}, cur: {cur}, dep: {self.dep}")
        if cur[u] == -1:
            return 0
        if u == t:
            return flow
        tmp = flow
        for i in range(cur[u], len(self.graph[u])):
            if tmp <= 0:
                break
            cur[u] = i
            v = self.graph[u][i]
            if self.dep[v] == self.dep[u] + 1 and self.weight[u][v] > 0:
                log.debug(f"DFS: {u} -> {v}")
                res = self.dfs(v, t, min(flow, self.weight[u][v]), cur)
                if res == 0:  # no more flow to v
                    self.dep[v] = 0
                self.weight[u][v] -= res
                self.weight[v][u] += res
                tmp -= res  # update
        log.info("DFS completed")
        log.debug(f"Current flow {flow - tmp}")
        return flow - tmp

    def dinic(self, s: int, t: int) -> int:
        """Find the maxium flow(minimum cut) from s to t
        Args:
            s (int): the starting point
            t (int): the ending point
        Returns:
            int: the max flow
        """
        log = get_log()
        log.info("Start Dinic...")
        log.debug(f"s: {s}, t: {t}")
        ans = 0
        while self.bfs(s, t):  # Split
            cur = [
                0 if len(self.graph[i]) != 0 else -1
                for i in range(len(self.graph))
            ]
            tmp = 1
            while tmp:
                tmp = self.dfs(s, t, 1 << 30, cur)  # sum
                ans += tmp
                log.debug(f"Current ans: {ans}")
        log.info("Dinic completed")
        log.debug(f"Final ans: {ans}")
        return ans
