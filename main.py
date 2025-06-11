import pygame
import sys


import settings
from player import Player
from board import Board


class Game:
    def __init__(self) -> None:
        self.settings = settings.Settings()

        pygame.init()
        self._setWindow()
        self.clock = pygame.time.Clock()
        self.running = True

        self.board = Board(self.settings)

        self.black = Player(self, "black")
        self.white = Player(self, "white")

        self.players = [self.white, self.black]
        self.current_player = 0

        self.tiles = [pygame.Surface(
            (self.settings.squarewidth, self.settings.squareheight)),
            pygame.Surface(
            (self.settings.squarewidth, self.settings.squareheight))]

        self.tiles[0].fill(self.settings.squareColors[0])
        self.tiles[1].fill(self.settings.squareColors[1])

        self.next_move_icon = pygame.image.load(self.settings.next_move_icon)
        self.next_moves_surface = None

    def change_turn(self, piece_id):
        piece = self.board.get_piece(piece_id)
        piece.selected = False
        self.players[self.current_player].selected = False

        self.current_player = (self.current_player + 1) % 2
        self.next_moves_surface = None
        piece.valid_moves.clear()

    def _render_pieces(self):
        # This function is temporarily used to render all pieces. A class Player will be made to handle respective piece's movements and rendering.
        # print(self.board.pieces.values())
        for piece in self.board.pieces.values():
            piece.render_piece()

    def _setWindow(self):
        self.screen = pygame.display.set_mode(
            (self.settings.SCREEN_WIDTH, self.settings.SCREEN_HEIGHT))

        pygame.display.set_caption(self.settings.title)
        self.icon = pygame.image.load(self.settings.icon)
        pygame.display.set_icon(self.icon)

    def _render_board(self):
        y = 0
        for row in range(8):
            x = 0
            for col in range(1, 9):

                self.screen.blit(self.tiles[(row+col) % 2], (x, y))
                x += self.settings.squarewidth
            y += self.settings.squareheight

    def _checkEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.players[self.current_player].check_selection(event)

    def _updateWindow(self):
        pygame.display.flip()
        self.clock.tick(self.settings.frame_rate)

    def _show_moves(self):
        if self.next_moves_surface:
            self.screen.blit(self.next_moves_surface, (0, 0))

    def runGame(self):
        while self.running:
            self._checkEvents()
            self._render_board()
            self._render_pieces()
            self._show_moves()

            self._updateWindow()
            # print(*self.board, sep='\n')
            # self.running = False


chess = Game()
chess.runGame()
