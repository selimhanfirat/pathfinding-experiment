from algorithm import algorithm
from generate import make_grid
import util
from generate_dataset import path 


obstacle_density = 40
num_goals = 5
grid, source, goals = util.load_grid_from_pickle(path)

results = None

for goal in goals:
    results = algorithm(grid, source, goal, debug=False)
    if results:
        print(True)



