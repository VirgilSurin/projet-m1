# <<<=== START OF UTILITY ===>>>
class Graph:
    def __init__(self, order=None):
        self.order = order
        self.adj = {}

    def __str__(self) -> str:
        s = ""
        for v in self.adj:
            s += f"{v:<6} : {self.adj[v]}\n"
        return f"n : {self.order}\n{s}"

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

    def to_g6(self):
        # Constructing the bit vector
        bit_vector = []
        if self.order == None:
            return None
        for u in range(self.order):
            for v in range(0, u):
                if v in self.adj[u]:
                    bit_vector.append('1')
                else:
                    bit_vector.append('0')
        # Padding the bit vector
        while len(bit_vector) % 6 != 0:
            bit_vector.append('0')

        # Splitting into groups of 6 bits
        six_bit_groups = ["".join(bit_vector[i:i+6]) for i in range(0, len(bit_vector), 6)]
        # Converting each group to its decimal representation
        decimal_values = [chr(int(group, 2) + 63) for group in six_bit_groups]

        # Constructing the graph6 representation
        graph6 = []
        graph6.append(self.encode_n(self.order))  # Add the N(n) part
        graph6.extend(decimal_values)  # Add the R(x) part

        return "".join(map(str, graph6))

    def encode_n(self, n):
        if n <= 62:
            return chr(n + 63)
        elif n <= 258047:
            return chr(126) + self.encode_big_endian(n, 4)
        else:
            return chr(126) * 2 + self.encode_big_endian(n, 8)

    def encode_big_endian(self, num, bytes_num):
        num_bytes = []
        for _ in range(bytes_num):
            num_bytes.append(chr(63 + (num >> ((bytes_num - 1) * 6)) & 63))
            num <<= 6
        return "".join(num_bytes)

    def save_to_g6(self, filename):
        """
        Save the current instantiated graph to g6 format
        """
        with open(f"{filename}.g6", 'w') as fout:
            fout.write(f'{self.to_g6()}\n')

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
