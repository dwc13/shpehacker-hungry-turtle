import pygame
import math
import random
import cv2
import numpy as np

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

##### MODEL #####
net = cv2.dnn.readNet("yolov3.weights", "yolov3.cfg")
classes = ['circle', 'turtle']
# classes = []
# with open("9k.names", "r") as f:
#     classes = [line.strip() for line in f.readlines()]

##### GLOBAL VARS #####
SIZE = 40
MIN_SIZE = 20

food_change = False
food_pos = pygame.Vector2(random.randrange(40,display.get_width()),
                            random.randrange(40,display.get_height()))

##### FUNCTIONS #####
def turtle_display(pos_x, pos_y):
    display.blit(turtle, (pos_x-(turtle_width/2),pos_y-(turtle_height/2)))

def detect(display):
    pygame.image.save(display, "display-image.png")
    cv_img = cv2.imread('display-image.png')
    cv_img_h, cv_img_w, _ = cv_img.shape
    blob = cv2.dnn.blobFromImage(cv_img, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
    net.setInput(blob)
    layer_names = net.getLayerNames()
    output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()] 
    outs = net.forward(output_layers)
    for out in outs:
        for detection in out:
            print(detection)
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.05:
                # Object detected
                center_x = int(detection[0] * cv_img_w)
                center_y = int(detection[1] * cv_img_h)
                w = int(detection[2] * cv_img_w)
                h = int(detection[3] * cv_img_h)

                # Rectangle coordinates
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)

                cv2.rectangle(cv_img, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(cv_img, f"{classes[class_id]} {int(confidence * 100)}%",
                             (x, y + 30), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 2)
    cv2.imshow("Image", cv_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

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

    ##### IF FOOD ATE THEN MAKE NEW ONE
    if food_change:
        food_pos = pygame.Vector2(random.randrange(40,display.get_width()),
                                  random.randrange(40,display.get_height()))
        food_change = False

    ##### SCALING CIRCLE
    # print(f'sin(tick): {math.sin(pygame.time.get_ticks()/250)}')
    # print(f'tick: {int(pygame.time.get_ticks()/250%9)}')
    # rate = math.sin(pygame.time.get_ticks()/150)
    # scale = rate * 5
    # pygame.draw.circle(display, "cyan", player_pos, max(MIN_SIZE*scale, MIN_SIZE))

    ##### CHECK TURTLE CAN EAT🍖
    if food_pos.x - 40 >= player_pos.x < food_pos.x + 40 and \
        food_pos.y - 40 >= player_pos.y < food_pos.y + 40:
        food_change = True 

    ##### TURTLE
    turtle_display(player_pos.x, player_pos.y)

    ##### FOOD
    pygame.draw.circle(display, "black", food_pos, max(MIN_SIZE, MIN_SIZE))

    detect(display=display)
    ##### DISPLAY
    pygame.display.flip()
    dt = clock.tick(60) / 1000
##### EXIT LOOP #####
pygame.quit()