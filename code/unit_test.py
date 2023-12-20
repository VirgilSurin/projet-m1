from sys import stderr
import sys
import deepdiff as diff
import networkx as nx
from CLIQUES import CLIQUES
from BK import BK
from BKP_M import BKP_M
from BKP_R import BKP_R
from utils import *

def test(fn, filename: str):
    with open(f"./samples/{filename}.g6", "r") as f:
        line = f.readline().strip()
        while line:
            # correct answer given by NetworkX
            nx_G = nx.from_graph6_bytes(bytes(line, "utf-8"))
            nx_ans = nx.find_cliques_recursive(nx_G)
            nx_res = []
            for clique in nx_ans:
                clique.sort()
                nx_res.append(" ".join(map(str, clique)))

            G = decode_g6(line.encode())
            my_ans = []
            fn(set(G.adj.keys()), set(G.adj.keys()), [], G, my_ans)
            my_res = []
            for clique in my_ans:
                c = clique.split(" ")
                c.sort()
                my_res.append(" ".join(map(str, c)))
                
            nx_res.sort()
            my_res.sort()
            assert nx_res == my_res, f"==ERROR==\nFunction: {fn}\n in {filename}, graph: {line}\nexpected: {nx_res}\ngot:      {my_res}\n{diff.DeepDiff(nx_res, my_res)}"
            line = f.readline().strip()

if __name__ == "__main__":
    # test CLIQUE
    print("Testing CLIQUES")
    test(CLIQUES, "graph6")
    test(CLIQUES, "graph7")

    # test BK
    print("Testing BK")
    test(BK, "graph6")
    test(BK, "graph7")

    # test BKP_M
    print("Testing BKP_M")
    test(BKP_M, "graph6")
    test(BKP_M, "graph7")

    # test BKP_R
    print("Testing BKP_R")
    test(BKP_R, "graph6")
    test(BKP_R, "graph7")
