import random
import pygame 
from spot import Spot
from algorithm import algorithm
from dijkstra import dijkstra_algorithm
from constants import astar

def make_grid(rows, width, obstacle_density, num_goals, solvable_check=False):
    while True:
        grid = []
        gap = width // rows
        source = None
        goals = []

        for i in range(rows):
            grid.append([])
            for j in range(rows):
                # Create a Spot object
                spot = Spot(i, j, gap, rows)

                # Randomly set some spots as barriers
                if random.randint(1, 100) <= obstacle_density:  # Adjust the percentage as needed (20% in this case)
                    spot.make_barrier()              

                grid[i].append(spot)
                
        # Randomly set three spots as goals
        while len(goals) < num_goals:
            while True:
                row = random.randint(0, rows - 1)
                col = random.randint(0, rows - 1)
                goal_spot = grid[row][col]
                if goal_spot not in goals and goal_spot != source:
                    goal_spot.make_end()
                    goals.append(goal_spot)
                    break
        
        # Randomly set the source node
        while source is None:
            row = random.randint(0, rows - 1)
            col = random.randint(0, rows - 1)
            source = grid[row][col]
            if source.is_blank: 
                source.make_start()
            else:
                source = None
        
        print("grid has been generated")
    

        # Verify solvability
        if solvable_check:
            if is_grid_solvable(grid, source, goals, astar):
                print("it is solvable")
                return grid, source, goals
            else:
                print("grid did not pass the check")
        else:
            return grid, source, goals


def is_grid_solvable(grid, source, goals, astar):
    for row in grid:
        for spot in row:
            spot.update_neighbors(grid)
    
    if astar:
        print("checking with A*")
        for goal in goals:
            temp = algorithm(grid, source, goal)
            if temp is None:
                return False
    else:
        print("checking with Dijkstra")
        # Check if there is a path for each goal
        paths = dijkstra_algorithm(grid, source, goals)
        for path in paths.values():
            if not path:
                return False
    
    return True

        
# Example usage:
if __name__ == "__main__":
    pygame.quit()
