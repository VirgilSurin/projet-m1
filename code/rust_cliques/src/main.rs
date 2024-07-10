use std::vec::Vec;
use utils::Graph;
mod utils;

fn main() {
    let mut vec: Vec<u32> = Vec::new();
    vec.push(1);
    vec.push(2);
    vec.push(3);
    let mut g: Graph = Graph::new(0);
    g.add_nodes(vec);
    g.add_edge(1, 2);
    g.add_edge(1, 3);
    g.add_edge(2, 3);
    println!("{}", g.to_string());
}
