import pygame
import random
from models.bullet import Bullet

# Color definitions to randomly change color of bullets
# White=1, Red=2, Green=3, Yellow=4, Blue=5
WHITE = (202, 213, 218)
RED = (232, 53, 38)
GREEN = (87, 171, 65)
YELLOW = (250, 228, 25)
BLUE = (22, 114, 184)
BLACK = (30, 30, 30)


class Player(pygame.sprite.Sprite):
    """
    Defines the player sprite and its behavior.

    The player is represented by a red rectangle. The user can move the player
    left and right using the left and right arrow keys, and shoot a bullet
    using the space bar. The player sprite is bound by the left and right
    edges of the screen, and bullets can only be shot once every 600ms.
    """
    # Class attributes
    player_width = 60
    player_height = 20
    player_color = RED

    def __init__(self, pos, speed):
        """
        Initializes the player sprite.

        Args:
            pos: A tuple specifying the (x, y) position of the player sprite.
            speed: An integer specifying the speed at which the player
            sprite moves.
        """
        # Call the `__init__()` method of the superclass
        # (`pygame.sprite.Sprite`)
        super().__init__()

        # Create a new surface representing the player sprite
        self.image = pygame.Surface([self.player_width, self.player_height])

        # Set the position of the player sprite to the given position
        self.image.fill(self.player_color)
        self.rect = self.image.get_rect(midbottom=pos)

        # Set the speed of the player sprite to the given speed
        self.speed = speed

        # Set the initial state of the player sprite's bullet
        self.ready = True           # Bullets can be fired when True
        self.bullet_time = 0
        self.bullet_cooldown = 600  # Bullets can be shot every 600ms

        # Bring in the laser
        self.bullets = pygame.sprite.Group()

    def update_player_color(self):
        """Updates player color"""
        next_color_number = random.randint(1, 5)
        if next_color_number == 1:
            next_color = WHITE
        elif next_color_number == 2:
            next_color = RED
        elif next_color_number == 3:
            next_color = GREEN
        elif next_color_number == 4:
            next_color = YELLOW
        else:
            next_color = BLUE
        self.image.fill(next_color)
        self.player_color = next_color

    def get_input(self):
        """
        Gets input from the user and updat  es the state of the player sprite
        accordingly.
        """
        # Get the keys that are currently being pressed
        keys = pygame.key.get_pressed()

        # If the right arrow key is being pressed, move the player sprite to
        # the right
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed

        # If the left arrow key is being pressed, move the player sprite to
        # the left
        elif keys[pygame.K_LEFT]:
            self.rect.x -= self.speed

        # If the space bar is being pressed and the player sprite is ready to
        # fire a bullet, shoot a bullet and start the bullet recharge timer
        if keys[pygame.K_SPACE] and self.ready:
            self.shoot_bullet()
            self.ready = False
            self.bullet_time = pygame.time.get_ticks()

    def recharge(self):
        """
        Checks if a bullet has been fired, and recharges the player sprite's
        bullet if the bullet cooldown time has been reached.
        """
        # Check if a bullet has been fired
        if self.ready is not True:
            # Get the current time
            current_time = pygame.time.get_ticks()

            # Check if the bullet cooldown time has been reached
            if current_time - self.bullet_time >= self.bullet_cooldown:
                # Recharge the player sprite's bullet
                self.ready = True

    def constraint(self):
        """
        Constrains the player sprite's position to the left and right edges of
        the screen.
        """
        # Import the `screen_width` variable from the `main` module
        from main import screen_width

        # If the player sprite's left edge is less than or equal to 0, set the
        # left edge to 0
        if self.rect.left <= 0:
            self.rect.left = 0

        # If the player sprite's right edge is greater than or equal to the
        # screen width, set the right edge to the screen width
        if self.rect.right >= screen_width:
            self.rect.right = screen_width

    # def get_color(self):
    #     return self.color

    def shoot_bullet(self):
        """
        Shoots a bullet
        """
        text = "COLOR"
        bullet_speed = -8
        self.bullets.add(Bullet(self.rect.center,
                                bullet_speed,
                                self.rect.bottom,
                                self.player_color
                                )
                         )
        # Pew
        self.update_player_color()
        print('Pew but with ', end="")
        print("\x1B[3m" + text + "\x1B[0m")

    def update(self):
        """
        Updates the state of the player sprite.
        """
        # Get input from the user
        self.get_input()

        # Constrain the player sprite's position to the edges of the screen
        self.constraint()

        # Recharge the player sprite's bullet if necessary
        self.recharge()

        # Move the lasers up
        self.bullets.update()
