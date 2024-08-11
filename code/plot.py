#!/usr/bin/env python3
import os
import re
import numpy as np
import matplotlib.pyplot as plt

# Function to read data from file
def read_data(file_path):
    with open(file_path, 'r') as file:
        data = [float(line.strip()) for line in file]
    return data

def calculate_mean(data):
    return np.mean(data)

def python_plot(typ, directory):
    """
    Plot les résultats des différents algo sur les graphes classiques.
    """
    fns = ["CLIQUES", "BKP_R", "BKP_M", "BK"]
    function_data = {fn: {} for fn in fns}
    orders = None
    for fn in fns:
        pattern = re.compile(rf'^{typ}_res_{fn}_(\d+)\.out$')
        orders = set()
        for filename in os.listdir(directory):
            if pattern.match(filename):
                parts = filename.split('_')
                order = int(parts[-1].split('.')[0])
                data = read_data(os.path.join(directory, filename))
                mean_value = calculate_mean(data)
                function_data[fn][order] = mean_value
                orders.add(order)

        orders = sorted(list(orders))

    plt.figure()
    for fn, data in function_data.items():
        plt.plot(orders, [data.get(order, 0) for order in orders], label=fn)

    plt.xlabel('Ordre')
    plt.ylabel("Temps d'exécution moyen (secondes)")
    plt.legend()
    plt.savefig(f'./out_fig/{typ}_plot.png')


def python_plot_special(typ, directory, g=None):
    """
    Plot les résultats des différents algo sur les graphes spéciaux.
    """
    fns = ["CLIQUES", "BKP_R", "BKP_M"]
    function_data = {fn: {} for fn in fns}
    orders = None
    for fn in fns:
        orders = set()
        for filename in os.listdir(directory):
            if filename.startswith(f'{typ}_res_{fn}_{g}') and filename.endswith('.out'):
                parts = filename.split('_')
                order = int(parts[-1].split('.')[0])
                data = read_data(os.path.join(directory, filename))
                mean_value = calculate_mean(data)
                function_data[fn][order] = mean_value
                orders.add(order)

        orders = sorted(list(orders))

    plt.figure()
    for fn, data in function_data.items():
        plt.plot(orders, [data.get(order, 0) for order in orders], label=fn)

    plt.xlabel('Ordre')
    plt.ylabel("Temps d'exécution moyen (secondes)")
    plt.legend()
    plt.savefig(f'./out_fig/{typ}_pivot_{g}_plot.png')

def plot_py_rust(typ, directory):
    """
    Compare algo par algo les résultats entre Rust et Python pour les graphes
    """
    fns = ["CLIQUES", "BKP_R", "BKP_M", "BK"]
    function_data = {fn: {} for fn in fns}
    rust_data = {fn: {} for fn in fns}
    orders = None
    for fn in fns:
        orders = set()
        pattern = re.compile(rf'^{typ}_res_({fn})_(\d+)\.out$')
        rust_pattern = re.compile(rf'^{typ}_rust_res_({fn})_(\d+)\.out$')
        for filename in os.listdir(directory):
            if pattern.match(filename):
                parts = filename.split('_')
                order = int(parts[-1].split('.')[0])
                data = read_data(os.path.join(directory, filename))
                mean_value = calculate_mean(data)
                function_data[fn][order] = mean_value
                orders.add(order)
            elif rust_pattern.match(filename):
                parts = filename.split('_')
                order = int(parts[-1].split('.')[0])
                data = read_data(os.path.join(directory, filename))
                mean_value = calculate_mean(data)
                rust_data[fn][order] = mean_value

        orders = sorted(list(orders))

    for fn, data in function_data.items():
        plt.figure()
        python_data = function_data[fn]
        rust_data_fn = rust_data[fn]
        plt.plot(orders, [python_data.get(order, 0) for order in orders], label=f'{fn} - Python')
        plt.plot(orders, [rust_data_fn.get(order, 0) for order in orders], label=f'{fn} - Rust')
        plt.xlabel('Ordre')
        plt.ylabel("Temps d'exécution moyen (secondes)")
        plt.legend()
        plt.savefig(f'./out_fig/{typ}_pyrust_{fn}_plot.png')
        plt.close()

def plot_py_rust_special(typ, directory, g):
    """
    Compare algo par algo les résultats entre Rust et Python pour les graphes spéciaux
    """
    fns = ["CLIQUES", "BKP_R", "BKP_M"]
    function_data = {fn: {} for fn in fns}
    rust_data = {fn: {} for fn in fns}
    orders = None
    for fn in fns:
        orders = set()
        for filename in os.listdir(directory):
            if filename.startswith(f'{typ}_res_{fn}_{g}') and filename.endswith('.out'):
                parts = filename.split('_')
                order = int(parts[-1].split('.')[0])
                data = read_data(os.path.join(directory, filename))
                mean_value = calculate_mean(data)
                function_data[fn][order] = mean_value
                orders.add(order)
            elif filename.startswith(f'{typ}_rust_res_{fn}_{g}') and filename.endswith('.out'):
                parts = filename.split('_')
                order = int(parts[-1].split('.')[0])
                data = read_data(os.path.join(directory, filename))
                mean_value = calculate_mean(data)
                rust_data[fn][order] = mean_value

        orders = sorted(list(orders))

    for fn in fns:
        plt.figure()
        python_data = function_data[fn]
        rust_data_fn = rust_data[fn]

        plt.plot(orders, [python_data.get(order, 0) for order in orders], label=f'{fn} - Python')
        plt.plot(orders, [rust_data_fn.get(order, 0) for order in orders], label=f'{fn} - Rust')

        plt.xlabel('Ordre')
        plt.ylabel("Temps d'exécution moyen (secondes)")
        plt.legend()
        plt.savefig(f'./out_fig/{typ}_{fn}_pyrust_pivot_{g}_plot.png')
        plt.close()

def main():
    print("Please choose the type of plots to generate:")
    print("1 - Standard plot from Python benchmark (order 4-10)")
    print("2 - Special plot from Python benchmark (graph types: complete, moon-moser, empty)")
    print("3 - Standard plot comparing Python vs Rust benchmark (order 4-10)")
    print("4 - Special plot comparing Python vs Rust benchmark (graph types: complete, moon-moser, empty)")
    print("5 - All the above")
    plot_choice = ""
    while plot_choice not in ["1", "2", "3", "4", "5"]:
        plot_choice = input("Enter the number corresponding to you choice: ").strip()
    print("Generating plots...")
    if plot_choice == "1":
        python_plot("total", "./out/")
        python_plot("delay", "./out/")
    elif plot_choice == "2":
        python_plot_special("total", "./out/specials/", "complete")
        python_plot_special("delay", "./out/specials/", "complete")
        python_plot_special("total", "./out/specials/", "empty")
        python_plot_special("delay", "./out/specials/", "empty")
        python_plot_special("total", "./out/specials/", "turan")
        python_plot_special("delay", "./out/specials/", "turan")
    elif plot_choice == "3":
        plot_py_rust("total", "./out/")
        plot_py_rust("delay", "./out/")
    elif plot_choice == "4":
        plot_py_rust_special("total", "./out/specials/", "complete")
        plot_py_rust_special("delay", "./out/specials/", "complete")
        plot_py_rust_special("total", "./out/specials/", "empty")
        plot_py_rust_special("delay", "./out/specials/", "empty")
        plot_py_rust_special("total", "./out/specials/", "turan")
        plot_py_rust_special("delay", "./out/specials/", "turan")
    elif plot_choice == "5":
        python_plot("total", "./out/")
        python_plot("delay", "./out/")
        python_plot_special("total", "./out/specials/", "complete")
        python_plot_special("delay", "./out/specials/", "complete")
        python_plot_special("total", "./out/specials/", "empty")
        python_plot_special("delay", "./out/specials/", "empty")
        python_plot_special("total", "./out/specials/", "turan")
        python_plot_special("delay", "./out/specials/", "turan")
        plot_py_rust("total", "./out/")
        plot_py_rust("delay", "./out/")
        plot_py_rust_special("total", "./out/specials/", "complete")
        plot_py_rust_special("delay", "./out/specials/", "complete")
        plot_py_rust_special("total", "./out/specials/", "empty")
        plot_py_rust_special("delay", "./out/specials/", "empty")
        plot_py_rust_special("total", "./out/specials/", "turan")
        plot_py_rust_special("delay", "./out/specials/", "turan")
    else:
        print("Invalid test choice.")

if __name__ == "__main__":
    main()
