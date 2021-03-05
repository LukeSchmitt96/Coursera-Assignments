from math import inf, sqrt
import numpy as np
from numpy.linalg import norm
		
class Node():
	"""Node used in search algorithms.

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
	pos : float 2-tuple
		(x,y) of node
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
	dist_to_point(pos)
		gets euclidean distance to a position from this node
	"""

	def __init__(self, id_, x_, y_, goal_pos_, parent_=None):
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
		self.pos		= np.array([self.x, self.y])
		self.h 			= self._dist_to_point(goal_pos_)
		self.parent 	= parent_
		self.neighbors	= dict()

		self.gScore 	= inf
		self.fScore 	= inf

	def __repr__(self):
		"""Prints node information."""
		return (
			f"""ID: 	{self.id}
			pos:		{self.pos}
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

	def _dist_to_point(self, pos):
		"""Gets euclidean distance to a position from this node"""
		return sqrt((self.pos[0] - pos[0])**2 + (self.pos[1] - pos[1])**2)