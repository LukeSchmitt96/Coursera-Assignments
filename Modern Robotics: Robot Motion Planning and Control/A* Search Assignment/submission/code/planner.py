import csv
from numpy import argmin
from operator import attrgetter

from node import Node

class Planner():
	"""Class for planning optimal paths on graph-based networks.

	...

	Attributes
	----------
	nodes : dict of Node objects in graph network
	path : list of nodes in optimal path (start -> goal)

	Methods
	-------
	_load_data(path)
		private method to parse nodes.csv and edges.csv to build network

	_reconstruct_path(node)
		private method to build optimal path by looping through parents until reaching start node

	plan_astar(start, goal)
		uses the A* algorithm to build an optimal path through the network

	save_path(path)
		saves optimal path to a csv file
	"""
	def __init__(self, path_to_data):
		"""Constructor for Planner class. Loads data from specified location"""
		self.nodes = dict()
		self.path = []
		self._load_data(path_to_data)

	def _load_data(self, path):
		"""Loads data from specified directory. Parses and stores in list of Node objects."""
		# load node data
		with open(path + 'nodes.csv', 'r') as node_file:
			for row in csv.reader(node_file):
				if row[0][0] != "#":
					# make new node with ID, x, y, and cost2go
					self.nodes[row[0]] = Node(row[0], float(row[1]), float(row[2]), float(row[3]))

		# load edge data
		with open(path + 'edges.csv', 'r') as edge_file:
			for row in csv.reader(edge_file):
				if row[0][0] != '#':
					# create edge from ID1 to ID2 with cost
					self.nodes[row[0]].set_neighbor(row[1], float(row[2]))

					# create edge from ID2 to ID1 with cost
					self.nodes[row[1]].set_neighbor(row[0], float(row[2]))

	def _reconstruct_path(self, current):
		"""Build optimal path by looping through parents until reaching start node.
		
		Parameters
		----------
		current : Node object
			node to build the path from
		"""

		# add current node to path
		self.path = [current.id]

		# loop until no parents exist
		while current.parent is not None:

			# add node parent to beginning of path
			self.path.insert(0, self.nodes[current.id].parent)

			# new current node as current node's parent
			current = self.nodes[current.parent]

		print("Optimal Path Found: ", self.path)

	def plan_astar(self, start, goal):
		"""Plans an optimal path through the graph network using the A* algorithm.
		
		Parameters
		----------
		start : str
			id of the starting node
		goal: str
			id of the goal node
		"""

		openSet = []
		# set openSet to the starting node
		openSet.append(self.nodes[start])

		# the node immediately preceding with the cheapest path
		self.nodes[start].parent = None

		# set gScore and gScore for start node
		self.nodes[start].gScore = 0
		self.nodes[start].fScore = self.nodes[start].h + self.nodes[start].gScore

		# run while there are objects in openSet list
		while openSet:
			# sort openSet by fScore, node with smallest fScore will be at 0
			openSet.sort(key=lambda x: x.fScore)
			c = openSet[0].id

			# check if current node is the goal
			if c == goal:
				# get optimal path
				self._reconstruct_path(self.nodes[c])
				return

			# remove current node from openSet
			openSet.remove(self.nodes[c])

			# sort through neighbors of c based on their gScore
			for n in sorted(self.nodes[c].neighbors.keys(), key=lambda x: self.nodes[x].gScore):
				# distance from start to neighbor through current (gScore + edge_cost)
				temp_score = self.nodes[c].gScore + self.nodes[c].neighbors[n]
				
				# check for score less than best gScore
				if temp_score < self.nodes[n].gScore:

					# if better, update parent, gScore, and fScore
					self.nodes[n].parent = c
					self.nodes[n].gScore = temp_score
					self.nodes[n].fScore = self.nodes[n].gScore + self.nodes[n].h

					# add nieghbor to openSet if not already in
					if n not in openSet:
						openSet.append(self.nodes[n])
		
		# return start node if no solution is found
		print("No Path Found!")
		self.path = [start]

	def save_path(self, path):
		"""Saves the optimal path as a csv file in the specified directory

		If optimal path does not exist (i.e. path is empty), returns error

		Parameters
		----------
		path : str
			path to directory in which to save results
		"""

		with open(path + "path.csv", 'w') as path_file:
			writer = csv.writer(path_file)
			writer.writerow(self.path)
