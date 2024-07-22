use std::collections::HashSet;
use std::fs::File;
use std::io::{BufRead, BufReader, Write};
use std::path::Path;
use std::time::{Instant, Duration};
use indicatif::ProgressIterator;

use crate::algo::*;
use crate::utils::Graph;

pub type AlgoFn = fn(&mut HashSet<u32>, &mut HashSet<u32>, &mut Vec<u32>, &Graph, &mut Vec<String>, &mut Vec<Duration>);

fn bench_total_time(order: u32, algo: AlgoFn) {
    let str_in: String = format!("../samples/graph{}.g6", order);
    let str_out: String = format!("../out/total_rust_res_{}_{}.out", get_algorithm_name(algo), order);
    let input_path = Path::new(&str_in);
    let output_path = Path::new(&str_out);

    let input = File::open(input_path);
    let mut output = File::create(output_path).expect("Unable to create output file");
    let reader = BufReader::new(input.unwrap());

    for line in reader.lines().collect::<Vec<_>>().into_iter().progress() {
        let g6 = line.unwrap();
        let G: Graph = Graph::from_g6(&g6).expect("Unable to decode g6");
        let mut subg: HashSet<u32> = G.adj.keys().cloned().collect();
        let mut cand: HashSet<u32> = G.adj.keys().cloned().collect();
        let mut q = Vec::new();
        let mut res = Vec::new();
        let now = Instant::now();
        let mut delay = vec![now.elapsed()];

        let start = Instant::now();
        algo(&mut subg, &mut cand, &mut q, &G, &mut res, &mut delay);
        let duration = start.elapsed();

        writeln!(output, "{:.6}", duration.as_secs_f64()).expect("Unable to write to output file");
    }
}

fn bench_total_time_special(order: u32, algo: AlgoFn, graph_type: &str) {
    let str_in: String = format!("../samples/graphs/{}_{}.g6", graph_type, order);
    let str_out: String = format!("../out/specials/total_rust_res_{}_{}_{}.out", get_algorithm_name(algo), graph_type, order);
    let input_path = Path::new(&str_in);
    let output_path = Path::new(&str_out);

    let input = File::open(input_path);
    let mut output = File::create(output_path).expect("Unable to create output file");
    let reader = BufReader::new(input.unwrap());

    for line in reader.lines().collect::<Vec<_>>().into_iter().progress() {
        let g6 = line.unwrap();
        let G: Graph = Graph::from_g6(&g6).expect("Unable to decode g6");
        let mut subg: HashSet<u32> = G.adj.keys().cloned().collect();
        let mut cand: HashSet<u32> = G.adj.keys().cloned().collect();
        let mut q = Vec::new();
        let mut res = Vec::new();
        let now = Instant::now();
        let mut delay = vec![now.elapsed()];

        let start = Instant::now();
        algo(&mut subg, &mut cand, &mut q, &G, &mut res, &mut delay);
        let duration = start.elapsed();

        writeln!(output, "{:.6}", duration.as_secs_f64()).expect("Unable to write to output file");
    }
}

fn clique_delay(order: u32, algo: AlgoFn) {
    let str_in: String = format!("../samples/graph{}.g6", order);
    let str_out: String = format!("../out/delay_rust_res_{}_{}.out", get_algorithm_name(algo), order);
    let input_path = Path::new(&str_in);
    let output_path = Path::new(&str_out);

    let input = File::open(input_path).expect("Unable to open input file");
    let mut output = File::create(output_path).expect("Unable to create output file");
    let reader = BufReader::new(input);

    // for line in reader.lines().progress() {
    for line in reader.lines().collect::<Vec<_>>().into_iter().progress() {
        let g6 = line.unwrap();
        let G: Graph = Graph::from_g6(&g6).expect("Unable to decode g6");
        let mut subg: HashSet<u32> = G.adj.keys().cloned().collect();
        let mut cand: HashSet<u32> = G.adj.keys().cloned().collect();
        let mut q = Vec::new();
        let mut res = Vec::new();
        let now = Instant::now();
        let mut delay = vec![now.elapsed()];

        algo(&mut subg, &mut cand, &mut q, &G, &mut res, &mut delay);

        for i in 0..(delay.len() - 1) {
            // println!("{} - {}", delay[i+1].as_secs_f64(), delay[1].as_secs_f64());
            let time_taken = delay[i + 1].saturating_sub(delay[i]);
            writeln!(output, "{:.6}", time_taken.as_secs_f64()).expect("Unable to write to output file");
        }
    }
}

fn clique_delay_special(order: u32, algo: AlgoFn, graph_type: &str) {
    let str_in: String = format!("../samples/graphs/{}_{}.g6", graph_type, order);
    let str_out: String = format!("../out/specials/delay_rust_res_{}_{}_{}.out", get_algorithm_name(algo), graph_type, order);
    let input_path = Path::new(&str_in);
    let output_path = Path::new(&str_out);

    let input = File::open(input_path).expect("Unable to open input file");
    let mut output = File::create(output_path).expect("Unable to create output file");
    let reader = BufReader::new(input);

    // for line in reader.lines().progress() {
    for line in reader.lines().collect::<Vec<_>>().into_iter().progress() {
        let g6 = line.unwrap();
        let G: Graph = Graph::from_g6(&g6).expect("Unable to decode g6");
        let mut subg: HashSet<u32> = G.adj.keys().cloned().collect();
        let mut cand: HashSet<u32> = G.adj.keys().cloned().collect();
        let mut q = Vec::new();
        let mut res = Vec::new();
        let now = Instant::now();
        let mut delay = vec![now.elapsed()];

        algo(&mut subg, &mut cand, &mut q, &G, &mut res, &mut delay);

        for i in 0..(delay.len() - 1) {
            let time_taken = delay[i + 1].saturating_sub(delay[i]);
            writeln!(output, "{:.6}", time_taken.as_secs_f64()).expect("Unable to write to output file");
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

pub fn total_time_main() {
    println!("BENCHMARK\n=========\n\n");
    for order in 4..=10 {
        bench_total_time(order, cliques);
    }

    println!("=========\n\n");
    for order in 4..=10 {
        bench_total_time(order, bk);
    }

    println!("=========\n\n");
    for order in 4..=10 {
        bench_total_time(order, bk_m);
    }

    println!("=========\n\n");
    for order in 4..=10 {
        bench_total_time(order, bk_r);
    }
}

pub fn total_time_special() {
    println!("BENCHMARK\n=========\n\n");
    for graph_type in ["complete", "turan", "empty"] {
        for order in 3..45 {
        bench_total_time_special(order, cliques, graph_type);
        bench_total_time_special(order, bk_m, graph_type);
        bench_total_time_special(order, bk_r, graph_type);
        }
    }
}

pub fn delay_main() {
    println!("BENCHMARK\n=========\n\n");
    for order in 4..=10 {
        clique_delay(order, cliques);
    }

    println!("=========\n\n");
    for order in 4..=10 {
        clique_delay(order, bk);
    }

    println!("=========\n\n");
    for order in 4..=10 {
        clique_delay(order, bk_m);
    }

    println!("=========\n\n");
    for order in 4..=10 {
        clique_delay(order, bk_r);
    }
}

pub fn delay_special() {
    println!("BENCHMARK\n=========\n\n");
    for graph_type in ["complete", "turan", "empty"] {
        for order in 3..45 {
        clique_delay_special(order, cliques, graph_type);
        clique_delay_special(order, bk_m, graph_type);
        clique_delay_special(order, bk_r, graph_type);
        }
    }
}
