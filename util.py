import pickle
from spot import Spot  # Import your Spot class or adjust the import as needed
from constants import grid_size

def load_grid_from_pickle(pickle_path):
    gap = 10 # gap is used when trying to visualize. In this context 10 represents 800 / 80.
    try:
        with open(pickle_path, 'rb') as file:
            # Load the data from the pickle file
            letter_grid, letter_to_spot, source_pos, goal_positions = pickle.load(file)

            # Convert the letter-based grid back to a grid of Spot objects
            grid = []
            goals = []
            source = None  # Initialize source as None

            for row_index, row in enumerate(letter_grid):
                grid_row = []
                for col_index, letter in enumerate(row):
                    spot_type = letter_to_spot[letter]

                    if spot_type == 'blank':
                        spot = Spot(row_index, col_index, gap, grid_size)  # Create a blank spot
                    
                    elif spot_type == 'barrier':
                        spot = Spot(row_index, col_index, gap, grid_size)  # Create a barrier spot
                        spot.make_barrier()
                    elif spot_type == 'start':
                        spot = Spot(row_index, col_index, gap, grid_size)  # Create a start spot
                        spot.make_start()

                        source = spot  # Assign source when 'start' is found
                    elif spot_type == 'end':
                        spot = Spot(row_index, col_index, gap, grid_size)  # Create an end spot
                        spot.make_end()
                        goals.append(spot)

                    grid_row.append(spot)

                grid.append(grid_row)
            
            return grid, source, goals
        
    except Exception as e:
        print(f"Error loading grid from {pickle_path}: {str(e)}")
        return None, None, None
