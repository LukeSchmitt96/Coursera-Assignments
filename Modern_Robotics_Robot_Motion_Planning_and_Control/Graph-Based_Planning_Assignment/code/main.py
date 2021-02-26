import argparse
import time
from planner import Planner


if __name__ == "__main__":

    start = time.time()

    # parse command line args
    parser = argparse.ArgumentParser()
    parser.add_argument("--path_to_data", default="../data/")
    parser.add_argument("--path_to_output", default="../data/")
    parser.add_argument("--start_node", default='1')
    parser.add_argument("--goal_node", default='12')
    args = parser.parse_args()

    # initialize planner object
    planner = Planner(args.path_to_data)

    # run A* planner
    planner.plan_astar(args.start_node,args.goal_node)

    # save path data
    planner.save_path(args.path_to_output)

    end = time.time()
    print(f"Elapsed Time: {end-start}s")