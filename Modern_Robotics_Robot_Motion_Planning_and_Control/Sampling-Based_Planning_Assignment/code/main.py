import argparse
import time
from rrt import RRT
# from prm import PRM

if __name__ == "__main__":

    start = time.time()

    # parse command line args
    parser = argparse.ArgumentParser()
    parser.add_argument("-path_to_data",    default="../results/")
    parser.add_argument("-path_to_output",  default="../results/")
    parser.add_argument("-visualize",       action="store_true")
    parser.add_argument("-method",          choices=["RRT", "PRM"], default="RRT")
    parser.add_argument("-step",            default=0.05, type=float)
    args = parser.parse_args()

    if args.method == "RRT":
        RRT(data_dir=args.path_to_data, out_dir=args.path_to_output, viz_=args.visualize, step_=args.step)
    elif args.method == "PRM":
        print("PRM not implemented!")
        # PRM(data_dir=args.path_to_data, out_dir=args.path_to_output, viz_=args.visualize, N=500)
    else:
        print("Choose RRT or PRM for method")
        exit()

    end = time.time()
    print(f"Elapsed Time: {(end-start):.4f}s")

    # keep visualization on screen
    if args.visualize: input("Press any button to continue...\n")