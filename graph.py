import os
import csv
import matplotlib.pyplot as plt

# Function to read the peak memory usage from a CSV file
def read_memory_data_from_csv(file_path):
    memory_data = []
    with open(file_path, 'r') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            peak_memory = float(row['peak'])
            memory_data.append(peak_memory)
    return memory_data

# Define the directory containing the CSV files
results_directory = "results/"

# Initialize lists to store data for Dijkstra and A* algorithms
dijkstra_peak_memory = []
a_star_peak_memory = []

# Define the grid sizes (you may adjust these as needed)
grid_sizes = [128, 256, 512, 1024]

# Loop through grid sizes
for grid_size in grid_sizes:
    # Define the paths to the CSV files for Dijkstra and A*
    dijkstra_csv_path = os.path.join(results_directory, "Dijkstra/grid_size", str(grid_size) + ".csv")
    a_star_csv_path = os.path.join(results_directory, "A*/grid_size", str(grid_size) + ".csv")

    # Read the peak memory data from the CSV files
    dijkstra_memory_data = read_memory_data_from_csv(dijkstra_csv_path)
    a_star_memory_data = read_memory_data_from_csv(a_star_csv_path)

    # Find the maximum and minimum peak memory for each algorithm
    dijkstra_max_peak = max(dijkstra_memory_data)
    dijkstra_min_peak = min(dijkstra_memory_data)
    a_star_max_peak = max(a_star_memory_data)
    a_star_min_peak = min(a_star_memory_data)

    # Append the max and min peaks to the respective lists
    dijkstra_peak_memory.append((dijkstra_min_peak, dijkstra_max_peak))
    a_star_peak_memory.append((a_star_min_peak, a_star_max_peak))

# Create a line graph with error bars showing the range (min to max)
plt.figure(figsize=(8, 6))
plt.errorbar(grid_sizes, [((d_min + d_max) / 2) for d_min, d_max in dijkstra_peak_memory],
             yerr=[(d_max - d_min) / 2 for d_min, d_max in dijkstra_peak_memory], label='Dijkstra', marker='o', capsize=5)
plt.errorbar(grid_sizes, [((a_min + a_max) / 2) for a_min, a_max in a_star_peak_memory],
             yerr=[(a_max - a_min) / 2 for a_min, a_max in a_star_peak_memory], label='A*', marker='o', capsize=5)

# Set the x-axis ticks explicitly
plt.xticks(grid_sizes)

# Add labels and title
plt.xlabel('Grid Size')
plt.ylabel('Peak Memory Usage')
plt.title('Peak Memory Usage vs. Grid Size')

# Add a legend
plt.legend()

# Show the plot
plt.grid(True)
plt.show()
