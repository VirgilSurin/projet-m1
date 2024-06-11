#!/usr/bin/env python3
import os
import numpy as np
import matplotlib.pyplot as plt

# Function to read data from file
def read_data(file_path):
    with open(file_path, 'r') as file:
        data = [float(line.strip()) for line in file]
    return data

def calculate_mean(data):
    return np.mean(data)

def process_and_plot(typ, directory, g):
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

# Call the main function with the directory containing the files
process_and_plot('total', './out/specials/', "complete")
process_and_plot('total', './out/specials/', "empty")
process_and_plot('total', './out/specials/', "turan")
process_and_plot('delay', './out/specials/', "complete")
process_and_plot('delay', './out/specials/', "empty")
process_and_plot('delay', './out/specials/', "turan")
