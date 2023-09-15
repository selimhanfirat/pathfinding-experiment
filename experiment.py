import os
import util
import time
from algorithm import algorithm
from dijkstra import dijkstra_algorithm
import csv
from constants import astar, grid_size, num_goals, obstacle_density, num_grids

# Define the directory structure
datasets_dir = 'datasets'

experiment_type = "grid_size"

if experiment_type == 'grid_size':
    obstacle_density = 0
    num_goals = 1
    independent_var = grid_size    
elif experiment_type == 'num_goals':
    obstacle_density = 0
    grid_size = 256
    independent_var = num_goals
elif experiment_type == 'obstacle_density':
    num_goals = 1
    grid_size = 256
    independent_var = obstacle_density

print(f"Running experiment for {experiment_type} with {num_goals} goal(s), {grid_size} size, and {obstacle_density}% obstacle density")

# Get a list of files in the specified directory
grid_dir = os.path.join(datasets_dir, experiment_type, str(independent_var))
file_list = os.listdir(grid_dir)

# Create a directory for experiment times if it doesn't exist
ex_times_dir = 'ex_times'
os.makedirs(ex_times_dir, exist_ok=True)

# Create a CSV file with experiment parameters and runtime for each grid
csv_filename = f'{independent_var}.csv'
csv_path = os.path.join(ex_times_dir, csv_filename)

with open(csv_path, mode='w', newline='') as csv_file:
    fieldnames = ['grid_number', 'runtime']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

    writer.writeheader()

    for count, file_name in enumerate(file_list, 1):
        if file_name.endswith('.pkl'):  # Ensure it's a pickle file
            path = os.path.join(grid_dir, file_name)
            grid, source, goals = util.load_grid_from_pickle(path)
            results = None

            start_cpu_time = time.process_time()
            if astar:
                total_path_length = 0
                for goal in goals:
                    results = algorithm(grid, source, goal)
                    if results:
                        total_path_length += len(results)
                print(f"{num_grids - count} grids remaining" )
            else:
                results = dijkstra_algorithm(grid, source, goals)
                total_path_length = sum(len(path) for path in results.values())
                print(f"{num_grids - count} grids remaining" )
                
            end_cpu_time = time.process_time()
            cpu_time_used = end_cpu_time - start_cpu_time
            print(f"it took {cpu_time_used} seconds")

            # Write data for this grid to the CSV file
            writer.writerow({
                'grid_number': count,
                'runtime': cpu_time_used
            })
