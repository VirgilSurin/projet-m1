#!/usr/bin/env python3
import os
import time
import numpy as np
from utils import decode_g6
from algo import *

def format_time(duration):
    if duration >= 1:
        return f"{duration:.6f} s"
    elif duration >= 1e-6:
        return f"{duration * 1e6:.3f} µs"
    elif duration >= 1e-9:
        return f"{duration * 1e9:.3f} ns"
    else:
        return f"{duration * 1e12:.3f} ps"

def main():
    print("Please enter the graph in g6 format:")
    g6 = input().strip()

    try:
        G = decode_g6(g6.encode())
    except ValueError as e:
        print(f"Error parsing graph: {e}")
        return
    print(f"{G}\n")

    print("Please choose the algorithm to use:")
    print("1 for BK")
    print("2 for BKP_M")
    print("3 for BKP_R")
    print("4 for CLIQUES")
    print("Enter your choice :")
    algo_choice = int(input().strip())

    SUBG = set(G.adj.keys())
    CAND = set(G.adj.keys())
    Q = []
    result = []
    delay = []
    start_time = time.perf_counter()

    if algo_choice == 1:
        BK(SUBG, CAND, Q, G, result, delay)
    elif algo_choice == 2:
        BKP_M(SUBG, CAND, Q, G, result, delay)
    elif algo_choice == 3:
        BKP_R(SUBG, CAND, Q, G, result, delay)
    elif algo_choice == 4:
        CLIQUES(SUBG, CAND, Q, G, result, delay)
    else:
        print("Invalid choice. Please choose a number between 1 and 4.")
        return

    total_time = time.perf_counter() - start_time
    mean_delay = 0
    for i in range(len(delay) -1):
        mean_delay += (delay[i+1] - delay[i])
    mean_delay /= len(delay)

    print("\nResult of the algorithm:")
    for clique in result:
        print(f"{{{clique}}}")

    print(f"Mean delay: {format_time(mean_delay)}")
    print(f"Total execution time: {format_time(total_time)}")

if __name__ == "__main__":
    main()
