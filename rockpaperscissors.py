import pygame
import sys
import numpy as np
pygame.init()

screen_size = 600
icons_size = 30
pi = np.pi

velocity = 10       # speed at which objects move
nrock = 40          # initial number of rocks
npaper = 40         # intitial number of papers
nscissors = 15      # intiital number of scissors
number_of_objects = nrock + npaper + nscissors

# define the screen
screen = pygame.display.set_mode((screen_size, screen_size))
pygame.display.set_caption("Rock Paper Scissors war")

# import images
scissors = pygame.image.load("scissors.png")
scissors = pygame.transform.scale(scissors,(icons_size,icons_size))

paper = pygame.image.load("paper.png")
paper = pygame.transform.scale(paper,(icons_size,icons_size))

rock = pygame.image.load("rock.jpeg")
rock = pygame.transform.scale(rock,(icons_size,icons_size))

# randomly generate the positions and directios of the objects
positions = [ (np.random.randint(0,500), np.random.randint(0,500)) for i in range(number_of_objects) ]  # the (x,y) coordinates
directios = [ np.random.random()*pi for i in range(number_of_objects) ]                                 # direction of movement in radians
objects = [rock]*nrock + [paper]*npaper + [scissors]*nscissors                                          # types of objects

 
def GameStep(change_direction) :
    global positions
    global directios
    global objects
    screen.fill((255,255,255))

    updated_position = []
    for i in range(len(positions)):
        x, y = positions[i][0], positions[i][1]
        theta = directios[i]
        screen.blit(objects[i], (x,y))

        # move the object[i] in the direction of theta with given velocity
        x += np.cos(theta)*velocity
        y += np.sin(theta)*velocity
    
        # at regular intervals, change theta by a random amount
        if change_direction : 
            directios[i] *= ( np.random.random() - 0.5)
        
        # bouncing off of corners
        if ( (x <= 0 and y <= 0)
            or  ( x >= screen_size - icons_size and y <= 0) 
            or ( x >= screen_size - icons_size and y >= screen_size - icons_size  ) 
            or ( x <= 0 and y >= screen_size - icons_size  )  ) :
            directios[i] = pi + theta  

        # bouncing off of boundaries
        elif x >= screen_size - icons_size  :
            directios[i] = pi- theta    
        elif x <= 0 :
            directios[i] = pi- theta 
        elif y >= screen_size - icons_size :
            directios[i] = -theta
        elif y <= 0:
            directios[i] = -theta

        
        # the battles
        for j in range(len(positions)) :
            x1,y1 = positions[i] 
            x2,y2 = positions[j] 
            # find collisions 
            if abs(x1-x2)< 10 and abs(y1-y2) < 10 :
                obj1 = objects[i]
                obj2 = objects[j]

                # paper beats rock
                if ( obj1 == rock and obj2 == paper ) or ( obj2 == rock and obj1 == paper ) :
                    obj1 = paper
                    obj2 = paper
                # rock beats scisors
                if ( obj1 == rock and obj2 == scissors ) or ( obj2 == rock and obj1 == scissors ) :
                    obj1 = rock
                    obj2 = rock
                # scissors beat paper
                if ( obj1 == scissors and obj2 == paper ) or ( obj2 == scissors and obj1 == paper ) :
                    obj1 = scissors
                    obj2 = scissors

                objects[i] = obj1
                objects[j] = obj2
                break
        # update new position
        positions[i] = (x,y)

    pygame.display.update()



run = True
while run:
    pygame.time.delay(100) # in ms
    current_time = pygame.time.get_ticks()
    # randomly change direction of the objects after regular intervals
    change_direction = ( ( current_time % 10000 ) < 100 )

    GameStep(change_direction)
    
    # closing the screen when button "x" is clicked
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
