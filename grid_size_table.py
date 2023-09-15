import os
import csv
from tabulate import tabulate  # Import the tabulate library
from statistics import mean

# Function to calculate the average CPU time from a list of CPU times
def calculate_average_cpu_time(cpu_time_data):
    return mean(cpu_time_data)  # Use the mean function from the statistics module

# Define the directory containing the CSV files
ex_times_directory = "ex_times"

# Initialize lists to store data for Dijkstra and A* algorithms at different grid sizes
dijkstra_avg_cpu_time = []
a_star_avg_cpu_time = []

# Define the grid sizes you have (128, 256, 512, 1024)
grid_sizes = [128, 256, 512, 1024]

# Create a table to store the data
table = []

# Loop through grid sizes
for grid_size in grid_sizes:
    # Define the paths to the CSV files for Dijkstra and A* at the current grid size
    dijkstra_csv_path = os.path.join(ex_times_directory, f'Dijkstra/grid_size/{grid_size}.csv')
    a_star_csv_path = os.path.join(ex_times_directory, f'A*/grid_size/{grid_size}.csv')

    # Read the CPU time data from the CSV files
    dijkstra_cpu_time_data = []
    a_star_cpu_time_data = []

    with open(dijkstra_csv_path, 'r') as dijkstra_csv_file:
        dijkstra_reader = csv.DictReader(dijkstra_csv_file)
        for row in dijkstra_reader:
            dijkstra_cpu_time_data.append(float(row['runtime']))

    with open(a_star_csv_path, 'r') as a_star_csv_file:
        a_star_reader = csv.DictReader(a_star_csv_file)
        for row in a_star_reader:
            a_star_cpu_time_data.append(float(row['runtime']))

    # Calculate the average CPU time for Dijkstra and A* at the current grid size
    dijkstra_avg_time = calculate_average_cpu_time(dijkstra_cpu_time_data)
    a_star_avg_time = calculate_average_cpu_time(a_star_cpu_time_data)

    # Append the data to the table
    table.append([grid_size, dijkstra_avg_time, a_star_avg_time])

# Create a header for the table
header = ["Grid Size", "Dijkstra Avg CPU Time (s)", "A* Avg CPU Time (s)"]

# Print the table using tabulate
print(tabulate(table, headers=header, tablefmt="grid"))
