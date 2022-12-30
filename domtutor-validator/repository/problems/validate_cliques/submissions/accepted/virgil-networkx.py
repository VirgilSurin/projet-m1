import networkx as nx
g6 = input()
G = nx.from_graph6_bytes(g6.encode())
for c in nx.find_cliques_recursive(G):
    print(" ".join(map(str, c)))


