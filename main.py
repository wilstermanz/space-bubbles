from models.game import Game
from models.button import Button
import pygame
import sys
import sqlite3

pygame.init()

# Define Default Colors
WHITE = (202, 213, 218)
RED = (232, 53, 38)
GREEN = (87, 171, 65)
YELLOW = (250, 228, 25)
BLUE = (22, 114, 184)
BLACK = (30, 30, 30)

# Set the screen dimensions
screen_width = 600
screen_height = 600

# Initialize the screen and game clock
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
pygame.display.set_caption("Menu")


def main_menu():
    """ Main Menu Screen """

    pygame.display.set_caption("Menu")

    screen.fill((30, 30, 30))

    MenuText = get_font(100).render("MAIN MENU", True, WHITE)
    MenuRect = MenuText.get_rect(center=(300, 100))

    PlayButton = Button(image=None,
                        pos=(300, 250),
                        text_input="PLAY",
                        font=get_font(50),
                        base_color=WHITE,
                        hovering_color=GREEN
                        )

    LeaderBoardButton = Button(image=None,
                               pos=(300, 425),
                               text_input="LEADERBOARD",
                               font=get_font(50),
                               base_color=WHITE,
                               hovering_color=GREEN)

    QuitButton = Button(image=None,
                        pos=(300, 525),
                        text_input="QUIT (while you're ahead)",
                        font=get_font(50),
                        base_color=WHITE,
                        hovering_color=GREEN)

    running = True

    while running:

        MenuMouse = pygame.mouse.get_pos()

        screen.blit(MenuText, MenuRect)

        for button in [PlayButton, LeaderBoardButton, QuitButton]:
            button.changeColor(MenuMouse)
            button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PlayButton.checkForInput(MenuMouse):
                    # Create a new game instance
                    game = Game()
                    game.run()
                    screen.fill((30, 30, 30))
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
    
    leaderDbBuild()

    screen.fill((30, 30, 30))

    MenuMouse = pygame.mouse.get_pos()

    LeaderboardText = get_font(100).render("Leaderboard", True, "#b68f40")
    LeaderboardRect = LeaderboardText.get_rect(center=(screen_width // 2, 100))
    BackButton = Button(image=None,
                        pos=(300, 525),
                        text_input="Back",
                        font=get_font(50),
                        base_color="White",
                        hovering_color="Green")

    screen.blit(LeaderboardText, LeaderboardRect)

    while True:
        pygame.display.set_caption("Leaderboard")

        MenuMouse = pygame.mouse.get_pos()

        for button in [BackButton]:
            button.changeColor(MenuMouse)
            button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if BackButton.checkForInput(MenuMouse):
                    main_menu()

        pygame.display.update()
        pygame.display.flip()
        clock.tick(60)

def leaderDbBuild():
    """Makes storage file/connection and creates table if not exists"""
    
    # creates sqlite connection and creates the db
    conn = sqlite3.connect('leaderboard.db')
    c = conn.cursor()
    # creates the table in the db
    c.execute("""CREATE TABLE IF NOT EXISTS performanceData (
                Initials text,
                Score integer,
                BubblesPopped integer,
                ShotsFired integer
                )""")
    # 
    # inserts a row into the table BUT values need to be
    # established. Those are just placeholders currently
    #c.execute("INSERT INTO performanceData VALUES (?, ?, ?, ?)", (initials, score, bubblespopped, shotsfired))

    # prints the db for funsies right now
    c.execute("SELECT * FROM performanceData")
    print(c.fetchall())

    conn.commit()

    conn.close()

def get_font(size):     # Returns Press-Start-2P in the desired size
    return pygame.font.Font("fonts/Branda-yolq.ttf", size)


if __name__ == '__main__':
    # Run the main game loop when the program is executed
    main_menu()
