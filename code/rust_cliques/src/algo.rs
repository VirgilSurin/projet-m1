use rand::seq::SliceRandom;
use rand::thread_rng;
use std::collections::HashSet;
use std::time::{Instant, Duration};
use crate::utils::Graph;

pub fn cliques(subg: &mut HashSet<u32>, cand: &mut HashSet<u32>, q: &mut Vec<u32>, g: &Graph, result: &mut Vec<String>, delay: &mut Vec<Duration>, now: &Instant) {
    if subg.is_empty() {
        let clique_str = q.iter().map(|&x| x.to_string()).collect::<Vec<String>>().join(" ");
        result.push(clique_str);
        delay.push(now.elapsed());
    } else {
        let u = *subg.iter().max_by_key(|&&u| g.adj[&u].iter().filter(|&&neighbor| cand.contains(&neighbor)).count()).unwrap();
        let u_neighbors: HashSet<_> = g.adj[&u].iter().copied().collect();

        for p in cand.difference(&u_neighbors).copied().collect::<Vec<u32>>() {
            let p_neighbors: HashSet<_> = g.adj[&p].iter().copied().collect();
            q.push(p);

            let mut subg_p: HashSet<u32> = subg.intersection(&p_neighbors).copied().collect();
            let mut cand_p: HashSet<u32> = cand.intersection(&p_neighbors).copied().collect();

            cliques(&mut subg_p, &mut cand_p, q, g, result, delay, now);

            q.pop();
            cand.remove(&p);
        }
    }
}

pub fn bk(subg: &mut HashSet<u32>, cand: &mut HashSet<u32>, q: &mut Vec<u32>, g: &Graph, result: &mut Vec<String>, delay: &mut Vec<Duration>, now: &Instant) {
    if subg.is_empty() {
        let clique_str = q.iter().map(|&x| x.to_string()).collect::<Vec<String>>().join(" ");
        result.push(clique_str);
        delay.push(now.elapsed());
    } else {
        for p in cand.iter().copied().collect::<Vec<u32>>() {
            let p_neighbors: HashSet<u32> = g.adj[&p].iter().copied().collect();
            q.push(p);

            let mut subg_p: HashSet<u32> = subg.intersection(&p_neighbors).copied().collect();
            let mut cand_p: HashSet<u32> = cand.intersection(&p_neighbors).copied().collect();

            bk(&mut subg_p, &mut cand_p, q, g, result, delay, now);

            q.pop();
            cand.remove(&p);
        }
    }
}

pub fn bk_r(subg: &mut HashSet<u32>, cand: &mut HashSet<u32>, q: &mut Vec<u32>, g: &Graph, result: &mut Vec<String>, delay: &mut Vec<Duration>, now: &Instant) {
    if subg.is_empty() {
        let clique_str = q.iter().map(|&x| x.to_string()).collect::<Vec<String>>().join(" ");
        result.push(clique_str.clone());
        delay.push(now.elapsed());
    } else {
        let mut rng = thread_rng();
        let subg_vec: Vec<&u32> = subg.iter().collect();
        let u = subg_vec.choose(&mut rng).unwrap();
        let u_neighbors: HashSet<_> = g.adj[&u].iter().copied().collect();
    
        for p in cand.difference(&u_neighbors).copied().collect::<Vec<u32>>() {
            let p_neighbors: HashSet<_> = g.adj[&p].iter().copied().collect();
            q.push(p);

            let mut subg_p: HashSet<u32> = subg.intersection(&p_neighbors).copied().collect();
            let mut cand_p: HashSet<u32> = cand.intersection(&p_neighbors).copied().collect();

            bk_r(&mut subg_p, &mut cand_p, q, g, result, delay, now);

            q.pop();
            cand.remove(&p);
        }
    }
}
pub fn bk_m(subg: &mut HashSet<u32>, cand: &mut HashSet<u32>, q: &mut Vec<u32>, g: &Graph, result: &mut Vec<String>, delay: &mut Vec<Duration>, now: &Instant) {
    if subg.is_empty() {
        let clique_str = q.iter().map(|&x| x.to_string()).collect::<Vec<String>>().join(" ");
        result.push(clique_str.clone());
        delay.push(now.elapsed());
    } else {
        let u = *subg.iter().max_by_key(|&&u| g.adj[&u].len()).unwrap();
        let u_neighbors: HashSet<_> = g.adj[&u].iter().copied().collect();

        for p in cand.difference(&u_neighbors).copied().collect::<Vec<u32>>() {
            let p_neighbors: HashSet<_> = g.adj[&p].iter().copied().collect();
            q.push(p);

            let mut subg_p: HashSet<u32> = subg.intersection(&p_neighbors).copied().collect();
            let mut cand_p: HashSet<u32> = cand.intersection(&p_neighbors).copied().collect();

            bk_m(&mut subg_p, &mut cand_p, q, g, result, delay, now);

            q.pop();
            cand.remove(&p);
        }
    }
}
