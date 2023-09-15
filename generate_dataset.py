import os
import pickle
from generate import make_grid
from constants import grid_size, num_goals, obstacle_density, num_grids, width


# Create the directory structure if it doesn't exist
datasets_dir = 'datasets'

test_name = "num_goals"

if test_name == 'grid_size':
    independent_var = grid_size    
elif test_name == 'num_goals':
    independent_var = num_goals
elif test_name == 'obstacle_density':
    independent_var = obstacle_density


dir_name = os.path.join(datasets_dir, test_name, str(independent_var))
os.makedirs(dir_name, exist_ok=True)

# Define a mapping for letters to spot types
letter_to_spot = {
    'W': 'blank',
    'B': 'barrier',
    'S': 'start',
    'G': 'end'
}

# Generate and save the grids
count = 0
for i in range(num_grids):
    print(f"{num_grids - count} iterations remain")
    count += 1
    grid, source, goals = make_grid(grid_size, width, obstacle_density, num_goals, solvable_check=True)
    
    # Convert the grid to a letter-based representation
    letter_grid = [['W' if spot.is_blank() else 'B' if spot.is_barrier() else 'S' if spot.is_start() else 'G' for spot in row] for row in grid]

    # Define a unique filename for each grid
    filename = os.path.join(dir_name, f'{independent_var}_{i+1}.pkl')
        
    # Save the letter-based grid using pickle
    with open(filename, 'wb') as file:
        pickle.dump((letter_grid, letter_to_spot, source.get_pos(), [goal.get_pos() for goal in goals]), file)

print(f'{num_grids} grids with {grid_size} rows, {obstacle_density}% obstacle density, and {num_goals} goal(s) saved in {dir_name}.')
