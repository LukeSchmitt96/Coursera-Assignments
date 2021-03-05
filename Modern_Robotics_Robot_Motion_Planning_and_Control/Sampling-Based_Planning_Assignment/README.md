## Submission for Coursera's Modern Robotics Course's Sampling-Based Planning Project


## Directory layout:
	
	code/main.py                - contains code to run planner
	code/sampling_planners.py   - base class for rrt and prm (not in this submission) classes
	code/rrt.py	            - child class of sampling_planners, contains methods for rrt algorithm
	code/node.py	            - contains Node class that contains data describing nodes
	code/obstacle.py            - contains Obstacle class that contains data describing obstacles

	results/edges.csv           - edge data in format [ID1, ID2, cost]
	results/nodes.csv           - node data in format [ID, x, y, heuristic-cost-to-go]
	results/obstacles.csv       - obstacle data in format [x, y, diameter]
	results/path.csv            - path data in format [node_1, node_2, ..., node_goal]

	rrt_output.png              - screenshot of sim showing path from start [-0.5,-0.5] to goal [0.5,0.5]
	Scene5_motion_planning.ttt  - motion planning scene


## Running the program:
`python3 main.py`

Can use command line args to specify other start/goal nodes or paths to data/outputs
        
args:

	-path_to_data       [relative path ending in /]
	-path_to_output     [relative path ending in /]
	-visualize          [if flagged, shows a visualion]
	-methods            [RRT or PRM (not implemented)]
