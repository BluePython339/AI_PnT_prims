import heapq
import sys

MAX_INT = sys.MAX_INT

#  1 2 3 4 
#1 0 
#2 1 0
#3 3
#4 4

class node(object):

	def __init__(self, node):
		node = node
		key = MAX_INT
		parent = -1


class matrix(object):

	def __init__(self, matrix:list ):
		self.adj = matrix

	def get_weight(u,v):
		return matrix[u][v]

	def get_adj(u):
		nodes = []
		for i in self.adj[u]:
			if i > 0:
				nodes.append(i)
		return nodes

def MST_PRIM(G:matrix , r:int):
	Q = []
	for u in G.adj:
		Q.append(node(u))
	Q[r].key = 0
	while Q:
		u = min(Q, key=key)
		Q.remove(u)
		for v in G.get_adj():
			for i in Q:
				if v == i.node and i.key > G.get_weight(u.node,v):
					i.parent = u.node
					i.key = G.get_weight(u.node,v)

