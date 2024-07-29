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

def get_values(typ, directory):
    """
    Retourne les valeurs moyennes pour exécuter tous les algorithmes sur les graphes d'ordres donnés.
    """
    fns = ["CLIQUES", "BKP_R", "BKP_M", "BK"]
    pattern = re.compile(rf'^{typ}_res_({"|".join(fns)})_(\d+)\.out$')
    dirs = os.listdir(directory)
    dirs.sort()
    for filename in dirs:
        if pattern.match(filename):
            data = read_data(os.path.join(directory, filename))
            mean_value = calculate_mean(data)
            print(f"{filename:<26} = {mean_value:<16}")

def process_and_plot(typ, directory):
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

                # Read data from file
                data = read_data(os.path.join(directory, filename))

                # Calculate mean
                mean_value = calculate_mean(data)

                # Store mean value for function and order
                function_data[fn][order] = mean_value

                # Add order to set of orders
                orders.add(order)

        # Convert orders set to sorted list
        orders = sorted(list(orders))

    plt.figure()
    # Plotting
    print(function_data)
    for fn, data in function_data.items():
        plt.plot(orders, [data.get(order, 0) for order in orders], label=fn)

    plt.xlabel('Ordre')
    plt.ylabel("Temps d'exécution moyen (secondes)")
    plt.legend()
    plt.savefig(f'./out_fig/{typ}_plot.png')


def process_and_plot_special(typ, directory, g=None):
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

                # Read data from file
                data = read_data(os.path.join(directory, filename))

                # Calculate mean
                mean_value = calculate_mean(data)

                # Store mean value for function and order
                function_data[fn][order] = mean_value

                # Add order to set of orders
                orders.add(order)

        # Convert orders set to sorted list
        orders = sorted(list(orders))

    plt.figure()
    # Plotting
    for fn, data in function_data.items():
        plt.plot(orders, [data.get(order, 0) for order in orders], label=fn)

    plt.xlabel('Ordre')
    plt.ylabel("Temps d'exécution moyen (secondes)")
    plt.legend()
    plt.savefig(f'./out_fig/{typ}_pivot_{g}_plot.png')

def process_and_plot_pyrust_special(typ, directory, g):
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

                # Read data from file
                data = read_data(os.path.join(directory, filename))

                # Calculate mean
                mean_value = calculate_mean(data)

                # Store mean value for function and order
                function_data[fn][order] = mean_value

                # Add order to set of orders
                orders.add(order)
            elif filename.startswith(f'{typ}_rust_res_{fn}_{g}') and filename.endswith('.out'):
                parts = filename.split('_')
                order = int(parts[-1].split('.')[0])

                # Read data from file
                data = read_data(os.path.join(directory, filename))

                # Calculate mean
                mean_value = calculate_mean(data)

                # Store mean value for function and order
                rust_data[fn][order] = mean_value

        # Convert orders set to sorted list
        orders = sorted(list(orders))

    # Plotting
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

def process_and_plot_pyrust(typ, directory):
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

                # Read data from file
                data = read_data(os.path.join(directory, filename))

                # Calculate mean
                mean_value = calculate_mean(data)

                # Store mean value for function and order
                function_data[fn][order] = mean_value

                # Add order to set of orders
                orders.add(order)
            elif rust_pattern.match(filename):
                parts = filename.split('_')
                order = int(parts[-1].split('.')[0])

                # Read data from file
                data = read_data(os.path.join(directory, filename))

                # Calculate mean
                mean_value = calculate_mean(data)

                # Store mean value for function and order
                rust_data[fn][order] = mean_value

        # Convert orders set to sorted list
        orders = sorted(list(orders))

    # Plotting
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

process_and_plot_pyrust('total', './out/')
process_and_plot_pyrust('delay', './out/')
