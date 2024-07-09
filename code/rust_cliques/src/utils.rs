use std::vec::Vec;
use std::collections::HashMap;

pub struct Graph {
    order: u32,
    adj: HashMap<u32, Vec<u32>>
}

impl Graph {

    pub fn new(order: u32) -> Self {
        Graph {
            order,
            adj: HashMap::new(),
        }
    }

    pub fn add_edge(&mut self, u: u32, v: u32) {
        if self.adj.contains_key(&u) {
            if let Some(vec) = self.adj.get_mut(&u) {
                if !vec.contains(&v) {
                    vec.push(v);
                }
            };
        } else {
            self.adj.insert(u, vec![v]);
        };
        if self.adj.contains_key(&v) {
            if let Some(vec) = self.adj.get_mut(&v) {
                if !vec.contains(&u) {
                    vec.push(u);
                }
            };
        } else {
            self.adj.insert(v, vec![u]);
        };
    }

    pub fn add_nodes(&mut self, nodes: Vec<u32>) {
        self.order += nodes.len() as u32;
        for n in nodes {
            self.adj.insert(n, Vec::new());
        }
    }

    pub fn to_string(&self) -> String {
        let mut s = String::new();
        for (k, v) in self.adj.iter() {
            let mut v_str = String::new();
            for val in v {
                v_str.push_str(&val.to_string());
                v_str.push(' ');
            }
            s.push_str(&format!("{} : {}\n", k, v_str.trim()));
        }
        s
    }
}
