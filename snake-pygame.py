
import pygame
import random
import sys
import math
import os
from pygame.locals import *

width  = 630
height = 630
size   = 42

pygame.init()
screen = pygame.display.set_mode((width, height))

clock = pygame.time.Clock()

current_path = os.path.dirname(__file__)
resource_path = os.path.join(current_path, 'sprite')

screen_rect = screen.get_rect()
image_orig = pygame.image.load(os.path.join(resource_path, 'head.png'))
body_img   = pygame.image.load(os.path.join(resource_path, 'body.png'))
fruit_img  = pygame.image.load(os.path.join(resource_path, 'fruit.png'))

angle = 0
done = False

class Box:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.s = 42
        self.xspeed = 0
        self.yspeed = 0
        self.angle = 0

    def update(self):
        self.x += self.xspeed
        self.y += self.yspeed

    def accel(self, px, py):
        self.xspeed = px
        self.yspeed = py

    def hit(self, other):
        posx = self.x - other.x
        posy = self.y - other.y

        dist  = math.sqrt((posx * posx) + (posy * posy))
        return dist < size

    def newpos(self):
        self.x = random.randrange(0, width, size )
        self.y = random.randrange(0, height, size)

    def display(self, img):
        global angle
        global image_rect

        #pygame.draw.rect(screen, (255, 0, 0), (self.x, self.y, 42, 42), 1)
        image = pygame.transform.rotate(img, self.angle)
        image_rect = image.get_rect(center= (self.x + 21, self.y + 21))
        screen.blit(image, image_rect)



snake = [Box(2 * size, 2 * size)]
fruit = Box(random.randrange(0, width, size), random.randrange(0, height, size));


def draw():

    keys = pygame.key.get_pressed()
    speed = 42

    if keys[pygame.K_LEFT ] and snake[0].xspeed == 0:
        snake[0].accel(-speed, 0 )
        snake[0].angle  = 0
        snake[0].angle -= 90


    if keys[pygame.K_RIGHT] and snake[0].xspeed == 0:
        snake[0].accel( speed, 0 )
        snake[0].angle  = 0
        snake[0].angle += 90
    if keys[pygame.K_UP   ] and snake[0].yspeed == 0:
        snake[0].accel( 0, -speed)
        snake[0].angle  = 0
        snake[0].angle += 180
    if keys[pygame.K_DOWN ] and snake[0].yspeed == 0:
        snake[0].accel( 0,  speed)
        snake[0].angle  = 0

    if fruit.hit(snake[0]):
        fruit.newpos()

    elif len(snake) > 2:
        snake.pop()

    oldx = snake[0].x
    oldy = snake[0].y

    addTail = Box(oldx, oldy)
    snake.insert(2, addTail)

    for i in range(3, len(snake)):
        snake[i].display(body_img)

    fruit.display(fruit_img)
    snake[0].display(image_orig)
    snake[0].update()

game = True
while game:
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False
            sys.exit

    draw()
    pygame.display.update()
    clock.tick(8)
