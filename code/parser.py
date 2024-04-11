#!/usr/bin/env python3

from utils import Graph

path = "./samples/"
filename = "email-Enron.txt"
# n
# m
# n_i -> n_i'
# ...

with open(path+filename) as f:
    n = int(f.readline())
    m = int(f.readline())
    G = Graph(n)
    G.add_nodes(range(n))
    i = 0
    lines = f.readlines()
    for l in lines:
        edge = l.strip().split(	)
        G.add_edge(int(edge[0]), int(edge[1]))
