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
GOLD = (217, 187, 106)
PURPLE = (115, 43, 245)

# Set the screen dimensions
screen_width = 600
screen_height = 600

# Initialize the screen and game clock
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
pygame.display.set_caption("Menu")


def main_menu():
    """ Main Menu Screen """

    # Change background to image
    bg_image = pygame.image.load('images/background.png')

    # Play music on start
    pygame.mixer.init()
    music = pygame.mixer.Sound('audio/menu_music.wav')
    music.set_volume(0.2)
    music.play(loops = -1)

    pygame.display.set_caption("Menu")

    # screen.fill((30, 30, 30))
    screen.blit(bg_image, bg_image.get_rect())

    MenuText = get_font(85).render("SPACE BUBBLES!!", True, PURPLE)
    MenuRect = MenuText.get_rect(center=(300, 100))

    PlayButton = Button(image=None,
                        pos=(300, 275),
                        text_input="PLAY",
                        font=get_font(50),
                        base_color=WHITE,
                        hovering_color=GREEN
                        )

    LeaderBoardButton = Button(image=None,
                               pos=(300, 375),
                               text_input="LEADERBOARD",
                               font=get_font(50),
                               base_color=WHITE,
                               hovering_color=GREEN)

    QuitButton = Button(image=None,
                        pos=(300, 475),
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
                    name = input()
                    print("Name: {}, Score: {}, Bubbles Popped: {}, Shots Fired: {}, Total Misses: {}".format(name, game.score, (game.hits + (40 * game.level - 1)), game.shots_fired, game.misses))
                    leaderDbBuild(game, name)
                    screen.blit(bg_image, bg_image.get_rect())
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
    from models.table import Table
    
    """Place holder for pulling and displaying a leaderboard"""
    
    # Change background to image
    bg_image = pygame.image.load('images/background.png')

    leaderDbBuild()
    conn = sqlite3.connect('leaderboard.db')
    c = conn.cursor()
    c.execute("SELECT * FROM performanceData ORDER BY Score DESC")
    leaders = c.fetchmany(10)
    
    table = Table()
    table.set_column_num(5)
    table.set_row_num(11, 30)
    table.resize(517, 330)
    table.set_text(0, 0, f"Initials")
    table.set_text(0, 1, f"Score")
    table.set_text(0, 2, f"# Popped")
    table.set_text(0, 3, f"# Fired")
    table.set_text(0, 4, f"Misses")
    
        
    for i in range(1, 11):
        for j in range(5):
            table.set_text(i, j, f"{leaders[i - 1][j]}")


    # screen.fill((30, 30, 30))
    screen.blit(bg_image, bg_image.get_rect())

    LeaderboardText = get_font(100).render("Leaderboard", True, PURPLE)
    LeaderboardRect = LeaderboardText.get_rect(center=(screen_width // 2, 100))
    BackButton = Button(image=None,
                        pos=(300, 525),
                        text_input="Back",
                        font=get_font(50),
                        base_color=WHITE,
                        hovering_color=GREEN)

    screen.blit(LeaderboardText, LeaderboardRect)
    conn.close()

    pygame.display.set_caption("Leaderboard")

    while True:

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
        
        table.draw(screen)
        pygame.display.update()
        pygame.display.flip()
        clock.tick(60)

def leaderDbBuild(game=None, name=""):
    """Makes storage file/connection and creates table if not exists"""
    
    
    # creates sqlite connection and creates the db
    conn = sqlite3.connect('leaderboard.db')
    c = conn.cursor()
    # creates the table in the db
    c.execute("""CREATE TABLE IF NOT EXISTS performanceData (
                Initials text,
                Score integer,
                BubblesPopped integer,
                ShotsFired integer,
                ShotsMissed integer
                )""")
    
    # inserts a row into the table if it was an instance of a game play
    if game is not None:
        c.execute("INSERT INTO performanceData VALUES(:name, :score, :bubblespopped, :shotsfired, :shotsmissed)", {'name': name, 'score': game.score, 'bubblespopped': game.hits, 'shotsfired': game.shots_fired, 'shotsmissed': game.misses})

    # prints the db for funsies right now
    c.execute("SELECT * FROM performanceData ORDER BY Score DESC")
    conn.commit()
    conn.close()
    
def input():
    """ Gets user name"""
    name=""
    NamePromptText = get_font(35).render("What are your initials, playa?", True, WHITE)
    NamePromptRect = NamePromptText.get_rect(center=(300, 100))
    screen.blit(NamePromptText, NamePromptRect)
    # Change background to image
    bg_image = pygame.image.load('images/background.png')

    pygame.display.update()
    done = True
    while done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN and len(name) < 3:
                if event.key == pygame.K_a:
                    name += str(chr(event.key))
                if event.key == pygame.K_b:
                    name += str(chr(event.key))
                if event.key == pygame.K_c:
                    name += chr(event.key)
                if event.key == pygame.K_d:
                    name += chr(event.key)
                if event.key == pygame.K_e:
                    name += chr(event.key)
                if event.key == pygame.K_f:
                    name += chr(event.key)
                if event.key == pygame.K_g:
                    name += chr(event.key)
                if event.key == pygame.K_h:
                    name += chr(event.key)
                if event.key == pygame.K_i:
                    name += chr(event.key)
                if event.key == pygame.K_j:
                    name += chr(event.key)
                if event.key == pygame.K_k:
                    name += chr(event.key)
                if event.key == pygame.K_l:
                    name += chr(event.key)
                if event.key == pygame.K_m:
                    name += chr(event.key)
                if event.key == pygame.K_n:
                    name += chr(event.key)
                if event.key == pygame.K_o:
                    name += chr(event.key)
                if event.key == pygame.K_p:
                    name += chr(event.key)
                if event.key == pygame.K_q:
                    name += chr(event.key)
                if event.key == pygame.K_r:
                    name += chr(event.key)
                if event.key == pygame.K_s:
                    name += chr(event.key)
                if event.key == pygame.K_t:
                    name += chr(event.key)
                if event.key == pygame.K_u:
                    name += chr(event.key)
                if event.key == pygame.K_v:
                    name += chr(event.key)
                if event.key == pygame.K_w:
                    name += chr(event.key)
                if event.key == pygame.K_x:
                    name += chr(event.key)
                if event.key == pygame.K_y:
                    name += chr(event.key)
                if event.key == pygame.K_z:
                    name += chr(event.key)
                if event.key == pygame.K_1:
                    name += chr(event.key)
                if event.key == pygame.K_2:
                    name += chr(event.key)
                if event.key == pygame.K_3:
                    name += chr(event.key)
                if event.key == pygame.K_4:
                    name += chr(event.key)
                if event.key == pygame.K_5:
                    name += chr(event.key)
                if event.key == pygame.K_6:
                    name += chr(event.key)
                if event.key == pygame.K_7:
                    name += chr(event.key)
                if event.key == pygame.K_8:
                    name += chr(event.key)
                if event.key == pygame.K_9:
                    name += chr(event.key)
                if event.key == pygame.K_0:
                    name += chr(event.key)
                if event.key == pygame.K_SPACE:
                    name += chr(event.key)
                if event.key == pygame.K_BACKSPACE:
                    if len(name) > 0:
                        name = name[:-1]
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    if len(name) > 0:
                        name = name[:-1]
                if event.key == pygame.K_RETURN:
                    done = False
            
            screen.blit(bg_image, bg_image.get_rect())
            NameText = get_font(30).render(name, True, GREEN)
            NameRect = NameText.get_rect(center=(300, 200))
            screen.blit(NamePromptText, NamePromptRect)
            screen.blit(NameText, NameRect)
            pygame.display.update()

    return name

def text1(name, x, y):
    font = pygame.font.SysFont(None, 25)
    text = font.render("{}".format(name), True, RED)
    return screen.blit(text, (x,y))

def get_font(size):     # Returns Press-Start-2P in the desired size
    return pygame.font.Font("fonts/CaveatBrush-Regular.ttf", size)


if __name__ == '__main__':
    # Run the main game loop when the program is executed
    main_menu()
