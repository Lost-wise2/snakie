import pygame
from pygame.math import Vector2
import sys
import random

pygame.init()

titleFont = pygame.font.Font(None, 60)
scoreFont = pygame.font.Font(None, 40)

#game definitions
clock = pygame.time.Clock()

BLACK = (0,0,0)

TileSize = 25
NumberTiles = 30

SCREEN_WIDTH = TileSize*NumberTiles
SCREEN_HEIGHT = TileSize*TileSize


OFFSET = 75



class Fruit:
    def __init__(self, snakie_body):
        self.position = self.generRandomPos(snakie_body)


    def draw(self):
        fruitRect = pygame.Rect(OFFSET + self.position.x * TileSize, OFFSET + self.position.y * TileSize, TileSize, TileSize)
        #pygame.draw.rect(screen, BLACK, fruitRect)
        screen.blit(fruitSurface, fruitRect)

    
    def generRandomCell(self):
        x = random.randint(0, NumberTiles-1)
        y = random.randint(0, TileSize-1)
        return Vector2(x,y)
    
    def generRandomPos(self, snakie_body):
        
        position = self.generRandomCell()

        while position in snakie_body:
            position = self.generRandomCell()
            

        return position



class Snakie:
    def __init__(self):
        self.body = [Vector2(6,9), Vector2(5,9), Vector2(4,9)]
        self.direction = Vector2(1,0)
        self.add_body = False

    def draw(self):
        for segment in self.body:
            segmentRect = (OFFSET + segment.x * TileSize, OFFSET + segment.y *TileSize, TileSize, TileSize)
            pygame.draw.rect(screen, BLACK, segmentRect, 0,7)


    def update(self):
        self.body.insert(0,self.body[0] + self.direction)
        if self.add_body == True:
            
            self.add_body = False
        else:
            self.body = self.body[:-1]


    def reset(self):
        self.body = [Vector2(6,9), Vector2(5,9), Vector2(4,9)]
        self.direction = Vector2(1,0)
            




class Game:
    def __init__(self):
        self.snakie = Snakie()
        self.fruit = Fruit(self.snakie.body)
        self.state = "RUNNING"
        self.score = 0

    def draw(self):
        self.fruit.draw()
        self.snakie.draw()

    def update(self):
        if self.state == "RUNNING":
            self.snakie.update()
            self.check_collision()
            self.check_deadEND()
            self.check_eatSELF()


    def check_collision(self):
        if self.snakie.body[0] == self.fruit.position:
            #print("yummy in my tummy")
            self.fruit.position = self.fruit.generRandomPos(self.snakie.body)
            self.snakie.add_body = True
            self.score += 1

    def check_deadEND(self):
        if self.snakie.body[0].x == NumberTiles or self.snakie.body[0].x == -1:
            self.game_over()
        if self.snakie.body[0].y == TileSize or self.snakie.body[0].y == -1:
            self.game_over()
    
    def check_eatSELF(self):
        headless_snake = self.snakie.body[1:]
        if self.snakie.body[0] in headless_snake:
            self.game_over()

    
    def game_over(self):
        print("oopsies")
        self.snakie.reset()
        self.fruit.position = self.fruit.generRandomPos(self.snakie.body)
        self.state = "STOPPED"
        self.score = 0





screen = pygame.display.set_mode((2*OFFSET + SCREEN_WIDTH, 2*OFFSET + SCREEN_HEIGHT))
pygame.display.set_caption("Snakie")


#fruit = Fruit()
#snakie = Snakie()

game = Game()

fruitSurface = pygame.image.load("test_fuit.jpg")



SNAKE_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SNAKE_UPDATE, 150)


#The game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == SNAKE_UPDATE:
            game.update()
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()



        if event.type == pygame.KEYDOWN:
            if game.state == "STOPPED":
                game.state = "RUNNING"
            if event.key == pygame.K_UP and game.snakie.direction != Vector2(0,1):
                game.snakie.direction = Vector2(0,-1)

            if event.key == pygame.K_DOWN and game.snakie.direction != Vector2(0,-1):
                game.snakie.direction = Vector2(0,1)

            if event.key == pygame.K_LEFT and game.snakie.direction != Vector2(1,0):
                game.snakie.direction = Vector2(-1,0)

            if event.key == pygame.K_RIGHT and game.snakie.direction != Vector2(-1,0):
                game.snakie.direction = Vector2(1,0)


    #snakie.update()


    #Frame rate and background
    clock.tick(60)
    screen.fill((255,255,255))
    pygame.draw.rect(screen, (148, 201, 40), (OFFSET-5,OFFSET-5, SCREEN_WIDTH + 10, SCREEN_HEIGHT + 10), 5)
    #fruit.draw()
    #snakie.draw()

    game.draw()
    title_surface = titleFont.render("Snakie game", True, (148, 201, 40))
    score_surface = scoreFont.render(str(game.score), True, (148, 201, 40))

    screen.blit(title_surface, (OFFSET + 5, 20))
    screen.blit(score_surface, (OFFSET + 5, OFFSET + SCREEN_HEIGHT + 10))




    pygame.display.flip()