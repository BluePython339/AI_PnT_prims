import heapq

class node(object):

	def __init__(self, neighbours:list, name:str):
		self.name = name
		self.neighbours = neighbours #[8, "A"]


	def get_neighbours(self):
		return self.neighbours #returns all neighbours


class graph(object):

	def __init__(self, nodes:list):
		queue = []
		explored = []
		nodes = self.nodes

	def prims(self):
		#get initial node
		node = self.nodes.pop()
		self.explored.append(node.name)
		for i in node.get_neighbours():
			heappush(self.queue, i)
		#add name and weight to queue
		#continue loop
		while len(explored) not len(nodes):
			node = heappop(self.queue) # we need a way to remove an item from the queue if its node has been explored
			for i in node.get_neighbours():
				heappush(self.queue, i)

			#implement some logging system to return the MST

	def show_mst():
		pass
		#make a representation of the mst

#@TODO -input graph method
# 	   -finnish implementing prims
#      -optimise
#      -create GML parser to graph
#      -create random graph creator
