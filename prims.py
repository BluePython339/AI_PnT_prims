import heapq as h
import sys
import numpy as np

MAX_INT = 9223372036854775807


#  1 2 3 4 
#1 0 
#2 1 0
#3 3
#4 4

class node(object):

	def __init__(self, node, key):
		self.node = node
		self.key = key
		self.parent = None

	def get_key(self): 
		return self.key

	def __lt__(self, other):
		return self.key < other.key


class matrix(object):

	def __init__(self, matrix:list ):
		self.adj = matrix

	def get_weight(self, u, v):
		return self.adj[u][v]

	def get_adj(self, u):
		nodes = []
		for index, weight in enumerate(self.adj[u]):
			if weight > 0:
				nodes.append(index)
		return nodes


def MST_PRIM(G:matrix , r:int):
	mst = []
	Q = []
	for i in range(len(G.adj)):
		if i  == r:
			h.heappush(Q,node(i, 0))
		else:
			h.heappush(Q, node(i, MAX_INT))
	while Q:
		u = h.heappop(Q)
		for v in G.get_adj(u.node):
			for i in Q:
				if v == i.node and i.key > G.get_weight(u.node, v):
					i.parent = u.node
					i.key = G.get_weight(u.node, v)
		mst.append(u)
		h.heapify(Q)
	return mst

def random_graph(vertices, edges, weight_min, weight_max):
	gr = np.array(np.zeros(vertices**2)).reshape(vertices, vertices)
	for i in range(vertices):
		for j in range(vertices):
			if i != j:
				weight = np.random.randint(weight_min, weight_max+1)
				gr[i, j] = weight
				gr[j, i] = weight
	return matrix(gr)


root = 1

				# 0  1  2  3
graph = matrix(	[[0,-1,2,3],
			   	[ -1,0,2,1],
				[  2,2,0,5],
				[  3,1,5,0]])

graph = random_graph(4, 3, 1, 10)

mst = MST_PRIM(graph, root)
for node in mst:
	print(node.node, node.parent)