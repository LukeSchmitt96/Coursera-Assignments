Submission for Coursera's Modern Robotics Course's A* Graph Search Project


Directory layout:
	
	code/main.py            - contains code to run planner
	code/planner.py	        - contains Planner class that contains A* algorithm and methods for loading/saving data
	code/node.py	        - contains Node class that contains data describing nodes in a graph network

    results/edges.csv       - edge data in format [ID1, ID2, cost]
    results/nodes.csv       - node data in format [ID, x, y, heuristic-cost-to-go]
    results/obstacles.csv   - obstacle data in format [x, y, diameter]
    results/path.csv        - path data in format [node_1, node_2, ..., node_goal]

    a-star-derived-path-from-1-to-12.png    - screenshot of motion planning sim showing optimal path from 1 to 12
    Scene5_motion_planning.ttt              - motion planning scene


Running the program:

    python3 main.py

    Can use command line args to specify other start/goal nodes or paths to data/outputs
        args:
            --start_node        [node id]
            --goal_node         [node id]
            --path_to_data      [relative path ending in /]
            --path_to_output    [relative path ending in /]
