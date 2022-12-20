from datetime import timedelta
from models.bubbles import Bubble
from models.player import Player
import pygame
from pygame import time
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

        # Game state
        self.game_over = False
        self.start_time = time.get_ticks()
        self.current_time = timedelta(
            milliseconds=time.get_ticks() - self.start_time)
        self.score_clock = time.get_ticks()

        # Player setup
        player_sprite = Player((screen_width / 2, screen_height - 5), 5)
        self.player = pygame.sprite.GroupSingle(player_sprite)

        # Bubble setup
        self.bubbles = pygame.sprite.Group()
        self.bubbles_setup()
        self.bubbles_speed = 1
        self.bubbles_direction = 1

        # Player stats
        self.score = 0
        self.font = pygame.font.Font('fonts/default.ttf', 20)
        self.shots_fired = 0
        self.hits = 0
        self.hits_this_lvl = 0
        self.misses = 0
        self.level = 1

        # Audio
        self.bullet_sound = pygame.mixer.Sound('audio/laser.wav')
        self.bullet_sound.set_volume(0.3)
        self.pop_sound = pygame.mixer.Sound('audio/pop.wav')
        self.pop_sound.set_volume(0.5)
        self.splat_sound = pygame.mixer.Sound('audio/splat.wav')
        self.splat_sound.set_volume(0.8)

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
                      y_distance=60, x_offset=5, y_offset=30):
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
                            self.pop_sound.play()
                            self.hits += 1
                            self.hits_this_lvl += 1
                            self.score += 1000
                            bubble.kill()
                        else:
                            self.splat_sound.play()
                            self.misses += 1
                            if self.score >= 275:
                                self.score -= 275
                            else:
                                self.score = 0
                            self.bubbles_speed += 0.3

        # bubble player check
        for player in self.player:
            player_hit = pygame.sprite.spritecollide(
                player, self.bubbles, True)
            if player_hit:
                self.game_over = True

    def time_points(self):
        """Removes 10 points to score each second"""
        self.clock_check = time.get_ticks()
        if self.clock_check - self.score_clock >= 1000 and self.score >= 10:
            self.score -= 10
            self.score_clock = time.get_ticks()

    def display_score(self, screen):
        """Displays the current score on the screen"""
        score_surface = self.font.render(f'score: {self.score}', False, WHITE)
        score_rect = score_surface.get_rect(topleft=(10, 0))
        screen.blit(score_surface, score_rect)

    def display_hits(self, screen):
        """Displays the number of hits next to score"""
        from main import screen_width
        hits_surface = self.font.render(
            f'hits: {self.hits + 40 * (self.level - 1)}', False, WHITE)
        hits_rect = hits_surface.get_rect(topleft=(screen_width * (1 / 3), 0))
        screen.blit(hits_surface, hits_rect)

    def display_level(self, screen):
        """Displays the current level"""
        from main import screen_width
        level_surface = self.font.render(f'level: {self.level}', False, WHITE)
        level_rect = level_surface.get_rect(
            topright=(screen_width * (2 / 3), 0))
        screen.blit(level_surface, level_rect)

    def display_time(self, screen):
        from main import screen_width
        time_surface = self.font.render(
            f"{str(self.current_time)[2:-5]}", False, WHITE)
        time_rect = time_surface.get_rect(topright=(screen_width - 10, 0))
        screen.blit(time_surface, time_rect)

    def run(self):
        """
        Runs a single iteration of the game loop.

        This method updates the state of the player sprite, and then draws all
        sprite groups to the screen.
        """
        from main import screen
        from main import clock
        # Load background image
        bg_image = pygame.image.load('images/background.png')
        while self.game_over is False:

            # screen.fill(BLACK)
            screen.blit(bg_image, bg_image.get_rect())

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # If the user has clicked the 'x' in the top right corner,
                    # quit the game and exit the program
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return

            # Update the player sprite
            self.player.update()
            for player in self.player.sprites():
                self.shots_fired = player.shots_fired

            # Update the bubbles sprite
            self.bubbles.update(self.bubbles_speed, self.bubbles_direction)
            self.bubble_position_checker()

            # Draw all sprite groups to the screen
            self.player.sprite.bullets.draw(screen)
            self.player.draw(screen)
            self.bubbles.draw(screen)

            # Collisions
            self.collision_checks()

            # update points and time clock
            self.time_points()
            self.current_time = timedelta(
                milliseconds=time.get_ticks() - self.start_time)
            self.display_score(screen)
            self.display_hits(screen)
            self.display_time(screen)
            self.display_level(screen)

            # Update screen
            pygame.display.flip()
            clock.tick(60)

            # Start new level when all bubbles popped
            if self.hits_this_lvl % 40 == 0 and self.hits_this_lvl > 0:
                self.hits_this_lvl = 0
                self.level += 1
                self.bubbles_setup(5, 8, 60, 60, 5, 30)
                self.bubbles.draw(screen)
