import heapq
import sys

MAX_INT = 9223372036854775807


#  1 2 3 4 
#1 0 
#2 1 0
#3 3
#4 4

class node(object):

	def __init__(self, node):
		self.node = node
		self.key = MAX_INT
		self.parent = None

	def get_key(self): return self.key


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
		Q.append(node(i))
	Q[r].key = 0
	while Q:
		u = min(Q, key=lambda k: k.key)
		for v in G.get_adj(u.node):
			for i in Q:
				if v == i.node and i.key > G.get_weight(u.node, v):
					i.parent = u.node
					i.key = G.get_weight(u.node, v)
		mst.append(u)
		Q.remove(u)
	return mst


root = 1

				# 0  1  2  3
graph = matrix(	[[0,-1,2,3],
			   	[ -1,0,2,1],
				[  2,2,0,5],
				[  3,1,5,0]])
mst = MST_PRIM(graph, root)
for node in mst:
	print(node.node, node.parent)