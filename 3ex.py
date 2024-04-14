import pygame
import math

# Initialize Pygame
pygame.init()

# Set up the drawing window
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Paint Program')

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Default brush color
current_color = BLACK

# Brush sizes
brush_size = 5

# Font for displaying text
font = pygame.font.SysFont(None, 24)

# Create a surface to draw on
drawing_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
drawing_surface.fill(WHITE)

# Function to draw a square
def draw_square(surface, color, center, size):
    half_size = size // 2
    top_left = (center[0] - half_size, center[1] - half_size)
    pygame.draw.rect(surface, color, (top_left, (size, size)))

# Function to draw a right triangle
def draw_right_triangle(surface, color, start_pos, base, height):
    points = [start_pos, (start_pos[0] + base, start_pos[1]), (start_pos[0], start_pos[1] + height)]
    pygame.draw.polygon(surface, color, points)

# Function to draw an equilateral triangle
def draw_equilateral_triangle(surface, color, center, size):
    height = size * math.sqrt(3) / 2
    half_base = size // 2
    points = [(center[0], center[1] - height / 2),
              (center[0] - half_base, center[1] + height / 2),
              (center[0] + half_base, center[1] + height / 2)]
    pygame.draw.polygon(surface, color, points)

# Function to draw a rhombus
def draw_rhombus(surface, color, center, width, height):
    points = [(center[0], center[1] - height // 2),
              (center[0] + width // 2, center[1]),
              (center[0], center[1] + height // 2),
              (center[0] - width // 2, center[1])]
    pygame.draw.polygon(surface, color, points)

# Run the game loop
running = True
drawing = False
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                drawing = True
            elif event.button == 3:  # Right mouse button
                drawing_surface.fill(WHITE)  # Clear the drawing surface
        elif event.type == pygame.MOUSEBUTTONUP:
            drawing = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                current_color = RED
            elif event.key == pygame.K_g:
                current_color = GREEN
            elif event.key == pygame.K_b:
                current_color = BLUE
            elif event.key == pygame.K_w:
                current_color = WHITE
            elif event.key == pygame.K_1:
                brush_size = 5
            elif event.key == pygame.K_2:
                brush_size = 10
            elif event.key == pygame.K_3:
                brush_size = 20
            elif event.key == pygame.K_4:
                brush_size = 30
            elif event.key == pygame.K_s:
                draw_square(drawing_surface, current_color, pygame.mouse.get_pos(), 100)  # Draw square
            elif event.key == pygame.K_t:
                draw_right_triangle(drawing_surface, current_color, pygame.mouse.get_pos(), 100, 100)  # Draw right triangle
            elif event.key == pygame.K_e:
                draw_equilateral_triangle(drawing_surface, current_color, pygame.mouse.get_pos(), 100)  # Draw equilateral triangle
            elif event.key == pygame.K_h:
                draw_rhombus(drawing_surface, current_color, pygame.mouse.get_pos(), 100, 100)  # Draw rhombus

    # Draw on the surface if the mouse button is pressed
    if drawing:
        pos = pygame.mouse.get_pos()
        pygame.draw.circle(drawing_surface, current_color, pos, brush_size)

    # Clear the screen
    window.fill(WHITE)

    # Draw the drawing surface onto the window
    window.blit(drawing_surface, (0, 0))

    # Display instructions
    text = font.render("Press 1, 2, 3, or 4 to change brush size", True, BLACK)
    window.blit(text, (10, 10))
    text = font.render("Press 'r' for red, 'g' for green, 'b' for blue, 'w' for white", True, BLACK)
    window.blit(text, (10, 30))
    text = font.render("Left click to draw, right click to clear", True, BLACK)
    window.blit(text, (10, 50))
    text = font.render("Press 's' to draw square, 't' for right triangle, 'e' for equilateral triangle, 'h' for rhombus", True, BLACK)
    window.blit(text, (10, 70))

    # Update the display
    pygame.display.flip()

# Done! Time to quit.
pygame.quit()