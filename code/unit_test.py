import time
from tqdm import tqdm
from algo import *
from utils import *


def bench_total_time(order: int, algo):
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
    lines = input.readlines()
    input.close()
    for i in tqdm(range(len(lines))):
        g6 = lines[i].strip()
        G = decode_g6(g6.encode())
        res = []
        start = time.perf_counter()
        algo(set(G.adj.keys()), set(G.adj.keys()), [], G, res, [])
        end = time.perf_counter()
        out.write(f'{end - start}\n')

def clique_delay(order: int, algo):
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
    out = open(f'./out/delay_res_{str(alg)}_{order}.out', 'w')
    lines = input.readlines()
    input.close()
    for i in tqdm(range(len(lines))):
        g6 = lines[i].strip()
        G = decode_g6(g6.encode())
        res = []
        delay = [time.perf_counter()]
        algo(set(G.adj.keys()), set(G.adj.keys()), [], G, res, delay)
        for i in range(len(delay) - 1):
            time_taken = delay[i+1] - delay[i]
            out.write(f'{time_taken}\n')

def total_time_main():
    print("BENCHMARK")
    print("=========\n\n")
    bench_total_time(4, CLIQUES)
    bench_total_time(5, CLIQUES)
    bench_total_time(6, CLIQUES)
    bench_total_time(7, CLIQUES)
    bench_total_time(8, CLIQUES)
    bench_total_time(9, CLIQUES)
    bench_total_time(10, CLIQUES)

    print("=========\n\n")
    bench_total_time(4, BK)
    bench_total_time(5, BK)
    bench_total_time(6, BK)
    bench_total_time(7, BK)
    bench_total_time(8, BK)
    bench_total_time(9, BK)
    bench_total_time(10, BK)

    print("=========\n\n")
    bench_total_time(4, BKP_M)
    bench_total_time(5, BKP_M)
    bench_total_time(6, BKP_M)
    bench_total_time(7, BKP_M)
    bench_total_time(8, BKP_M)
    bench_total_time(9, BKP_M)
    bench_total_time(10, BKP_M)

    print("=========\n\n")
    bench_total_time(4, BKP_R)
    bench_total_time(5, BKP_R)
    bench_total_time(6, BKP_R)
    bench_total_time(7, BKP_R)
    bench_total_time(8, BKP_R)
    bench_total_time(9, BKP_R)
    bench_total_time(10, BKP_R)

def delay_main():
    print("BENCHMARK")
    print("=========\n\n")
    clique_delay(4, CLIQUES)
    clique_delay(5, CLIQUES)
    clique_delay(6, CLIQUES)
    clique_delay(7, CLIQUES)
    clique_delay(8, CLIQUES)
    clique_delay(9, CLIQUES)
    clique_delay(10, CLIQUES)

    print("=========\n\n")
    clique_delay(4, BK)
    clique_delay(5, BK)
    clique_delay(6, BK)
    clique_delay(7, BK)
    clique_delay(8, BK)
    clique_delay(9, BK)
    clique_delay(10, BK)

    print("=========\n\n")
    clique_delay(4, BKP_M)
    clique_delay(5, BKP_M)
    clique_delay(6, BKP_M)
    clique_delay(7, BKP_M)
    clique_delay(8, BKP_M)
    clique_delay(9, BKP_M)
    clique_delay(10, BKP_M)

    print("=========\n\n")
    clique_delay(4, BKP_R)
    clique_delay(5, BKP_R)
    clique_delay(6, BKP_R)
    clique_delay(7, BKP_R)
    clique_delay(8, BKP_R)
    clique_delay(9, BKP_R)
    clique_delay(10, BKP_R)


def bench_total_time_special(order: int, algo, graph_type: str):
    input_file = f'./samples/graphs/{graph_type}_{order}.g6'
    with open(input_file, 'r') as input:
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
        lines = input.readlines()
        for i in range(len(lines)):
            g6 = lines[i].strip()
            G = decode_g6(g6.encode())
            res = []
            start = time.perf_counter()
            algo(set(G.adj.keys()), set(G.adj.keys()), [], G, res, [])
            end = time.perf_counter()
            out.write(f'{end - start}\n')  # in s

def clique_delay_special(order: int, algo, graph_type: str):
    input_file = f'./samples/graphs/{graph_type}_{order}.g6'
    with open(input_file, 'r') as input:
        out = open(f'./out/specials/delay_res_{algo}_{graph_type}_{order}.out', 'w')
        lines = input.readlines()
        for i in range(len(lines)):
            g6 = lines[i].strip()
            G = decode_g6(g6.encode())
            res = []
            delay = [time.perf_counter()]
            algo(set(G.adj.keys()), set(G.adj.keys()), [], G, res, delay)
            for i in range(len(delay) - 1):
                time_taken = (delay[i+1] - delay[i])  # in s
                out.write(f'{time_taken}\n')

def total_time_special():
    print("BENCHMARK")
    print("=========\n\n")
    for graph_type in ['complete', 'turan', 'empty']:
        for order in tqdm(range(3, 45)):
            bench_total_time_special(order, CLIQUES, graph_type)
            # bench_total_time_special(order, BK, graph_type)
            bench_total_time_special(order, BKP_M, graph_type)
            bench_total_time_special(order, BKP_R, graph_type)

def delay_special():
    print("BENCHMARK")
    print("=========\n\n")
    for graph_type in ['complete', 'turan', 'empty']:
        for order in tqdm(range(3, 45)):
            clique_delay_special(order, CLIQUES, graph_type)
            # clique_delay_special(order, BK, graph_type)
            clique_delay_special(order, BKP_M, graph_type)
            clique_delay_special(order, BKP_R, graph_type)



def main():
    print("Choose the type of benchmark:")
    print("1 - Total Time Benchmark")
    print("2 - Delay Benchmark")
    benchmark_type = input("Enter the number corresponding to your choice: ").strip()

    print("Choose the algorithm:")
    print("1 - CLIQUES")
    print("2 - Bron-Kerbosch (BK)")
    print("3 - Bron-Kerbosch with Pivoting (BKP_M)")
    print("4 - Randomized Bron-Kerbosch (BKP_R)")
    algo_choice = input("Enter the number corresponding to your choice: ").strip()

    print("Choose the test set:")
    print("1 - Standard (order 4-10)")
    print("2 - Special (graph types: complete, turan, empty)")
    test_set_choice = input("Enter the number corresponding to your choice: ").strip()

    algorithm = None
    if algo_choice == '1':
        algorithm = CLIQUES
    elif algo_choice == '2':
        algorithm = BK
    elif algo_choice == '3':
        algorithm = BKP_M
    elif algo_choice == '4':
        algorithm = BKP_R
    else:
        print("Invalid algorithm choice.")
        return

    if benchmark_type == '1':
        if test_set_choice == '1':
            total_time_main()
        elif test_set_choice == '2':
            total_time_special()
        else:
            print("Invalid test set choice.")
    elif benchmark_type == '2':
        if test_set_choice == '1':
            delay_main()
        elif test_set_choice == '2':
            delay_special()
        else:
            print("Invalid test set choice.")
    else:
        print("Invalid benchmark type choice.")


if __name__ == "__main__":
    main()
