#!/usr/bin/env python3

import os
import csv
from tqdm import tqdm
from utils import Graph

path = "./samples/"
fin = [# "email-Enron.txt",
       "email-EuAll.txt"]
fout = [# "email-Enron",
        "email-EuAll"]
# n
# m
# n_i -> n_i'
# ...

# parsing email-*.txt
# for filename in tqdm(fin):
#     with open(path+filename) as f:
#         n = int(f.readline())
#         m = int(f.readline())
#         G = Graph(n)
#         G.add_nodes(range(n))
#         i = 0
#         lines = f.readlines()
#     print(filename)
#     for i in tqdm(range(len(lines))):
#         edge = lines[i].strip().split(	)
#         G.add_edge(int(edge[0]), int(edge[1]))
#     G.save_to_g6(path+filename[:-4])
# parsing deezer_clean_data

def parse_csv(file_path, filename):
    """
    Parse the CSV file at the given file_path.
    """
    with open(file_path, 'r') as csv_file:
        print(filename)
        reader = csv.reader(csv_file)
        header = next(reader)  # Read the header
        G = Graph()
        order = 0
        for row in tqdm(reader):
            G.add_edge(int(row[0]), int(row[1]))
            order += 1
        G.order = order
    for i in range(order):
        if i not in G.adj:
            G.adj[i] = set()
    G.save_to_g6(path+filename[:-4])

def traverse_directory(directory):
    """
    Recursively traverse the directory and parse CSV files.
    """
    for root, dirs, files in os.walk(directory):
        for f in files:
            if f.endswith(".csv"):
                file_path = os.path.join(root, f)
                print(f"Parsing CSV f: {file_path}")
                parse_csv(file_path, f[:-4])

traverse_directory(path)
