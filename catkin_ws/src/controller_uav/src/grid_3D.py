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
		self.dict_obj = defaultdict(list)

	def update_env_obj(self,dict_obj):
		self.dict_obj = dict_obj


	def checker(self,c):

		for name in self.dict_obj:

			coords = self.dict_obj[name]
			xmax = coords[0]+0.8
			xmin = coords[0]-0.8
			ymax = coords[1]+0.8
			ymin = coords[1]-0.8
			zmax = coords[2]+4
			zmin = coords[2]

			if((c[0]<=xmax and c[0]>=xmin) and (c[1]<=ymax and c[1]>=ymin) and (c[2]<=zmax and c[2]>=zmin)):
				print('Collision detected at',c)
				print('Colliding with object',name)
				return True
		return False
			


	def add_edge(self,u,v,edgeval): # u,v :(x,y,z)

		#Check if any of the nodes lie within the object: If yes, change edgeval = 1000
		if(self.checker(u) or self.checker(v)):
			#print('Edgeval updated for collision')
			#print(u,v)
			edgeval=1000

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



def create_graph(grid_resolution, range_max_xy, range_min_xy, range_max_z,range_min_z,edgeval,diag_edgeval,world_file):

	dict_obj = parser_world(world_file)
	print('Calling parser ....\n',dict_obj)
	
	g = Graph()
	g.update_env_obj(dict_obj)
	node_dict = defaultdict(list)
	
	for z in range(range_min_z,range_max_z):
		for y in range(range_min_xy, range_max_xy):
			for x in range(range_min_xy, range_max_xy):
				# Along edges of length 1 unit
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
				#Diagonal edges
				if((x+grid_resolution<range_max_xy) and (y+grid_resolution<range_max_xy)):
					g.add_edge((x,y,z),(x+grid_resolution,y+grid_resolution,z),diag_edgeval)
				if((x+grid_resolution<range_max_xy) and (y-grid_resolution>=range_min_xy)):
					g.add_edge((x,y,z),(x+grid_resolution,y-grid_resolution,z),diag_edgeval)
				if((x-grid_resolution>=range_min_xy) and (y+grid_resolution<range_max_xy)):
					g.add_edge((x,y,z),(x+grid_resolution,y-grid_resolution,z),diag_edgeval)
				if((x-grid_resolution>=range_min_xy) and (y-grid_resolution>=range_min_xy)):
					g.add_edge((x,y,z),(x-grid_resolution,y-grid_resolution,z),diag_edgeval)

	# save the model to disk

	filename = 'Graph_world2.sav'

	pickle.dump(g, open(filename, 'wb'))

	
	print(dict_obj)

	return g	


if __name__ == '__main__':
	# Parse the world data to obtain object's data points
	#TO DO: Add scaling data
	#dict_obj = parser_world('my_world_2.world')
	#print('Calling parser ....\n',dict_obj)

	filename = 'my_world_2.world'


	g = create_graph(grid_resolution = 0.5,range_max_xy = 10,range_min_xy = -10,range_max_z = 7, range_min_z = 0,edgeval=0.5,diag_edgeval=0.707,world_file=filename)
	edgelist = g.get_edge_list()
	#print(edgelist)
	#The following code snippet writes graph data to the file
	with open('Grid_3D_updated_diag_world2.txt','w') as f:

		for each in edgelist:
			#print('\n',each)
			f.write(str(each))

                                                   
	print(g.dict_obj)





		
		
		
