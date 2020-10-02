import heapq as h
import sys
import numpy as np
import random
import argparse
import time

MAX_INT = 9223372036854775807

parser = argparse.ArgumentParser()
parser.add_argument("-r","--random",default=False, action='store_true', help='create random graph (must also have arguments -v -e --min --max) Chance at disconnected graph')
parser.add_argument("-e", "--edges",type=int, default=0, help='amount of edged in random graph (minimaly vertices-1)')
parser.add_argument("-v", "--vertices",type=int,default=0, help='amount of vertices')
parser.add_argument("--min",type=int, default=0,help="minimal edge weight")
parser.add_argument("--max",type=int, default=0,help="maximal edge weight")
parser.add_argument('--root', type=int,default = 1, help="set root node of graph")
parser.add_argument('-f', '--file',type=str, help="read graph from GML file")
parser.add_argument('-rf','--random_full', default=False, action='store_true', help="create random STRONGLY CONNECTED graph, needs -v, --min and --max")
#  1 2 3 4 
# 1 0
# 2 1 0
# 3 3
# 4 4
times = []
start_time = 0
end_time = 0

class node(object):

    def __init__(self, node, key):
        self.node = node #identifier of this node
        self.key = key #key value of this node
        self.parent = None #parent node of this node

    def __str__(self):
        return ("name: {} key: {}".format(self.node, self.key))

    def get_key(self):
        return self.key # returns current key

    def __lt__(self, other):
        return self.key < other.key #comparator for the node object


class matrix(object):

    def __init__(self, matrix: list):
        self.adj = matrix #n*n matrix that reprisents the adjacency matrix

    def get_weight(self, u, v):
        return self.adj[u][v] #returns the weight of an edge

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
    start_time = time.time()
    mst = []
    Q = []
    for i in range(len(G.adj)):
        if i == r:
            h.heappush(Q, node(i, 0))
        else:
            h.heappush(Q, node(i, MAX_INT))
    while Q:
        u = h.heappop(Q)
        #test = "current pick: {}"
        #print(test.format(u))
        #for i in Q:
        #    print(i)
        #print("___________________________________")
        for v in G.get_adj(u.node):
            for i in Q:
                if v == i.node and i.key > G.get_weight(u.node, v):
                    i.parent = u.node
                    i.key = G.get_weight(u.node, v)
        mst.append(u)
        h.heapify(Q)
    end_time = time.time()
    times.append((start_time, end_time))
    return mst

def fully_connected(vertices:int, min_w:int, max_w:int)->matrix:
    start_time = time.time()
    gr = np.array(np.zeros(vertices ** 2)).reshape(vertices, vertices) #create and fill the matrix with 0
    gr.fill(-1)
    for i in range(vertices):
        for j in range(vertices):
            if i != j:
                weight = np.random.randint(min_w, max_w + 1)
                gr[i,j] = weight
                gr[j,i] = weight
    end_time = time.time()
    times.append((start_time,end_time))
    return matrix(gr) 


def random_graph(vertices: int, edges: int, min_w: int, max_w: int) -> matrix:
    start_time = time.time()
    if (edges >= vertices * vertices) or (edges < (vertices - 1)) or (min_w <= 0) or (max_w <= min_w):
        return [[0]]

    gr = np.array(np.zeros(vertices ** 2)).reshape(vertices, vertices) #create and fill the matrix with 0
    gr.fill(-1) #fill the matrix with -1 (our representation of not connected)
    placed = []
    for i in range(vertices):  #
        gr[i, i] = 0 #set the diagonal to 0
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
        #randomly start setting edges on the locations where this is possible (no 2 spots get to go agian)

    for i in range(vertices):
        if sum(gr[i]) <= (vertices - 1)*-1:
            edges -= 1
            randpos = i
            while randpos == i:
                randpos = np.random.randint(0, vertices)
            gr[i, randpos] = np.random.randint(min_w, max_w + 1)
    for i in range(vertices):
        check = 0
        for j in range(vertices):
            check +=gr[j,i]
        if check <= (vertices - 1)*-1:
            edges -= 1 #found another disconnection

        #check for filtering out disconnected nodes, (at least most of them)
        #this does not account for disconnected graphs (since it can't find those)

    while edges < 0:
        i = np.random.randint(0, vertices)
        if (sum(gr[i]) >= max_w) and edges < 0:  # pretty much means that it has more than 1 connection
            edges += 1
            while randpos == i:
                randpos = np.random.randint(0, vertices)
            gr[i, randpos] = -1
        #here we need to remove extra edges from well connected vertices to get the required graph 
    end_time = time.time()
    times.append((start_time, end_time))
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
    args = parser.parse_args()
    if args.random and not args.file and not args.random_full:
        try:
            graph = random_graph(args.vertices,args.edges, args.min, args.max)
        except:
            print("Check arguments!")
            exit()
    elif args.file and not args.random and not args.random_full:
        graph = load_graph(args.file)
    elif args.random_full and not args.file and not args.random:
        try:
            graph = fully_connected(args.vertices, args.min, args.max)
        except:
            print("check arguments!")
            exit()
    elif not args.file and not args.random and not args.random_full:
        print("please choose one of the options --file or --random")
        exit()
    else:
        print("can't combine random and file")
        exit()

    root = args.root
    # 0  1  2  3
    #graph = matrix([[0, -1, 2, 3],
    #                [-1, 0, 2, 1],
    #                [2, 2, 0, 5],
    #                [3, 1, 5, 0]])
    #
    #graph = random_graph(50, 100, 1, 300)
    print(graph)
    #print(type(graph))

    #graph = load_graph("graph.txt")
    #print(graph.adj)
    mst = MST_PRIM(graph, root)
    for node in mst:
        print(node.node, node.parent)

    gentime = times[0][1]-times[0][0]
    msttime = times[1][1]-times[1][0]

    print("""Graph generation time: {} seconds
MST calculation time: {} seconds""".format(gentime, msttime))