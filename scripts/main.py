
import pygame
from world import World
from player import Player
from window import Window
from camera import Camera
from input import Input
BLACK = (0, 0, 0)

pygame.init()

window = Window((700,500),"Nea Project",60)
surface = window.createNewSurface((300,200))
world1 = World(50)
player1 = Player(0,0)
camera = Camera(player1)
input = Input()

# -------- Main Program Loop -----------
while True:
    window.screen.fill(BLACK)
    input.update(player1)
    camera.update()
    surface.fill(BLACK)
    world1.update(surface, camera)
    player1.update(world1,surface,camera)
    window.update(surface)
    

