from collections import defaultdict
import numpy as np
from xml_parser import *
import pickle

class Edge():
	def __init__(self,node1,node2,edgeval):
		self.node1 = node1
		self.node2 = node2
		self.edgeval = edgeval


class Graph():

	def __init__(self,nodes= [], edges=[]):
		self.graph = defaultdict(list)
		self.nodes = nodes
		self.edges = edges

	def add_edge(self,u,v,edgeval): # u,v :(x,y,z)

		# Update graoh
		if((u,edgeval) not in self.graph[v]): # Check if the edge already exists
			self.graph[u].append((v,edgeval))
			e = Edge(u,v,edgeval)
			if(e not in self.edges):	
				self.edges.append(e)

		# Update node tracker in the graph
		if u not in self.nodes:
			self.nodes.append(u)
		if v not in self.nodes:
			self.nodes.append(v)
		
		# Add the edge to the edgelist
		#e = Edge(u,v,edgeval)
		#if(e not in edges):
			#edges.append(e)
		

	def get_edge_list(self):
		edgevalues = []

		for edge in self.edges:
			edgevalues.append((edge.node1,edge.node2,edge.edgeval))

		return edgevalues



def create_graph(grid_resolution, range_max_xy, range_min_xy, range_max_z,range_min_z,edgeval):

	g = Graph()
	node_dict = defaultdict(list)
	
	#Updating node numbers

	#Iteratively add all edges
	# Case 1:
	num_neighbors = 6
	for z in range(range_min_z,range_max_z):
		for y in range(range_min_xy, range_max_xy):
			for x in range(range_min_xy, range_max_xy):
				if((x+grid_resolution)<range_max_xy):
					g.add_edge((x,y,z),(x+grid_resolution,y,z),edgeval)
				if((y+grid_resolution)<range_max_xy):
					g.add_edge((x,y,z),(x,y+grid_resolution,z),edgeval)
				if((x-grid_resolution)>=range_min_xy):
					g.add_edge((x,y,z),(x-grid_resolution,y,z),edgeval)
				if((y-grid_resolution)>=range_min_xy):
					g.add_edge((x,y,z),(x,y-grid_resolution,z),edgeval)
				if((z+grid_resolution)<range_max_z):
					g.add_edge((x,y,z),(x,y,z+grid_resolution),edgeval)
				if((z-grid_resolution)>=range_min_z):
					g.add_edge((x,y,z),(x,y,z-grid_resolution),edgeval)

	# save the model to disk
	filename = 'Graph.sav'
	pickle.dump(g, open(filename, 'wb'))

	return g.get_edge_list()			

def main():
    edgelist = create_graph(grid_resolution = 1,range_max_xy = 6,range_min_xy = -5,range_max_z = 10, range_min_z = 0,edgeval=1)
    
    with open('Grid_3D.txt','w') as f:
    	for each in edgelist:
    		print('\n',each)
    		f.write(str(each))
    
    # Parse the world data 
    #TO DO: Add scaling data
    dict_obj = parser_world('my_world.world')
    print('Calling parser ....\n',dict_obj)
    
    #for name in dict_obj:
    	#coords = dict_obj[name]

if (__name__ == '__main__'):
    main()