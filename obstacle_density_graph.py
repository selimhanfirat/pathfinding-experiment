import os
import csv
import matplotlib.pyplot as plt

# Function to calculate the average CPU time from a list of CPU times
def calculate_average_cpu_time(cpu_time_data):
    return sum(cpu_time_data) / len(cpu_time_data)

# Define the directory containing the CSV files
ex_times_directory = "ex_times"

# Initialize lists to store data for Dijkstra and A* algorithms at different obstacle densities
dijkstra_avg_cpu_time = []
a_star_avg_cpu_time = []

# Define the obstacle density values you have (0, 10, 20, 30)
obstacle_density_values = [0, 10, 20, 30]

# Loop through obstacle density values
for obstacle_density in obstacle_density_values:
    # Define the paths to the CSV files for Dijkstra and A* at the current obstacle density
    dijkstra_csv_path = os.path.join(ex_times_directory, f'Dijkstra/obstacle_density/{obstacle_density}.csv')
    a_star_csv_path = os.path.join(ex_times_directory, f'A*/obstacle_density/{obstacle_density}.csv')

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

    # Calculate the average CPU time for Dijkstra and A* at the current obstacle density
    dijkstra_avg_time = calculate_average_cpu_time(dijkstra_cpu_time_data)
    a_star_avg_time = calculate_average_cpu_time(a_star_cpu_time_data)

    # Append the average times to the respective lists
    dijkstra_avg_cpu_time.append(dijkstra_avg_time)
    a_star_avg_cpu_time.append(a_star_avg_time)

# Create a line graph showing the average CPU time vs. obstacle density
plt.figure(figsize=(8, 6))
plt.plot(obstacle_density_values, dijkstra_avg_cpu_time, label='Dijkstra', marker='o')
plt.plot(obstacle_density_values, a_star_avg_cpu_time, label='A*', marker='o')

# Set the x-axis ticks explicitly
plt.xticks(obstacle_density_values)

# Add labels and title
plt.xlabel('Obstacle Density (%)')
plt.ylabel('Average CPU Time (s)')
plt.title('Average CPU Time vs. Obstacle Density')

# Add a legend
plt.legend()

# Show the plot
plt.grid(True)
plt.show()
