import pygame, sys
from models.game import Game
from models.button import Button

pygame.init()

# Set the screen dimensions
screen_width = 600
screen_height = 600

# Initialize the screen and game clock
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
pygame.display.set_caption("Menu")

# Create a new game instance
game = Game()

def main_loop():
    """
    Runs the main game loop.

    This method initializes Pygame, and then enters the main game loop. In each
    iteration of the game loop, the method checks for user input (to quit the
    game), updates the state of the game, and then draws the game to the screen.
    """


    # Game loop
    while True:
        # Check for user input
        

        # Cover the screen with the background color
        screen.fill((30, 30, 30))

        # Run a single iteration of the game
        main_menu()

        # Update the screen and tick the game clock
        

def main_menu():
    """ Main Menu Screen """
    
    pygame.display.set_caption("Menu")
    
    screen.fill((30, 30, 30))

    
    
    MenuText = get_font(100).render("MAIN MENU", True, "#b68f40")
    MenuRect = MenuText.get_rect(center=(300, 100))
    
    PlayButton = Button(image=None, pos=(300, 250), text_input="PLAY", font=get_font(50), base_color="White", hovering_color="Green")
    
    LeaderBoardButton = Button(image=None, pos=(300, 425), text_input="LEADERBOARD", font=get_font(50), base_color="White", hovering_color="Green")
    
    QuitButton = Button(image=None, pos=(300, 525), text_input="QUIT (while you're ahead)", font=get_font(50), base_color="White", hovering_color="Green")
    
    screen.blit(MenuText, MenuRect)
    running = True
    
    while running:
        
        MenuMouse = pygame.mouse.get_pos()
        
        for button in [PlayButton, LeaderBoardButton, QuitButton]:
            button.changeColor(MenuMouse)
            button.update(screen)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PlayButton.checkForInput(MenuMouse):
                    running = False
                    game.run()
                if LeaderBoardButton.checkForInput(MenuMouse):
                    running = False
                    leaderboard()
                if QuitButton.checkForInput(MenuMouse):
                    pygame.quit()
                    sys.exit()
        
        pygame.display.update()
        pygame.display.flip()
        clock.tick(60)


def leaderboard():
    """Place holder for pulling and displaying a leaderboard"""
    
    while True:
        
        MenuMouse = pygame.mouse.get_pos()
        screen.fill((30, 30, 30))
        pygame.display.set_caption("Leaderboard")
    
        LeaderboardText = get_font(100).render("MAIN MENU", True, "#b68f40")
        LeaderboardRect = LeaderboardText.get_rect(center=(640, 100))
        screen.blit(LeaderboardText, LeaderboardRect)
        BackButton = Button(image=None, pos=(640, 250), text_input="BACK", font=get_font(75), base_color="White", hovering_color="Green")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if BackButton.checkForInput(MenuMouse):
                    main_loop()

def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("fonts/Branda-yolq.ttf", size)

if __name__ == '__main__':
    # Run the main game loop when the program is executed
    main_menu()
