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

def process_and_plot_tabular(typ, directory):
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

    # Calcul des différences en pourcentage et génération du tableau LaTeX
    latex_table = "\\begin{tabular}{|l||l|l|l|l|}\n"
    latex_table += "  \\hline\n"
    latex_table += "  Ordre & BK & BKP\\_R & BKP\\_M & CLIQUES \\\\\n"
    latex_table += "  \\hline\n"
    latex_table += "  \\hline\n"
    orders = [4,5,6,7,8,9,10]
    for order in orders:
        latex_table += f"  {order} "
        for fn in fns:
            python_mean = function_data[fn].get(order, 0)
            rust_mean = rust_data[fn].get(order, 0)
            if python_mean == 0:  # Avoid division by zero
                difference = 0
            else:
                difference = ((rust_mean - python_mean) / python_mean) * 100
            arrow = "\\uparrow" if difference > 0 else "\\downarrow"
            latex_table += f"& ${arrow}{difference:.1f}^{{\\%}}$ "
        latex_table += "\\\\\n"

    latex_table += "  \\hline\n"
    latex_table += "\\end{tabular}"
    return latex_table



def process_and_plot_tabular_special(typ, directory):
    """
    Génère un tableau LaTeX avec les résultats d'exécution pour les graphes spéciaux (Empty, Turan, Complete).
    """
    fns = ["CLIQUES", "BKP_R", "BKP_M"]
    graph_types = ["empty", "turan", "complete"]
    function_data = {fn: {g: {} for g in graph_types} for fn in fns}

    orders = set()

    for fn in fns:
        for g in graph_types:
            for filename in os.listdir(directory):
                if filename.startswith(f'{typ}_res_{fn}_{g}') and filename.endswith('.out'):
                    parts = filename.split('_')
                    order = int(parts[-1].split('.')[0])

                    # Read data from file
                    data = read_data(os.path.join(directory, filename))

                    # Calculate mean
                    mean_value = calculate_mean(data)

                    # Store mean value for function and order
                    function_data[fn][g][order] = mean_value

                    # Add order to set of orders
                    orders.add(order)

    # Convert orders set to sorted list
    orders = sorted(list(orders))

    # Génération du tableau LaTeX
    latex_table = "\\begin{longtable}{|l||l|l|l|l|}\n"
    latex_table += "  \\hline\n"
    latex_table += "  Ordre & Graphe & CLIQUES & BKP\\_R & BKP\\_M \\\\endhead\\\n"
    latex_table += "  \\hline\n"
    latex_table += "  \\hline\n"

    orders = list(range(5, 45))
    for order in orders:
        first_row = True
        for g in graph_types:
            if first_row:
                latex_table += f"  {order} & {g.capitalize()} "
                first_row = False
            else:
                latex_table += f"  & {g.capitalize()} "
            for fn in fns:
                result = function_data[fn][g].get(order, 0)
                latex_table += f"& ${result:.2e}$ "
            latex_table += "\\\\\n"
        latex_table += "  \\hline\n"

    latex_table += "\\end{longtable}"
    return latex_table


def process_and_plot_tabular_special_pyrust(typ, directory):
    """
    Génère un tableau LaTeX avec les différences de performance en pourcentage entre Rust et Python pour les graphes spéciaux (Empty, Turan, Complete).
    """
    fns = ["CLIQUES", "BKP_R", "BKP_M"]
    graph_types = ["empty", "turan", "complete"]
    function_data = {fn: {g: {} for g in graph_types} for fn in fns}
    rust_data = {fn: {g: {} for g in graph_types} for fn in fns}

    orders = set()

    for fn in fns:
        for g in graph_types:
            pattern = re.compile(rf'^{typ}_res_{fn}_{g}_(\d+)\.out$')
            rust_pattern = re.compile(rf'^{typ}_rust_res_{fn}_{g}_(\d+)\.out$')

            for filename in os.listdir(directory):
                if pattern.match(filename):
                    parts = filename.split('_')
                    order = int(parts[-1].split('.')[0])

                    # Read data from file
                    data = read_data(os.path.join(directory, filename))

                    # Calculate mean
                    mean_value = calculate_mean(data)

                    # Store mean value for function and order
                    function_data[fn][g][order] = mean_value

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
                    rust_data[fn][g][order] = mean_value

    # Convert orders set to sorted list
    orders = sorted(list(orders))

    # Génération du tableau LaTeX
    latex_table = "\\begin{longtable}{|l||l|l|l|l|}\n"
    latex_table += "  \\hline\n"
    latex_table += "  \\textbf{Ordre} & \\textbf{Graphe} & \\textbf{CLIQUES} & \\textbf{BKP\\_R} & \\textbf{BKP\\_M} \\\\\n"
    latex_table += "  \\hline\n"
    latex_table += "  \\endfirsthead\n"
    latex_table += "  \\hline\n"
    latex_table += "  \\textbf{Ordre} & \\textbf{Graphe} & \\textbf{CLIQUES} & \\textbf{BKP\\_R} & \\textbf{BKP\\_M} \\\\\n"
    latex_table += "  \\hline\n"
    latex_table += "  \\endhead\n"
    latex_table += "  \\hline\n"
    latex_table += "  \\endfoot\n"
    latex_table += "  \\hline\n"
    latex_table += "  \\endlastfoot\n"

    orders = list(range(5, 46))
    for order in orders:
        first_row = True
        for g in graph_types:
            if first_row:
                latex_table += f"  {order} & {g.capitalize()} "
                first_row = False
            else:
                latex_table += f"  & {g.capitalize()} "
            for fn in fns:
                python_mean = function_data[fn][g].get(order, 0)
                rust_mean = rust_data[fn][g].get(order, 0)
                if python_mean == 0:  # Avoid division by zero
                    difference = 0
                else:
                    difference = ((rust_mean - python_mean) / python_mean) * 100
                color_start = "\\textcolor{red}{" if difference > 0 else ""
                color_end = "}" if difference > 0 else ""
                latex_table += f"& {color_start}{difference:.1f}\\%{color_end} "
            latex_table += "\\\\\n"
        latex_table += "  \\hline\n"

    latex_table += "\\end{longtable}"
    return latex_table

# Exemple d'utilisation
table = process_and_plot_tabular_special_pyrust('total', './out/specials/')
print(table)
