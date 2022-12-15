from models.bubbles import Bubble
from models.player import Player
import pygame
import random
import sys

# Define Default Colors
WHITE = (202, 213, 218)
RED = (232, 53, 38)
GREEN = (87, 171, 65)
YELLOW = (250, 228, 25)
BLUE = (22, 114, 184)
BLACK = (30, 30, 30)


class Game:
    def __init__(self):
        """
        Initializes the game.

        This method creates a new `Player` sprite and adds it to the `player`
        sprite group.
        """
        from main import screen_width, screen_height

        self.game_over = False
        # Player setup
        player_sprite = Player((screen_width / 2, screen_height), 5)
        self.player = pygame.sprite.GroupSingle(player_sprite)

        # Bubble setup
        self.bubbles = pygame.sprite.Group()
        self.bubbles_setup()
        self.bubbles_speed = 1.5
        self.bubbles_direction = 1

    def rand_color_picker(self):
        """Picks a random color for bubbles"""
        color_number = random.randint(1, 5)
        if color_number == 1:
            color = 'white'
        elif color_number == 2:
            color = 'red'
        elif color_number == 3:
            color = 'green'
        elif color_number == 4:
            color = 'yellow'
        else:
            color = 'blue'
        return color

    def bubbles_setup(self, rows=5, cols=8, x_distance=60,
                      y_distance=60, x_offset=5, y_offset=15):
        """
        Creates an array of bubbles that are ready to be popped.

        Bubbles colors are randomly chosen
        """
        for row_index, row in enumerate(range(rows)):
            for col_index, col in enumerate(range(cols)):
                x = col_index * x_distance + x_offset
                y = row_index * y_distance + y_offset
                bubble_sprite = Bubble(self.rand_color_picker(), x, y)
                self.bubbles.add(bubble_sprite)

    def bubble_position_checker(self):
        from main import screen_width, screen_height

        all_bubbles = self.bubbles.sprites()
        for bubble in all_bubbles:
            if bubble.rect.right >= screen_width:
                self.bubbles_direction = -1
                self.bubbles_drop()
            if bubble.rect.left <= 0:
                self.bubbles_direction = 1
                self.bubbles_drop()
            if bubble.rect.bottom >= screen_height:
                self.game_over = True

    def bubbles_drop(self, drop=2):
        if self.bubbles:
            for bubble in self.bubbles.sprites():
                bubble.rect.y += drop

    def collision_checks(self):
        # player bullets pop bubbles
        if self.player.sprite.bullets:
            for bullet in self.player.sprite.bullets:
                pops = pygame.sprite.spritecollide(bullet, self.bubbles, False)
                if pops:
                    bullet.kill()
                    for bubble in pops:
                        if bubble.color == bullet.color:
                            bubble.kill()
                        else:
                            self.bubbles_speed *= 1.1

        # bubble player check
        for player in self.player:
            player_hit = pygame.sprite.spritecollide(
                player, self.bubbles, True)
            if player_hit:
                print("fuck you suck")
                self.game_over = True

    def run(self):
        """
        Runs a single iteration of the game loop.

        This method updates the state of the player sprite, and then draws all
        sprite groups to the screen.
        """
        from main import screen
        from main import clock
        while self.game_over is False:

            screen.fill(BLACK)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # If the user has clicked the 'x' in the top right corner,
                    # quit the game and exit the program
                    pygame.quit()
                    sys.exit()

            # Update the player sprite
            self.player.update()

            # Update the bubbles sprite
            self.bubbles.update(self.bubbles_speed, self.bubbles_direction)
            self.bubble_position_checker()

            # Draw all sprite groups to the screen
            self.player.sprite.bullets.draw(screen)
            self.player.draw(screen)

            self.bubbles.draw(screen)

            # Collisions
            self.collision_checks()

            pygame.display.flip()
            clock.tick(60)
