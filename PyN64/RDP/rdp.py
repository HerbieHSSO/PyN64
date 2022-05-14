


import pygame
from pygame.surface import Surface





class RDP:
    def __init__(self):
        pygame.init()
        
        self.screen_resolution = (640, 480)


        self.width = self.screen_resolution[0]
        self.height = self.screen_resolution[1]

        self.black = (0, 0, 0)
        
        
        self.screen = pygame.display.set_mode(self.screen_resolution)

    def set_title(self, title: str):
        pygame.display.set_caption(title)

    def draw(self):
        self.screen.fill(self.black)
        pygame.draw.rect(self.screen, (255, 255, 255), (20, 10, 20, 20))

        pygame.display.flip()
