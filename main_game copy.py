import pygame
from pygame.math import Vector2
import sys
import random

pygame.init()

#game definitions
clock = pygame.time.Clock()

BLACK = (0,0,0)

TileSize = 25
TilesX = 30
TilesY = 25

SCREEN_WIDTH = TileSize*TilesX
SCREEN_HEIGHT = TileSize*TilesY



class Fruit:
    def __init__(self):
        self.position = self.generRandomPos()


    def draw(self):
        fruitRect = pygame.Rect(self.position.x * TileSize, self.position.y * TileSize, TileSize, TileSize)
        #pygame.draw.rect(screen, BLACK, fruitRect)
        screen.blit(fruitSurface, fruitRect)

    def generRandomPos(self):
        x = random.randint(0, TilesX-1)
        y = random.randint(0, TilesY-1)
        position = Vector2(x,y)
        return position



class Snakie:
    def __init__(self):
        self.body = [Vector2(6,9), Vector2(5,9), Vector2(4,9)]
        self.direction = Vector2(1,0)

    def draw(self):
        for segment in self.body:
            segmentRect = (segment.x * TileSize, segment.y *TileSize, TileSize, TileSize)
            pygame.draw.rect(screen, BLACK, segmentRect, 0,7)


    def update(self):
        self.body = self.body[:-1]
        self.body.insert(0,
                         Vector2( (self.body[0].x + self.direction.x) % TilesX , (self.body[0].y + self.direction.y) % TilesY)
                         )




screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snakie")


fruit = Fruit()
snakie = Snakie()
fruitSurface = pygame.image.load("test_fuit.jpg")



SNAKE_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SNAKE_UPDATE, 200)


#The game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == SNAKE_UPDATE:
            snakie.update()
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()



        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snakie.direction != Vector2(0,1):
                snakie.direction = Vector2(0,-1)

            if event.key == pygame.K_DOWN and snakie.direction != Vector2(0,-1):
                snakie.direction = Vector2(0,1)

            if event.key == pygame.K_LEFT and snakie.direction != Vector2(1,0):
                snakie.direction = Vector2(-1,0)

            if event.key == pygame.K_RIGHT and snakie.direction != Vector2(-1,0):
                snakie.direction = Vector2(1,0)


    #snakie.update()


    #Frame rate and background
    clock.tick(60)
    screen.fill((255,255,255))
    fruit.draw()
    snakie.draw()




    pygame.display.flip()