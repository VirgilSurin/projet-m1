mod benchmark;
mod algo;
mod utils;
use std::env;
use std::vec::Vec;
use std::collections::HashSet;
use utils::Graph;
use algo::*;
use benchmark::*;

fn main() {
    env::set_var("RUST_BACKTRACE", "1");
    // total_time_main();
    // total_time_special();
    delay_special();
}

fn test(f: AlgoFn, g: &mut Graph) {
    let mut res = Vec::new();
    let mut delay = Vec::new();

    let subg: HashSet<u32> = g.adj.keys().cloned().collect();
    let cand: HashSet<u32> = g.adj.keys().cloned().collect();
    let mut q = Vec::new();

    f(&mut subg.clone(), &mut cand.clone(), &mut q, &g, &mut res, &mut delay);
    println!("{:?}", res);
}
fn simple_test() {
    let mut g: Graph = Graph::new(9);
    g.add_edge(1, 2);
    g.add_edge(1, 9);
    g.add_edge(9, 2);
    g.add_edge(9, 3);
    g.add_edge(3, 2);
    g.add_edge(3, 8);
    g.add_edge(3, 4);
    g.add_edge(8, 4);
    g.add_edge(4, 5);
    g.add_edge(4, 7);
    g.add_edge(4, 6);
    g.add_edge(8, 7);
    g.add_edge(8, 6);
    g.add_edge(6, 7);

    test(cliques, &mut g);
    test(bk, &mut g);
    test(bk_m, &mut g);
    test(bk_r, &mut g);
}
