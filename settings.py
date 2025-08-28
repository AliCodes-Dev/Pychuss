import pygame
from enum import Enum


class ColorPalette(Enum):
    BACKGROUND = (10, 10, 20)        # deep space black/blue
    PANEL = (30, 30, 60)             # dark indigo
    BUTTON = (200, 30, 60)           # arcade red
    BUTTON_HOVER = (30, 144, 255)    # vivid blue
    BUTTON_DISABLED = (90, 90, 120)  # muted gray
    TEXT = (255, 220, 0)             # golden yellow (arcade style)
    TEXT_SECONDARY = (255, 180, 70)  # orange-yellow for glow/secondary
    BORDER = (255, 0, 128)     # neon magenta
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GRAY = (128, 128, 128)
    LIGHT_GRAY = (200, 200, 200)
    DARK_GRAY = (50, 50, 50)

    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)

    YELLOW = (255, 255, 0)
    CYAN = (0, 255, 255)
    MAGENTA = (255, 0, 255)

    ORANGE = (255, 165, 0)
    PURPLE = (128, 0, 128)
    PINK = (255, 192, 203)
    BROWN = (139, 69, 19)


class Settings:
    def __init__(self) -> None:
        self.SCREEN_WIDTH = 1024
        self.SCREEN_HEIGHT = 512
        self.BOARD_HEIGHT = 512
        self.BOARD_WIDTH = 512
        self.BOARD_SIZE = 8
        self.squarewidth = self.BOARD_WIDTH/self.BOARD_SIZE
        self.squareheight = self.BOARD_HEIGHT/self.BOARD_SIZE
        self.frame_rate = 30
        self.title = "PyChuss"
        self.icon = "icon.png"
        self.next_move_icon = "assets/move.png"
        self.squareColors = [(181, 136, 99), (240, 217, 181)]

        self.emptyboard = [[None for col in range(
            self.BOARD_SIZE)] for row in range(self.BOARD_SIZE)]
        self.padding = 2
        self.directions = {
            "up": (-1, 0),
            "down": (1, 0),
            "left": (0, -1),
            "right": (0, 1),
            "up_left": (-1, -1),
            "up_right": (-1, 1),
            "down_left": (1, -1),
            "down_right": (1, 1),
            "knight": [(2, 1), (2, -1), (-2, 1), (-2, -1),
                       (1, 2), (1, -2), (-1, 2), (-1, -2)]
        }

        self.tiles = [pygame.Surface(
            (self.squarewidth, self.squareheight)),
            pygame.Surface(
            (self.squarewidth, self.squareheight))]

        self.tiles[0].fill(self.squareColors[0])
        self.tiles[1].fill(self.squareColors[1])


# seti = Settings()
