import pygame
import sys


import settings
from player import Player
from board import Board


class Game:
    def __init__(self) -> None:
        pygame.init()

        self.settings = settings.Settings()
        self._setWindow()
        self.board = Board(self.settings)

        self._set_players()

        self.tiles = self.settings.tiles

        self.next_move_icon = pygame.image.load(self.settings.next_move_icon)
        self.next_moves_surface: None | pygame.Surface = None
        self._set_clock()

    def change_turn(self, piece_id: str) -> None:
        piece = self.board.get_piece(piece_id)
        if piece is None:
            print(f"Invalid piece_id: {piece_id}")
            return

        piece.selected = False
        self.players[self.current_player].selected = False

        self.current_player = (self.current_player + 1) % 2
        self.next_moves_surface = None
        piece.valid_moves.clear()

    def _set_players(self) -> None:
        self.black = Player(self, "black")
        self.white = Player(self, "white")
        self.players = [self.white, self.black]
        self.current_player = 0

    def _set_clock(self) -> None:
        self.clock = pygame.time.Clock()
        self.running = True

    def _render_pieces(self) -> None:

        for piece in self.board.pieces.values():
            piece.render_piece()

    def _setWindow(self) -> None:
        self.screen = pygame.display.set_mode(
            (self.settings.SCREEN_WIDTH, self.settings.SCREEN_HEIGHT))

        pygame.display.set_caption(self.settings.title)
        self.icon = pygame.image.load(self.settings.icon)
        pygame.display.set_icon(self.icon)

    def _render_board(self) -> None:
        self.board.render_board(
            self.screen, (self.settings.squarewidth, self.settings.squareheight), self.tiles)

    def _checkEvents(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.players[self.current_player].check_selection(event)

    def _updateWindow(self) -> None:
        pygame.display.flip()
        self.clock.tick(self.settings.frame_rate)

    def _show_moves(self) -> None:
        if self.next_moves_surface:
            self.screen.blit(self.next_moves_surface, (0, 0))

    def runGame(self) -> None:
        while self.running:
            try:
                self._checkEvents()
                self._render_board()
                self._render_pieces()
                self._show_moves()

                self._updateWindow()
            except KeyboardInterrupt:
                print("Bye Bye")
                self.running = False


chess_game = Game()
chess_game.runGame()
