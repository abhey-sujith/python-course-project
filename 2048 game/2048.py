##xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx              
#                        2048 GAME
##xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

from pygame.locals import *
from random import randint

import pygame
import sys
import time
import math


TOTAL_POINTS =0


##xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
##xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx


# The below class if for making the board defining all its properties
class Board:
    #list for storing elements of board
    boards=[]
    x=0
    y=0

    #initialising the board with zeros and placing 2 numbers in random positions
    def __init__(self,x,y):
        self.x=x
        self.y=y

        for i in range(0,y):
            self.boards.append([])

        self.clearBoard()

        self.randomNumber()
        self.randomNumber()

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------

    #clearing all values of the board to zero
    def clear(self):
        for i in range(0, self.x):
            for j in range(0, self.y):
                self.boards[i][j]=0;



#----------------------------------------------------------------------------------------------------------------------------------------------------------------------

    #making a 2D list initially and storing all zeroes to it
    def clearBoard(self):
        for i in range(0, self.x):
            for j in range(0, self.y):
                self.boards[i].append(0);


#----------------------------------------------------------------------------------------------------------------------------------------------------------------------


    #code to print the score, and the nxn tiles of the game
    def printBoard(self, surf):
        global TOTAL_POINTS
        #drawing a rectangle so that score can be placed in it
        pygame.draw.rect(surf,(0,0,0),(10,10,230,40))
        score = pygame.font.SysFont("monospace", 30)
        labe2 = score.render("Score:" + str(TOTAL_POINTS), 1, (255, 255, 255))
        surf.blit(labe2, (30, 15))

        #drawing the nxn blocks
        for y in range(0, self.y):
            for x in range(0, self.x):
                block_image = pygame.image.load("images\\" + str(self.boards[y][x]) + ".png").convert()
                surf.blit(block_image, (10 + (60 * x), 60 + (60 * y)));


#----------------------------------------------------------------------------------------------------------------------------------------------------------------------


    #code to print the gameover screen which shows the score and if you want to play again it will prompt to press r
    def printGameoverScreen(self, surf):
        global TOTAL_POINTS
        myfont = pygame.font.SysFont("monospace", 20)
        scorefont = pygame.font.SysFont("monospace", 30)
        label = scorefont.render("Game Over!", 1, (255,255,255))
        label2 = scorefont.render("Score:" + str(TOTAL_POINTS), 1, (255,255,255))
        label3 = myfont.render("Press r to restart!", 1, (255,255,255))
        surf.blit(label, (40, 100))
        surf.blit(label2, (50, 150))
        surf.blit(label3, (10, 200))
        pygame.display.flip()
        #asking the user to press r to restart the game
        while(1):
            events = pygame.event.get()
            for event in events:
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if (event.type == pygame.KEYDOWN):
                    keys = event.key
                    if (keys == pygame.K_r):
                        return 1
        

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
               

    #code to make a random number if any tiles are free 
    def randomNumber(self):
        isZeroTilesAvailable = False
        #checking if any free tiles available
        for y in range(0, self.y):
            for x in range(0, self.x):
                if self.boards[y][x] == 0:
                    isZeroTilesAvailable = True
                    break;
        #if zero tiles if available then placing a random number on any random position in the board
        if isZeroTilesAvailable:
            x = randint(0,(self.x-1))
            y = randint(0,(self.y-1))

            while 1:
                if self.boards[y][x] == 0:
                    n = int(math.pow(2,randint(1,3)))
                    self.boards[y][x] = n
                    print("Put " + str(n) +", on block: " + str(x) + "," + str(y) + ".")
                    break
                else:
                    x = randint(0,3)
                    y = randint(0,3);
             


#------------------------------------------------------------------------------------------------------------------------------------------------------------------------


    #This is the code which shifts the numbers to the left when the left arrow key is pressed 
    def moveLeft(self, surf):
        print("Move Left")
        currVal=0
        global TOTAL_POINTS
        isMoved = False
	# We want to work column by column shifting up each element in turn.
        for y in range(0,self.y):
            for x1 in range(1,self.x):
                #checking the value at position y,x1 is a positive number
                if self.boards[y][x1] > 0:
                    currVal = self.boards[y][x1]
                    for x2 in range((x1-1),-1,-1):
                        #if current value and the tile close to it or the tile at position left of it is same the
                        #joint the blocks
                        #so 2+2=4 or 8+8=16
                        if currVal == self.boards[y][x2] and self.boards[y][(x2+1)] == self.boards[y][x2]:
                            print("Join the Block " + str(x2) + "," + str(y) + " with " + str((x2+1)) + "," + str(y))
                            self.boards[y][x2] = self.boards[y][x2] + currVal
                            self.boards[y][(x2+1)] = 0
                            #if merged currentvalue is added to total points
                            TOTAL_POINTS +=self.boards[y][x2]
                            isMoved = True
                            self.drawBlocks(x2,y,surf)
                            self.drawBlocks((x2+1),y,surf)
                            time.sleep (15.0 / 1000.0)
                            currVal = -1
                        #if the block close to current value is 0 the move the current value to the left
                        
                        elif self.boards[y][x2] == 0:
                            print("Move Block " + str(x2) + "," + str(y) + " to " + str((x2+1)) + "," + str(y))
                            self.boards[y][x2] = currVal
                            self.boards[y][(x2+1)] = 0
                            isMoved = True
                            self.drawBlocks(x2,y,surf)
                            self.drawBlocks((x2+1),y,surf)
                            time.sleep (15.0 / 1000.0)
        return isMoved;


#---------------------------------------------------------------------------------------------------------------------------------------------------------------------

    #code which shifts the numbers to the right when the right arrow key is pressed 
    def moveRight(self, surf):
        print("Move Right")
        currVal=0
        global TOTAL_POINTS
        isMoved = False
 
        for y in range(0,self.y):
            for x1 in range((self.x-2),-1,-1):
                if self.boards[y][x1] > 0:
                    currVal = self.boards[y][x1]
                    for x2 in range(x1+1,self.x):
                        if currVal == self.boards[y][x2] and self.boards[y][(x2-1)] == self.boards[y][x2]:
                            print("Join Block " + str(x2) + "," + str(y) + " with " + str((x2-1)) + "," + str(y))
                            self.boards[y][x2] = self.boards[y][x2] + currVal
                            self.boards[y][(x2-1)] = 0
                            TOTAL_POINTS +=self.boards[y][x2]
                            isMoved = True
                            self.drawBlocks(x2,y,surf)
                            self.drawBlocks((x2-1),y,surf)
                            time.sleep (15.0 / 1000.0)
                            currVal = -1
                        elif self.boards[y][x2] == 0:
                            print("Move Block " + str(x2) + "," + str(y) + " to " + str((x2-1)) + "," + str(y))
                            self.boards[y][x2] = currVal
                            self.boards[y][(x2-1)] = 0
                            isMoved = True;
                            self.drawBlocks(x2,y,surf)
                            self.drawBlocks((x2-1),y,surf)
                            time.sleep (15.0 / 1000.0)
        return isMoved;


#---------------------------------------------------------------------------------------------------------------------------------------------------------------------

    #code which shifts the numbers to up when the up arrow key is pressed 
    def moveUp(self, surf):
        print("Move Up");
        currVal=0
        global TOTAL_POINTS
        isMoved = False

        for x in range(0,self.x):
            for y1 in range(1,self.y):
                if self.boards[y1][x] > 0:
                    currVal = self.boards[y1][x]
                    for y2 in range((y1-1),-1,-1):
                        if currVal == self.boards[y2][x] and self.boards[(y2+1)][x] == self.boards[y2][x]:
                            print("Join Block " + str(x) + "," + str(y2) + " with " + str(x) + "," + str(y2 + 1))
                            self.boards[y2][x] = self.boards[y2][x] + currVal
                            self.boards[y2+1][x] = 0
                            TOTAL_POINTS +=self.boards[y2][x]
                            isMoved = True
                            self.drawBlocks(x,y2,surf)
                            self.drawBlocks(x,y2+1,surf)
                            time.sleep (15.0 / 1000.0)
                            currVal = -1
                        elif self.boards[y2][x] == 0:
                            print("Move Block " + str(x) + "," + str(y2) + " to " + str(x) + "," + str(y2+1))
                            self.boards[y2][x] = currVal
                            self.boards[(y2+1)][x] = 0
                            isMoved = True
                            self.drawBlocks(x,y2,surf)
                            self.drawBlocks(x,(y2+1),surf)
                            time.sleep (15.0 / 1000.0)
        return isMoved;


    
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------

    #code which shifts the numbers to down when the down arrow key is pressed 
    def moveDown(self, surf):
        print("Move Down");
        currVal=0
        global TOTAL_POINTS
        isMoved = False
        for x in range(0,self.x):
            for y1 in range((self.y-2),-1,-1):
                if self.boards[y1][x] > 0:
                    currVal = self.boards[y1][x]
                    for y2 in range(y1+1,self.y):
                        if currVal == self.boards[y2][x] and self.boards[(y2-1)][x] == self.boards[y2][x]:
                            print("Join Block " + str(x) + "," + str(y2) + " with " + str(x) + "," + str(y2-1))
                            self.boards[y2][x] = self.boards[y2][x] + currVal
                            self.boards[(y2-1)][x] = 0
                            TOTAL_POINTS +=self.boards[y2][x]
                            isMoved = True
                            self.drawBlocks(x,y2,surf)
                            self.drawBlocks(x,(y2-1),surf)
                            time.sleep (15.0 / 1000.0)
                            currVal = -1
                        elif self.boards[y2][x] == 0:
                            print("Move Block " + str(x) + "," + str(y2) + " to " + str(x) + "," + str(y2-1))
                            self.boards[y2][x] = currVal
                            self.boards[(y2-1)][x] = 0
                            isMoved = True;
                            self.drawBlocks(x,y2,surf)
                            self.drawBlocks(x,(y2-1),surf)
                            time.sleep (15.0 / 1000.0)
        
        return isMoved;
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------
    
    #code to update the block and the points when arrow keys are pressed
    def drawBlocks(self, x, y, surf):
        global TOTAL_POINTS
        pygame.draw.rect(surf,(0,0,0),(10,10,230,40))
        score = pygame.font.SysFont("monospace", 30)
        labe2 = score.render("Score:" + str(TOTAL_POINTS), 1, (255, 255, 255))
        surf.blit(labe2, (30, 15))
        block_image = pygame.image.load("images\\" + str(self.boards[y][x]) + ".png").convert()
        surf.blit(block_image, (10 + (60 * x), 60 + (60 * y)))
        pygame.display.flip()



#----------------------------------------------------------------------------------------------------------------------------------------------------------------------


    #code to check if game is over (no elements can be combined /elements close to each other are not same)
    def gameOver(self):
        for y in range(0, self.y):
            for x in range(0, self.x):
                if self.boards[y][x] == 0:
                    return False
                else:
                    if (y > 0):
                        if self.boards[(y-1)][x] == self.boards[y][x]:
                            return False
                    if (y < (self.y - 1)):
                        if self.boards[(y+1)][x] == self.boards[y][x]:
                            return False
                    if (x > 0):
                        if self.boards[y][x-1] == self.boards[y][x]:
                            return False
                    if (x < (self.x - 1)):
                        if self.boards[y][x+1] == self.boards[y][x]:
                            return False;
        return True;


##xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
##xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx


#This is the class where main execution happens
class App:
    #A window is created of size 250x300
    windowWidth = 250
    windowHeight = 300

    #creating a board of size 4x4
    def __init__(self):        
        self._running = True
        self._display_surf = None
        self.board = Board(4,4)

    #displaying the window with caption and icon
    def on_init(self):
        pygame.init();
        self._display_surf = pygame.display.set_mode((self.windowWidth, self.windowHeight), pygame.HWSURFACE)

        self._display_surf.fill((187,173,160))
        pygame.display.set_caption('2048')

        icon =pygame.image.load('images\\name.png')
        pygame.display.set_icon(icon)
        
        self._running = True

    #displaying the board 
    def on_render(self):
        self.board.printBoard(self._display_surf)
        pygame.display.flip()
        print(self.board.boards);


    def printGameOver(self):
        global TOTAL_POINTS
        self._display_surf.fill((187,173,160))
        r=self.board.printGameoverScreen(self._display_surf)
        pygame.display.flip()
        #if r is pressed the game is restarted
        if(r==1):
            TOTAL_POINTS=0
            self.board.clear()
            self.board.randomNumber()
            self.board.randomNumber()
            self.on_execute()


#----------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def on_execute(self):
        if self.on_init() == False:
            self._running = False;
        self.on_render()

        while(self._running):
            pygame.event.pump()

            events = pygame.event.get()
            for event in events:
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                    
                if (event.type == pygame.KEYDOWN):
                    keys = event.key
                
                    if (keys == pygame.K_RIGHT):
                        if (self.board.moveRight(self._display_surf)):
                            self.board.randomNumber()
                        
                    if (keys == pygame.K_LEFT):
                        if (self.board.moveLeft(self._display_surf)):
                            self.board.randomNumber()

                    if (keys == pygame.K_UP):
                        if (self.board.moveUp(self._display_surf)):
                            self.board.randomNumber()

                    if (keys == pygame.K_DOWN):
                        if (self.board.moveDown(self._display_surf)):
                            self.board.randomNumber()

                    if (keys == pygame.K_ESCAPE):
                        self._running = False

                    if (keys == pygame.K_r):
                        global TOTAL_POINTS
                        TOTAL_POINTS=0
                        self.board.clear()
                        self.board.randomNumber()
                        self.board.randomNumber()
                        

                    self.on_render()

                    if self.board.gameOver():
                        self._running = False;

            time.sleep (40.0 / 1000.0);
        self.printGameOver()
        

##xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
##xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx



if __name__ == "__main__":
    theApp = App()
    theApp.on_execute()





    
