import pygame

class Window:
    def __init__(self,windowSize,windowTitle,fps):
        self.windowSize = windowSize
        self.windowTitle = windowTitle
        self.fps = fps
        self.screen = pygame.display.set_mode(self.windowSize)
        pygame.display.set_caption(self.windowTitle)
        self.clock = pygame.time.Clock()
    def createNewSurface(self,size):
        return pygame.Surface(size)
    def update(self,surface):
        self.screen.blit(pygame.transform.scale(surface,self.windowSize),(0,0))
        # --- Limit to 60 frames per second
        pygame.display.update()
        self.clock.tick(self.fps)
        
        