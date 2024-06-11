#!/usr/bin/env python3
import networkx as nx
import matplotlib.pyplot as plt
import math

# for i in range(3, 50):
#     print(f"{i}")
#     G = nx.turan_graph(i, math.ceil(i/3))
#     nx.write_graph6(G, f"./samples/graphs/turan_{i}.g6")

#     G = nx.complete_graph(i)
#     nx.write_graph6(G, f"./samples/graphs/complete_{i}.g6")

#     G = nx.empty_graph(i)
#     nx.write_graph6(G, f"./samples/graphs/empty_{i}.g6")

G = nx.read_graph6(f"./samples/graphs/turan_{6}.g6")
nx.draw(G, pos=nx.spring_layout(G), with_labels=True)
plt.show()
