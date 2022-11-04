
import pygame,threading,time
from world import World
from player import Player
import enemy
from enemy import *
import AITEST
from AITEST import *
WINDOW_SIZE = (700,500)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

pygame.init()
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()
surface = pygame.Surface((300,200))
worldgen = World(50)

 
done = False
true_scroll = [0,0]


PLAYER_W = 32
start = [0,0]
end = [0,0]
s = worldgen.WorldIn01
start[0] = (int(start[0])*32)+PLAYER_W
start[1] = (int(start[1])*32)+PLAYER_W/2
end[0] = (int(end[0])*32)+32
end[1] = (int(end[1])*32)+16
rects = []
for room in worldgen.rooms:
    for rect in room.rects:
        rects.append(rect)
player = Player(0,0,rects)
enemy1 = Player(start[1], start[0],rects)
enemyXVelocity = 0
playerXVelocity = 0
currentStep = 0
solveObj = solveClass()
solved = True
solve = threading.Thread(target=solveObj.solve, args=(s, (player.rect.y, player.rect.x), (end[0], end[1]),rects,))



# -------- Main Program Loop -----------
while not done:
    enemy1.triggerJump = False
    screen.fill(BLACK)
    #<--------------------------------move through Ai Path-------------------------->
    if (not solve.is_alive()):
        if (solveObj.path is not None and currentStep/NODE_THRESHOLD < len(solveObj.path)):
            if (solveObj.path[int(currentStep/NODE_THRESHOLD)].y < enemy1.rect.bottom):
                enemy1.triggerJump = True
            elif (enemy1.yVelocity < 0):
                enemy1.yVelocity = 0
            if (solveObj.path[int(currentStep/NODE_THRESHOLD)].x > enemy1.rect.center[0]):
                enemyXVelocity = MAX_SPEED
            elif (solveObj.path[int(currentStep/NODE_THRESHOLD)].x < enemy1.rect.center[0]):
                enemyXVelocity = -1*MAX_SPEED
            else:
                enemyXVelocity = 0
            currentStep += 1
        else:
            enemyXVelocity = 0
            nextSolve = True
    #<------------------------------------------------------------------------------->
    #<------------------------------solve for path----------------------------------->
    if nextSolve and player.inAggroRange(enemy1) and not player.inAttackRange(enemy1):
        solve = threading.Thread(target=solveObj.solve, 
                                args=(s, 
                                        (enemy1.rect.y, enemy1.rect.x), 
                                        (player.rect.y, player.rect.x)
                                    ,rects,))
        solve.start()
        currentStep = 0
        nextSolve = False
    #<------------------------------------------------------------------------------->
    # --- Main event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.left = True
            if event.key == pygame.K_RIGHT:
                player.right = True
            if event.key == pygame.K_UP:
                player.triggerJump = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                player.left = False
            if event.key == pygame.K_RIGHT:
                player.right= False
            if event.key == pygame.K_UP:
                player.triggerJump = False
                
    true_scroll[0] += (player.rect.x-true_scroll[0]-152)/20 
    true_scroll[1] += (player.rect.y-true_scroll[1]-106)/20
    scroll = true_scroll.copy()
    scroll[0] = int(scroll[0])
    scroll[1] = int(scroll[1])

    surface.fill(BLACK)
    for room in worldgen.rooms:
        surface.blit(room.roomImg,(room.x-scroll[0],room.y-scroll[1]))

    enemy1.move()
    player.move()
    player.drawPlayer(surface,scroll)
    enemy1.drawPlayer(surface,scroll)
    screen.blit(pygame.transform.scale(surface,WINDOW_SIZE),(0,0))
    
    # --- Limit to 60 frames per second
    pygame.display.update()
    clock.tick(60)
    
# Close the window and quit.
pygame.quit()