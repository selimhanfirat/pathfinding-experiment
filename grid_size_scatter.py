import os
import csv
import matplotlib.pyplot as plt

# Function to calculate the average CPU time from a list of CPU times
def calculate_average_cpu_time(cpu_time_data):
    return sum(cpu_time_data) / len(cpu_time_data)

# Define the directory containing the CSV files
ex_times_directory = "ex_times"

# Initialize lists to store data for Dijkstra and A* algorithms at different grid sizes
dijkstra_cpu_times = []
a_star_cpu_times = []

# Define the grid sizes you have (128, 256, 512, 1024)
grid_sizes = [128, 256, 512, 1024]

# Define an offset for x-coordinates to avoid overlap
x_offset = 10

# Create lists to store labels and colors for the legend
legend_labels = []
legend_colors = []

# Create a list to store the x-axis positions
x_positions = []

# Loop through grid sizes
for i, grid_size in enumerate(grid_sizes):
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

    # Create x-coordinates with an offset to avoid overlap
    x_dijkstra = [grid_size + x_offset * i] * len(dijkstra_cpu_time_data)
    x_a_star = [grid_size + x_offset * i] * len(a_star_cpu_time_data)

    # Append the CPU times and x-coordinates to the respective lists
    dijkstra_cpu_times.extend(dijkstra_cpu_time_data)
    a_star_cpu_times.extend(a_star_cpu_time_data)

    # Set labels and colors for the legend
    if i == 0:
        legend_labels.append(f"Dijkstra's algorithm")
        legend_labels.append(f'A*')
        legend_labels.append(f'Avg Dijkstra')
        legend_labels.append(f'Avg A*')
        legend_colors.extend(['orange', 'blue', 'red', 'purple'])

    # Create scatter plots with specified colors and smaller dots
    plt.scatter(x_dijkstra, dijkstra_cpu_time_data, label=f'Dijkstra {grid_size}', marker='o', color='orange', alpha=0.5, s=20)
    plt.scatter(x_a_star, a_star_cpu_time_data, label=f'A* {grid_size}', marker='o', color='blue', alpha=0.5, s=20)

    # Calculate and plot the average CPU time as a red dot with a label above
    avg_dijkstra = calculate_average_cpu_time(dijkstra_cpu_time_data)
    avg_a_star = calculate_average_cpu_time(a_star_cpu_time_data)

    plt.scatter(grid_size, avg_dijkstra, color='red', marker='o', s=100, alpha=0.8)
    plt.scatter(grid_size + x_offset, avg_a_star, color='purple', marker='o', s=100, alpha=0.8)
    plt.text(grid_size, avg_dijkstra, f'{avg_dijkstra:.2f}', ha='center', va='bottom', fontsize=10, color='black')
    plt.text(grid_size + x_offset, avg_a_star, f'{avg_a_star:.2f}', ha='center', va='bottom', fontsize=10, color='black')

    # Append the x-position for the current grid size
    x_positions.append(grid_size)

# Set the x-axis ticks explicitly
plt.xticks(x_positions)

# Add labels and title
plt.xlabel('Grid Size')
plt.ylabel('CPU Time (s)')
plt.title('CPU Time vs. Grid Size')

# Add a legend with specified labels and colors
plt.legend(legend_labels, loc='upper left', frameon=True, title='Algorithms', labelcolor=legend_colors)

# Show the plot
plt.grid(True)
plt.show()
