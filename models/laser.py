import pygame

class Laser(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.Surface((16, 16))
        self.image.fill((255, 255, 255))
        pygame.draw.circle(self.image, (0, 0, 0), pos, 8)
        self.rect = self.image.get_rect(center = pos)