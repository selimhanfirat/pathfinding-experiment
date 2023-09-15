import pygame
from queue import PriorityQueue

def reconstruct_path(came_from, current):
    path = []
    while current in came_from:
        current = came_from[current]
        path.append(current)
    return path

def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2

    D = 10
    D2 = 14
    
    dx = abs(x1 - x2)
    dy = abs(y1 - y2)

    return D * (dx + dy) + (D2 - 2 * D) * min(dx, dy)

#from memory_profiler import profile
#@profile(stream=open('logs/A*/num_goals/10.txt', 'w+'))
def algorithm(grid, start, end, draw=None, debug=False, experiment=False):
    for row in grid:
        for spot in row:
            spot.update_neighbors(grid)

    open_set = PriorityQueue()
    open_set.put((0, start))
    came_from = {}
    g_score = {spot: float("inf") for row in grid for spot in row}
    g_score[start] = 0
    f_score = {spot: float("inf") for row in grid for spot in row}
    f_score[start] = h(start.get_pos(), end.get_pos())
    open_set_hash = {start}

    cost_diagonal = 14
    cost_vertical_horizontal = 10

    while not open_set.empty():
        if draw: 
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

        current = open_set.get()[1]
        open_set_hash.remove(current)

        if debug:
            if not current.is_blank():
                print(current.color)
                
        if current == end:
            if draw:
                end.make_end()
            if experiment:
                return reconstruct_path(came_from, end)
            else:
                return reconstruct_path(came_from, end)
            
        for neighbor in current.neighbors:
            if current.row != neighbor.row and current.col != neighbor.col:
                temp_g_score = g_score[current] + cost_diagonal
            else:
                temp_g_score = g_score[current] + cost_vertical_horizontal

            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())
                if neighbor not in open_set_hash:
                    open_set.put((f_score[neighbor], neighbor))
                    open_set_hash.add(neighbor)
                    
        if draw is not None:
            draw()

        if current != start and draw:
            current.make_closed()

    print("No path found")
    return None
