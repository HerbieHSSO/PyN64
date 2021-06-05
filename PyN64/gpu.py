



import pygame







class GPU:
    def __init__(self):
        resolution = (640, 480)

        self.VRAM = [0] * 1000 # 4kB video ram
        
        self.screen = pygame.display.set_mode(resolution)
        pygame.init()
        
        pygame.display.update()































