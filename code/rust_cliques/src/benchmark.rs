mod algo;
mod utils;
use crate::algo::*;
use crate::utils::Graph;

use std::collections::HashSet;
use std::fs::File;
use std::io::{self, BufRead, BufReader, Write};
use std::path::Path;
use std::time::{Instant, Duration};
use indicatif::ProgressIterator;


pub type AlgoFn = fn(&mut HashSet<u32>, &mut HashSet<u32>, &mut Vec<u32>, &Graph, &mut Vec<String>, &mut Vec<Duration>, &Instant);

fn bench_time(order: u32, algo: AlgoFn) {
    let str_in: String = format!("../samples/graph{}.g6", order);
    let str_out: String = format!("../out/total_rust_res_{}_{}.out", get_algorithm_name(algo), order);
    let delay_out: String = format!("../out/delay_rust_res_{}_{}.out", get_algorithm_name(algo), order);
    let input_path = Path::new(&str_in);
    let output_path = Path::new(&str_out);
    let delay_path = Path::new(&delay_out);

    let input = File::open(input_path);
    let mut output = File::create(output_path).expect("Unable to create output file");
    let mut delay_output = File::create(delay_path).expect("Unable to create output file");
    let reader = BufReader::new(input.unwrap());

    for line in reader.lines().collect::<Vec<_>>().into_iter() {
        let g6 = line.unwrap();
        let g: Graph = Graph::from_g6(&g6).expect("Unable to decode g6");
        let mut subg: HashSet<u32> = g.adj.keys().cloned().collect();
        let mut cand: HashSet<u32> = g.adj.keys().cloned().collect();
        let mut q = Vec::new();
        let mut res = Vec::new();
        let now = Instant::now();
        let mut delay = vec![now.elapsed()];

        algo(&mut subg, &mut cand, &mut q, &g, &mut res, &mut delay, &now);
        let duration = now.elapsed();

        writeln!(output, "{:.6}", duration.as_secs_f64()).expect("Unable to write to output file");
        for i in 0..(delay.len() - 1) {
            let time_taken = delay[i + 1].saturating_sub(delay[i]);
            writeln!(delay_output, "{:.6}", time_taken.as_secs_f64()).expect("Unable to write to output file");
        }
    }
}

fn bench_time_special(order: u32, algo: AlgoFn, graph_type: &str) {
    let str_in: String = format!("../samples/graphs/{}_{}.g6", graph_type, order);
    let str_out: String = format!("../out/specials/total_rust_res_{}_{}_{}.out", get_algorithm_name(algo), graph_type, order);
    let delay_out: String = format!("../out/specials/delay_rust_res_{}_{}_{}.out", get_algorithm_name(algo), graph_type, order);
    let input_path = Path::new(&str_in);
    let output_path = Path::new(&str_out);
    let delay_path = Path::new(&delay_out);

    let input = File::open(input_path);
    let mut output = File::create(output_path).expect("Unable to create output file");
    let mut delay_output = File::create(delay_path).expect("Unable to create output file");
    let reader = BufReader::new(input.unwrap());

    for line in reader.lines().collect::<Vec<_>>().into_iter() {
        let g6 = line.unwrap();
        let g: Graph = Graph::from_g6(&g6).expect("Unable to decode g6");
        let mut subg: HashSet<u32> = g.adj.keys().cloned().collect();
        let mut cand: HashSet<u32> = g.adj.keys().cloned().collect();
        let mut q = Vec::new();
        let mut res = Vec::new();
        let now = Instant::now();
        let mut delay = vec![now.elapsed()];

        algo(&mut subg, &mut cand, &mut q, &g, &mut res, &mut delay, &now);
        let duration = now.elapsed();

        writeln!(output, "{:.6}", duration.as_secs_f64()).expect("Unable to write to output file");
        for i in 0..(delay.len() - 1) {
            let time_taken = delay[i + 1].saturating_sub(delay[i]);
            writeln!(delay_output, "{:.6}", time_taken.as_secs_f64()).expect("Unable to write to output file");
        }
    }
}

fn get_algorithm_name(algo: AlgoFn) -> &'static str {
    if algo as usize == cliques as usize {
        "CLIQUES"
    } else if algo as usize == bk as usize {
        "BK"
    } else if algo as usize == bk_m as usize {
        "BKP_M"
    } else if algo as usize == bk_r as usize {
        "BKP_R"
    } else {
        "UNKNOWN"
    }
}

fn bench_main(algo_choice: &str) {
    match algo_choice {
        "1" => {
            for order in (4..11).progress() {
                bench_time(order, cliques);
            };
        },
        "2" => {
            for order in (4..11).progress() {
                bench_time(order, bk);
            };
        },
        "3" => {
            for order in (4..11).progress() {
                bench_time(order, bk_m);
            };
        },
        "4" => {
            for order in (4..11).progress() {
                bench_time(order, bk_r);
            };
        },
        "5" => {
            for order in (4..11).progress() {
                bench_time(order, cliques);
                bench_time(order, bk);
                bench_time(order, bk_m);
                bench_time(order, bk_r);
            };
        },
        _ => println!("Invalid choice."),
    };
}

fn bench_special(algo_choice: &str) {
    for graph_type in ["complete", "turan", "empty"] {
        println!("{:?}", graph_type);
        match algo_choice {
            "1" => {
                for order in (3..45).progress() {
                    bench_time_special(order, cliques, graph_type);
                };
            },
            "2" => {
                for order in (3..45).progress() {
                    bench_time_special(order, bk, graph_type);
                };
            },
            "3" => {
                for order in (3..45).progress() {
                    bench_time_special(order, bk_m, graph_type);
                };
            },
            "4" => {
                for order in (3..45).progress() {
                    bench_time_special(order, bk_r, graph_type);
                };
            },
            "5" => {
                for order in (3..45).progress() {
                    bench_time_special(order, cliques, graph_type);
                    bench_time_special(order, bk, graph_type);
                    bench_time_special(order, bk_m, graph_type);
                    bench_time_special(order, bk_r, graph_type);
                };
            },
            _ => println!("Invalid choice."),
        }
    };
}

fn main() {
    println!("Choose the algorithm:");
    println!("1 - CLIQUES");
    println!("2 - Bron-Kerbosch (BK)");
    println!("3 - Bron-Kerbosch with Pivoting (BKP_M)");
    println!("4 - Randomized Bron-Kerbosch (BKP_R)");
    println!("5 - All Algorithms");

    let mut algo_choice = String::new();
    while !["1", "2", "3", "4", "5"].contains(&algo_choice.trim()) {
        print!("Enter the number corresponding to your choice: ");
        io::stdout().flush().expect("Failed to flush stdout");
        io::stdin().read_line(&mut algo_choice).expect("Failed to read line");
        algo_choice = algo_choice.trim().to_string();
    }
    println!("");
    println!("Choose the test set:");
    println!("1 - Standard (order 4-10)");
    println!("2 - Special (graph types: complete, turan, empty)");

    let mut test_set_choice = String::new();
    while !["1", "2"].contains(&test_set_choice.trim()) {
        print!("Enter the number corresponding to your choice: ");
        io::stdout().flush().expect("Failed to flush stdout");
        io::stdin().read_line(&mut test_set_choice).expect("Failed to read line");
        test_set_choice = test_set_choice.trim().to_string();
    }
    println!("");

    if test_set_choice == "1" {
        bench_main(&algo_choice);
    } else if test_set_choice == "2" {
        bench_special(&algo_choice);
    } else {
        println!("Invalid test set choice.");
    }
}
