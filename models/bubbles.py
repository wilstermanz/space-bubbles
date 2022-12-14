import pygame


class Bubble(pygame.sprite.Sprite):
    def __init__(self, color, x, y):
        super().__init__()
        self.color = color
        file_path = 'images/' + color + '_bubble.png'
        self.image = pygame.image.load(file_path).convert_alpha()
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self, speed, direction):
        self.rect.x += int(speed) * direction
