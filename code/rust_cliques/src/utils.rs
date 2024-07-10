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

    fn data_to_n(mut data: Vec<u8>) -> Result<(usize, Vec<u8>), String> {
        if data.is_empty() {
            return Err("Data is empty".into());
        }
        if data[0] <= 62 {
            let value = data[0] as usize;
            data.remove(0);
            Ok((value, data))
        } else if data.get(1).map_or(false, |&d| d <= 62) {
            if data.len() < 4 {
                return Err("Data is too short for 4-unit value".into());
            }
            let value = ((data[1] as usize) << 12) + ((data[2] as usize) << 6) + data[3] as usize;
            data.drain(0..4);
            Ok((value, data))
        } else {
            if data.len() < 8 {
                return Err("Data is too short for 8-unit value".into());
            }
            let value = ((data[2] as usize) << 30)
                + ((data[3] as usize) << 24)
                + ((data[4] as usize) << 18)
                + ((data[5] as usize) << 12)
                + ((data[6] as usize) << 6)
                + data[7] as usize;
            data.drain(0..8);
            Ok((value, data))
        }
    }

    pub fn from_g6(&self, g6: &str) -> Result<bool, GraphError> {
        let mut bytes: &[u8] = g6.as_bytes();
        if bytes.starts_with(">>graph6<<".as_bytes()) {
            bytes = &bytes[..10];
        };
        let mut data: Vec<u8> = vec![];
        for c in bytes.iter() {
            let d: u8 = c - 0b111111;
            if d > 63 {
                Err(GraphError::InvalidG6Character);
            } else {
                data.push(d);
            };
        };
    }


}
