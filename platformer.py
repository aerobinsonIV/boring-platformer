import pygame

gameHeight = 900
gameWidth = 1600

pygame.init()
gameDisplay = pygame.display.set_mode((gameWidth, gameHeight))
pygame.display.set_caption('Jousboxx')
clock = pygame.time.Clock()

jousImg = pygame.image.load('jousboxx.png')
jousHeight = 80
jousWidth = 40

#colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
blue = (100, 100, 255)
yellow = (255, 255, 100)
green = (100, 255, 100)

#key variables
leftKey = False
rightKey = False
upKey = False
downKey = False

#pos variables
x = 400
y = 400

#speed/acceleration variables
accel = 2
deccel = 0.5
topSpeed = 20

#map/block stuff
blkSize = 100
curBlkX = 0
curBlkY = 0

checkCornerCollisions = False

#map
blkMap = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1],
    [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]


horizontalEdgeState = 0 # -1 = off left edge, 0 = within current block, 1 = off right edge
verticalEdgeState = 0 # -1 = off top edge, 0 = within current block, 1 = off bottom edge

xSpeed = 0
ySpeed = 0

onGround = True
facingRight = True

dead = False

def jousboxx(x, y):
    if facingRight:
        gameDisplay.blit(pygame.transform.flip(jousImg, True, False), (x, y))
    else:
        gameDisplay.blit(jousImg, (x, y))

def drawBlock(x, y, color):
    pygame.draw.rect(gameDisplay, color, [x * blkSize, y * blkSize, blkSize, blkSize])

def bc(blockCoord): #converts block coordinates into pixel/global game coordinates
    return blockCoord * blkSize
    

while not dead:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

        #Key press handling
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                leftKey = True
            elif event.key == pygame.K_RIGHT:
                rightKey = True
            elif event.key == pygame.K_UP:
                upKey = True
            elif event.key == pygame.K_DOWN:
                downKey = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                leftKey = False
            elif event.key == pygame.K_RIGHT:
                rightKey = False
            elif event.key == pygame.K_UP:
                upKey = False
            elif event.key == pygame.K_DOWN:
                downKey = False
    
    gameDisplay.fill(white)


    #keypresses to acceleration
    if leftKey:
        facingRight = False
        xSpeed -= accel
        if xSpeed < -topSpeed:
            xSpeed = -topSpeed
    if rightKey:
        facingRight = True
        xSpeed += accel
        if xSpeed > topSpeed:
            xSpeed = topSpeed
    if upKey and onGround:
        ySpeed = -30
    if downKey:
        ySpeed += accel
        if ySpeed > topSpeed:
            ySpeed = topSpeed

    #gravity
    ySpeed += 1

    #actual motion
    x += xSpeed
    y += ySpeed

    #decceleration
    if abs(xSpeed) < deccel:
        xSpeed = 0
    elif xSpeed > 0:
        xSpeed -= deccel
    elif xSpeed < 0:
        xSpeed += deccel

    if abs(ySpeed) < deccel:
        ySpeed = 0
    elif ySpeed > 0:
        ySpeed -= deccel
    elif ySpeed < 0:
        ySpeed += deccel
    

    #screen edges
    if x > (gameWidth - jousWidth):
        x = gameWidth - jousWidth
        xSpeed = 0
    elif x < 0:
        x = 0
        xSpeed = 0

    if y > (gameHeight - jousHeight):
        y = gameHeight - jousHeight
    elif y < 0:
        y = 0    

    #determine what block we are primarily in
    curBlkX = int((x + jousWidth / 2) // blkSize)
    curBlkY = int((y + jousHeight / 2) // blkSize)

    onGround = False

    #horizontal edge crossing detection
    if x < curBlkX * blkSize:
        horizontalEdgeState = -1
    elif x + jousWidth > curBlkX * blkSize + blkSize:
        horizontalEdgeState = 1
    else:
        horizontalEdgeState = 0

    #vertical edge crossing detection
    if y < curBlkY * blkSize:
        verticalEdgeState = -1
    elif y + jousHeight > curBlkY * blkSize + blkSize:
        verticalEdgeState = 1
    else:
        verticalEdgeState = 0

    #vertical collision detection
    if verticalEdgeState == -1:
        #test for top edge collision
        if blkMap[curBlkY - 1][curBlkX] == 1:
            ySpeed = 0
            y = bc(curBlkY - 1) + blkSize
            verticalEdgeState = 0

    elif verticalEdgeState == 1:
        #test for bottom edge collision
        if blkMap[curBlkY + 1][curBlkX] == 1:
            ySpeed = 0
            y = bc(curBlkY + 1) - jousHeight
            verticalEdgeState = 0
            onGround = True

    #horizontal collision detection
    if horizontalEdgeState == -1:
        #test for left edge collision
        if blkMap[curBlkY][curBlkX - 1] == 1:
            xSpeed = 0
            x = bc(curBlkX - 1) + blkSize
            horizontalEdgeState = 0

    elif horizontalEdgeState == 1:
        #test for right edge collision
        if blkMap[curBlkY][curBlkX + 1] == 1:
            xSpeed = 0
            x = bc(curBlkX + 1) - jousWidth
            horizontalEdgeState = 0

    #Do we need to check for a corner collision?
    if abs(horizontalEdgeState) + abs(verticalEdgeState) > 1:
        checkCornerCollisions = True
    else:
        checkCornerCollisions = False

    #check horizontal corner collisions if necessary
    if checkCornerCollisions:
        if verticalEdgeState == 1:
            #bottom corner
            if horizontalEdgeState == 1:
                #bottom right corner
                if blkMap[curBlkY + 1][curBlkX + 1] == 1:
                    x = bc(curBlkX + 1) - jousWidth
                    if xSpeed > 0:
                        xSpeed = 0
                    horizontalEdgeState = 0
            else:
                #bottom left corner
                if blkMap[curBlkY + 1][curBlkX - 1] == 1:
                    x = bc(curBlkX - 1) + blkSize
                    if xSpeed < 0:
                        xSpeed = 0
                    horizontalEdgeState = 0
        else:
            #top corner
            if horizontalEdgeState == 1:
                #top right corner
                if blkMap[curBlkY - 1][curBlkX + 1] == 1:
                    x = bc(curBlkX + 1) - jousWidth
                    if xSpeed > 0:
                        xSpeed = 0
                    horizontalEdgeState = 0
            else:
                #top left corner
                if blkMap[curBlkY - 1][curBlkX - 1] == 1:
                    x = bc(curBlkX - 1) + blkSize
                    if xSpeed < 0:
                        xSpeed = 0
                    horizontalEdgeState = 0
                       
    #Do we still need to check for a corner collision or did we already fix it? (skip if we didn't need to check in the first place)
    if abs(horizontalEdgeState) + abs(verticalEdgeState) > 1 and checkCornerCollisions == True:
        checkCornerCollisions = True
    else:
        checkCornerCollisions = False
    
    if abs(horizontalEdgeState) + abs(verticalEdgeState) > 1: #Check for vertical corner collisions if necessary
        if verticalEdgeState == 1:
            #bottom corner
            if horizontalEdgeState == 1:
                #bottom right corner
                if blkMap[curBlkY + 1][curBlkX + 1] == 1:
                    y = bc(curBlkY + 1) - jousHeight
                    ySpeed = 0
                    onGround = True
            else:
                #bottom left corner
                if blkMap[curBlkY + 1][curBlkX - 1] == 1:
                    y = bc(curBlkY + 1) - jousHeight
                    ySpeed = 0
                    onGround = True
        else:
            #top corner
            if horizontalEdgeState == 1:
                #top right corner
                if blkMap[curBlkY - 1][curBlkX + 1] == 1:
                    y = bc(curBlkY - 1) + blkSize
                    ySpeed = 0           
            else:
                #top left corner
                if blkMap[curBlkY - 1][curBlkX - 1] == 1:
                    y = bc(curBlkY - 1) + blkSize
                    ySpeed = 0


    #render map
    for row in range(0, 9):
        for col in range(0, 16):
            if blkMap[row][col] == 1:
                drawBlock(col, row, black)    

    jousboxx(x, y)

    pygame.display.update()
    clock.tick(60)



