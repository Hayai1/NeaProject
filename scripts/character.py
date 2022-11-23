import pygame
class Character:
    def __init__(self,x,y):
        self.left = False
        self.right = False
        self.triggerJump = False
        self.airTimer = 0
        self.velocity = [0,0]
        self.acceleration = [0,0]
        self.x = x
        self.y = y
        self.flip = False
        self.rect = pygame.Rect(self.x,self.y,16,16)
        self.animations = self.getAnimations()
    def draw(self,surface,scroll):
        img = self.animations.getImg()
        surface.blit(pygame.transform.flip(img,self.flip,False),(self.rect.x-scroll[0],self.rect.y-scroll[1]))
    def getCollisions(self,tiles):
        collisions = []
        for tile in tiles:
            if self.rect.colliderect(tile):
                collisions.append(tile)
        return collisions

    def updateVelocity(self):
        self.velocity[0] += self.acceleration[0]
        self.velocity[1] += self.acceleration[1]
        if self.left:
            self.velocity[0] -= 2
        if self.right:
            self.velocity[0] += 2
    def playerJump(self):
        if self.airTimer < 6:
            self.acceleration[1] = -5

    def move(self,rectsToCollide):
        collisionTypes = {'top':False,'bottom':False,'right':False,'left':False}
        if self.acceleration[1] < 3:
            self.acceleration[1] += 0.2
        self.updateVelocity()
        if self.triggerJump:
            self.playerJump()
        self.rect.x += self.velocity[0]
        collisions = self.getCollisions(rectsToCollide)
        for tile in collisions:
            if self.velocity[0] > 0:
                self.rect.right = tile.left
                collisionTypes['right'] = True
            elif self.velocity[0] < 0:
                self.rect.left = tile.right
                collisionTypes['left'] = True
        self.rect.y += self.velocity[1]
        collisions = self.getCollisions(rectsToCollide)
        for tile in collisions:
            if self.velocity[1] > 0:
                self.rect.bottom = tile.top
                collisionTypes['bottom'] = True
            elif self.velocity[1] < 0:
                self.rect.top = tile.bottom
                collisionTypes['top'] = True  
        if collisionTypes['bottom']:
            self.airTimer = 0
            self.acceleration = [0,0]
        elif collisionTypes['top']:
            self.acceleration = [0,0]
        else:
            self.airTimer += 1