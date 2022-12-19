import pygame
from main import

class Table:
    def __init__(self):
        self.rect = pygame.rect.Rect((50, 0, 400, 500))
        # self.background_color = ("BLACK")
        self.border_color = ("GREEN")
        self.font_color = ("WHITE")
        self.scroll_y = 0
        self.is_scroll = False
        self.is_down = False
        self.is_up = False
        self.data_y = 0
        self.max_y = 1
        self.row_sizes = []
        self.column_sizes = []
        self.data = []
        self.draw_group = pygame.sprite.Group()
        self.scroll_area = pygame.sprite.Sprite(self.draw_group)
        self.scroll_arrow_up = pygame.sprite.Sprite(self.draw_group)
        self.scroll_arrow_down = pygame.sprite.Sprite(self.draw_group)
        self.scroll_box = pygame.sprite.Sprite(self.draw_group)

    def load_sprites(self):
        self.scroll_area.image = pygame.Surface((16, self.rect.height))
        self.scroll_area.image.fill((241, 241, 241))
        self.scroll_area.rect = self.scroll_area.image.get_rect()
        self.scroll_area.rect.x, self.scroll_area.rect.y = self.rect.width - 16, 0

        sfc = pygame.Surface((16, 16))
        sfc.fill((241, 241, 241))
        pygame.draw.polygon(sfc, (80, 80, 80), [(8, 8), (5, 11), (11, 11)])
        self.scroll_arrow_up.image = sfc
        self.scroll_arrow_up.rect = self.scroll_arrow_up.image.get_rect()
        self.scroll_arrow_up.rect.x, self.scroll_arrow_up.rect.y = self.rect.width - 16, 0

        sfc = pygame.Surface((16, 16))
        sfc.fill((241, 241, 241))
        pygame.draw.polygon(sfc, (80, 80, 80), [(8, 8), (11, 5), (5, 5)])
        self.scroll_arrow_down.image = sfc
        self.scroll_arrow_down.rect = self.scroll_arrow_down.image.get_rect()
        self.scroll_arrow_down.rect.x, self.scroll_arrow_down.rect.y = self.rect.width - 16, self.rect.height - 16

        self.scroll_box.image = pygame.Surface((14, self.rect.height ** 2 / self.max_y))
        self.scroll_box.image.fill((192, 192, 192))
        self.scroll_box.rect = self.scroll_box.image.get_rect()
        self.scroll_box.rect.x, self.scroll_box.rect.y = self.rect.width - 15, 16

    def resize(self, width, height):
        self.rect.width, self.rect.height = width, height
        self.load_sprites()

    def draw(self, screen: pygame.Surface, width=1):
        font = pygame.font.Font(None, 30)
        if self.is_up:
            self.move_data(True)
        elif self.is_down:
            self.move_data(False)
        surface = pygame.Surface(self.rect.size)
        x, y = 0, self.data_y
        for row in range(len(self.row_sizes)):
            x = 0
            for col in range(len(self.column_sizes)):
                pygame.draw.rect(surface, self.border_color,
                                 (x, y, self.column_sizes[col], self.row_sizes[row]), width)
                text = font.render(self.data[row][col], True, self.font_color)
                string = pygame.Surface((self.column_sizes[col] - 2 * width, self.row_sizes[row] - 2 * width))
                # string.fill(self.background_color)
                string.blit(text, (5, 5))
                surface.blit(string, (x + width, y + width))
                x += self.column_sizes[col]
            y += self.row_sizes[row]
        if self.max_y > self.rect.height:
            self.draw_group.draw(surface)
        else:
            surface.fill((193, 40, 52), (self.rect.width - 16, 0, 16, self.rect.height))
            surface.set_colorkey((193, 40, 52))
        screen.blit(surface, self.rect.topleft)

    def move(self, x, y):
        self.rect.x, self.rect.y = x, y

    def move_data(self, upper):
        if upper:
            if self.rect.height >= self.max_y:
                return
            self.data_y -= 20
            if self.data_y < self.rect.height - self.max_y:
                self.data_y = self.rect.height - self.max_y
        else:
            self.data_y += 20
            if self.data_y > 0:
                self.data_y = 0
        self.scroll_box.rect.y  = -self.data_y / (self.max_y + 32) * (self.rect.height - 32) + 16

    def set_column_num(self, n, size=100):
        self.column_sizes = [size for _ in range(n)]
        self.data = [["" for _ in range(len(self.column_sizes))] for _ in range(len(self.row_sizes))]

    def set_row_num(self, n, size=30):
        self.row_sizes = [size for _ in range(n)]
        self.data = [["" for _ in range(len(self.column_sizes))] for _ in range(len(self.row_sizes))]
        self.max_y = sum(self.row_sizes)

    def set_text(self, row, col, text):
        self.data[row][col] = text

    def set_column_size(self, col, size):
        self.column_sizes[col] = size

    def set_row_size(self, row, size):
        self.max_y += size - self.row_sizes[row]
        self.row_sizes[row] = size

    def scroll(self, ev: pygame.event.Event):
        if ev.type == pygame.MOUSEBUTTONDOWN:
            if self.scroll_arrow_up.rect.collidepoint((ev.pos[0] - self.rect.x, ev.pos[1] - self.rect.y)):
                self.is_down = True
            if self.scroll_arrow_down.rect.collidepoint((ev.pos[0] - self.rect.x, ev.pos[1] - self.rect.y)):
                self.is_up = True
            if self.scroll_box.rect.collidepoint((ev.pos[0] - self.rect.x, ev.pos[1] - self.rect.y)):
                self.is_scroll = True
                self.scroll_y = ev.pos[1]
        if ev.type == pygame.MOUSEMOTION and self.is_scroll:
            del_y = ev.pos[1] - self.scroll_y
            self.scroll_box.rect = self.scroll_box.rect.move(0, del_y)
            if self.scroll_box.rect.y < 16:
                self.scroll_box.rect.y = 16
            if self.scroll_box.rect.y > self.rect.height - 16 - self.scroll_box.rect.height:
                self.scroll_box.rect.y = self.rect.height - 16 - self.scroll_box.rect.height
            self.data_y = (-self.scroll_box.rect.y + 16) / (self.rect.height - 32) * (self.max_y + 32)
            self.scroll_y = ev.pos[1]
        elif ev.type == pygame.MOUSEBUTTONUP:
            self.is_up = False
            self.is_down = False
            self.is_scroll = False
