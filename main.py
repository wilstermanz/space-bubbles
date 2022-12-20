from models.game import Game
from models.button import Button
import pygame
import requests
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
    music.play(loops=-1)

    pygame.display.set_caption("Menu")

    # screen.fill((30, 30, 30))
    screen.blit(bg_image, bg_image.get_rect())

    MenuTextL1 = get_font(85, 'title').render("Space", True, PURPLE)
    MenuRectL1 = MenuTextL1.get_rect(center=(300, 90))
    MenuTextL2 = get_font(85, 'title').render("Bubbles", True, PURPLE)
    MenuRectL2 = MenuTextL2.get_rect(
        center=(300, MenuRectL1.bottom + 20))

    quote = get_quote()

    PlayButton = Button(image=None,
                        pos=(300, 250),
                        text_input="PLAY",
                        font=get_font(50),
                        base_color=WHITE,
                        hovering_color=GREEN
                        )

    LeaderBoardButton = Button(image=None,
                               pos=(300, 325),
                               text_input="LEADERBOARD",
                               font=get_font(50),
                               base_color=WHITE,
                               hovering_color=GREEN)

    QuitButton = Button(image=None,
                        pos=(300, 400),
                        text_input="QUIT (while you're ahead)",
                        font=get_font(50),
                        base_color=WHITE,
                        hovering_color=GREEN)

    running = True

    while running:

        MenuMouse = pygame.mouse.get_pos()

        quoteText = get_font(18, 'quote').render(f'"{quote}."', True, YELLOW)
        quoteRect = quoteText.get_rect(
            center=(screen_width / 2, screen_height - 90))

        screen.blit(MenuTextL1, MenuRectL1)
        screen.blit(MenuTextL2, MenuRectL2)
        screen.blit(quoteText, quoteRect)

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
                    name = input(game.score,
                                 game.hits,
                                 game.level,
                                 game.current_time)
                    leaderDbBuild(game, name)
                    screen.blit(bg_image, bg_image.get_rect())
                    quote = get_quote()
                if LeaderBoardButton.checkForInput(MenuMouse):
                    running = False
                    leaderboard()
                    quote = get_quote()
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
    with sqlite3.connect('leaderboard.db') as conn:
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

        if len(leaders) > 0:
            for i in range(1, len(leaders) + 1):
                for j in range(5):
                    table.set_text(i, j, f"{leaders[i - 1][j]}")

        screen.blit(bg_image, bg_image.get_rect())

        LeaderboardText = get_font(100).render("Leaderboard", True, PURPLE)
        LeaderboardRect = LeaderboardText.get_rect(
            center=(screen_width // 2, 100))
        BackButton = Button(image=None,
                            pos=(300, 525),
                            text_input="Back",
                            font=get_font(50),
                            base_color=WHITE,
                            hovering_color=GREEN)

        screen.blit(LeaderboardText, LeaderboardRect)
        c.close()

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
    with sqlite3.connect('leaderboard.db') as conn:
        c = conn.cursor()
        # creates the table in the db
        c.execute("""CREATE TABLE IF NOT EXISTS performanceData (
                    Initials text,
                    Score integer,
                    BubblesPopped integer,
                    ShotsFired integer,
                    ShotsMissed integer
                    )""")
        c.close()

        # inserts a row into the table if it was an instance of a game play
        if game is not None:
            c = conn.cursor()
            c.execute("INSERT INTO performanceData VALUES(:name,"
                      ":score, :bubblespopped, :shotsfired, :shotsmissed)",
                      {'name': name,
                       'score': game.score,
                       'bubblespopped': game.hits,
                       'shotsfired': game.shots_fired,
                       'shotsmissed': game.misses})
            c.close()

        c = conn.cursor()
        c.execute("SELECT * FROM performanceData ORDER BY Score DESC")
        c.close()
        conn.commit()


def input(score, hits, level, time):
    """ Gets user name"""

    name = ""
    NamePromptText = get_font(35).render(
        "What are your initials, playa?", True, WHITE)
    NamePromptRect = NamePromptText.get_rect(center=(300, 100))

    GameStatsSurface = pygame.surface.Surface((screen_width * 0.8, 200))
    GameStatsSurface.fill((50, 50, 50))
    GameStatsRect = GameStatsSurface.get_rect(
        center=(screen_width / 2, screen_height * (2 / 3)))

    levelText = get_font(40).render(f'You made it to level {level}!',
                                    True, WHITE)
    levelRect = levelText.get_rect(
        midbottom=(GameStatsRect.centerx, GameStatsRect.top - 10))

    scoreText = get_font(35).render(f'Score: {score}', True, WHITE)
    scoreRect = scoreText.get_rect(
        midbottom=(GameStatsRect.centerx,
                   GameStatsRect.top + (GameStatsRect.height * (1 / 3)) - 10)
        )

    hitsText = get_font(35).render(f'Bubbles popped: {hits}',
                                   True, WHITE)
    hitsRect = hitsText.get_rect(
        center=(GameStatsRect.center))

    timeText = get_font(35).render(f'Time: {str(time)[2:-5]}',
                                   True, WHITE)
    timeRect = timeText.get_rect(
        midtop=(GameStatsRect.centerx,
                GameStatsRect.top + (GameStatsRect.height * (2 / 3)) + 10)
    )

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
                    name += 'A'
                if event.key == pygame.K_b:
                    name += 'B'
                if event.key == pygame.K_c:
                    name += 'C'
                if event.key == pygame.K_d:
                    name += 'D'
                if event.key == pygame.K_e:
                    name += 'E'
                if event.key == pygame.K_f:
                    name += 'F'
                if event.key == pygame.K_g:
                    name += 'G'
                if event.key == pygame.K_h:
                    name += 'H'
                if event.key == pygame.K_i:
                    name += 'I'
                if event.key == pygame.K_j:
                    name += 'J'
                if event.key == pygame.K_k:
                    name += 'K'
                if event.key == pygame.K_l:
                    name += 'L'
                if event.key == pygame.K_m:
                    name += 'M'
                if event.key == pygame.K_n:
                    name += 'N'
                if event.key == pygame.K_o:
                    name += 'O'
                if event.key == pygame.K_p:
                    name += 'P'
                if event.key == pygame.K_q:
                    name += 'Q'
                if event.key == pygame.K_r:
                    name += 'R'
                if event.key == pygame.K_s:
                    name += 'S'
                if event.key == pygame.K_t:
                    name += 'T'
                if event.key == pygame.K_u:
                    name += 'U'
                if event.key == pygame.K_v:
                    name += 'V'
                if event.key == pygame.K_w:
                    name += 'W'
                if event.key == pygame.K_x:
                    name += 'X'
                if event.key == pygame.K_y:
                    name += 'Y'
                if event.key == pygame.K_z:
                    name += 'Z'
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
                if event.key == pygame.K_SPACE and len(name) != 0:
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
            NameText = get_font(50).render(name, True, GREEN)
            NameRect = NameText.get_rect(center=(300, 190))
            screen.blit(GameStatsSurface, GameStatsRect)
            screen.blit(NamePromptText, NamePromptRect)
            screen.blit(NameText, NameRect)
            screen.blit(scoreText, scoreRect)
            screen.blit(hitsText, hitsRect)
            screen.blit(levelText, levelRect)
            screen.blit(timeText, timeRect)

            pygame.display.update()

    return name


def text1(name, x, y):
    font = pygame.font.SysFont(None, 25)
    text = font.render("{}".format(name), True, RED)
    return screen.blit(text, (x, y))


def get_font(size, font="default"):
    if font == "title":
        return pygame.font.Font("fonts/title.ttf", size)
    if font == "quote":
        return pygame.font.Font("fonts/quote.ttf", size)
    else:
        return pygame.font.Font("fonts/default.ttf", size)


def get_quote():
    """Uses an API to get a random techy soundy quote"""
    error = "You should really get to fixing your flux connector"
    try:
        r = requests.get("https://techy-api.vercel.app/api/json")
        while len(r.json()["message"]) > 55:
            r = requests.get("https://techy-api.vercel.app/api/json")
        if r.status_code == 200:
            return r.json()["message"]
        else:
            return error
    except Exception:
        return error


if __name__ == '__main__':
    # Run the main game loop when the program is executed
    main_menu()
