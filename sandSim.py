import pygame
import random as r
from copy import copy

pygame.init() # Setup
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Sand")
run = True
clock = pygame.time.Clock() # Helps limit frame rate

SAND = (194,178,128) # define colours
WHITE = (255,255,255)
BLACK = (0,0,0)

HUE = [255,200,15]


col = 100
rows = 100

brushSize = 3

w = int(SCREEN_WIDTH / col)
h = int(SCREEN_HEIGHT / rows)
screen.fill((0,0,0))

def changeHue(HUE, stage):
    if HUE[0] == 15:
        stage = 2
    if HUE[1] == 15:
        stage = 3
    if HUE[2] == 15:
        stage = 1

    if stage == 1:
        HUE[0] -= 1
        HUE[2] += 1
    if stage == 2:
        HUE[1] -= 1
        HUE[0] += 1
    if stage == 3:
        HUE[2] -= 1
        HUE[1] += 1
    return HUE, stage


def createGrid():
    grid = []
    for y in range(rows):
        grid.append([])
        grid[y] = [0] * col
        #grid.append([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,]) # for every row, create 10 columns
    return grid

grid = createGrid() # creates 2d array that holds sand values
nextGrid = createGrid()

        
def displaySand(w,h,col,rows,grid):
    for x in range(col):
        for y in range(rows):
            if grid[y][x] == 0: #square is empty
                pygame.draw.rect(screen,BLACK,(x*w,y*h,h,w))
            elif grid[y][x] != 0: # sand in position
                right = False
                left = False
                if y < rows - 1:
                    if grid[y+1][x] == 0:
                        nextGrid[y+1][x] = copy(grid[y][x])
                        nextGrid[y][x] = 0
                    else:
                        if x < col - 1:
                            if grid[y+1][x+1] == 0:
                                right = True
                        if x > 0:
                            if grid[y+1][x-1] == 0 and x > 0:
                                left = True
                        if left and right:
                            flip = r.randint(0,1)
                            if flip == 0:
                                right = False
                            if flip == 1:
                                left = False
                        if right:
                            nextGrid[y+1][x+1] = copy(grid[y][x])
                            nextGrid[y][x] = 0
                        if left:
                            nextGrid[y+1][x-1] = copy(grid[y][x])
                            nextGrid[y][x] = 0
                pygame.draw.rect(screen,grid[y][x],(x*w,y*h,h,w))
    return nextGrid


def findSquare(pos, w, h): # Function used to find exact square that has been clicked
    squareCount = 0
    for x in range(0,SCREEN_WIDTH,w):
        if pos[0] >= x and pos[0] < x+w: # Uses the even width sizes to determine which square has been clicked due to it being between two borders
            initialX = squareCount # Count of squares across
            squareCount = 0
            break
        else:
            squareCount += 1
    for y in range(0,SCREEN_HEIGHT, h):
        if pos[1] >= y and pos[1] < y+h:
            initialY = squareCount # Count of squares down
            break
        else:
            squareCount += 1
    return initialX,  initialY # Returns both coordinates

def clickedSand(brushMatrix):
    for i in brushMatrix:
        if grid[i[1]][i[0]] == 0:
            grid[i[1]][i[0]] = HUE

def expandBrush(coord, brushSize,col):
    cl = []
    for i in range(-1, brushSize-1):
        if (coord + i >= 0) and coord+i < col:
            cl.append(coord + i)
    return cl

def createMatrix(xcList, ycList):
    brushMatrix = []
    for y in ycList:
        for x in xcList:
            brushMatrix.append([x,y])
    return brushMatrix
    




    

    


mouseDown = False
stage = 3 # starting colour stage
while run:
    changedFrame = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouseDown = True
        elif event.type == pygame.MOUSEBUTTONUP:
            mouseDown = False
    if mouseDown == True:
        pos = pygame.mouse.get_pos()
        xc, yc = findSquare(pos,w,h)
        xcList = expandBrush(xc,brushSize,col)
        ycList = expandBrush(yc,brushSize,col)
        brushMatrix = createMatrix(xcList,ycList)
        clickedSand(brushMatrix)
        HUE, stage = changeHue(HUE,stage)
    grid = list(map(list,displaySand(w,h,col, rows, grid)))
    pygame.display.update()
    clock.tick(30)