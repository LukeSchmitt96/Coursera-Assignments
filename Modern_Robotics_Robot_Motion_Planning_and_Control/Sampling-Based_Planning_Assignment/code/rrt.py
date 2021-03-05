from sampling_planners import *

class RRT(SamplingPlanner):
    """Rapidly-exploring random tree (RRT) sampling-based algorithm"""

    def __init__(self, data_dir, out_dir, *args, **kwargs):
        # calls base class constructor
        super().__init__(data_dir, out_dir, *args, **kwargs)
        
        # runs rrt algo
        self.plan_rrt()

        # saves planner data
        self._save_data(out_dir)

    def plan_rrt(self, max_size=500):
        """Runs the RRT algo"""

        # run loop until sample max number of nodes
        while len(self.nodes) < max_size:

            # sample a random position in space, occasionally sampling goal position
            if random.randint(0,10) == 0:
                if not self._is_in_collision_point(self.goal_pos):
                    sample_pos = np.array(self.goal_pos)
            else:
                sample_pos = self._sample()

            # get sample node position and distance from nearest node
            nearest, d = self._neartest_node(sample_pos)

            # new position after taking a step towards the sample position
            new = self._motion(nearest, sample_pos, d)

            if not self._is_in_collision_point(new):

                # create new node at new
                id_ = str(len(self.nodes)+1)
                self.nodes[id_] = Node(
                    id_ = id_,
                    x_ = new[0],
                    y_ = new[1],
                    goal_pos_ = self.goal_pos,
                    parent_=nearest.id)

                # update neighbors
                self.nodes[id_].neighbors[nearest.id] = self._dist(self.nodes[id_].pos, nearest.pos)
                self.nodes[nearest.id].neighbors[id_] = self._dist(self.nodes[id_].pos, nearest.pos)

                # visuzlize update
                if self.viz: self._viz_update(nearest.pos, new, sample_pos)

                # check if we are close enough to the goal position
                if self._dist(self.nodes[id_].pos, self.goal_pos) < self.goal_tol:

                    # if close enough, add node at goal position
                    id_goal = str(len(self.nodes)+1)
                    self.nodes[id_goal] = Node(
                        id_=id_goal,
                        x_=self.goal_pos[0],
                        y_=self.goal_pos[1],
                        goal_pos_=self.goal_pos,
                        parent_=id_)

                    # update neighbors
                    self.nodes[id_].neighbors[id_goal] = self._dist(self.nodes[id_goal].pos, self.nodes[id_].pos)
                    self.nodes[id_goal].neighbors[id_] = self._dist(self.nodes[id_goal].pos, self.nodes[id_].pos)

                    # visualize update
                    if self.viz: self._viz_update(self.nodes[id_].pos, 
                                                  self.nodes[id_goal].pos, 
                                                  self.nodes[id_goal].pos)
                    
                    # reconstruct path through parents
                    self._reconstruct_path(self.nodes[id_goal])
                    
                    # visualize path
                    if self.viz: self._viz_path()
                    
                    # done!
                    return

        # print failure message
        print(f"Max nodes of {max_size} reached. No valid path found. Try increasing max number of nodes?")

    def _neartest_node(self, pos):
        """search through nodes to find closest neighbor"""
        nn = self.nodes[self._knn(1, pos)[0]]
        return nn, self._dist(nn.pos, pos)

    def _motion(self, nearest, sample_pos, d):
        """get position of nearest node plus a step towards the sample pos"""
        return nearest.pos + self.step * np.array(sample_pos-nearest.pos)/d

    def _reconstruct_path(self, current):
        """Build path by looping through parents until reaching start node.

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

        print("Path to goal found : " , self.path)

    def _viz_update(self, old, new, samp):
        """visualize update"""
        sc = self.ax.scatter(samp[0], samp[1], color=[0.5,0.0,0.5], s=100)
        self.ax.plot([old[0], new[0]], [old[1], new[1]], 'ko-', markersize=1, zorder=1)
        plt.pause(0.001)
        sc.remove()
