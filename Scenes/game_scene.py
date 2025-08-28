import pygame
from player import Player
from board import Board


class GameScene:
    def __init__(self, game):
        self.game = game
        self.settings = game.settings
        self.name = "Playing"

        # Core game state
        self.board = Board(self.settings)
        self._set_players()
        self.is_game_over = False
        self.next_moves_surface: None | pygame.Surface = None
        self.next_move_icon = pygame.image.load(self.settings.next_move_icon)
        self.hovering = False

    def restart(self):
        self.white.pieces.clear()
        self.black.pieces.clear()
        self.board.clear()
        self._set_players()
        self.is_game_over = False
        self.next_moves_surface: None | pygame.Surface = None
        self.hovering = False

    @property
    def screen(self):
        return self.game.screen

    def _set_players(self):
        self.white = Player(self, "white")
        
        self.black = Player(self, "black")
        self.players = [self.white, self.black]
        for piece in self.board.get_all_pieces():
            piece.has_moved = False
        self.current_player = 0
        self.players[self.current_player].start_turn(self.get_next_player())

    def get_current_player(self) -> Player:
        return self.players[self.current_player]

    def get_next_player(self) -> Player:
        return self.players[(self.current_player + 1) % 2]

    def _toggle_player(self):
        self.current_player = (self.current_player + 1) % 2

    def change_turn(self):
        if self.is_game_over:
            self.game.running = False
            return

        self.get_current_player().selected = False
        self.get_current_player().turn_complete = False
        self._toggle_player()
        self.get_current_player().start_turn(self.get_next_player())
        self.next_moves_surface = None
        self.get_next_player().revoke_turn()

    # ==== Scene API ====

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.get_current_player().check_selection(event)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.game.pause()

        hovering = self.get_current_player().selected
        if self.hovering != hovering:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND) if hovering else pygame.mouse.set_cursor(
                pygame.SYSTEM_CURSOR_ARROW)
            self.hovering = hovering

    def update(self, dt: float):
        if self.get_current_player().turn_complete:
            self.change_turn()

    def draw(self, surface: pygame.Surface):
        # draw board
        self.board.render_board(
            surface,
            (self.settings.squarewidth, self.settings.squareheight),
            self.settings.tiles,
        )

        # draw pieces
        for piece in self.board.get_all_pieces():
            piece.render_piece()

        # show valid moves
        if self.next_moves_surface:
            surface.blit(self.next_moves_surface, (0, 0))
