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

# Define the obstacle density values you have (0, 10, 20, 30)
obstacle_density_values = [0, 10, 20, 30]

# Loop through obstacle density values
for obstacle_density in obstacle_density_values:
    # Define the paths to the CSV files for Dijkstra and A*
    dijkstra_csv_path = os.path.join(results_directory, "Dijkstra/obstacle_density", str(obstacle_density) + ".csv")
    a_star_csv_path = os.path.join(results_directory, "A*/obstacle_density", str(obstacle_density) + ".csv")

    # Read the peak memory data from the CSV files
    dijkstra_memory_data = read_memory_data_from_csv(dijkstra_csv_path)
    a_star_memory_data = read_memory_data_from_csv(a_star_csv_path)

    # Check if the memory data lists are empty
    if not dijkstra_memory_data:
        dijkstra_max_peak = dijkstra_min_peak = 0
    else:
        # Find the maximum and minimum peak memory for each algorithm
        dijkstra_max_peak = max(dijkstra_memory_data)
        dijkstra_min_peak = min(dijkstra_memory_data)

    if not a_star_memory_data:
        a_star_max_peak = a_star_min_peak = 0
    else:
        a_star_max_peak = max(a_star_memory_data)
        a_star_min_peak = min(a_star_memory_data)

    # Append the max and min peaks to the respective lists
    dijkstra_peak_memory.append((dijkstra_min_peak, dijkstra_max_peak))
    a_star_peak_memory.append((a_star_min_peak, a_star_max_peak))

# Create a line graph with error bars showing the range (min to max)
plt.figure(figsize=(8, 6))
plt.errorbar(obstacle_density_values, [((d_min + d_max) / 2) for d_min, d_max in dijkstra_peak_memory],
             yerr=[(d_max - d_min) / 2 for d_min, d_max in dijkstra_peak_memory], label='Dijkstra', marker='o', capsize=5)
plt.errorbar(obstacle_density_values, [((a_min + a_max) / 2) for a_min, a_max in a_star_peak_memory],
             yerr=[(a_max - a_min) / 2 for a_min, a_max in a_star_peak_memory], label='A*', marker='o', capsize=5)

# Set the x-axis ticks explicitly
plt.xticks(obstacle_density_values)

# Add labels and title
plt.xlabel('Obstacle Density')
plt.ylabel('Peak Memory Usage')
plt.title('Peak Memory Usage vs. Obstacle Density')

# Add a legend
plt.legend()

# Show the plot
plt.grid(True)
plt.show()
