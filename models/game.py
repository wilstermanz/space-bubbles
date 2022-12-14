import pygame
from models.player import Player
from models.laser import Laser

class Game:
    def __init__(self):
        """
        Initializes the game.

        This method creates a new `Player` sprite and adds it to the `player`
        sprite group.
        """
        from main import screen_width, screen_height

        player_sprite = Player((screen_width / 2, screen_height), 5)
        self.player = pygame.sprite.GroupSingle(player_sprite)

    def run(self):
        """
        Runs a single iteration of the game loop.

        This method updates the state of the player sprite, and then draws all
        sprite groups to the screen.
        """
        from main import screen

        # Update the player sprite
        self.player.update()

        # Draw all sprite groups to the screen
        self.player.draw(screen)

        # Draw the laser sprite group to the screen
        self.player.sprite.lasers.draw(screen)

        # update all sprite groups
        # draw all sprite groups
