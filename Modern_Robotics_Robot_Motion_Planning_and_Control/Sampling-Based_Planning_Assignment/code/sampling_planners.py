import numpy as np
import matplotlib.pyplot as plt
import csv
import random
from math import sqrt, inf

from obstacle import Obstacle
from node import Node

class SamplingPlanner():
    """Base class for RRT and PRM sample-based planners"""
    
    def __init__(self, data_dir, out_dir, start_=np.array([-0.5, -0.5]), goal_=np.array([0.5, 0.5]), step_=0.05, goal_tol=0.05, viz_=False):
        
        # bounds on C-space
        self.C = np.array([[-0.5, 0.5], [-0.5, 0.5]])

        # start and end goal positions
        self.start_pos = start_
        self.goal_pos = goal_
        self.goal_tol = goal_tol

        # dictionary for nodes
        self.nodes = dict()

        # add first (starting) node to list
        self.nodes[str(1)] = Node(str(1), start_[0], start_[1], self.goal_pos)
        
        # list for obstacles
        self.obs = []

        # step size parameter
        self.step = step_

        # load obstacle data
        self._load_data(data_dir)

        # list for path
        self.path = []

        # visualize?
        self.viz = viz_
        if self.viz:
            self._init_viz()

    def _load_data(self, dir_):
        """Loads data from obstacles.csv and stores in obstacles list

        Parameters
        ----------
        dir_ : str
            path to directory for obstacles.csv
        """
        with open(dir_ + 'obstacles.csv') as obs_file:
            for row in csv.reader(obs_file):
                if row[0][0] != '#':
                    self.obs.append(Obstacle(float(row[0]), float(row[1]), float(row[2])/2.0))

    def _save_data(self, out_dir):
        """saves path, node, and edge data"""

        # save path data in csv [node_0, node_1, ...]
        def _save_path():
            with open(out_dir + "path.csv", 'w') as path_file:
                writer = csv.writer(path_file)
                writer.writerow(self.path)

        # save node data in csv [ID,x,y]
        def _save_nodes():
            with open(out_dir + "nodes.csv", 'w') as node_file:
                writer = csv.writer(node_file)
                writer.writerow(['# ID','x','y'])
                for n in self.nodes.values():
                    writer.writerow([n.id, n.x, n.y])

        # save edge data in csv [ID1,ID2,cost]
        def _save_edges():
            with open(out_dir + "edges.csv", 'w') as edge_file:
                writer = csv.writer(edge_file)
                writer.writerow(['# ID1','ID2','cost'])
                saved_edges = [[]]
                for node in self.nodes.values():
                    for neighbor in node.neighbors:
                        node_id = int(node.id)
                        neighbor_id = int(neighbor)
                        if [neighbor_id,node_id] in saved_edges:
                            continue
                        else:
                            writer.writerow([node_id, neighbor_id, node.neighbors[neighbor]])
                            saved_edges.append([node_id, neighbor_id])
                            continue

        # run save subfunctions
        _save_path()
        _save_nodes()
        _save_edges()

    def _is_in_collision_point(self, pos):
        """Checks point collision for every obstacle

        Parameters
        ----------
        pos : float 2-tuple

        Returns
        -------
        b : bool
            True if in collision
            False if not in collision
        """

        # loop through each obstacle
        for o in self.obs: 

            # check if pos collides with obstacle
            if o.is_in_collision_point(pos):

                # returns True if in collision
                return True

        # return False if not in collision
        return False

    def _is_in_collision_line(self, a, b):
        """Checks line collision between two points for every obstacle

        Parameters
        ----------
        a, b : float 2-tuples
            points to check for collision between

        Returns
        -------
        b : bool
            True if line between two points would be invalid,
            False if line between two points would be valid
        """

        # loop through each obstacle
        for o in self.obs:

            # check if pos collides with obstacle
            if o.is_in_collision_line(a, b):

                # returns True if in collision
                return True

        # return False if not in collision
        return False

    def _sample(self):
        """Samples from C until a valid node (not in collision with any obstacles) is created
        
        Returns
        -------
        x,y : float 2-tuple
            valid node position
        """
        # run until valid point is found
        while True:

            # get random x,y in C-space
            x, y = np.random.uniform(-0.5, 0.5), np.random.uniform(-0.5, 0.5)

            # check for collision with any obstacles
            if not self._is_in_collision_point([x,y]):

                # point is valid, return position
                return np.array([x,y])

    def _dist(self, point_1, point_2):
        """Get euclidian distance between two points

        Parameters
        ----------
        point_1 : float 2-tuple
            x,y pos of first point
        point_2 : float 2-tuple
            x,y pos of first point

        Returns
        -------
        d : float
            euclidian distance between the given points
        """
        return sqrt((point_1[0] - point_2[0])**2 + (point_1[1] - point_2[1])**2)

    def _init_viz(self):
        self.fig = plt.figure()
        self.ax = self.fig.gca()
        plt.axis([-0.5, 0.5, -0.5, 0.5])

        # obstacles
        for o in self.obs:
            self.ax.add_patch(plt.Circle((o.x, o.y), o.r, color=[0.5, 0.5, 0.5]))

        # start and goal
        self.ax.scatter(self.start_pos[0], self.start_pos[1], c='g', marker='o')
        self.ax.scatter(self.goal_pos[0], self.goal_pos[1], c='b', marker='o')

        # plt.show()
        plt.pause(0.1)

    def _viz_path(self):
        """Visualizes path"""
        for p in self.path:
            self.ax.scatter(self.nodes[p].x, self.nodes[p].y, c='r', marker='o', s=200, zorder=2)
            plt.pause(0.0001)

    def _knn(self, k, pos):
        """Gets k closest neighbors to a position"""
        return sorted(self.nodes, key=lambda x: sqrt((self.nodes[x].x - pos[0])**2 + (self.nodes[x].y - pos[1])**2))[:k]