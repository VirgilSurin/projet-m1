from utils import *

def BK(SUBG: set, CAND: set, Q: list, G: Graph, result: list):
    """
    :param SUBG: set of vertices in the current subgraph
    :param CAND: set of vertices in the current candidate set
    :param Q: current clique
    :param G: a graph represented by it's adjecency list
    :param result: a list that will be populate with all the maximal clique of G


    Print all maximal cliques of G.
    The implementation is based on the BK algorithm described in
    the paper "On the overall and delay complexity of the CLIQUES and
Bron-Kerbosch algorithms" by Alessio Conte and Etsuji Tomita.
    """
    if len(SUBG) == 0:
        result.append(" ".join(map(str, Q)))
        # print(" ".join(map(str, Q)))
    else:
        for p in list(CAND):
            p_neighbors = G.adj[p]
            Q.append(p)
            SUBG_p = SUBG & p_neighbors
            CAND_p = CAND & p_neighbors
            BK(SUBG_p, CAND_p, Q, G, result)
            Q.pop()
            CAND.remove(p)


if __name__ == "__main__":
    g6 = input()
    G = decode_g6(g6.encode())
    res = []
    BK(set(G.adj.keys()), set(G.adj.keys()), [], G, res)
    # coucou
