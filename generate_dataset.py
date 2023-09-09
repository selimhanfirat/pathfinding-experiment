import os
import pickle
from generate import make_grid

# Width is for visualization therefore we set it to 0 when we don't visualize
width = 800

# Define the parameters for the grid generation
grid_size = 80  # Specify the grid size here
obstacle_density = 30
num_goals = 1
num_grids = 1  # Number of grids to generate

# Create the directory structure if it doesn't exist
datasets_dir = 'datasets'
test_name = 'grid_size'

grid_size_dir = os.path.join(datasets_dir, test_name, str(grid_size))
os.makedirs(grid_size_dir, exist_ok=True)

# Define a mapping for letters to spot types
letter_to_spot = {
    'W': 'blank',
    'B': 'barrier',
    'S': 'start',
    'G': 'end'
}

# Generate and save the grids
for i in range(num_grids):
    grid, source, goals = make_grid(grid_size, width, obstacle_density, num_goals, solvable_check=True)
    
    # Convert the grid to a letter-based representation
    letter_grid = [['W' if spot.is_blank() else 'B' if spot.is_barrier() else 'S' if spot.is_start() else 'G' for spot in row] for row in grid]

    # Define a unique filename for each grid
    filename = os.path.join(grid_size_dir, f'{grid_size}_{i+1}.pkl')
    
    if i == 0:
        path = filename
    
    # Save the letter-based grid using pickle
    with open(filename, 'wb') as file:
        pickle.dump((letter_grid, letter_to_spot, source.get_pos(), [goal.get_pos() for goal in goals]), file)

print(f'{num_grids} grids with {grid_size} rows, {obstacle_density}% obstacle density, and {num_goals} goal(s) saved in {grid_size_dir}.')
