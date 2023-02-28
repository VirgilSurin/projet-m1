import deepdiff as diff
import networkx as nx
from CLIQUES import CLIQUES
from utils import *

# n = 6, every graph
with open("./samples/graph6.g6", "r") as f:
    line = f.readline().strip()
    while line:
        #TODO
        # correct answer given by NetworkX
        nx_G = nx.from_graph6_bytes(bytes(line, "utf-8"))
        nx_ans = nx.find_cliques_recursive(nx_G)
        nx_res = []
        for clique in nx_ans:
            nx_res.append(" ".join(map(str, clique)))

        G = decode_g6(line.encode())
        my_ans = []
        CLIQUES(set(G.adj.keys()), set(G.adj.keys()), [], G, my_ans)

        assert diff.DeepDiff(nx_res, my_ans) == {}, f"ERROR: {line}\nexpected: {nx_res}\ngot:      {my_ans}\n{diff.DeepDiff(nx_res, my_ans)}"
        line = f.readline().strip()
