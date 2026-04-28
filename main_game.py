import pygame
from pygame.math import Vector2
import sys
import random

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
        self.position = self.generRandomPos()


    def draw(self):
        fruitRect = pygame.Rect(self.position.x * TileSize, self.position.y * TileSize, TileSize, TileSize)
        #pygame.draw.rect(screen, BLACK, fruitRect)
        screen.blit(fruitSurface, fruitRect)

    def generRandomPos(self):
        x = random.randint(0, NumberTiles-1)
        y = random.randint(0, NumberTiles-1)
        position = Vector2(x,y)
        return position



class Snakie:
    def __init__(self):
        self.body = [Vector2(6,9), Vector2(5,9), Vector2(4,9)]

    def draw(self):
        for segment in self.body:
            segmentRect = (segment.x * TileSize, segment.y *TileSize, TileSize, TileSize)
            pygame.draw.rect(screen, BLACK, segmentRect, 0,7)




screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snakie")


fruit = Fruit()
snakie = Snakie()
fruitSurface = pygame.image.load("test_fuit.jpg")


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
    snakie.draw()




    pygame.display.flip()