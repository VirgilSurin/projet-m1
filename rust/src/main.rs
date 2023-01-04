use std::collections::HashMap;


struct Graph {
    adj: HashMap<usize, Vec<usize>>,
}

impl Graph {
    fn new() -> Self {
        Graph {
            adj: HashMap::new(),
        }
    }
    
    fn add_nodes(&mut self, nodes: Vec<usize>) {
        for node in &nodes {
            self.adj.insert(*node, Vec::new());
        }
    }

    fn add_edge(&mut self, i: usize, j: usize) {
        if !self.adj.contains_key(&i) {
            self.adj.insert(i, Vec::new());
        }
        if !self.adj.contains_key(&j) {
            self.adj.insert(j, Vec::new());
        }
        self.adj.get_mut(&i).unwrap().push(j);
        self.adj.get_mut(&j).unwrap().push(i);
    }
    
    fn print(&self) {
        for (node, adjacency_list) in &self.adj {
            print!("{}: ", node);
            for &adjacent_node in adjacency_list {
                print!("{} ", adjacent_node);
            }
            println!();
        }
    }
        
    fn decode_g6(g6: &str) -> Self {
        let mut graph = Graph::new();
        // decode graph order

        // transofrm g6 string into a vector of bits
        let mut bits = Vec::new();
        for c in g6.chars() {
            let mut n = c as u8 - 63;
            for _ in 0..6 {
                bits.push(n & 1);
                n >>= 1;
            }
        }
        // decode graph order
        let order = (((g6.len() * 6) as f64) / 64.).ceil() as usize;
        // delete the bits corresponding to the order
        bits.drain(0..order * 6);
        // decode adjacency matrix
        let mut nodes = Vec::new();
        for i in 0..order {
            nodes.push(i);
        }
        graph.add_nodes(nodes);
        let mut i = 0;
        let mut j = 0;
        for bit in bits {
            if bit == 1 {
                graph.add_edge(i, j);
            }
            j += 1;
            if j == order {
                i += 1;
                j = i + 1;
            }
        }
        graph 
    }
}


fn main() {
    println!("first graph");
    let g = Graph::decode_g6("H?ABFJy");
    g.print();
    println!("second graph");
    let g: Graph = Graph::decode_g6("qGg?Yc?????_?C@CES?tP?KQGCOGA????O?OAO@?@???@?Xaq@?C?EH??S??@?COAQ??A?GWa_?A_???A@B?OCw?B?AAGBCHQO?W?pTG???Os??_S?K?E?|?@?QC?G?AG?C?u@o@??Q@@CCODDAGBcGCOP???OG?AC?OK?A??W?QBda?O_AS@IO???@gGBA@D?G?AC?GG?E@??");
    g.print();
}
