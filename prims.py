import heapq

class node(object):

	def __init__(self, neighbours:list, name:str):
		self.name = name
		self.neighbours = neighbours #[8, "A"]


	def get_neighbours(self):
		return self.neighbours #returns all neighbours


class graph(object):

	def __init__(self, nodes:list):
		self.queue = []
		self.explored = []
		self.nodes = nodes

	def prims(self):
		#get initial node
		node = self.nodes.pop()
		self.explored.append(node.name)
		for i in node.get_neighbours():
			heapq.heappush(self.queue, i)
		#add name and weight to queue
		#continue loop
		while len(self.explored) < len(self.nodes):
			node = heapq.heappop(self.queue) # we need a way to remove an item from the queue if its node has been explored
			for i in node.get_neighbours():
				heapq.heappush(self.queue, i)

			#implement some logging system to return the MST

	def show_mst(self):
		print(self.nodes)
		#make a representation of the mst

nodeA = node([node([], "nodeB")], "nodeA") #A node nodeA with 1 neighbour nodeB
print(nodeA.name, nodeA.neighbours[0].name)
gr = graph([nodeA])
print(gr.nodes[0].name)
gr.prims()

#@TODO -input graph method
# 	   -finnish implementing prims
#      -optimise
#      -create GML parser to graph
#      -create random graph creator
