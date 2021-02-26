from math import inf
		
class Node():
	"""Node used in graph search algorithms.

	Contains node information like position, least-cost parent, 
	and any neighbors connected to this node.

	...

	Attributes
	----------
	id : str
		id of the node object
	x : float
		x location of the node
	y : float
		y location of the node
	h : float
		heuristic cost-to-go of the node
	parent : str
		id of the least-cost parent node
	neighbors : dict
		dictionary containing any neighboring nodes and associated edge cost
	gScore : float
		cost of traveling to this node from starting node
	fScore : float
		cost of traveling from the starting node to the goal node through this node

	Methods
	-------
	set_neighbor(id_, cost)
		adds neightbor id and associated edge cost to neighbors dict
	"""

	def __init__(self, id_, x_, y_, h_):
		"""
		Parameters
		----------
		id : str
			string denoting the id of the node
		x : float
			x location of the node
		y : float
			y location of the node
		h : float
			heuristic cost-to-go of the node
		"""

		self.id 		= id_
		self.x 			= x_
		self.y 			= y_
		self.h 			= h_
		self.parent 	= None
		self.neighbors	= dict()

		self.gScore 	= inf
		self.fScore 	= inf

	def __repr__(self):
		"""Prints node information."""
		return (
			f"""ID: 	{self.id}
			Parent: 	{self.parent} 
			Neighbors:	{self.neighbors} 
			gScore: 	{self.gScore}
			hScore: 	{self.h}
			fScore: 	{self.fScore}\n"""
			)

	def set_neighbor(self, id_, cost):
		"""Sets any neighbor with the node id and the cost.
		
		Parameters
		----------
		id : str
			id of the neighbor
		cost : float
			edge cost between this node and the specified neighbor
		"""
		
		self.neighbors[id_] = cost

	