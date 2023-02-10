# <<<=== START OF UTILITY ===>>>
class Graph:
    def __init__(self, order):
        self.order = order
        self.adj = {}

    def add_edge(self, u, v):
        if u not in self.adj:
            self.adj[u] = {v}
        else:
            self.adj[u].add(v)
        if v not in self.adj:
            self.adj[v] = {u}
        else:
            self.adj[v].add(u)

    def add_nodes(self, nodes):
        for node in nodes:
            self.adj[node] = set()


def decode_g6(bytes_in):
    """
    Decode a graph6 string into a graph object.
    Source : networkx library - https://networkx.org/documentation/stable/_modules/networkx/readwrite/graph6.html#from_graph6_bytes (29/12/2022, 14:15)
    """
    def bits():
        """Returns sequence of individual bits from 6-bit-per-value
            list of data values."""
        for d in data:
            for i in [5, 4, 3, 2, 1, 0]:
                yield (d >> i) & 1

    def data_to_n(data):
        """Read initial one-, four- or eight-unit value from graph6
        integer sequence.
        
        Return (value, rest of seq.)"""
        if data[0] <= 62:
            return data[0], data[1:]
        if data[1] <= 62:
            return (data[1] << 12) + (data[2] << 6) + data[3], data[4:]
        return (
            (data[2] << 30)
            + (data[3] << 24)
            + (data[4] << 18)
            + (data[5] << 12)
            + (data[6] << 6)
            + data[7],
            data[8:],
        )
    
    if bytes_in.startswith(b">>graph6<<"):
        bytes_in = bytes_in[10:]

    data = [c - 63 for c in bytes_in]
    if any(c > 63 for c in data):
        raise ValueError("each input character must be in range(63, 127)")

    n, data = data_to_n(data)
    nd = (n * (n - 1) // 2 + 5) // 6
    if len(data) != nd:
        raise ValueError(
            f"Expected {n * (n - 1) // 2} bits but got {len(data) * 6} in graph6"
        )
    G = Graph(n)
    G.add_nodes(range(n))
    for (i, j), b in zip([(i, j) for j in range(1, n) for i in range(j)], bits()):
        if b:
            G.add_edge(i, j)
    return G
# <<<=== END OF UTILITY ===>>>

# BKP_M algorithm
def BKP_M(SUBG: set, CAND: set, Q: list, G: Graph):
    """
    :param SUBG: set of vertices in the current subgraph
    :param CAND: set of vertices in the current candidate set
    :param Q: current clique
    :param G: a graph represented by it's adjecency list

    Print all maximal cliques of G.
    The implementation is based on the BKP_M algorithm described in
    the paper "On the overall and delay complexity of the CLIQUES and
Bron-Kerbosch algorithms" by Alessio Conte and Etsuji Tomita. 
    
    """
    if len(SUBG) == 0:
        print(" ".join(map(str, Q)))
    else:
        u = max(SUBG, key=lambda u: len(G.adj[u]))        
        for p in CAND - G.adj[u]:
            p_neighbors = G.adj[p]
            Q.append(p)
            SUBG_p = SUBG & p_neighbors
            CAND_p = CAND & p_neighbors
            BKP_M(SUBG_p, CAND_p, Q, G)
            Q.pop()
            CAND.remove(p)
                

if __name__ == '__main__':
    g6 = input()
    G = decode_g6(g6.encode())
    BKP_M(set(G.adj.keys()), set(G.adj.keys()), [], G)
        
