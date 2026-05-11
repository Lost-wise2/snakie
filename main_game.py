import pygame
from pygame.math import Vector2
import sys
import random

import json




with open("highScores.json", "r", encoding="utf-8") as HIGHscores:
    the_HIGHscores = json.load(HIGHscores)
        
        


pygame.init()

nameFont = pygame.font.Font(None, 60)
titleFont = pygame.font.Font(None, 30)
scoreFont = pygame.font.Font(None, 40)

#game definitions
clock = pygame.time.Clock()

BLACK = (0,0,0)
WHITE = (255,255,255)
TEXT = (161, 105, 191)

TileSize = 20
NumberTiles = 30

SCREEN_WIDTH = TileSize*NumberTiles
SCREEN_HEIGHT = TileSize*TileSize


OFFSET = 75

OFFSETLEFT = 117
OFFSETRIGHT = 35
OFFSETWIDTH = OFFSETLEFT + OFFSETRIGHT

OFFSETTOP = 72
OFFSETBOTTOM = 143
OFFSETHEIGHT = OFFSETTOP + OFFSETBOTTOM

SPEED = 140




button_image = pygame.image.load('buttone.jpg')
class button:
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)

    def draw(self):

        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                game.paused = False
                game.started = False
                game.ended = False

        screen.blit(self.image, (self.rect.x, self.rect.y))


test_button = button(280,400,button_image)




class Fruit():
    def __init__(self, snakie_body):
        self.position = self.generRandomPos(snakie_body)


    def draw(self):
        fruitRect = pygame.Rect(OFFSETLEFT + self.position.x * TileSize, OFFSETTOP + self.position.y * TileSize, TileSize, TileSize)
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





class Star(Fruit):
    def __init__(self, snakie_body):
        self.starChance = 0
        self.position = self.generRandomPos(snakie_body)
        self.appeared = False
        
    
    def draw(self):
        starRect = pygame.Rect(OFFSETLEFT + self.position.x * TileSize, OFFSETTOP + self.position.y * TileSize, TileSize, TileSize)
        screen.blit(starSurface, starRect)

    def increaseChance(self):
        self.starChance = random.randint(0,100)

    def noStar(self):
        self.starChance = 0

    def generRandomCell(self):
        
        if self.starChance >= 60:
            x = random.randint(0, NumberTiles-1)
            y = random.randint(0, TileSize-1)
            
            self.appeared = True
            self.powerUP_timer = pygame.time.get_ticks()

            return Vector2(x,y)
        else:
            self.appeared = False
            return Vector2(-200, -200)
            
    
    def generRandomPos(self, snakie_body):
        super().generRandomPos(snakie_body)
        
        position = self.generRandomCell()
            

        return position


class Bomb(Star):
    def __init__(self, snakie_body):
        self.starChance = 0
        self.position = self.generRandomPos(snakie_body)
        self.appeared = False



    def draw(self):
        bombRect = pygame.Rect(OFFSETLEFT + self.position.x * TileSize, OFFSETTOP + self.position.y * TileSize, TileSize, TileSize)
        screen.blit(bombSurface, bombRect)

    def increaseChance(self):
        self.starChance = random.randint(0,100)

    def noStar(self):
        self.starChance = 0

    def generRandomCell(self):
        if self.starChance >= 20:
            x = random.randint(0, NumberTiles-1)
            y = random.randint(0, TileSize-1)
            
            self.appeared = True
            self.powerDOWN_timer = pygame.time.get_ticks()

            return Vector2(x,y)
        else:
            self.appeared = False
            return Vector2(-200, -200)

    def generRandomPos(self, snakie_body):
        super().generRandomPos(snakie_body)
        position = self.generRandomCell()
        return position

    




class Snakie:
    def __init__(self):
        self.body = [Vector2(6,9), Vector2(5,9), Vector2(4,9)]
        self.direction = Vector2(1,0)
        self.add_body = False

        self.eat_fruit = pygame.mixer.Sound("eatsound.wav")
        self.eat_star = pygame.mixer.Sound("powerupsound.wav")
        self.eat_bomb = pygame.mixer.Sound("powerdownsound.wav")

        self.move_pos = pygame.mixer.Sound("movepositive.wav")
        self.move_neg = pygame.mixer.Sound("movenegative.wav")

        self.hit_wall = pygame.mixer.Sound("hitwall.wav")

    def draw(self):
        if game.powerUP == True:
            color = 255
        elif game.powerDOWN == True:
            color = 70
        else:
            color = 190

        for segment in self.body:
            segmentRect = (OFFSETLEFT + segment.x * TileSize, OFFSETTOP + segment.y *TileSize, TileSize, TileSize)
            pygame.draw.rect(screen, (color, (0+8*segment[1]), (0+8*segment[0])), segmentRect, 0,7)


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
        self.star = Star(self.snakie.body)
        self.bomb = Bomb(self.snakie.body)
        
        self.state = "RUNNING"
        self.score = 0
        self.latestScore = 0

        self.paused =  False
        self.started = False
        self.ended = False


        self.powerUP = False
        self.powerDOWN = False
        self.powerUP_time = 0
        self.powerDOWN_time = 0

    def draw(self):
        self.fruit.draw()
        self.snakie.draw()
        
        self.star.draw()
        self.bomb.draw()

    def update(self):
        if self.state == "RUNNING":
            self.snakie.update()
            self.check_collision()
            self.ate_star()
            self.ate_bomb()
            self.check_deadEND()
            self.check_eatSELF()
            self.draw_end()


    def check_collision(self):
        if self.snakie.body[0] == self.fruit.position:
            self.fruit.position = self.fruit.generRandomPos(self.snakie.body)
            self.snakie.add_body = True
            if self.powerUP == True:
                self.score += 2
            else:
                self.score += 1
            self.star.increaseChance()
            self.bomb.increaseChance()
            self.star.position = self.star.generRandomPos(self.snakie.body)
            self.bomb.position = self.bomb.generRandomPos(self.snakie.body)

            self.snakie.eat_fruit.play()
            

    def ate_star(self):
        if self.snakie.body[0] == self.star.position:
            
            self.score += 1
            self.star.noStar()
            self.star.position = self.star.generRandomPos(self.snakie.body)

            global SPEED
            SPEED -= 50
            pygame.time.set_timer(SNAKE_UPDATE, SPEED)

            self.snakie.eat_star.play()

            self.powerUP = True
            if self.powerDOWN == True:
                self.powerDOWN = False
            
            self.powerUP_time = pygame.time.get_ticks()


    def ate_bomb(self):
        if self.snakie.body[0] == self.bomb.position:
            
            if self.powerUP == False:
                self.score -= 1
            
            
                global SPEED
                SPEED += 50
                pygame.time.set_timer(SNAKE_UPDATE, SPEED)

                self.snakie.eat_bomb.play()

                self.powerDOWN = True
            
                self.powerDOWN_time = pygame.time.get_ticks()
            self.bomb.noStar()
            self.bomb.position = self.bomb.generRandomPos(self.snakie.body)

        



    def check_deadEND(self):
        if self.snakie.body[0].x == NumberTiles or self.snakie.body[0].x == -1:
            self.game_over()
            self.snakie.hit_wall.play()
        if self.snakie.body[0].y == TileSize or self.snakie.body[0].y == -1:
            self.game_over()
            self.snakie.hit_wall.play()
    
    def check_eatSELF(self):
        headless_snake = self.snakie.body[1:]
        if self.snakie.body[0] in headless_snake and self.powerUP == False:
            self.game_over()

    
    def game_over(self):
        self.ended = True
        self.snakie.reset()
        self.fruit.position = self.fruit.generRandomPos(self.snakie.body)
        self.state = "STOPPED"


        if self.score > the_HIGHscores["highestScore"]:
            the_HIGHscores["highestScore"] = self.score
            with open("highScores.json", "w", encoding="utf-8") as file:
                the_HIGHscores["highestScore"] = self.score
                data = the_HIGHscores
                json.dump(data, file, ensure_ascii=False)



        global SPEED
        SPEED = 140
        self.latestScore = self.score
        self.score = 0
        pygame.time.set_timer(SNAKE_UPDATE, SPEED)


        


    def draw_end(self):
        if self.paused == True or self.ended == True or self.started == True:
            self.state = "STOPPED"
            
        else:
            SPEED = 140
            if self.powerUP == True:
                SPEED -= 50
            if self.powerDOWN == True:
                SPEED += 50
            
            pygame.time.set_timer(SNAKE_UPDATE, SPEED)







#screen size
screen = pygame.display.set_mode((OFFSETWIDTH + SCREEN_WIDTH, OFFSETHEIGHT + SCREEN_HEIGHT))
pygame.display.set_caption("Snakie")



game = Game()
game.started = True

fruitSurface = pygame.image.load("test_fuit.jpg")
starSurface = pygame.image.load("powerup.jpg")
bombSurface = pygame.image.load("bomb.jpg")


lowbackSurface = pygame.image.load("LOWLAYER.png")
topbackSurface = pygame.image.load("smaller_over.png")



SNAKE_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SNAKE_UPDATE, SPEED)


#The game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == SNAKE_UPDATE:
            game.update()
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()


        if game.powerUP == True:
            if pygame.time.get_ticks() - game.powerUP_time > 4000:
                game.powerUP = False
                SPEED = 150
                pygame.time.set_timer(SNAKE_UPDATE, SPEED)

        if game.star.appeared == True:
            if pygame.time.get_ticks() - game.star.powerUP_timer > 6000:
                game.star.appeared = False
                game.star.noStar()
                game.star.position = game.star.generRandomPos(game.snakie.body)





        if game.powerDOWN == True:
            if pygame.time.get_ticks() - game.powerDOWN_time > 4000:
                game.powerDOWN = False
                SPEED = 150
                pygame.time.set_timer(SNAKE_UPDATE, SPEED)

        if game.bomb.appeared == True:
            if pygame.time.get_ticks() - game.bomb.powerDOWN_timer > 6000:
                game.bomb.appeared = False
                game.bomb.noStar()
                game.bomb.position = game.bomb.generRandomPos(game.snakie.body)




        if event.type == pygame.KEYDOWN:
            if game.state == "STOPPED":
                game.state = "RUNNING"
            if event.key == pygame.K_UP and game.snakie.direction != Vector2(0,1) and game.paused == False and game.ended == False and game.started == False:
                game.snakie.direction = Vector2(0,-1)
                game.snakie.move_neg.play()

            if event.key == pygame.K_DOWN and game.snakie.direction != Vector2(0,-1) and game.paused == False and game.ended == False and game.started == False:
                game.snakie.direction = Vector2(0,1)
                game.snakie.move_neg.play()
                

            if event.key == pygame.K_LEFT and game.snakie.direction != Vector2(1,0) and game.paused == False and game.ended == False and game.started == False:
                game.snakie.direction = Vector2(-1,0)
                game.snakie.move_pos.play()

            if event.key == pygame.K_RIGHT and game.snakie.direction != Vector2(-1,0) and game.paused == False and game.ended == False and game.started == False:
                game.snakie.direction = Vector2(1,0)
                game.snakie.move_pos.play()

            if event.key == pygame.K_ESCAPE:
                if game.paused == False:
                    game.paused = True
                    #screen.fill((255,0,0,150))
                else:
                    game.paused = False

            


    #snakie.update()


    #Frame rate and background
    clock.tick(60)
    screen.fill((255,255,255))
    screen.blit(lowbackSurface, (OFFSETLEFT, OFFSETTOP)) #background low
    screen.blit(topbackSurface, (0, 0)) #background top
    
    
    pygame.draw.rect(screen, (0, 0, 0), (OFFSETLEFT-2,OFFSETTOP-2, SCREEN_WIDTH + 4, SCREEN_HEIGHT + 4), 2) #the border
    
    #fruit.draw()
    #snakie.draw()

    game.draw()
    title_surface = titleFont.render("Snakie game - Paint", True, WHITE)
    score_surface = scoreFont.render(str(game.score), True, WHITE)
    highscore_surface = titleFont.render("Current Highscore: " + str(the_HIGHscores["highestScore"]), True, WHITE)

    screen.blit(title_surface, (45, 10))
    screen.blit(highscore_surface, (300, 10))
    screen.blit(score_surface, (SCREEN_WIDTH - 25, SCREEN_HEIGHT + OFFSETTOP + 48))


    if game.paused == True and game.started == False:
        s = pygame.Surface((1000,750))
        s.set_alpha(150)
        s.fill((255,255,255))
        screen.blit(s, (0,0))


        gamePaused_surface = nameFont.render("Game paused", True, TEXT)
        

        screen.blit(gamePaused_surface, (OFFSET + 160, 100))
        

        test_button.draw()




    if game.started == True:
        game.paused = True
        
        s = pygame.Surface((1000,750))
        s.set_alpha(150)
        s.fill((255,255,255))
        screen.blit(s, (0,0))


        gameName_surface = nameFont.render("Snakeie!", True, TEXT)
        gameStart_surface = scoreFont.render("Clcik to start!", True, TEXT)
        

        screen.blit(gameName_surface, (OFFSET + 220, 100))
        screen.blit(gameStart_surface, (OFFSET + 220, 355))
        

        test_button.draw()



    if game.ended == True:
        s = pygame.Surface((1000,750))
        s.set_alpha(150)
        s.fill((255,255,255))
        screen.blit(s, (0,0))


        gameOver_surface = nameFont.render("Game over", True, TEXT)
        currentScore_surface = scoreFont.render("Current score: " + str(game.latestScore), True, TEXT)
        currentHighscore_surface = scoreFont.render("Current Highscore: " + str(the_HIGHscores["highestScore"]), True, TEXT)

        screen.blit(gameOver_surface, (OFFSET + 200, 130))
        screen.blit(currentScore_surface, (OFFSET + 200, 200))
        screen.blit(currentHighscore_surface, (OFFSET + 200, 270))

        test_button.draw()
        
        
    


    pygame.display.flip()