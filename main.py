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
    score_text = font.render(f'Length: {player.length}', True, (255, 255, 255))
    hp_text = font.render(f'Health: {player.hp}', True, (255, 0, 0))
    screen.blit(score_text, (10, 10))
    screen.blit(hp_text, (10, 60))


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
        self.hp = 3
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



player = Player()

while running:
    if(frame % 80 == 0):
        if(gameover != True):
            Enemy.enemyList.append(Enemy())
            Enemy.updateSpeed()
            player.length += 1
            screen


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

    player.updatePosition()
    player.checkIfOutOfBounds()
    player.display()
    displayInfo()
    for enemy in Enemy.enemyList:
        
        if(player.hitbox.colliderect(enemy.hitbox)):
            Enemy.enemyList.pop(Enemy.enemyList.index(enemy))
            player.hp -= 1
            if(player.hp <= 0):
                gameover = True
                Enemy.enemyList.clear()
            

        if(enemy.x <= -100):
            Enemy.enemyList.pop(Enemy.enemyList.index(enemy))
        enemy.display()
        enemy.updateX()

    frame += 1
    pygame.display.update()
