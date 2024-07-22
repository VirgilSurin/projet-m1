use bitvec::prelude::*;
use std::vec::Vec;
use std::collections::HashMap;

#[derive(Debug)]
pub enum GraphError {
    InvalidG6Character,
    InvalidG6Size,
}

pub struct Graph {
    order: u32,
    pub adj: HashMap<u32, Vec<u32>>
}

#[allow(dead_code)]
impl Graph {

    pub fn new(order: u32) -> Self {
        Graph {
            order,
            adj: HashMap::with_capacity(order as usize),
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
            self.order += 1;
        };
        if self.adj.contains_key(&v) {
            if let Some(vec) = self.adj.get_mut(&v) {
                if !vec.contains(&u) {
                    vec.push(u);
                }
            };
        } else {
            self.adj.insert(v, vec![u]);
            self.order += 1;
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

    fn encode_n(&self, n: u32) -> String {
        if n <= 62 {
            (n + 63).to_string()
        } else if n <= 258_047 {
            format!("{}{}", char::from(126), self.encode_big_endian(n, 4))
        } else {
            format!("{}{}{}", char::from(126), char::from(126), self.encode_big_endian(n, 8))
        }
    }

    fn encode_big_endian(&self, num: u32, bytes_num: usize) -> String {
        let mut num = num;
        let mut num_bytes = Vec::new();

        for _ in 0..bytes_num {
            let byte = (63 + ((num >> ((bytes_num - 1) * 6)) & 63)) as u8;
            num_bytes.push(char::from(byte));
            num <<= 6;
        }

        num_bytes.into_iter().collect()
    }

    pub fn to_g6(&self) -> Option<String> {
        let mut bit_vec: BitVec = bitvec!();
        if self.order <= 0 {
            return None
        }
        for u in 0..self.order {
            for v in 0..u {
                if let Some(adj_list) = self.adj.get(&u) {
                    if adj_list.contains(&v) {
                        bit_vec.push(true);
                    } else {
                        bit_vec.push(false);
                    }
                }
            }
        }
        while bit_vec.len() % 6 != 0 {
            bit_vec.push(false);
        }
        // Split into groups of 6 bits
        let six_bit_groups: Vec<String> = (0..bit_vec.len())
            .step_by(6)
            .map(|i| {
                (0..6)
                    .map(|j| {
                        if i + j < bit_vec.len() && bit_vec[i + j] {
                            '1'
                        } else {
                            '0'
                        }
                    })
                    .collect()
            }).collect();

        // Convert each group to its decimal representation and then to a character
        let decimal_values: Vec<char> = six_bit_groups
            .iter()
            .map(|group| {
                let decimal_value = u8::from_str_radix(&group, 2).unwrap();
                (decimal_value + 63) as char
            }).collect();

        let mut graph6 = vec![self.encode_n(self.order)];
        graph6.extend(decimal_values.into_iter().map(|c| c.to_string()));
        Some(graph6.join(""))
    }

    fn data_to_n(mut data: Vec<u32>) -> Result<(u32, Vec<u32>), String> {
        if data.is_empty() {
            return Err("Data is empty".into());
        }
        if data[0] <= 62 {
            let value = data[0];
            data.remove(0);
            Ok((value.into(), data))
        } else if data.get(1).map_or(false, |&d| d <= 62) {
            if data.len() < 4 {
                return Err("Data is too short for 4-unit value".into());
            }
            let value = (data[1] << 12) + (data[2] << 6) + data[3];
            data.drain(0..4);
            Ok((value.into(), data))
        } else {
            if data.len() < 8 {
                return Err("Data is too short for 8-unit value".into());
            }
            let value = (data[2] << 30)
                + (data[3] << 24)
                + (data[4] << 18)
                + (data[5] << 12)
                + (data[6] << 6)
                + data[7];
            data.drain(0..8);
            Ok((value.into(), data))
        }
    }

    fn bits(data: &[u32]) -> Vec<bool> {
        let mut result = Vec::new();
        for &d in data {
            for i in (0..6).rev() {
                result.push((d >> i) & 1 == 1);
            }
        }
        result
    }

    pub fn from_g6(g6: &str) -> Result<Graph, GraphError> {
        let mut bytes: &[u8] = g6.trim().as_bytes();
        if bytes.starts_with(">>graph6<<".as_bytes()) {
            bytes = &bytes[10..];
        };
        let mut data: Vec<u32> = vec![];
        for c in bytes.iter() {
            let c_u32 = *c as u32;
            if c_u32 >= 63 as u32 {
                let d = c_u32 - 63;
                if d > 63 {
                    return Err(GraphError::InvalidG6Character);
                } else {
                    data.push(d);
                };
            } else {
                panic!("Invalid character, got {}", c_u32)
            }
        };
        let (n, data) = Graph::data_to_n(data).unwrap();
        let nd = (n * (n - 1) / 2 + 5) / 6;
        if data.len() != nd as usize {
            return Err(GraphError::InvalidG6Size);
        };

        let mut graph = Graph::new(n);
        graph.add_nodes((0..n).collect());

        if data.len() as u32 != (n * (n - 1) / 2 + 5) / 6 {
            return Err(GraphError::InvalidG6Size);
        };
        let bit_iter = Graph::bits(&data);
        for i in 1..n {
            for j in 0..i {
                if bit_iter[(i * (i - 1) / 2 + j) as usize] {
                    graph.add_edge(i as u32, j as u32);
                }
            }
        }
        Ok(graph)
    }
}
