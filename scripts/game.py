
import pygame
import time

from scripts.world import World
from scripts.player import Player
from scripts.window import Window
from scripts.camera import Camera
from scripts.enemy import Enemy

class Game:
    def __init__(self):
        pygame.init()
        self.window = Window((700,500),"Nea Project",60)
        self.camera = Camera()
        self.world = World(self.window.surface,self.camera,50)
        self.player = Player(self.world.rects[0].x+8*16,self.world.rects[0].y+16, 16, 16,self.window.surface,self.camera,[0,0])
        self.enemy = Enemy(self.world.rects[0].x+8*16,self.world.rects[0].y+16, 16, 16,self.world.graph,'assets/playerAnimations/idle/idle0.png',[0,0])
        self.player.setRectsToCollideWith(self.world.rects)
        self.camera.set_target(self.player)
    def update(self):
        self.camera.update()
        self.world.update()
        self.enemy.update(self.player,self.window.surface,self.camera.scroll,self.world.rects)
        self.player.update()
        self.window.update()
        
    def runGame(self):
        while True:
            self.update()
    

