# Wormy (a Nibbles clone)
# By Al Sweigart al@inventwithpython.com
# http://inventwithpython.com/pygame
# Released under a "Simplified BSD" license

import random, pygame, sys
import time
from pygame.locals import *
winner1 = 0
winner2 = 0   
winner3 = 0
FPS = 15
WINDOWWIDTH = 1200
WINDOWHEIGHT = 600
CELLSIZE = 20
assert WINDOWWIDTH % CELLSIZE == 0, "Window width must be a multiple of cell size."
assert WINDOWHEIGHT % CELLSIZE == 0, "Window height must be a multiple of cell size."
CELLWIDTH = int(WINDOWWIDTH / CELLSIZE)
CELLHEIGHT = int(WINDOWHEIGHT / CELLSIZE)

#             R    G    B
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
DARKRED = (155, 0, 0)
GREEN = (0, 255, 0)
DARKGREEN = (0, 155, 0)
DARKGRAY = (40, 40, 40)
PURPLE = (200, 0, 200)
DARKPURPLE = (128, 0, 128)
BLUE = (0, 0, 255)
DARKBLUE = (0, 0, 155)
YELLOW = (255, 255, 0)
DARKYELLOW = (155, 155, 0)
ORANGE = (255, 155, 0)
BGCOLOR = BLACK

imageapple = pygame.image.load("pictures/Apple.png")
imagewatermelon = pygame.image.load("pictures/watermelon.png")
headimg = pygame.image.load("pictures/head_snek.png")
bocht1img = pygame.image.load("pictures/snek_bocht_1.png")
bocht2img = pygame.image.load("pictures/snek_bocht_2.png")
bodyimg = pygame.image.load("pictures/snek_body.png")
tailimg = pygame.image.load("pictures/snek_tail.png")
head2img = pygame.image.load("pictures/head_2.png")
bocht3img = pygame.image.load("pictures/bocht_2.png")
body2img = pygame.image.load("pictures/body_2.png")
tail2img = pygame.image.load("pictures/tail_2.png")
imagebom = pygame.image.load("pictures/bom.png")
imageflashbang = pygame.image.load("pictures/flashbang.png")
worm1pictures = {"recht":{"RL": bodyimg, "LR": pygame.transform.rotate(bodyimg, 180), "OB": pygame.transform.rotate(bodyimg, 270), "BO": pygame.transform.rotate(bodyimg, 90)}, 
                 "hoofd":{"L": headimg, "R": pygame.transform.rotate(headimg, 180), "B": pygame.transform.rotate(headimg, 90), "O": pygame.transform.rotate(headimg, 270)},
                 "staart":{"L": tailimg, "R": pygame.transform.rotate(tailimg, 180), "B": pygame.transform.rotate(tailimg, 90), "O": pygame.transform.rotate(tailimg, 270)},
                 "bocht1":{"OL": bocht1img, "LB": pygame.transform.rotate(bocht1img, 270), "BR": pygame.transform.rotate(bocht1img, 180), "RO": pygame.transform.rotate(bocht1img, 90)},
                 "bocht2":{"LO": bocht2img, "OR": pygame.transform.rotate(bocht2img, 90), "RB": pygame.transform.rotate(bocht2img, 180), "BL": pygame.transform.rotate(bocht2img, 270)},
                }
worm2pictures = {"recht":{"horizontaal": body2img, "verticaal": pygame.transform.rotate(body2img, 90)},
                 "hoofd":{"L": head2img, "R": pygame.transform.rotate(head2img, 180), "B": pygame.transform.rotate(head2img, 90), "O": pygame.transform.rotate(head2img, 270)},
                 "staart":{ "L": tail2img, "R": pygame.transform.rotate(tail2img, 180), "B": pygame.transform.rotate(tail2img, 90), "O": pygame.transform.rotate(tail2img, 270)},
                 "bocht":{ "OL": bocht3img, "BL": pygame.transform.rotate(bocht3img, 270), "BR": pygame.transform.rotate(bocht3img, 180), "OR": pygame.transform.rotate(bocht3img, 90)}
                 }

UP = "up"
DOWN = "down"
LEFT = "left"
RIGHT = "right"

HEAD = 0  # syntactic sugar: index of the worm's head
HEAD2 = 0


def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    BASICFONT = pygame.font.Font("freesansbold.ttf", 18)
    pygame.display.set_caption("Snek")

    showStartScreen()
    while True:
        runGame()
        if (winner1 == 1):
            showGameOverScreen()
            
        elif (winner2 == 1):
            showGameOverScreen2()
        
        elif (winner3 == 1 or (winner1 == 1 and winner2 == 1)):
            showGameOverScreen3()


def runGame():
    # Set a random start point.
    startx = random.randint(5, CELLWIDTH - 6)
    starty = random.randint(5, CELLHEIGHT - 6)
    wormCoords = [
        {"x": startx,     "y": starty, "in": LEFT, "out": "head", "image":worm1pictures["hoofd"]["R"]},
        {"x": startx - 1, "y": starty, "in":LEFT, "out":RIGHT, "image":worm1pictures["recht"]["LR"]},
        {"x": startx - 2, "y": starty, "in":LEFT, "out": "tail", "image":worm1pictures["staart"]["R"]},
    ]
    direction = RIGHT
    
    startx2 = random.randint(5, CELLWIDTH - 6)
    starty2 = random.randint(5, CELLHEIGHT - 6)
    wormCoords2 = [
        {"x": startx2,     "y": starty2, "in": LEFT, "out": "head", "image":worm2pictures["hoofd"]["R"]},
        {"x": startx2 - 1, "y": starty2, "in":LEFT, "out":RIGHT, "image":worm2pictures["recht"]["horizontaal"]},
        {"x": startx2 - 2, "y": starty2, "in":LEFT, "out": "tail", "image":worm2pictures["staart"]["R"]},
    ]
    
    direction2 = RIGHT
    

    # Start the apple in a random place.
    apple = getRandomLocation()

    # Start the apple2 in a random place.
    watermelon = getRandomLocation()

    bom = getRandomLocation()

    bom2 = getRandomLocation()

    bom3 = getRandomLocation()

    bom4 = getRandomLocation()

    bom5 = getRandomLocation()

    flashbang = getRandomLocation()
    
    flashbangexplosion = getRandomLocation()

    startflash = 0 

    winner1 = 0
    winner2 = 0
    winner3 = 0

    while True:  # main game loop
        for event in pygame.event.get():  # event handling loop
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                if event.key == K_k and direction != RIGHT:
                    direction = LEFT
                elif event.key == K_m and direction != LEFT:
                    direction = RIGHT
                elif event.key == K_o and direction != DOWN:
                    direction = UP
                elif event.key == K_l and direction != UP:
                    direction = DOWN
                elif event.key == K_ESCAPE:
                    terminate()
                elif event.key == K_q and direction2 != RIGHT:
                    direction2 = LEFT
                elif event.key == K_d and direction2 != LEFT:
                    direction2 = RIGHT
                elif event.key == K_z and direction2 != DOWN:
                    direction2 = UP
                elif event.key == K_s and direction2 != UP:
                    direction2 = DOWN

        flashbangexplosion["x"] = 0
        flashbangexplosion["y"] = 0
                    
        # teleport to other side when hit wall
        if (
            wormCoords[HEAD]["x"] == -1
        ):
            # teleport worm to other side
            wormCoords[HEAD]["x"] =  CELLWIDTH -1
            
        elif( 
            wormCoords[HEAD]["x"] == CELLWIDTH 
        ):
            wormCoords[HEAD]["x"] = 0
            
        elif(
            wormCoords[HEAD]["y"] == -1
        ):
            # teleport worm to other side
            wormCoords[HEAD]["y"] = CELLHEIGHT -1
            
        elif(
            wormCoords[HEAD]["y"] == CELLHEIGHT
        ):
            wormCoords[HEAD]["y"] = 0
            
        if (
            wormCoords2[HEAD2]["x"] == -1
        ):
            # teleport worm to other side
            wormCoords2[HEAD2]["x"] = CELLWIDTH -1
            
        elif( 
            wormCoords2[HEAD2]["x"] == CELLWIDTH
        ):
            wormCoords2[HEAD2]["x"] = 0
            
        elif(
            wormCoords2[HEAD2]["y"] == -1
        ):
            # teleport worm to other side
            wormCoords2[HEAD2]["y"] = CELLHEIGHT -1
            
        elif(
            wormCoords2[HEAD2]["y"] == CELLHEIGHT
        ):
            wormCoords2[HEAD2]["y"] = 0
        
        for wormBody in wormCoords[1:]:
            if (
                wormBody["x"] == wormCoords2[HEAD2]["x"] and wormBody["y"] == wormCoords2[HEAD2]["y"]
            ):
                winner1 = 1
                showGameOverScreen()
                return # Player 1 wins
        
        for wormBody2 in wormCoords2[1:]:
            if (
                wormBody2["x"] == wormCoords[HEAD]["x"] and wormBody2["y"] == wormCoords[HEAD]["y"]
            ):
                winner2 = 1
                showGameOverScreen2()
                return # Player 2 wins  
    
        if (
            wormCoords[HEAD]["x"] == wormCoords2[HEAD2]["x"] and wormCoords[HEAD]["y"] == wormCoords2[HEAD2]["y"]
        ): 
            winner3 = 1
            showGameOverScreen3()
            return

        # check if worm has eaten an apply
        if wormCoords[HEAD]["x"] == apple["x"] and wormCoords[HEAD]["y"] == apple["y"]:
            # don't remove worm's tail segment
            apple = getRandomLocation()  # set a new apple somewhere
            bom = getRandomLocation()
            bom2 = getRandomLocation()
            bom3 = getRandomLocation()
            bom4 = getRandomLocation()
            bom5 = getRandomLocation()
            flashbang = getRandomLocation()
        # move the worm by adding a segment in the direction it is moving

        # check if worm has eaten an apply2
        elif wormCoords[HEAD]["x"] == watermelon["x"] and wormCoords[HEAD]["y"] == watermelon["y"]:
            # don't remove worm's tail segment
            watermelon = getRandomLocation()  # set a new apple somewhere
            
            if direction == UP:
                newHead = {"x": wormCoords[HEAD]["x"], "y": wormCoords[HEAD]["y"] - 1, "in":DOWN, "out":"head", "image":worm1pictures["hoofd"]["O"]}
                new2head = {"x": wormCoords[HEAD]["x"], "y": wormCoords[HEAD]["y"], "in":wormCoords[HEAD]["in"], "out":UP}
            elif direction == DOWN:
                newHead = {"x": wormCoords[HEAD]["x"], "y": wormCoords[HEAD]["y"] + 1, "in":UP, "out":"head", "image":worm1pictures["hoofd"]["B"]}
                new2head = {"x": wormCoords[HEAD]["x"], "y": wormCoords[HEAD]["y"], "in":wormCoords[HEAD]["in"], "out":DOWN}
            elif direction == LEFT:
                newHead = {"x": wormCoords[HEAD]["x"] - 1, "y": wormCoords[HEAD]["y"], "in":RIGHT, "out":"head", "image":worm1pictures["hoofd"]["L"]}
                new2head = {"x": wormCoords[HEAD]["x"], "y": wormCoords[HEAD]["y"], "in":wormCoords[HEAD]["in"], "out":LEFT}
            elif direction == RIGHT:
                newHead = {"x": wormCoords[HEAD]["x"] + 1, "y": wormCoords[HEAD]["y"], "in":LEFT, "out":"head", "image":worm1pictures["hoofd"]["R"]}
                new2head = {"x": wormCoords[HEAD]["x"], "y": wormCoords[HEAD]["y"], "in":wormCoords[HEAD]["in"], "out":RIGHT}

            if(wormCoords[len(wormCoords)-1]["out"]==RIGHT):
                wormCoords[len(wormCoords)-1]["image"] = worm1pictures["staart"]["R"]
            elif(wormCoords[len(wormCoords)-1]["out"]==LEFT):
                wormCoords[len(wormCoords)-1]["image"] = worm1pictures["staart"]["L"]
            elif(wormCoords[len(wormCoords)-1]["out"]==UP):
                wormCoords[len(wormCoords)-1]["image"] = worm1pictures["staart"]["O"]
            elif(wormCoords[len(wormCoords)-1]["out"]==DOWN):
                wormCoords[len(wormCoords)-1]["image"] = worm1pictures["staart"]["B"]
        
            if(new2head["in"]==LEFT and new2head["out"]==RIGHT):
                new2head["image"] = worm1pictures["recht"]["LR"]

            elif(new2head["in"]==RIGHT and new2head["out"]==LEFT):
                new2head["image"] = worm1pictures["recht"]["RL"]

            elif(new2head["in"]==UP and new2head["out"]==DOWN):
                new2head["image"] = worm1pictures["recht"]["BO"]

            elif(new2head["in"]==DOWN and new2head["out"]==UP):
                new2head["image"] = worm1pictures["recht"]["OB"]

            elif(new2head["in"]==DOWN and new2head["out"]==LEFT):
                new2head["image"] = worm1pictures["bocht1"]["OL"]
        
            elif(new2head["in"]==LEFT and new2head["out"]==UP):
                new2head["image"] = worm1pictures["bocht1"]["LB"]
        
            elif(new2head["in"]==UP and new2head["out"]==RIGHT):
                new2head["image"] = worm1pictures["bocht1"]["BR"]
        
            elif(new2head["in"]==RIGHT and new2head["out"]==DOWN):
                new2head["image"] = worm1pictures["bocht1"]["RO"]
        
            elif(new2head["in"]==LEFT and new2head["out"]==DOWN):
                new2head["image"] = worm1pictures["bocht2"]["LO"]

            elif(new2head["in"]==LEFT and new2head["out"]==DOWN):
                new2head["image"] = worm1pictures["bocht2"]["LO"]
        
            elif(new2head["in"]==DOWN and new2head["out"]==RIGHT):
                new2head["image"] = worm1pictures["bocht2"]["OR"]
        
            elif(new2head["in"]==RIGHT and new2head["out"]==UP):
                new2head["image"] = worm1pictures["bocht2"]["RB"]

            elif(new2head["in"]==UP and new2head["out"]==LEFT):
                new2head["image"] = worm1pictures["bocht2"]["BL"]
        
            if direction2 == UP:
                newHead2 = {"x": wormCoords2[HEAD2]["x"], "y": wormCoords2[HEAD2]["y"] - 1}
            elif direction2 == DOWN:
                newHead2 = {"x": wormCoords2[HEAD2]["x"], "y": wormCoords2[HEAD2]["y"] + 1}
            elif direction2 == LEFT:
                newHead2 = {"x": wormCoords2[HEAD2]["x"] - 1, "y": wormCoords2[HEAD2]["y"]}
            elif direction2 == RIGHT: 
                newHead2 = {"x": wormCoords2[HEAD2]["x"] + 1, "y": wormCoords2[HEAD2]["y"]}
            wormCoords.insert(0, newHead)
            wormCoords[1] = new2head
            bom = getRandomLocation()
            bom2 = getRandomLocation()
            bom3 = getRandomLocation()
            bom4 = getRandomLocation()
            bom5 = getRandomLocation()
            flashbang = getRandomLocation()
        elif wormCoords[HEAD]["x"] == bom["x"] and wormCoords[HEAD]["y"] == bom["y"]:
        
            showGameOverScreen2()
            return
        
        elif wormCoords[HEAD]["x"] == bom2["x"] and wormCoords[HEAD]["y"] == bom2["y"] and (len(wormCoords) > 13 or len(wormCoords2) > 13):
            showGameOverScreen2()
            return
        
        elif wormCoords[HEAD]["x"] == bom3["x"] and wormCoords[HEAD]["y"] == bom3["y"] and (len(wormCoords) > 18 or len(wormCoords2) > 18):
            showGameOverScreen2()
            return

        elif wormCoords[HEAD]["x"] == bom4["x"] and wormCoords[HEAD]["y"] == bom4["y"] and (len(wormCoords) > 23 or len(wormCoords2) > 23):
            showGameOverScreen2()
            return
        
        elif wormCoords[HEAD]["x"] == bom5["x"] and wormCoords[HEAD]["y"] == bom5["y"] and (len(wormCoords) > 28 or len(wormCoords2) > 28):
            showGameOverScreen2()
            return
        elif wormCoords[HEAD]["x"] == flashbang["x"] and wormCoords[HEAD]["y"] == flashbang["y"]:
            startflash = 1
            flashbang = getRandomLocation()
            bom = getRandomLocation()
            bom2 = getRandomLocation()
            bom3 = getRandomLocation()
            bom4 = getRandomLocation()
            bom5 = getRandomLocation()
            del wormCoords[-1]

        else:
            del wormCoords[-1]  # remove worm's tail segmen
 
        # check if worm has eaten an apply
        if wormCoords2[HEAD2]["x"] == apple["x"] and wormCoords2[HEAD2]["y"] == apple["y"]:
            # don't remove worm's tail segment
            apple = getRandomLocation()  # set a new apple somewhere
            bom = getRandomLocation()
            bom2 = getRandomLocation()
            bom3 = getRandomLocation()
            bom4 = getRandomLocation()
            bom5 = getRandomLocation()
            flashbang = getRandomLocation()
        # move the worm by adding a segment in the direction it is moving

        # check if worm has eaten an apply2
        elif wormCoords2[HEAD2]["x"] == watermelon["x"] and wormCoords2[HEAD2]["y"] == watermelon["y"]:
            # don't remove worm's tail segment
            watermelon = getRandomLocation()  # set a new apple somewhere
            
            if direction2 == UP:
                newHead2 = {"x": wormCoords2[HEAD2]["x"], "y": wormCoords2[HEAD2]["y"] - 1, "in":DOWN, "out":"head", "image":worm2pictures["hoofd"]["O"]}
                new2head2 = {"x": wormCoords2[HEAD2]["x"], "y": wormCoords2[HEAD2]["y"], "in":wormCoords2[HEAD2]["in"], "out":UP}
            elif direction2 == DOWN:
                newHead2 = {"x": wormCoords2[HEAD2]["x"], "y": wormCoords2[HEAD2]["y"] + 1, "in":UP, "out":"head", "image":worm2pictures["hoofd"]["B"]}
                new2head2 = {"x": wormCoords2[HEAD2]["x"], "y": wormCoords2[HEAD2]["y"], "in":wormCoords2[HEAD2]["in"], "out":DOWN}
            elif direction2 == LEFT:
                newHead2 = {"x": wormCoords2[HEAD2]["x"] - 1, "y": wormCoords2[HEAD2]["y"], "in":RIGHT, "out":"head", "image":worm2pictures["hoofd"]["L"]}
                new2head2 = {"x": wormCoords2[HEAD2]["x"], "y": wormCoords2[HEAD2]["y"], "in":wormCoords2[HEAD2]["in"], "out":LEFT}
            elif direction2 == RIGHT:
                newHead2 = {"x": wormCoords2[HEAD2]["x"] + 1, "y": wormCoords2[HEAD2]["y"], "in":LEFT, "out":"head", "image":worm2pictures["hoofd"]["R"]}
                new2head2 = {"x": wormCoords2[HEAD2]["x"], "y": wormCoords2[HEAD2]["y"], "in":wormCoords2[HEAD2]["in"], "out":RIGHT}

            if(wormCoords2[len(wormCoords2)-1]["out"]==RIGHT):
                wormCoords2[len(wormCoords2)-1]["image"] = worm2pictures["staart"]["R"]
            elif(wormCoords2[len(wormCoords2)-1]["out"]==LEFT):
                wormCoords2[len(wormCoords2)-1]["image"] = worm2pictures["staart"]["L"]
            elif(wormCoords2[len(wormCoords2)-1]["out"]==UP):
                wormCoords2[len(wormCoords2)-1]["image"] = worm2pictures["staart"]["O"]
            elif(wormCoords2[len(wormCoords2)-1]["out"]==DOWN):
                wormCoords2[len(wormCoords2)-1]["image"] = worm2pictures["staart"]["B"]
        
            if((new2head2["in"]==LEFT or new2head2["in"]==RIGHT) and (new2head2["out"]==LEFT or new2head2["out"]==RIGHT)): 
                new2head2["image"] = worm2pictures["recht"]["horizontaal"]
            
            if((new2head2["in"]==UP or new2head2["in"]==DOWN) and (new2head2["out"]==UP or new2head2["out"]==DOWN)):  
                new2head2["image"] = worm2pictures["recht"]["verticaal"]

            if((new2head2["in"]==UP or new2head2["in"]==RIGHT) and (new2head2["out"]==UP or new2head2["out"]==RIGHT)):  
                new2head2["image"] = worm2pictures["bocht"]["BR"]

            if((new2head2["in"]==DOWN or new2head2["in"]==LEFT) and (new2head2["out"]==DOWN or new2head2["out"]==LEFT)):  
                new2head2["image"] = worm2pictures["bocht"]["OL"]

            if((new2head2["in"]==LEFT or new2head2["in"]==UP) and (new2head2["out"]==LEFT or new2head2["out"]==UP)):  
                new2head2["image"] = worm2pictures["bocht"]["BL"]

            if((new2head2["in"]==DOWN or new2head2["in"]==RIGHT) and (new2head2["out"]==DOWN or new2head2["out"]==RIGHT)):  
                new2head2["image"] = worm2pictures["bocht"]["OR"]
            wormCoords2.insert(0, newHead2) 
            wormCoords2[1] = new2head2
            bom = getRandomLocation()
            bom2 = getRandomLocation()
            bom3 = getRandomLocation()
            bom4 = getRandomLocation()
            bom5 = getRandomLocation()
            flashbang = getRandomLocation()
        elif wormCoords2[HEAD2]["x"] == bom["x"] and wormCoords2[HEAD2]["y"] == bom["y"]:
        
            showGameOverScreen()
            return
        
        elif wormCoords2[HEAD2]["x"] == bom2["x"] and wormCoords2[HEAD2]["y"] == bom2["y"] and (len(wormCoords2) > 13 or len(wormCoords) > 13):
        
            showGameOverScreen()
            return
        
        elif wormCoords2[HEAD2]["x"] == bom3["x"] and wormCoords2[HEAD2]["y"] == bom3["y"] and (len(wormCoords2) > 18 or len(wormCoords) > 18):
        
            showGameOverScreen()
            return

        elif wormCoords2[HEAD2]["x"] == bom4["x"] and wormCoords2[HEAD2]["y"] == bom4["y"] and (len(wormCoords2) > 23 or len(wormCoords) > 23):
        
            showGameOverScreen()
            return

        elif wormCoords2[HEAD2]["x"] == bom5["x"] and wormCoords2[HEAD2]["y"] == bom5["y"] and (len(wormCoords2) > 28 or len(wormCoords) > 28):
        
            showGameOverScreen()
            return
        elif wormCoords2[HEAD2]["x"] == flashbang["x"] and wormCoords2[HEAD2]["y"] == flashbang["y"]:
            startflash = 1
            flashbang = getRandomLocation()
            bom = getRandomLocation()
            bom2 = getRandomLocation()
            bom3 = getRandomLocation()
            bom4 = getRandomLocation()
            bom5 = getRandomLocation()
            del wormCoords2[-1]

        else:
            del wormCoords2[-1]  # remove worm's tail segment
        
        # move the worm by adding a segment in the direction it is moving
        if direction == UP:
            newHead = {"x": wormCoords[HEAD]["x"], "y": wormCoords[HEAD]["y"] - 1, "in":DOWN, "out":"head", "image":worm1pictures["hoofd"]["O"]}
            new2head = {"x": wormCoords[HEAD]["x"], "y": wormCoords[HEAD]["y"], "in":wormCoords[HEAD]["in"], "out":UP}
        elif direction == DOWN:
            newHead = {"x": wormCoords[HEAD]["x"], "y": wormCoords[HEAD]["y"] + 1, "in":UP, "out":"head", "image":worm1pictures["hoofd"]["B"]}
            new2head = {"x": wormCoords[HEAD]["x"], "y": wormCoords[HEAD]["y"], "in":wormCoords[HEAD]["in"], "out":DOWN}
        elif direction == LEFT:
            newHead = {"x": wormCoords[HEAD]["x"] - 1, "y": wormCoords[HEAD]["y"], "in":RIGHT, "out":"head", "image":worm1pictures["hoofd"]["L"]}
            new2head = {"x": wormCoords[HEAD]["x"], "y": wormCoords[HEAD]["y"], "in":wormCoords[HEAD]["in"], "out":LEFT}
        elif direction == RIGHT:
            newHead = {"x": wormCoords[HEAD]["x"] + 1, "y": wormCoords[HEAD]["y"], "in":LEFT, "out":"head", "image":worm1pictures["hoofd"]["R"]}
            new2head = {"x": wormCoords[HEAD]["x"], "y": wormCoords[HEAD]["y"], "in":wormCoords[HEAD]["in"], "out":RIGHT}

        if(wormCoords[len(wormCoords)-1]["out"]==RIGHT):
            wormCoords[len(wormCoords)-1]["image"] = worm1pictures["staart"]["R"]
        elif(wormCoords[len(wormCoords)-1]["out"]==LEFT):
            wormCoords[len(wormCoords)-1]["image"] = worm1pictures["staart"]["L"]
        elif(wormCoords[len(wormCoords)-1]["out"]==UP):
            wormCoords[len(wormCoords)-1]["image"] = worm1pictures["staart"]["O"]
        elif(wormCoords[len(wormCoords)-1]["out"]==DOWN):
            wormCoords[len(wormCoords)-1]["image"] = worm1pictures["staart"]["B"]
        
        if(new2head["in"]==LEFT and new2head["out"]==RIGHT):
            new2head["image"] = worm1pictures["recht"]["LR"]

        elif(new2head["in"]==RIGHT and new2head["out"]==LEFT):
            new2head["image"] = worm1pictures["recht"]["RL"]

        elif(new2head["in"]==UP and new2head["out"]==DOWN):
            new2head["image"] = worm1pictures["recht"]["BO"]

        elif(new2head["in"]==DOWN and new2head["out"]==UP):
            new2head["image"] = worm1pictures["recht"]["OB"]

        elif(new2head["in"]==DOWN and new2head["out"]==LEFT):
            new2head["image"] = worm1pictures["bocht1"]["OL"]
        
        elif(new2head["in"]==LEFT and new2head["out"]==UP):
            new2head["image"] = worm1pictures["bocht1"]["LB"]
        
        elif(new2head["in"]==UP and new2head["out"]==RIGHT):
            new2head["image"] = worm1pictures["bocht1"]["BR"]
        
        elif(new2head["in"]==RIGHT and new2head["out"]==DOWN):
            new2head["image"] = worm1pictures["bocht1"]["RO"]
        
        elif(new2head["in"]==LEFT and new2head["out"]==DOWN):
            new2head["image"] = worm1pictures["bocht2"]["LO"]

        elif(new2head["in"]==LEFT and new2head["out"]==DOWN):
            new2head["image"] = worm1pictures["bocht2"]["LO"]
        
        elif(new2head["in"]==DOWN and new2head["out"]==RIGHT):
            new2head["image"] = worm1pictures["bocht2"]["OR"]
        
        elif(new2head["in"]==RIGHT and new2head["out"]==UP):
            new2head["image"] = worm1pictures["bocht2"]["RB"]

        elif(new2head["in"]==UP and new2head["out"]==LEFT):
            new2head["image"] = worm1pictures["bocht2"]["BL"]
        
        if direction2 == UP:
            newHead2 = {"x": wormCoords2[HEAD2]["x"], "y": wormCoords2[HEAD2]["y"] - 1, "in":DOWN, "out":"head", "image":worm2pictures["hoofd"]["O"]}
            new2head2 = {"x": wormCoords2[HEAD2]["x"], "y": wormCoords2[HEAD2]["y"], "in":wormCoords2[HEAD2]["in"], "out":UP}
        elif direction2 == DOWN:
            newHead2 = {"x": wormCoords2[HEAD2]["x"], "y": wormCoords2[HEAD2]["y"] + 1, "in":UP, "out":"head", "image":worm2pictures["hoofd"]["B"]}
            new2head2 = {"x": wormCoords2[HEAD2]["x"], "y": wormCoords2[HEAD2]["y"], "in":wormCoords2[HEAD2]["in"], "out":DOWN}
        elif direction2 == LEFT:
            newHead2 = {"x": wormCoords2[HEAD2]["x"] - 1, "y": wormCoords2[HEAD2]["y"], "in":RIGHT, "out":"head", "image":worm2pictures["hoofd"]["L"]}
            new2head2 = {"x": wormCoords2[HEAD2]["x"], "y": wormCoords2[HEAD2]["y"], "in":wormCoords2[HEAD2]["in"], "out":LEFT}
        elif direction2 == RIGHT:
            newHead2 = {"x": wormCoords2[HEAD2]["x"] + 1, "y": wormCoords2[HEAD2]["y"], "in":LEFT, "out":"head", "image":worm2pictures["hoofd"]["R"]}
            new2head2 = {"x": wormCoords2[HEAD2]["x"], "y": wormCoords2[HEAD2]["y"], "in":wormCoords2[HEAD2]["in"], "out":RIGHT}

        if(wormCoords2[len(wormCoords2)-1]["out"]==RIGHT):
            wormCoords2[len(wormCoords2)-1]["image"] = worm2pictures["staart"]["R"]
        elif(wormCoords2[len(wormCoords2)-1]["out"]==LEFT):
            wormCoords2[len(wormCoords2)-1]["image"] = worm2pictures["staart"]["L"]
        elif(wormCoords2[len(wormCoords2)-1]["out"]==UP):
            wormCoords2[len(wormCoords2)-1]["image"] = worm2pictures["staart"]["O"]
        elif(wormCoords2[len(wormCoords2)-1]["out"]==DOWN):
            wormCoords2[len(wormCoords2)-1]["image"] = worm2pictures["staart"]["B"]
        
        if((new2head2["in"]==LEFT or new2head2["in"]==RIGHT) and (new2head2["out"]==LEFT or new2head2["out"]==RIGHT)): 
            new2head2["image"] = worm2pictures["recht"]["horizontaal"]
        
        if((new2head2["in"]==UP or new2head2["in"]==DOWN) and (new2head2["out"]==UP or new2head2["out"]==DOWN)):  
            new2head2["image"] = worm2pictures["recht"]["verticaal"]

        if((new2head2["in"]==UP or new2head2["in"]==RIGHT) and (new2head2["out"]==UP or new2head2["out"]==RIGHT)):  
            new2head2["image"] = worm2pictures["bocht"]["BR"]

        if((new2head2["in"]==DOWN or new2head2["in"]==LEFT) and (new2head2["out"]==DOWN or new2head2["out"]==LEFT)):  
            new2head2["image"] = worm2pictures["bocht"]["OL"]

        if((new2head2["in"]==LEFT or new2head2["in"]==UP) and (new2head2["out"]==LEFT or new2head2["out"]==UP)):  
            new2head2["image"] = worm2pictures["bocht"]["BL"]

        if((new2head2["in"]==DOWN or new2head2["in"]==RIGHT) and (new2head2["out"]==DOWN or new2head2["out"]==RIGHT)):  
            new2head2["image"] = worm2pictures["bocht"]["OR"]
            
        wormCoords.insert(0, newHead)
        wormCoords[1] = new2head
        wormCoords2.insert(0, newHead2) 
        wormCoords2[1] = new2head2
        DISPLAYSURF.fill(BGCOLOR)
        drawGrid()
        drawWorm(wormCoords)
        drawWorm2(wormCoords2)
        drawApple(apple)
        drawWatermelon(watermelon)
        drawBom(bom)
        if (len(wormCoords) > 13 or len(wormCoords2) > 13):
            drawBom2(bom2)
        if (len(wormCoords) > 18 or len(wormCoords2) > 18):
            drawBom3(bom3)
        if (len(wormCoords) > 23 or len(wormCoords2) > 23):
            drawBom4(bom4)
        if (len(wormCoords) > 28 or len(wormCoords2) > 28):
            drawBom5(bom5)
        drawFlashbang(flashbang)
        if startflash >= 1 and startflash != 45:
            drawFlashbangexplosion(flashbangexplosion)
            startflash += 1
        drawScore(len(wormCoords) - 3)
        drawScore2(len(wormCoords2) -3)
        if (winner3 == 1 or (winner1 == 1 and winner2 == 1)):
            showGameOverScreen3()
            return
        elif (winner1 == 1):
            showGameOverScreen()
            return
            
        elif (winner2 == 1):
            showGameOverScreen2()
            return
        pygame.display.update()
        FPSCLOCK.tick(FPS)


def drawPressKeyMsg():
    pressKeySurf = BASICFONT.render("Press a key to play.", True, DARKGRAY)
    pressKeyRect = pressKeySurf.get_rect()
    pressKeyRect.topleft = (WINDOWWIDTH - 200, WINDOWHEIGHT - 30)
    DISPLAYSURF.blit(pressKeySurf, pressKeyRect)


def checkForKeyPress():
    if len(pygame.event.get(QUIT)) > 0:
        terminate()
    keyUpEvents = pygame.event.get(KEYUP)
    if len(keyUpEvents) == 0:
        return None
    if keyUpEvents[0].key == K_ESCAPE:
        terminate()
    return keyUpEvents[0].key


def showStartScreen():
    titleFont = pygame.font.Font("freesansbold.ttf", 100)
    titleSurf1 = titleFont.render("SnekTron!", True, WHITE)
    titleSurf2 = titleFont.render("SnekTron!", True, PURPLE)

    degrees1 = 0
    degrees2 = 0
    while True:
        DISPLAYSURF.fill(BGCOLOR)
        rotatedSurf1 = pygame.transform.rotate(titleSurf1, degrees1)
        rotatedRect1 = rotatedSurf1.get_rect()
        rotatedRect1.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)
        DISPLAYSURF.blit(rotatedSurf1, rotatedRect1)

        rotatedSurf2 = pygame.transform.rotate(titleSurf2, degrees2)
        rotatedRect2 = rotatedSurf2.get_rect()
        rotatedRect2.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)
        DISPLAYSURF.blit(rotatedSurf2, rotatedRect2)

        drawPressKeyMsg()

        if checkForKeyPress():
            pygame.event.get()  # clear event queue
            return
        pygame.display.update()
        FPSCLOCK.tick(FPS)
        degrees1 += 3  # rotate by 3 degrees each frame
        degrees2 += 7  # rotate by 7 degrees each frame


def terminate():
    pygame.quit() 
    sys.exit()


def getRandomLocation():
    return {
        "x": random.randint(0, CELLWIDTH - 1),
        "y": random.randint(0, CELLHEIGHT - 1),
    }

def showGameOverScreen3():
    gameOverFont = pygame.font.Font("freesansbold.ttf", 150)
    gameSurf = gameOverFont.render("TIE", True, RED)
    overSurf = gameOverFont.render("", True, RED)
    gameRect = gameSurf.get_rect()
    overRect = overSurf.get_rect()
    gameRect.midtop = (WINDOWWIDTH / 2, 10)
    overRect.midtop = (WINDOWWIDTH / 2, gameRect.height + 10 + 25)

    DISPLAYSURF.blit(gameSurf, gameRect)
    DISPLAYSURF.blit(overSurf, overRect)
    drawPressKeyMsg()
    pygame.display.update()
    pygame.time.wait(500)
    checkForKeyPress()  # clear out any key presses in the event queue

    while True:
        if checkForKeyPress():
            pygame.event.get()  # clear event queue
            return

def showGameOverScreen():
    gameOverFont = pygame.font.Font("freesansbold.ttf", 150)
    gameSurf = gameOverFont.render("PLAYER1", True, RED)
    overSurf = gameOverFont.render("WINS", True, RED)
    gameRect = gameSurf.get_rect()
    overRect = overSurf.get_rect()
    gameRect.midtop = (WINDOWWIDTH / 2, 10)
    overRect.midtop = (WINDOWWIDTH / 2, gameRect.height + 10 + 25)

    DISPLAYSURF.blit(gameSurf, gameRect)
    DISPLAYSURF.blit(overSurf, overRect)
    drawPressKeyMsg()
    pygame.display.update()
    pygame.time.wait(500)
    checkForKeyPress()  # clear out any key presses in the event queue

    while True:
        if checkForKeyPress():
            pygame.event.get()  # clear event queue
            return

def showGameOverScreen2():
    gameOverFont = pygame.font.Font("freesansbold.ttf", 150)
    gameSurf = gameOverFont.render("PLAYER2", True, RED)
    overSurf = gameOverFont.render("WINS", True, RED)
    gameRect = gameSurf.get_rect()
    overRect = overSurf.get_rect()
    gameRect.midtop = (WINDOWWIDTH / 2, 10)
    overRect.midtop = (WINDOWWIDTH / 2, gameRect.height + 10 + 25)

    DISPLAYSURF.blit(gameSurf, gameRect)
    DISPLAYSURF.blit(overSurf, overRect)
    drawPressKeyMsg()
    pygame.display.update()
    pygame.time.wait(500)
    checkForKeyPress()  # clear out any key presses in the event queue

    while True:
        if checkForKeyPress():
            pygame.event.get()  # clear event queue
            return

def drawScore(score):
    scoreSurf = BASICFONT.render("Score1: %s" % (score), True, RED)
    scoreRect = scoreSurf.get_rect()
    scoreRect.topleft = (WINDOWWIDTH - 130, 10)
    DISPLAYSURF.blit(scoreSurf, scoreRect)

def drawScore2(score2):
    scoreSurf = BASICFONT.render("Score2: %s" % (score2), True, RED)
    scoreRect = scoreSurf.get_rect()
    scoreRect.topleft = (WINDOWWIDTH - 130, 40)
    DISPLAYSURF.blit(scoreSurf, scoreRect)
    


def drawWorm(wormCoords):
    for coord in wormCoords:
        x = coord["x"] * CELLSIZE
        y = coord["y"] * CELLSIZE
        DISPLAYSURF.blit(coord["image"], (x,y))

def drawWorm2(wormCoords2):
    for coord in wormCoords2:
        x = coord["x"] * CELLSIZE
        y = coord["y"] * CELLSIZE
        DISPLAYSURF.blit(coord["image"], (x,y))



def drawApple(coord):
    x = coord["x"] * CELLSIZE
    y = coord["y"] * CELLSIZE
    DISPLAYSURF.blit(imageapple, (x,y))

def drawWatermelon(coord):
    x = coord["x"] * CELLSIZE
    y = coord["y"] * CELLSIZE
    DISPLAYSURF.blit(imagewatermelon, (x,y))

def drawBom(coord):
    x = coord["x"] * CELLSIZE
    y = coord["y"] * CELLSIZE
    DISPLAYSURF.blit(imagebom, (x,y))

def drawBom2(coord):
    x = coord["x"] * CELLSIZE
    y = coord["y"] * CELLSIZE
    DISPLAYSURF.blit(imagebom, (x,y))

def drawBom3(coord):
    x = coord["x"] * CELLSIZE
    y = coord["y"] * CELLSIZE
    DISPLAYSURF.blit(imagebom, (x,y))

def drawBom4(coord):
    x = coord["x"] * CELLSIZE
    y = coord["y"] * CELLSIZE
    DISPLAYSURF.blit(imagebom, (x,y))

def drawBom5(coord):
    x = coord["x"] * CELLSIZE
    y = coord["y"] * CELLSIZE
    DISPLAYSURF.blit(imagebom, (x,y))

def drawFlashbang(coord):
    x = coord["x"] * CELLSIZE
    y = coord["y"] * CELLSIZE
    DISPLAYSURF.blit(imageflashbang, (x,y))
    
def drawFlashbangexplosion(coord):
    x = coord["x"] * CELLSIZE
    y = coord["y"] * CELLSIZE
    FlashRect = pygame.Rect(x , y , CELLSIZE * WINDOWWIDTH, CELLSIZE * WINDOWHEIGHT)
    pygame.draw.rect(DISPLAYSURF, WHITE, FlashRect)

def drawGrid():
    for x in range(0, WINDOWWIDTH, CELLSIZE):  # draw vertical lines
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (x, 0), (x, WINDOWHEIGHT))
    for y in range(0, WINDOWHEIGHT, CELLSIZE):  # draw horizontal lines
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (0, y), (WINDOWWIDTH, y))


if __name__ == "__main__":
    main()

