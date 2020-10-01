import heapq as h
import sys
import numpy as np
import random

MAX_INT = 9223372036854775807


#  1 2 3 4 
# 1 0
# 2 1 0
# 3 3
# 4 4

class node(object):

    def __init__(self, node, key):
        self.node = node
        self.key = key
        self.parent = None

    def __str__(self):
        return ("name: {} key: {}".format(self.node, self.key))

    def get_key(self):
        return self.key

    def __lt__(self, other):
        return self.key < other.key


class matrix(object):

    def __init__(self, matrix: list):
        self.adj = matrix

    def get_weight(self, u, v):
        return self.adj[u][v]

    def get_adj(self, u):
        nodes = []
        for index, weight in enumerate(self.adj[u]):
            if weight > 0:
                nodes.append(index)
        return nodes

    def __str__(self):
        full = ""
        for i in range(len(self.adj)):
            full += str(self.adj[i]) + "\n"
        return full


def MST_PRIM(G: matrix, r: int):
    mst = []
    Q = []
    for i in range(len(G.adj)):
        if i == r:
            h.heappush(Q, node(i, 0))
        else:
            h.heappush(Q, node(i, MAX_INT))
    while Q:
        u = h.heappop(Q)
        test = "current pick: {}"
        print(test.format(u))
        for i in Q:
            print(i)
        print("___________________________________")
        for v in G.get_adj(u.node):
            for i in Q:
                if v == i.node and i.key > G.get_weight(u.node, v):
                    i.parent = u.node
                    i.key = G.get_weight(u.node, v)
        mst.append(u)
        h.heapify(Q)
    return mst


def random_graph(vertices: int, edges: int, min_w: int, max_w: int) -> matrix:
    if (edges >= vertices * vertices) or (edges < (vertices - 1)) or (min_w <= 0) or (max_w <= min_w):
        return [[0, 0]]

    gr = np.array(np.zeros(vertices ** 2)).reshape(vertices, vertices)
    gr.fill(-1)
    placed = []
    for i in range(vertices):  # This is superfluous since everything is 0 anyway
        gr[i, i] = 0
    for a in range(edges):
        i = np.random.randint(0, vertices)
        j = np.random.randint(0, vertices)
        if (i != j) or ((i, j) in placed):
            weight = np.random.randint(min_w, max_w + 1)
            gr[i, j] = weight
            gr[j, i] = weight
            placed.append((i, j))
            placed.append((j, i))
        edges -= 1

    for i in range(vertices):
        if sum(gr[i]) <= vertices - 1 * -1:
            edges -= 1
            randpos = i
            while randpos == i:
                randpos = np.random.randint(0, vertices)
            gr[i, randpos] = np.random.randint(min_w, max_w + 1)

    while edges < 0:
        i = np.random.randint(0, vertices)
        if (sum(gr[i]) >= max_w) and edges < 0:  # pretty much means that it has more than 1 connection
            edges += 1
            while randpos == i:
                randpos = np.random.randint(0, vertices)
            gr[i, randpos] = -1

    return matrix(gr)


def load_graph(filename: str):
    n_nodes = 0
    edges = []
    file = open(filename, 'r')
    line = file.readline()
    while line:
        tag = line.split()[0]
        if tag == "node":
            n_nodes += 1
        if tag == "edge":
            edge_data = file.readline()
            while edge_data.split()[0] != "]":
                edge_tag = edge_data.split()[0]
                if edge_tag == "source":
                    i = int(edge_data.split()[1])-1
                if edge_tag == "target":
                    j = int(edge_data.split()[1])-1
                edge_data = file.readline()
            edges.append([i, j])
        line = file.readline()
    gr = np.array(np.zeros(n_nodes ** 2)).reshape(n_nodes, n_nodes)
    for e in edges:
        i, j = e
        gr[i, j] = 1
        gr[j, i] = 1
    return matrix(gr)


if __name__ == "__main__":
    root = 1

    # 0  1  2  3
    graph = matrix([[0, -1, 2, 3],
                    [-1, 0, 2, 1],
                    [2, 2, 0, 5],
                    [3, 1, 5, 0]])

    graph = random_graph(5, 10, 1, 15)
    print(graph)

    graph = load_graph("graph.txt")
    print(graph.adj)

    mst = MST_PRIM(graph, root)
    for node in mst:
        print(node.node, node.parent)
