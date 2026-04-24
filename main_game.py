import pygame
from pygame.math import Vector2
import sys

pygame.init()

#game definitions
clock = pygame.time.Clock()

BLACK = (0,0,0)

TileSize = 25
NumberTiles = 30

SCREEN_WIDTH = TileSize*NumberTiles
SCREEN_HEIGHT = TileSize*TileSize



class Fruit:
    def __init__(self):
        self.position = Vector2(5,6)


    def draw(self):
        fruitRect = pygame.Rect(self.position.x * TileSize, self.position.y * TileSize, TileSize, TileSize)
        pygame.draw.rect(screen, BLACK, fruitRect)







screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snakie")


fruit = Fruit()


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
    fruit.draw()




    pygame.display.flip()