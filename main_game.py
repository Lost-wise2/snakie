import pygame
import sys

pygame.init()

#game definitions
clock = pygame.time.Clock()


TileSize = 25
NumberTiles = 30

SCREEN_WIDTH = TileSize*NumberTiles
SCREEN_HEIGHT = TileSize*TileSize



screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snakie")



#The game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    #Frame rate and background
    clock.tick(60)
    screen.fill((255,255,255))
    pygame.display.flip()