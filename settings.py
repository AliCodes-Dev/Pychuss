import pygame


class Settings:
    def __init__(self) -> None:
        self.SCREEN_WIDTH = 512
        self.SCREEN_HEIGHT = 512
        self.BOARD_SIZE = 8
        self.squarewidth = self.SCREEN_WIDTH/self.BOARD_SIZE
        self.squareheight = self.SCREEN_HEIGHT/self.BOARD_SIZE
        self.frame_rate = 60
        self.title = "PyChuss"
        self.icon = "icon.png"
        self.next_move_icon = "assets/move.png"
        self.squareColors = [(181, 136, 99), (240, 217, 181)]

        self.emptyboard = [[None for col in range(self.BOARD_SIZE)] for row in range(self.BOARD_SIZE)]
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
