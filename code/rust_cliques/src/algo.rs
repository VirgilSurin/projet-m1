use rand::seq::SliceRandom;
use rand::thread_rng;
use std::collections::HashSet;
use std::time::{Instant, Duration};
use crate::utils::Graph;

pub fn cliques(subg: &mut HashSet<u32>, cand: &mut HashSet<u32>, q: &mut Vec<u32>, g: &Graph, result: &mut Vec<String>, delay: &mut Vec<Duration>) {
    if subg.is_empty() {
        let clique_str = q.iter().map(|&x| x.to_string()).collect::<Vec<String>>().join(" ");
        result.push(clique_str.clone());

        let now = Instant::now();
        delay.push(now.elapsed());

        // println!("{}", clique_str);
        // println!("clique");
    } else {
        let u = *subg.iter().max_by_key(|&&u| g.adj[&u].iter().filter(|&&neighbor| cand.contains(&neighbor)).count()).unwrap();
        let u_neighbors: HashSet<_> = g.adj[&u].iter().cloned().collect();

        for p in cand.difference(&u_neighbors).cloned().collect::<Vec<u32>>() {
            let p_neighbors: HashSet<_> = g.adj[&p].iter().cloned().collect();
            q.push(p);

            let subg_p: HashSet<u32> = subg.intersection(&p_neighbors).cloned().collect();
            let cand_p: HashSet<u32> = cand.intersection(&p_neighbors).cloned().collect();

            cliques(&mut subg_p.clone(), &mut cand_p.clone(), q, g, result, delay);

            q.pop();
            cand.remove(&p);
        }
    }
}

pub fn bk(subg: &mut HashSet<u32>, cand: &mut HashSet<u32>, q: &mut Vec<u32>, g: &Graph, result: &mut Vec<String>, delay: &mut Vec<Duration>) {
    if subg.is_empty() {
        let clique_str = q.iter().map(|&x| x.to_string()).collect::<Vec<String>>().join(" ");
        result.push(clique_str.clone());

        let now = Instant::now();
        delay.push(now.elapsed());

        // println!("{}", clique_str);
        // println!("clique");
    } else {
        for p in cand.clone().iter() {
            let p_neighbors: HashSet<_> = g.adj[&p].iter().cloned().collect();
            q.push(*p);

            let subg_p: HashSet<u32> = subg.intersection(&p_neighbors).cloned().collect();
            let cand_p: HashSet<u32> = cand.intersection(&p_neighbors).cloned().collect();

            cliques(&mut subg_p.clone(), &mut cand_p.clone(), q, g, result, delay);

            q.pop();
            cand.remove(&p);
        }
    }
}

pub fn bk_r(subg: &mut HashSet<u32>, cand: &mut HashSet<u32>, q: &mut Vec<u32>, g: &Graph, result: &mut Vec<String>, delay: &mut Vec<Duration>) {
    if subg.is_empty() {
        let clique_str = q.iter().map(|&x| x.to_string()).collect::<Vec<String>>().join(" ");
        result.push(clique_str.clone());

        let now = Instant::now();
        delay.push(now.elapsed());

        // println!("{}", clique_str);
        // println!("clique");
    } else {
        let mut rng = thread_rng();
        let subg_vec: Vec<&u32> = subg.iter().collect();
        let u = subg_vec.choose(&mut rng).unwrap();
        let u_neighbors: HashSet<_> = g.adj[&u].iter().cloned().collect();

        for p in cand.difference(&u_neighbors).cloned().collect::<Vec<u32>>() {
            let p_neighbors: HashSet<_> = g.adj[&p].iter().cloned().collect();
            q.push(p);

            let subg_p: HashSet<u32> = subg.intersection(&p_neighbors).cloned().collect();
            let cand_p: HashSet<u32> = cand.intersection(&p_neighbors).cloned().collect();

            cliques(&mut subg_p.clone(), &mut cand_p.clone(), q, g, result, delay);

            q.pop();
            cand.remove(&p);
        }
    }
}
pub fn bk_m(subg: &mut HashSet<u32>, cand: &mut HashSet<u32>, q: &mut Vec<u32>, g: &Graph, result: &mut Vec<String>, delay: &mut Vec<Duration>) {
    if subg.is_empty() {
        let clique_str = q.iter().map(|&x| x.to_string()).collect::<Vec<String>>().join(" ");
        result.push(clique_str.clone());

        let now = Instant::now();
        delay.push(now.elapsed());

        // println!("{}", clique_str);
        // println!("clique");
    } else {
        let u = *subg.iter().max_by_key(|&&u| g.adj[&u].len()).unwrap();
        let u_neighbors: HashSet<_> = g.adj[&u].iter().cloned().collect();

        for p in cand.difference(&u_neighbors).cloned().collect::<Vec<u32>>() {
            let p_neighbors: HashSet<_> = g.adj[&p].iter().cloned().collect();
            q.push(p);

            let subg_p: HashSet<u32> = subg.intersection(&p_neighbors).cloned().collect();
            let cand_p: HashSet<u32> = cand.intersection(&p_neighbors).cloned().collect();

            cliques(&mut subg_p.clone(), &mut cand_p.clone(), q, g, result, delay);

            q.pop();
            cand.remove(&p);
        }
    }
}
