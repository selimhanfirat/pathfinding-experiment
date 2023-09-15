import pygame
from queue import PriorityQueue

def dijkstra_algorithm(grid, start, goals, draw=None, experiment=False):
    for row in grid:
        for spot in row:
            spot.update_neighbors(grid)
            
    # Create a copy of the goals list to avoid modifying the original list
    remaining_goals = goals.copy()

    # Initialize data structures
    open_set = PriorityQueue()
    open_set.put((0, start))
    came_from = {}
    g_score = {spot: float("inf") for row in grid for spot in row}
    g_score[start] = 0


    while not open_set.empty():
        if draw:  # If there is draw it means the UI is running, check for quit event
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

        current = open_set.get()[1]

        if current in remaining_goals:
            remaining_goals.remove(current)  # Remove this goal from the list
            if not remaining_goals:
                break  # All goals found

        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 10  # Cost of moving orthogonally

            if current.row != neighbor.row and current.col != neighbor.col:
                temp_g_score = g_score[current] + 14  # Cost of moving diagonally

            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                open_set.put((temp_g_score, neighbor))

        if draw is not None:
            draw()
            
        if current != start and not current.is_end() and draw:
            current.make_closed()
            
    # Reconstruct paths to all goals
    paths = {}
    for goal in goals:
        paths[goal] = reconstruct_path(came_from, goal)

    return paths

def reconstruct_path(came_from, current):
    path = []
    while current in came_from:
        current = came_from[current]
        path.append(current)
    path.reverse()  # Reverse to get the correct path order
    return path
