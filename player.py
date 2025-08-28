

import pygame
import pieces


from typing import TYPE_CHECKING, Tuple
if TYPE_CHECKING:
    from Scenes.game_scene import GameScene
    from pieces import King


import logging
from rich.logging import RichHandler
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler()]
)
start_ranks = {
    "black": 0,
    "white": 6
}


piece_classes = {
    "pawn": pieces.Pawn,
    "queen": pieces.Queen,
    "rook": pieces.Rook,
    "bishop": pieces.Bishop,
    "king": pieces.King,
    "knight": pieces.Knight
}


piece_map = [
    ["pawn"] * 8,
    ["rook_1", "knight_1", "bishop_1", "queen",
        "king", "bishop_2", "knight_2", "rook_2"]
]


class Player:
    def __init__(self, game: "GameScene", color: str) -> None:
        """Initialize a player with their pieces and state."""
        self.color = color
        self.game_scene = game
        self.start_rank = start_ranks[color]
        self.pieces: list[str] = []
        self.selected = False
        self.selected_piece: str = ""
        self._create_pieces()
        # Always keep a direct reference to the king piece
        self.king: King = self.game_scene.board.get_piece(f"{self.color}_king")
        self.playable_moves_in_check = -1
        self.turn_complete = False
        
    
    def _create_pieces(self) -> None:
        """Create and place all pieces for this player."""
        rank = self.start_rank
        local_piece_map = piece_map[::-
                                    1] if self.color == "black" else piece_map
        for piece_rank in local_piece_map:
            for file, piece_name in enumerate(piece_rank):
                piece_data = piece_name.split('_')
                piece_type = piece_data[0]
                piece_class = piece_classes[piece_type]
                # Use index for pawns, otherwise use suffix if present
                piece_index = str(file) if piece_type == "pawn" else (
                    piece_data[1] if len(piece_data) == 2 else "")
                piece_id = f"{self.color}_{piece_type}{piece_index}"
                piece = piece_class(
                    (rank, file),
                    (self.game_scene.settings.squarewidth,
                     self.game_scene.settings.squareheight),
                    (self.game_scene.settings.SCREEN_WIDTH,
                     self.game_scene.settings.SCREEN_HEIGHT),
                    f"assets/{self.color}/{piece_type}.png",
                    self.game_scene.settings.padding,
                    piece_id,
                    self.color,
                    self.game_scene,
                )
                self.pieces.append(piece_id)
            rank += 1

    def get_all_valid_moves(self, save: bool = False):
        """Yield (valid_moves, piece) for all pieces of this player."""
        for piece_id in self.pieces:
            piece = self.game_scene.board.get_piece(piece_id)
            if piece.type == "pawn":
                valid_moves,check_by = piece.get_pawn_capture_moves(self.pieces,False)
            else:
                # logging.debug(f"Getting moves for {piece.id}")
                valid_moves, check_by = piece.generate_validmoves(
                    self.pieces,  False)
            yield valid_moves, check_by

    def is_mate(self):
        """Check if the player is in checkmate."""
        # if self.king.checked and self.king.valid_moves is not None and not self.king.valid_moves:
        #     print(f"{self.game_scene.get_current_player().color} has been checkmated!")
        self.king.generate_safe_king_moves(self.pieces)
        if self.king.checked:
            self.king.generate_check_defenses(self.pieces)

        if self.playable_moves_in_check == 0 and self.king.checked:
            logging.warning(
                f"{self.game_scene.get_current_player().color} has been checkmated!")
            self.game_scene.is_game_over = True

    

    def start_turn(self, opp_player: "Player"):
        """Prepare for this player's turn: update king's moves and check status."""
        self.king.checked = False
        self.king.checking_pieces.clear()
        self.is_mate()
        self.king.detect_pins(self.pieces)
        
    def revoke_turn(self):
        self.playable_moves_in_check = 0
        self.king.checked = False
        for piece_id in self.pieces:
            piece = self.game_scene.board.get_piece(piece_id)
            piece.valid_moves = None
            piece.pinned_status = {"pinned": False, "allowed_dir": ["all"]}
            
            

    

    def _handle_move_selected_piece(self, pos: Tuple[int, int]) -> None:
        """Handle moving the selected piece to a new position."""
        self.game_scene.board.get_piece(self.selected_piece).move_piece(
            pos, self.pieces)
        

    def _handle_deselect_piece(self, piece_id: str) -> None:
        """Deselect the currently selected piece."""
        self.game_scene.board.pieces[piece_id].selected = False
        self.selected_piece = ''
        self.selected = False
        self.game_scene.next_moves_surface = None

    def _handle_switch_selected_piece(self, piece_id: str) -> None:
        """Switch selection to another of the player's own pieces."""
        self.game_scene.board.get_piece(self.selected_piece).selected = False
        self.selected_piece = piece_id
        self.game_scene.board.get_piece(piece_id).selected = True
        self.game_scene.board.get_piece(
            piece_id).make_move_surface()

    def _handle_capture_opponent_piece(self, pos: Tuple[int, int]) -> None:
        """Handle capturing an opponent's piece."""
        self.game_scene.board.get_piece(self.selected_piece).capture(
            pos, self.pieces)

    def _handle_select_own_piece(self, piece_id: str) -> None:
        """Select one of the player's own pieces."""
        if self.king.checked:
            self.king.highlight_check()
        self.game_scene.board.get_piece(piece_id).selected = True
        self.selected_piece = piece_id
        self.selected = True
        self.game_scene.board.get_piece(
            piece_id).make_move_surface()

    def check_selection(self, event: pygame.event.Event) -> None:
        if event.type != pygame.MOUSEBUTTONDOWN or event.button != 1:
            return

        mouse_x, mouse_y = pygame.mouse.get_pos()
        rank = int(mouse_y // self.game_scene.settings.squareheight)
        file = int(mouse_x // self.game_scene.settings.squarewidth)

        if rank >= len(self.game_scene.board) or file >= len(self.game_scene.board):
            return

        piece_id = self.game_scene.board.get_piece_id((rank, file))
        print(f"Piece_ID: {piece_id}")
        print(f"rank: {rank}, File: {file}")

        # If a piece is selected and user clicks an empty square: move
        if self.selected and piece_id is None:
            self._handle_move_selected_piece(pos=(rank, file))
            return

        # If a piece is selected and user clicks a square with a piece
        if self.selected and piece_id is not None:

            # Deselect if clicking the selected piece
            if self.selected_piece == piece_id:
                self._handle_deselect_piece(piece_id)
                return

            # Switch selection to another of your own pieces
            if piece_id in self.pieces:
                self._handle_switch_selected_piece(piece_id)
                return

            # Capture opponent's piece
            if piece_id not in self.pieces:
                self._handle_capture_opponent_piece(pos=(rank, file))
                return

        # If no piece is selected and user clicks their own piece: select it
        if not self.selected and piece_id is not None and piece_id in self.pieces:
            self._handle_select_own_piece(piece_id)
