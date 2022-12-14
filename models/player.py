import pygame
from models.laser import Laser

class Player(pygame.sprite.Sprite):
    """
    Defines the player sprite and its behavior.

    The player is represented by a red rectangle. The user can move the player
    left and right using the left and right arrow keys, and shoot a bullet using
    the space bar. The player sprite is bound by the left and right edges of the
    screen, and bullets can only be shot once every 600ms.
    """
    # Class attributes
    player_width = 50
    player_height = 20

    def __init__(self, pos, speed):
        """
        Initializes the player sprite.

        Args:
            pos: A tuple specifying the (x, y) position of the player sprite.
            speed: An integer specifying the speed at which the player sprite moves.
        """
        # Call the `__init__()` method of the superclass (`pygame.sprite.Sprite`)
        super().__init__()

        # Create a new surface representing the player sprite
        self.image = pygame.Surface([self.player_width, self.player_height])

        # Fill the surface with the color red
        self.image.fill((255, 0, 0))

        # Set the position of the player sprite to the given position
        self.rect = self.image.get_rect(midbottom=pos)

        # Set the speed of the player sprite to the given speed
        self.speed = speed

        # Set the initial state of the player sprite's bullet
        self.ready = True           # Bullets can be fired when True
        self.bullet_time = 0
        self.bullet_cooldown = 600  # Bullets can be shot every 600ms

        # Bring in the laser
        self.lasers = pygame.sprite.Group()


    def get_input(self):
        """
        Gets input from the user and updat  es the state of the player sprite
        accordingly.
        """
        # Get the keys that are currently being pressed
        keys = pygame.key.get_pressed()

        # If the right arrow key is being pressed, move the player sprite to the
        # right
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed

        # If the left arrow key is being pressed, move the player sprite to the left
        elif keys[pygame.K_LEFT]:
            self.rect.x -= self.speed

        # If the space bar is being pressed and the player sprite is ready to fire a
        # bullet, shoot a bullet and start the bullet recharge timer
        if keys[pygame.K_SPACE] and self.ready:
            self.shoot_bullet()
            self.ready = False
            self.bullet_time = pygame.time.get_ticks()

    def recharge(self):
        """
        Checks if a bullet has been fired, and recharges the player sprite's bullet
        if the bullet cooldown time has been reached.
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
        Constrains the player sprite's position to the left and right edges of the
        screen.
        """
        # Import the `screen_width` variable from the `main` module
        from main import screen_width

        # If the player sprite's left edge is less than or equal to 0, set the left
        # edge to 0
        if self.rect.left <= 0:
            self.rect.left = 0

        # If the player sprite's right edge is greater than or equal to the screen
        # width, set the right edge to the screen width
        if self.rect.right >= screen_width:
            self.rect.right = screen_width

    def shoot_bullet(self):
        """
        Shoots a bullet
        """
        self.lasers.add(Laser(self.rect.center))
        # Pew
        print('pew')

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
