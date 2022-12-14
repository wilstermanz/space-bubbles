import pygame, sys
from models.game import Game

# Set the screen dimensions
screen_width = 600
screen_height = 600

# Initialize the screen and game clock
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()

# Create a new game instance
game = Game()

def main_loop():
    """
    Runs the main game loop.

    This method initializes Pygame, and then enters the main game loop. In each
    iteration of the game loop, the method checks for user input (to quit the
    game), updates the state of the game, and then draws the game to the screen.
    """
    pygame.init()

    # Game loop
    while True:
        # Check for user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # If the user has clicked the 'x' in the top right corner, quit
                # the game and exit the program
                pygame.quit()
                sys.exit()

        # Cover the screen with the background color
        screen.fill((30, 30, 30))

        # Run a single iteration of the game
        game.run()

        # Update the screen and tick the game clock
        pygame.display.flip()
        clock.tick(60)


if __name__ == '__main__':
    # Run the main game loop when the program is executed
    main_loop()
