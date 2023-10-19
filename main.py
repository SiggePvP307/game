import pygame
import random
from pygame import mixer

pygame.init()

clock = pygame.time.Clock()

screen_width = 1920
screen_height = 1020

screen = pygame.display.set_mode((screen_width, screen_height))


font = pygame.font.Font(None, 54)
GameLost_Font = pygame.font.Font(None, 300)
GameWon_Font = pygame.font.Font(None, 300)
bigfont = pygame.font.Font(None, 80)
smallfont = pygame.font.Font(None, 35)

pygame.display.set_caption("DodgeMaster")

# Global Variables
white = 255, 255, 255
gray = 169, 169, 169
blue = 0, 191, 255
black = 0, 0, 0
lightred = 240, 128, 128
limegreen = 50, 205, 50
yelloworange = 255, 214, 51
frame = 0
running = True
gameover = False


def displayInfo():
    length_text = font.render(
        f'Length: {player.length}', True, (255, 255, 255))
    hp_text = smallfont.render(f'HP', True, (255, 0, 0))
    score_text = font.render(f'Score: {player.score}', True, (255, 255, 255))
    level_text = font.render(f'Level: {levelbar.level}', True, (blue))
    xp_text = font.render(f'Experience: {levelbar.xp}', True, (black))
    screen.blit(length_text, (10, 10))
    screen.blit(hp_text, (10, 60))
    screen.blit(score_text, (1920/2 - 80, 10))
    screen.blit(level_text, (1920/2 - 95, 900))
    screen.blit(xp_text, (475 - 0, 945))


class LevelBar():
    def __init__(self):
        self.x = 1920/2 - (400/2)
        self.y = 950
        self.w = 400
        self.h = 25
        self.xp = 0
        self.level = 0
        self.maxlevel = 100

    def draw(self, surface):
        level_ratio = self.xp / self.maxlevel
        pygame.draw.rect(screen, black, pygame.Rect(
            self.x, self.y, self.w, self.h))
        pygame.draw.rect(screen, yelloworange, pygame.Rect(
            self.x, self.y, self.w * level_ratio, self.h))

    def levelUp(self, remainxp):
        self.level += 1
        self.xp = 0
        self.xp += remainxp

    def checkIfLevelUp(self):
        if (self.xp >= 100):
            self.levelUp(self.xp - self.maxlevel)


class HealthBar():
    def __init__(self):
        self.x = 53
        self.y = 59
        self.w = 400
        self.h = 25
        self.hp = 10
        self.maxhp = 10

    def draw(self, surface):
        hp_ratio = self.hp / self.maxhp
        pygame.draw.rect(screen, lightred, pygame.Rect(
            self.x, self.y, self.w, self.h))
        pygame.draw.rect(screen, limegreen, pygame.Rect(
            self.x, self.y, self.w * hp_ratio, self.h))

    def checkIfHpEmpty(self):
        if (self.xp >= 100):
            self.levelUp(self.xp - self.maxlevel)


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
        self.speed = 0.7
        self.img = pygame.image.load("img/player.png")
        self.count = 10
        self.score = 0
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
        if self.x <= -16:
            self.x = -16
        elif self.x >= 1920 - 48:
            self.x = 1920 - 48
        if self.y <= 175:
            self.y = 175
        if self.y >= 816:
            self.y = 816


class Enemy:
    list = []
    speed = 0.45
    speedchange = 0.00002

    def updateSpeed():
        for enemy in Enemy.list:
            Enemy.speed += Enemy.speedchange

    def __init__(self):
        self.y = random.randint(175, 850)
        self.x = 1920
        self.img = pygame.image.load("img/enemy.png")
        self.hitbox = pygame.Rect(self.x, self.y, 32, 32)

    def display(self):
        screen.blit(self.img, (self.x, self.y))

    def updateX(self):
        self.x -= Enemy.speed
        self.hitbox.update(self.x, self.y, 32, 32)


class Collectables:

    def __init__(self):
        self.apple = self.Apple()
        self.goldenapple = self.Goldenapple()
        self.tornado = self.Tornado()

    class Apple:
        list = []

        def __init__(self):
            self.y = random.randint(175, 840)
            self.x = random.randint(0, screen_width - 300)
            self.img = pygame.image.load("img/apple.png")
            self.hitbox = pygame.Rect(self.x, self.y, 32, 32)

        def display(self):
            screen.blit(self.img, (self.x, self.y))

        def playSound(self):
            collision_sound = \
                mixer.Sound("audio/applesound.mp3")
            collision_sound.play()

    class Goldenapple:
        list = []
        speed = 0.15

        def __init__(self):
            self.y = 175
            self.x = random.randint(200, screen_width - 50)
            self.img = pygame.image.load("img/goldenapple.png")
            self.hitbox = pygame.Rect(self.x, self.y, 48, 48)

        def display(self):
            screen.blit(self.img, (self.x, self.y))

        def updateY(self):
            self.y += collectables.goldenapple.speed
            self.hitbox.update(self.x, self.y, 48, 48)

        def playSound(self):
            collision_sound = \
                mixer.Sound("audio/goldenapplesound.mp3")
            collision_sound.play()

    class Tornado:
        list = []

        def __init__(self):
            self.y = random.randint(250, 850)
            self.x = random.randint(0, screen_width - 300)
            self.img = pygame.image.load("img/tornado.png")
            self.hitbox = pygame.Rect(self.x, self.y, 32, 32)

        def display(self):
            screen.blit(self.img, (self.x, self.y))

        def playSound(self):
            collision_sound = \
                mixer.Sound("audio/goldenapplesound.mp3")
            collision_sound.play()


collectables = Collectables()
player = Player()
levelbar = LevelBar()
healthbar = HealthBar()

# First Append to start showing

check = "false"
while running:
    screen.fill(gray)

    # Black bars
    pygame.draw.rect(screen, black, pygame.Rect(0, 165, 1920, 10))
    pygame.draw.rect(screen, black, pygame.Rect(0, 880, 1920, 10))

    # Level
    levelbar.draw(screen)
    healthbar.draw(screen)
    levelbar.checkIfLevelUp()

    # HP

    if (frame == 3000):
        collectables.apple.list.append(collectables.Apple())
        collectables.apple.list.append(collectables.Apple())
        collectables.apple.list.append(collectables.Apple())
        collectables.apple.list.append(collectables.Apple())
        collectables.apple.list.append(collectables.Apple())

    if (frame % 80 == 0):
        if (gameover != True):
            Enemy.list.append(Enemy())
            Enemy.updateSpeed()
            player.length += 1
    if (frame % 5000 == 0):
        collectables.Goldenapple().list.append(collectables.Goldenapple())

    if (frame % 20000 == 0):
        collectables.tornado.list.append(collectables.tornado)

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

    # collision Enemy
    for enemy in Enemy.list:
        if (player.hitbox.colliderect(enemy.hitbox)):
            Enemy.list.pop(Enemy.list.index(enemy))
            healthbar.hp -= 1
            collision_sound = \
                mixer.Sound("audio\\splat.mp3")
            collision_sound.play()

            if (healthbar.hp <= 0):
                gameover = True
                Enemy.list.clear()
                collision_sound = \
                    mixer.Sound("audio\\loser.mp3")
                collision_sound.play()

        if (enemy.x <= -100):
            Enemy.list.pop(Enemy.list.index(enemy))
        enemy.display()
        enemy.updateX()

    # collision Apple
    for apple in collectables.apple.list:
        if (player.hitbox.colliderect(apple.hitbox)):
            collectables.apple.list.pop(collectables.apple.list.index(apple))
            collectables.apple.list.append(collectables.Apple())
            player.score += 1
            levelbar.xp += 2

            collectables.apple.playSound()

        apple.display()

    # collision Goldenapple
    for goldenapple in collectables.goldenapple.list:
        if (player.hitbox.colliderect(goldenapple.hitbox)):
            collectables.goldenapple.list.pop(
                collectables.goldenapple.list.index(goldenapple))
            player.score += 2
            levelbar.xp += 10

            collectables.goldenapple.playSound()

            # pop golden apple
        if (goldenapple.y > 837):
            collectables.goldenapple.list.pop(
                collectables.goldenapple.list.index(goldenapple))
        goldenapple.display()
        goldenapple.updateY()

    # collision Tornado
    for tornado in collectables.tornado.list:
        if (player.hitbox.colliderect(tornado.hitbox)):
            collectables.tornado.list.pop(
                collectables.tornado.list.index(tornado))

            Enemy.list.clear()
            collectables.tornado.playSound()

        tornado.display()

    frame += 1
    pygame.display.update()
