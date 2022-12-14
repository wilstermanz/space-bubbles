import pygame
import random

# Color definitions to randomly change color of bullets
# White=1, Red=2, Green=3, Yellow=4, Blue=5
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, speed, screen_height, color):
        super().__init__()
        self.image = pygame.Surface((16, 16))
        self.image.fill(color)
        # pygame.draw.circle(self.image, (0, 0, 0), pos, 8)
        self.rect = self.image.get_rect(center = pos)
        self.speed = speed
        self.height_y_constraint = screen_height

    def destroy(self):
        """Destroyes laser sprites after they're off the window"""
        if self.rect.y <= -50 or self.rect.y >= self.height_y_constraint + 50:
            self.kill()

    def update(self):
        """Moves the laser sprites up"""
        self.rect.y += self.speed
        self.destroy()