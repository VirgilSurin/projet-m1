use std::{io, vec::Vec};
use utils::Graph;
mod utils;

fn main() {
    println!("Graph at g6 format :", );
    let mut g6 = String::new();
    io::stdin().read_line(&mut g6).expect("Failed to read");
    let g: Graph = Graph::from_g6(g6.as_str()).unwrap();
    println!("Result :\n{}", g.to_string());
}
