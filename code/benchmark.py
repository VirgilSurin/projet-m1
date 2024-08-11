#!/usr/bin/env python3
import time
from tqdm import tqdm
from algo import *
from utils import *


def bench_time(order: int, algo):
    input = open(f'./samples/graph{order}.g6', 'r')
    alg = ""
    if "CLIQUES" in str(algo):
        alg = "CLIQUES"
    elif "BKP_M" in str(algo):
        alg = "BKP_M"
    elif "BKP_R" in str(algo):
        alg = "BKP_R"
    elif "BK" in str(algo):
        alg = "BK"
    out = open(f'./out/total_res_{str(alg)}_{order}.out', 'w')
    delay_out = open(f'./out/delay_res_{str(alg)}_{order}.out', 'w')
    lines = input.readlines()
    input.close()
    for i in range(len(lines)):
        g6 = lines[i].strip()
        G = decode_g6(g6.encode())
        res = []
        delay = []
        start = time.perf_counter()
        algo(set(G.adj.keys()), set(G.adj.keys()), [], G, res, delay)
        end = time.perf_counter()
        out.write(f'{end - start}\n')
        for i in range(len(delay) - 1):
            time_taken = delay[i + 1] - delay[i]
            delay_out.write(f'{time_taken}\n')


def bench_time_special(order: int, algo, graph_type):
    input = open(f'./samples/graphs/{graph_type}_{order}.g6', 'r')
    alg = ""
    if "CLIQUES" in str(algo):
        alg = "CLIQUES"
    elif "BKP_M" in str(algo):
        alg = "BKP_M"
    elif "BKP_R" in str(algo):
        alg = "BKP_R"
    elif "BK" in str(algo):
        alg = "BK"
    out = open(f'./out/specials/total_res_{str(alg)}_{graph_type}_{order}.out', 'w')
    delay_out = open(f'./out/specials/delay_res_{str(alg)}_{graph_type}_{order}.out', 'w')
    lines = input.readlines()
    input.close()
    for i in range(len(lines)):
        g6 = lines[i].strip()
        G = decode_g6(g6.encode())
        res = []
        delay = []
        start = time.perf_counter()
        algo(set(G.adj.keys()), set(G.adj.keys()), [], G, res, delay)
        end = time.perf_counter()
        out.write(f'{end - start}\n')
        for i in range(len(delay) - 1):
            time_taken = delay[i + 1] - delay[i]
            delay_out.write(f'{time_taken}\n')


def bench_main(algo_choice: str):
    if algo_choice == '1':
            for order in tqdm(range(4, 11)):
                bench_time(order, CLIQUES)
    elif algo_choice == '2':
            for order in tqdm(range(4, 11)):
                bench_time(order, BK)
    elif algo_choice == '3':
            for order in tqdm(range(4, 11)):
                bench_time(order, BKP_M)
    elif algo_choice == '4':
            for order in tqdm(range(4, 11)):
                bench_time(order, BKP_R)
    elif algo_choice == '5':
            for order in tqdm(range(4, 11)):
                bench_time(order, CLIQUES)
                bench_time(order, BK)
                bench_time(order, BKP_M)
                bench_time(order, BKP_R)

def bench_special(algo_choice: str):
    for graph_type in ['complete', 'turan', 'empty']:
        print(f'{graph_type}')
        if algo_choice == '1':
                for order in tqdm(range(3, 45)):
                    bench_time_special(order, CLIQUES, graph_type)
        elif algo_choice == '2':
                for order in tqdm(range(3, 45)):
                    bench_time_special(order, BK, graph_type)
        elif algo_choice == '3':
                for order in tqdm(range(3, 45)):
                    bench_time_special(order, BKP_M, graph_type)
        elif algo_choice == '4':
                for order in tqdm(range(3, 45)):
                    bench_time_special(order, BKP_R, graph_type)
        elif algo_choice == '5':
                for order in tqdm(range(3, 45)):
                    bench_time_special(order, CLIQUES, graph_type)
                    bench_time_special(order, BK, graph_type)
                    bench_time_special(order, BKP_M, graph_type)
                    bench_time_special(order, BKP_R, graph_type)


def main():
    print("Choose the algorithm:")
    print("1 - CLIQUES")
    print("2 - Bron-Kerbosch (BK)")
    print("3 - Bron-Kerbosch with Pivoting (BKP_M)")
    print("4 - Randomized Bron-Kerbosch (BKP_R)")
    print("5 - All Algorithms")
    algo_choice = '-1'
    while algo_choice not in ['1', '2', '3', '4', '5']:
        algo_choice = input("Enter the number corresponding to your choice: ").strip()

    print("Choose the test set:")
    print("1 - Standard (order 4-10)")
    print("2 - Special (graph types: complete, turan, empty)")
    test_set_choice = '0'
    while test_set_choice not in ['1', '2']:
        test_set_choice = input("Enter the number corresponding to your choice: ").strip()

    if test_set_choice == '1':
        bench_main(algo_choice)
    elif test_set_choice == '2':
        bench_special(algo_choice)
    else:
        print("Invalid test set choice.")


if __name__ == "__main__":
    main()
