# Import a library of functions called 'pygame'
import pygame
import math,random
from math import pi
import numpy as np

# Initialize the game engine
pygame.init()

# Define the colors we will use in RGB format
BLACK = (0,   0,   0)
WHITE = (255, 255, 255)
BLUE = (0,   0, 255)
GREEN = (0, 255,   0)
RED = (255,   0,   0)

# Set the height and width of the screen
size = [800, 600]
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Example code for the draw module")

#Loop until the user clicks the close button.
done = False
clock = pygame.time.Clock()

streenwidth = 90
streen1 = [[0, 50], [150, 50], [150, 150], [
    250, 150], [250, 50], [350 + streenwidth, 50]]
streen2 = [[0, 50 + streenwidth], [150 - streenwidth, 50 + streenwidth],
           [150 - streenwidth, 150 + streenwidth], [250 + streenwidth, 150 + streenwidth], 
           [250 + streenwidth, 50 + streenwidth], [350 + streenwidth, 50 + streenwidth]]
playerwidth = 10
playerPoistion = [50,int((50+50+streenwidth)/2)]

boundary = []

def touch_boundary(poistion):
    left   = poistion[0] - streenwidth
    right  = poistion[0] + streenwidth
    up     = poistion[1] - streenwidth
    button = poistion[1] + streenwidth
    if poistion[0] in range(0, 60) or (poistion[0] in range(250 + streenwidth, 350 + streenwidth)):
        if poistion[1] in range(50, 50 + streenwidth):
            return True
        else:
            return False
    if poistion[0] in range(150 - streenwidth,150) or poistion[0] in range(250,250+streenwidth):
        if poistion[1] in range(50,150+streenwidth):
            return True
        else:
            return False
    if poistion[0] in range(150,250):
        if poistion[1] in range(150, 150 + streenwidth):
            return True
        else:
            return False
    if poistion[0] >= 350+streenwidth:
        return True
    else:
        return False
def change_dir(rad):
    return rad + random.randint(0,90)*([-1,1][random.randint(0,1)])

def next_poistion(cri,rad):
    x1 = cri[0] + 5 * math.cos(rad * pi/180)
    y1 = cri[1] + 5 * math.sin(rad * pi / 180)
    return [int(x1),int(y1)]


#每个小球的运动位置
poistions = []
#每个小球的运动方向
directions = []

for i in range(20):
    poistions.append([playerPoistion])
    directions.append([random.randint(0, 90), random.randint(270,360)][random.randint(0,1)])

step = 0

while not done:

    # This limits the while loop to a max of 10 times per second.
    # Leave this out and we will use all CPU we can.
    clock.tick(50)

    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            done = True  # Flag that we are done so we exit this loop


    # All drawing code happens after the for loop and but
    # inside the main while done==False loop.

    # Clear the screen and set the screen background
    screen.fill(WHITE)

    # Draw on the screen a GREEN line from (0,0) to (50.75)
    # 5 pixels wide.
    # pygame.draw.line(screen, GREEN, [0, 0], [50, 30], 5)

    # Draw on the screen a GREEN line from (0,0) to (50.75)
    # 5 pixels wide.
    pygame.draw.lines(screen, BLACK, False, streen1, 2)
    pygame.draw.lines(screen, BLACK, False, streen2, 2)
    # Draw on the screen a GREEN line from (0,0) to (50.75)
    # 5 pixels wide.
    # pygame.draw.aaline(screen, GREEN, [0, 50], [50, 80], True)

    # Draw a rectangle outline
    # pygame.draw.rect(screen, BLACK, [75, 10, 50, 20], 2)

    # # Draw a solid rectangle
    # pygame.draw.rect(screen, BLACK, [150, 10, 50, 20])

    # # Draw an ellipse outline, using a rectangle as the outside boundaries
    # pygame.draw.ellipse(screen, RED, [225, 10, 50, 20], 2)

    # # Draw an solid ellipse, using a rectangle as the outside boundaries
    # pygame.draw.ellipse(screen, RED, [300, 10, 50, 20])

    # This draws a triangle using the polygon command
    # pygame.draw.polygon(screen, BLACK, [[100, 100], [0, 200], [200, 200]], 5)

    # Draw an arc as part of an ellipse.
    # Use radians to determine what angle to draw.
    # pygame.draw.arc(screen, BLACK, [210, 75, 150, 125], 0, pi / 2, 2)
    # pygame.draw.arc(screen, GREEN, [210, 75, 150, 125], pi / 2, pi, 2)
    # pygame.draw.arc(screen, BLUE, [210, 75, 150, 125], pi, 3 * pi / 2, 2)
    # pygame.draw.arc(screen, RED,  [210, 75, 150, 125], 3 * pi / 2, 2 * pi, 2)

    # Draw a circle
    num = 0
    for i in range(len(poistions)):
        if poistions[i][-1] == False:
            pygame.draw.circle(screen, BLUE, poistions[i][-2], playerwidth)
            continue
        num += 1
        if step < len(poistions[i])-1:
            nepo = poistions[i][step]
            pygame.draw.circle(screen, BLUE, nepo, playerwidth)
        else:
            if type(poistions[i][-1]) != type([]):
                print(poistions[i])
                done = True
                break
            nepo = next_poistion(poistions[i][-1], directions[i])
            result = touch_boundary(nepo)
            #print(result)
            if 10 <= nepo[0] <= 790 and 10 <= nepo[1] <= 590 and result:
                pygame.draw.circle(screen, BLUE, nepo, playerwidth)
                poistions[i] += [nepo]
            else:
                pygame.draw.circle(screen, BLUE, poistions[i][-1], playerwidth)
                poistions[i] += [False]
                directions[i] = change_dir(directions[i])
    step += 1
    if num == 0:
        for j in range(len(poistions)):
            del poistions[j][-1]
        step = 0
    # Go ahead and update the screen with what we've drawn.
    # This MUST happen after all the other drawing commands.
    pygame.display.flip()

# Be IDLE friendly
pygame.quit()
