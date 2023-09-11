import os
import util
import time
from algorithm import algorithm
from dijkstra import dijkstra_algorithm
from constants import astar, grid_size, num_goals, obstacle_density

# Define the directory structure
datasets_dir = 'datasets'

experiment_type = "num_goals"

if experiment_type == 'grid_size':
    independent_var = grid_size    
elif experiment_type == 'num_goals':
    independent_var = num_goals
elif experiment_type == 'obstacle_density':
    independent_var = obstacle_density

# Get a list of files in the specified directory
grid_dir = os.path.join(datasets_dir, experiment_type, str(independent_var))
file_list = os.listdir(grid_dir)
total_path_length = 0
total_cpu_time = 0

# Loop over the files and load/run the algorithm
count = 0
total = 0
for file_name in file_list:
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
                    count += 1
            print(f"Total path length for grid {count}: {total_path_length}")
            total += total_path_length
        else:
            results = dijkstra_algorithm(grid, source, goals)
            total_path_length = sum(len(path) for path in results.values())
            count += 1
            print(f"Total path length for grid {count}: {total_path_length}")
            total += total_path_length

            # Fix the count bug. When using A* the count gets multiplied by num_gaols.
            
        if count == 50:
            break
        end_cpu_time = time.process_time()
        cpu_time_used = end_cpu_time - start_cpu_time
        total_cpu_time += cpu_time_used

average_cpu_time = total_cpu_time / count
print(f"Average CPU Time Used: {average_cpu_time} seconds")
print(f"Total path length for the whole algorithm: {total}")
