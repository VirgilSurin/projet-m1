mod utils;
mod algo;
use std::io::{self};
use std::collections::HashSet;
use std::time::Instant;
use utils::Graph;
use algo::{bk, bk_m, bk_r, cliques};

fn main() {
    println!("Please enter the graph in g6 format:");
    let mut g6 = String::new();
    io::stdin().read_line(&mut g6).expect("Failed to read line");
    let g6 = g6.trim();

    // HhCOhn_
    let graph = match Graph::from_g6(g6) {
        Ok(graph) => graph,
        Err(err) => {
            println!("Error parsing graph: {:?}", err);
            return;
        }
    };
    println!("{}\n", graph.to_string());

    println!("Please choose the algorithm to use:");
    println!("1 for BK");
    println!("2 for BKP_M");
    println!("3 for BKP_R");
    println!("4 for CLIQUES");

    println!("Enter your choice :");
    let mut algo_choice = String::new();
    io::stdin().read_line(&mut algo_choice).expect("Failed to read line");
    let algo_choice: u32 = algo_choice.trim().parse().expect("Please enter a valid number");

    let mut subg: HashSet<u32> = graph.adj.keys().cloned().collect();
    let mut cand: HashSet<u32> = graph.adj.keys().cloned().collect();
    let mut q: Vec<u32> = Vec::new();
    let mut result: Vec<String> = Vec::new();
    let mut delay: Vec<std::time::Duration> = Vec::new();
    let now = Instant::now();

    match algo_choice {
        1 => bk(&mut subg, &mut cand, &mut q, &graph, &mut result, &mut delay, &now),
        2 => bk_m(&mut subg, &mut cand, &mut q, &graph, &mut result, &mut delay, &now),
        3 => bk_r(&mut subg, &mut cand, &mut q, &graph, &mut result, &mut delay, &now),
        4 => cliques(&mut subg, &mut cand, &mut q, &graph, &mut result, &mut delay, &now),
        _ => {
            println!("Invalid choice. Please choose a number between 1 and 4.");
            return;
        }
    }

    let duration = now.elapsed();
    let mean_delay = delay.iter().sum::<std::time::Duration>() / delay.len() as u32;

   println!("\nResult of the algorithm:");
    for clique in result {
        println!("{{{}}}", clique);
    }
    println!("Mean delay: {:?}", mean_delay);
    println!("Total execution time: {:?}", duration);
}
