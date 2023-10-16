import pygame
import random
import math
#import numpy as np
from pygame import mixer

pygame.init()

clock = pygame.time.Clock()

screen_width = 1600
screen_height = 800

screen = pygame.display.set_mode((screen_width, screen_height))

font = pygame.font.Font(None, 54)
GameLost_Font = pygame.font.Font(None, 300)
GameWon_Font = pygame.font.Font(None, 300)
bigfont = pygame.font.Font(None, 80)
smallfont = pygame.font.Font(None, 45)

pygame.display.set_caption("DodgeMaster")

#Global Variables
white = 255, 255, 255
gray = 169, 169, 169
frame = 0
running = True
gameover = False

def displayInfo():
    length_text = font.render(f'Length: {player.length}', True, (255, 255, 255))
    hp_text = font.render(f'Health: {player.hp}', True, (255, 0, 0))
    score_text = font.render(f'Score: {player.score}', True, (255, 255, 255))
    screen.blit(length_text, (10, 10))
    screen.blit(hp_text, (10, 60))
    screen.blit(score_text, (720, 10))

class Player:
    def __init__(self):
        self.y = 400
        self.x = 0
        self.y_change = 0
        self.x_change = 0
        self.move_right = False
        self.move_left = False
        self.move_up = False
        self.move_down = False
        self.speed = .5
        self.img = pygame.image.load("img/player.png")
        self.score = 0
        self.count = 10
        self.hp = 10
        self.length = 0
        self.hitbox = pygame.Rect(self.x, self.y, 32, 64)

    def updatePosition(self):
        self.x += self.x_change
        self.y += self.y_change
        self.hitbox.update(self.x, self.y, 32, 64)

    def display(self):
        screen.blit(self.img, (self.x, self.y))

    def checkIfOutOfBounds(self):
        if self.x <= 0:
            self.x = 0
        elif self.x >= 1600 - 64:
            self.x = 1600 - 64
        if self.y <= 0:
            self.y = 0
        if self.y >= 800 - 64:
            self.y = 800 - 64
        
class Enemy:
    enemyList = []
    speed = 0.45
    speedchange = 0.00002
    def updateSpeed():
        for enemy in Enemy.enemyList:
            Enemy.speed += Enemy.speedchange

    def __init__(self):
            self.y = random.randint(0,800-32)
            self.x = 1700
            self.img = pygame.image.load("img/enemy.png")
            self.hitbox = pygame.Rect(self.x, self.y, 32, 32)

    def display(self):
        screen.blit(self.img, (self.x, self.y))

    def updateX(self):
        self.x -= Enemy.speed
        self.hitbox.update(self.x, self.y, 32, 32)

#Collectables
class Apple:
    appleList = []
    def __init__(self):
        self.y = random.randint(0, screen_height - 50)
        self.x = random.randint(0, screen_width - 300)
        self.img = pygame.image.load("img/apple.png")
        self.hitbox = pygame.Rect(self.x, self.y, 32, 32)

    def display(self):
        screen.blit(self.img, (self.x, self.y))

class Goldenapple:
    goldenappleList = []
    speed = 0.20
    def __init__(self):
        self.y = -80
        self.x = random.randint(50, screen_width - 50)
        self.img = pygame.image.load("img/goldenapple.png")
        self.hitbox = pygame.Rect(self.x, self.y, 48, 48)

    def display(self):
        screen.blit(self.img, (self.x, self.y))

    def updateY(self):
        self.y += Goldenapple.speed
        self.hitbox.update(self.x, self.y, 48, 48)

class Tornado:
    tornadoList = []
    def __init__(self):
        self.y = random.randint(0, screen_height - 50)
        self.x = random.randint(0, screen_width - 300)
        self.img = pygame.image.load("img/tornado.png")
        self.hitbox = pygame.Rect(self.x, self.y, 32, 32)

    def display(self):
        screen.blit(self.img, (self.x, self.y))


goldenapple = Goldenapple()
tornado = Tornado()
player = Player()


Apple.appleList.append(Apple())
Apple.appleList.append(Apple())
Apple.appleList.append(Apple())

while running:
    
    if(frame % 80 == 0):
        if(gameover != True):
            Enemy.enemyList.append(Enemy())
            Enemy.updateSpeed()
            player.length += 1
    if(frame % 5000 == 0 and Goldenapple.goldenappleList.index != 0):
        if(gameover != True):
            goldenapple.updateY()
            Goldenapple.goldenappleList.append(Goldenapple())

    if(frame % 20000 == 0):
        Tornado.tornadoList.append(Tornado())

    screen.fill(gray)
            

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                player.move_left = True
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                player.move_right = True
            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                player.move_down = True
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                player.move_up = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                player.move_left = False
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                player.move_right = False
            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                player.move_down = False
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                player.move_up = False

    if player.move_left:
        player.x_change = -player.speed
    if player.move_right:
        player.x_change = player.speed
    if not player.move_left and not player.move_right:
        player.x_change = 0

    if player.move_up:
        player.y_change = -player.speed
    if player.move_down:
        player.y_change = player.speed
    if not player.move_up and not player.move_down:
        player.y_change = 0

    #goldenapple.display()
    for apple in Apple.appleList:
        apple.display()
    

    player.updatePosition()
    player.checkIfOutOfBounds()
    player.display()
    displayInfo()

    #collision Enemy
    for enemy in Enemy.enemyList:
        if(player.hitbox.colliderect(enemy.hitbox)):
            Enemy.enemyList.pop(Enemy.enemyList.index(enemy))
            player.hp -= 1
            collision_sound = \
            mixer.Sound \
            ("audio\\splat.mp3")
            collision_sound.play()

            if(player.hp <= 0):
                gameover = True
                Enemy.enemyList.clear()
                collision_sound = \
                mixer.Sound \
                ("audio\\loser.mp3")
                collision_sound.play()
    

        if(enemy.x <= -100):
            Enemy.enemyList.pop(Enemy.enemyList.index(enemy))
        enemy.display()
        enemy.updateX()

    #collision Apple
    for apple in Apple.appleList:
        if(player.hitbox.colliderect(apple.hitbox)):
            Apple.appleList.pop(Apple.appleList.index(apple))
            Apple.appleList.append(Apple())
            player.score += 1

            collision_sound = \
            mixer.Sound \
                ("audio/applesound.mp3")
            collision_sound.play()

            # +1
            if(player.score == 5):
                player.hp += 1
            elif(player.score == 10):
                player.hp += 1

    #collision Goldenapple
    for goldenapple in Goldenapple.goldenappleList:
        if(player.hitbox.colliderect(goldenapple.hitbox)):
            Goldenapple.goldenappleList.pop(Goldenapple.goldenappleList.index(goldenapple))
            player.score += 2

            collision_sound = \
            mixer.Sound \
                ("audio/goldenapplesound.mp3")
            collision_sound.play()


            # +1 health when scoring
            if(player.score == 5):
                player.hp += 1
            elif(player.score == 10):
                player.hp += 1
            
            #pop golden apple
        if(goldenapple.y <= -100):
            Goldenapple.goldenappleList.pop(Goldenapple.goldenappleList.index(goldenapple))
        goldenapple.display()
        goldenapple.updateY()

    #collision Tornado
    for tornado in Tornado.tornadoList:
        if(player.hitbox.colliderect(tornado.hitbox)):
            Tornado.tornadoList.pop(Tornado.tornadoList.index(tornado))
            Enemy.enemyList.clear()

            collision_sound = \
            mixer.Sound \
                ("audio/goldenapplesound.mp3")
            collision_sound.play()
            
        tornado.display()

    frame += 1
    pygame.display.update()
