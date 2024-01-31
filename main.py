import pygame
import sys
import random

# Inicialización de Pygame
pygame.init()

# Configuración del grid y la ventana
WIDTH, HEIGHT = 50, 50
CELL_SIZE = 10
WINDOW_SIZE = (WIDTH * CELL_SIZE, HEIGHT * CELL_SIZE)

# Colores
SAND_COLOR = (194, 178, 128)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Inicializa la ventana de juego
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Juego de Granos de Arena - Arrastre")

# Funciones del juego
def init_grid(width, height):
    return [[0 for _ in range(width)] for _ in range(height)]

def update_sand(grid):
    height, width = len(grid), len(grid[0])
    for y in range(height - 2, -1, -1):
        for x in range(width):
            if grid[y][x] == 1:
                move_down = y + 1 < height and grid[y + 1][x] == 0
                move_left = x > 0 and y + 1 < height and grid[y + 1][x - 1] == 0
                move_right = x + 1 < width and y + 1 < height and grid[y + 1][x + 1] == 0

                if move_down:
                    grid[y][x], grid[y + 1][x] = 0, 1
                elif move_left and move_right:
                    direction = random.choice([-1, 1])  # Aleatoriamente hacia la izquierda o derecha
                    grid[y][x], grid[y + 1][x + direction] = 0, 1
                elif move_left:
                    grid[y][x], grid[y + 1][x - 1] = 0, 1
                elif move_right:
                    grid[y][x], grid[y + 1][x + 1] = 0, 1

def draw_grid(screen, grid):
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            color = SAND_COLOR if cell == 1 else WHITE
            pygame.draw.rect(screen, color, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

def toggle_sand(grid, x, y):
    grid_y = y // CELL_SIZE
    grid_x = x // CELL_SIZE
    if 0 <= grid_x < WIDTH and 0 <= grid_y < HEIGHT:
        grid[grid_y][grid_x] = 1

# Inicializa el grid
grid = init_grid(WIDTH, HEIGHT)

# Loop principal del juego
running = True
mouse_down = False  # Para rastrear si el botón del mouse está presionado
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_down = True
            x, y = pygame.mouse.get_pos()
            toggle_sand(grid, x, y)
        elif event.type == pygame.MOUSEBUTTONUP:
            mouse_down = False
        elif event.type == pygame.MOUSEMOTION:
            if mouse_down:
                x, y = event.pos
                toggle_sand(grid, x, y)

    update_sand(grid)

    screen.fill(BLACK)
    draw_grid(screen, grid)
    pygame.display.flip()
    pygame.time.delay(50)

pygame.quit()
sys.exit()