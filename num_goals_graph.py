import os
import csv
import matplotlib.pyplot as plt
from tabulate import tabulate  # Import the tabulate library

# Function to calculate the average CPU time from a list of CPU times
def calculate_average_cpu_time(cpu_time_data):
    return sum(cpu_time_data) / len(cpu_time_data)

# Define the directory containing the CSV files
ex_times_directory = "ex_times"

# Initialize lists to store data for Dijkstra and A* algorithms at different numbers of goals
dijkstra_avg_cpu_time = []
a_star_avg_cpu_time = []
dijkstra_time_per_goal = []  # Added list for time per goal for Dijkstra
a_star_time_per_goal = []    # Added list for time per goal for A*

# Define the number of goals values you have (1, 2, 3, 5, 7, 10)
num_goals_values = [1, 2, 3, 5, 7, 10]

# Initialize a list to store data for the table
table_data = []

# Loop through number of goals values
for num_goals in num_goals_values:
    # Define the paths to the CSV files for Dijkstra and A* at the current number of goals
    dijkstra_csv_path = os.path.join(ex_times_directory, f'Dijkstra/num_goals/{num_goals}.csv')
    a_star_csv_path = os.path.join(ex_times_directory, f'A*/num_goals/{num_goals}.csv')

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

    # Calculate the average CPU time for Dijkstra and A* at the current number of goals
    dijkstra_avg_time = calculate_average_cpu_time(dijkstra_cpu_time_data)
    a_star_avg_time = calculate_average_cpu_time(a_star_cpu_time_data)

    # Calculate time taken per goal
    dijkstra_time_per_goal.append(dijkstra_avg_time / num_goals)
    a_star_time_per_goal.append(a_star_avg_time / num_goals)

    # Append the average times and time per goal to the respective lists
    dijkstra_avg_cpu_time.append(dijkstra_avg_time)
    a_star_avg_cpu_time.append(a_star_avg_time)

    # Append data to the table
    table_data.append([num_goals, dijkstra_avg_time, a_star_avg_time, dijkstra_avg_time / num_goals, a_star_avg_time / num_goals])

# Create a line graph showing the average CPU time vs. number of goals
plt.figure(figsize=(8, 6))
plt.plot(num_goals_values, dijkstra_avg_cpu_time, label='Dijkstra', marker='o')
plt.plot(num_goals_values, a_star_avg_cpu_time, label='A*', marker='o')

# Set the x-axis ticks explicitly
plt.xticks(num_goals_values)

# Add labels and title
plt.xlabel('Number of Goals')
plt.ylabel('Average CPU Time (s)')
plt.title('Average CPU Time vs. Number of Goals')

# Add a legend
plt.legend()

# Print the table
headers = ["Number of Goals", "Dijkstra Avg Time (s)", "A* Avg Time (s)", "Dijkstra Time per Goal (s)", "A* Time per Goal (s)"]
print(tabulate(table_data, headers=headers, tablefmt="fancy_grid"))

# Show the plot
plt.grid(True)
plt.show()


