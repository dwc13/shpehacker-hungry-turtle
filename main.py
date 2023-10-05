import pygame
import math
import random

##### PYGAME SETUP #####
pygame.init()
display = pygame.display.set_mode((1280, 720))
pygame.display.set_caption('Hungry Turtle')
clock = pygame.time.Clock()
running = True
dt = 0

##### OBJECTS #####
player_pos = pygame.Vector2(display.get_width() / 2, display.get_height() / 2)
turtle = pygame.image.load('turtle.png')
turtle = pygame.transform.scale(turtle, (80, 80))
turtle_width = turtle.get_size()[0]
turtle_height = turtle.get_size()[1]

##### GLOBAL VARS #####
SIZE = 40
MIN_SIZE = 20

##### FUNCTIONS #####
def turtle_display(pos_x, pos_y):
    display.blit(turtle, (pos_x-(turtle_width/2),pos_y-(turtle_height/2)))

##### DISPLAY LOOP #####
while running:
    ##### EVENTS
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # EXIT LOOP
            running = False

    ##### BACKGROUND
    display.fill("white")

    # update player position
    if int(pygame.time.get_ticks()/550%9) == 0:
        player_pos.x = random.randrange(0,display.get_width())
        player_pos.y = random.randrange(0,display.get_height())

    ##### SCALING CIRCLE
    # print(f'sin(tick): {math.sin(pygame.time.get_ticks()/250)}')
    # print(f'tick: {int(pygame.time.get_ticks()/250%9)}')
    rate = math.sin(pygame.time.get_ticks()/150)
    scale = rate * 5
    pygame.draw.circle(display, "cyan", player_pos, max(MIN_SIZE*scale, MIN_SIZE))

    ##### TURTLE
    turtle_display(player_pos.x, player_pos.y)

    ##### DISPLAY
    pygame.display.flip()
    dt = clock.tick(60) / 1000
##### EXIT LOOP #####
pygame.quit()