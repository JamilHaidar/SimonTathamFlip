import pygame

from solve_barebones import GameController

WIDTH, HEIGHT = 600, 600
pygame.display.set_caption("Flip Solver")
screen = pygame.display.set_mode((WIDTH, HEIGHT))

n = 5
game_controller = GameController(screen,n)

while True:
    state = game_controller.handle_commands()
    if state:
        n=state
        game_controller = GameController(screen,n)
    game_controller.update()