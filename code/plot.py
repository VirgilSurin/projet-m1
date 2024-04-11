#!/usr/bin/env python3
import os
import numpy as np
import matplotlib.pyplot as plt

# Function to read data from file
def read_data(file_path):
    with open(file_path, 'r') as file:
        data = [float(line.strip()) for line in file]
    return data

# Function to calculate mean for each order
def calculate_mean(data):
    return np.mean(data)

# Main function to process files and plot results
def process_and_plot(directory):
    function_data = {}  # Dictionary to store data for each function
    orders = set()      # Set to store unique orders

    # Loop through each file in the directory
    for filename in os.listdir(directory):
        if filename.startswith('total') and filename.endswith('.out'):
            if "CLIQUES" in filename:
                function = "CLIQUES"
            elif "BKP_M" in filename:
                function = "BKP_M"
            elif "BKP_R" in filename:
                function = "BKP_R"
            elif "BK" in filename:
                function = "BK"
            parts = filename.split('_')
            order = int(parts[-1].split('.')[0])

            # Read data from file
            data = read_data(os.path.join(directory, filename))

            # Calculate mean
            mean_value = calculate_mean(data)

            # Store mean value for function and order
            if function not in function_data:
                function_data[function] = {}
            function_data[function][order] = mean_value

            # Add order to set of orders
            orders.add(order)

    # Convert orders set to sorted list
    orders = sorted(list(orders))

    # Plotting
    for function, data in function_data.items():
        plt.plot(orders, [data.get(order, 0) for order in orders], label=function)

    plt.xlabel('Order')
    plt.ylabel('Mean Value')
    plt.title('Mean Value for Each Order')
    plt.legend()
    plt.show()

# Call the main function with the directory containing the files
process_and_plot('./out/')
