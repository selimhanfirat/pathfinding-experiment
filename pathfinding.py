import pygame
from spot import Spot
from generate import ROWS, make_grid
from algorithm import algorithm
from dijkstra import dijkstra_algorithm

# Define the dimensions of the game window
WIDTH = 800

# Define which algorithm to use
ASTAR = True

# Define obstacle obstacle_density percentage
obstacle_density = 40

# Define the number of goals
num_goals = 5

WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("A* Path Finding Algorithm")

# Define color constants
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)


def draw_grid(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))

def draw(win, grid, rows, width):
    win.fill(WHITE)

    for row in grid:
        for spot in row:
            spot.draw(win)

    draw_grid(win, rows, width)
    pygame.display.update()


def get_clicked_pos(pos, rows, width):
    gap = width // rows
    y, x = pos

    row = y // gap
    col = x // gap

    return row, col


def main(win, width):
    grid, source, goals = make_grid(ROWS, width, obstacle_density, num_goals, solvable_check=True)

    paths = []
    algorithm_running = False

    run = True
    while run:
        draw(win, grid, ROWS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if not algorithm_running:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_s and source is None:
                        pos = pygame.mouse.get_pos()
                        row, col = get_clicked_pos(pos, ROWS, width)
                        source = grid[row][col]
                        source.make_start()

                if pygame.mouse.get_pressed()[0]:  # LEFT (set barrier)
                    pos = pygame.mouse.get_pos()
                    row, col = get_clicked_pos(pos, ROWS, width)
                    spot = grid[row][col]
                    if spot != source and spot not in goals:
                        spot.make_barrier()

                if pygame.mouse.get_pressed()[2]:  # RIGHT (add goal or reset to white)
                    pos = pygame.mouse.get_pos()
                    row, col = get_clicked_pos(pos, ROWS, width)
                    spot = grid[row][col]
                    
                    if spot.color == WHITE:
                        goals.append(spot)
                        spot.make_end()
                    else:
                        if spot.is_start:
                            source = None 
                        spot.reset()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and source is not None and goals:
                        algorithm_running = True
                                
                        if ASTAR:
                            print("A* algorithm is running") 
                            for goal in goals:
                                paths.append(algorithm(grid, source, goal, draw=lambda: draw(win, grid, ROWS, width)))
                        else:
                            print("Dijkstra's algorithm is running") 
                            dict_paths = dijkstra_algorithm(grid, source, goals, draw=lambda: draw(win, grid, ROWS, width))
                            for goal in goals:
                                paths.append(dict_paths[goal])
                            
                        for path in paths:
                            for spot in path:
                                spot.make_path()
                        draw(win, grid, ROWS, width) 

                                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    source = None
                    goals.clear()
                    paths.clear()
                    algorithm_running = False
                    grid, source, goals = make_grid(ROWS, width, obstacle_density, num_goals)
                    draw(win, grid, ROWS, width)


    pygame.quit()

if __name__ == "__main__":
    main(WIN, WIDTH)



