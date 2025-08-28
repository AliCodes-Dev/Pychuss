
from functools import wraps
import time
import pygame
import logging

from typing import TYPE_CHECKING, List, Tuple, Set
if TYPE_CHECKING:
    from main_old import Game  # Adjust the import path if needed

from rich.logging import RichHandler

logging.basicConfig(
    level=logging.DEBUG,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler()]
)


pieces = {
    "pawn": "Pawn",
    "queen": "Queen",
    "rook": "Rook",
    "bishop": "Bishop",
    "king": "King",
    "knight": "Knight"
}


def time_it(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        print(f"{func.__name__} took {end - start:.6f} seconds")
        return result
    return wrapper


class Piece:
    def __init__(
        self,
        coords: tuple[int, int],
        size: tuple[int | float, int | float],
        screen_size: tuple[int, int],

        texture_url: str,
        padding: int,
        piece_id: str,
        color: str,
        directions: List[str],
        squares: int,
        game: "Game"

    ) -> None:

        # Remember, rank species the Y axis and file species the X axis.

        # Game reference
        self.game_scene = game

        # Board and position
        self.board = game.board
        self.rank, self.file = coords

        # Size and screen
        self.width, self.height = size
        self.screenWidth, self.screenHeight = screen_size

        # Visuals
        self.padding = padding
        self.texture = pygame.image.load(texture_url)
        self.texture = pygame.transform.scale(
            self.texture, (self.width - self.padding, self.height - self.padding))
        self.selected = False

        # Identity
        self.id = piece_id
        self.color = color
        self.type = "base"
        self.category = "base"
        self.checked = False
        self.checking_pieces = []

        # Movement
        self.directions = directions
        self.squares = squares
        self.has_moved = False
        self.valid_moves: Set[Tuple[int, int]] = None
        self.pinned_status = {"pinned": False, "allowed_dir": ["all"]}
        self.is_pinned = False

        # logging.info(f"Piece created with ID:{self.id}")

        # Place piece on board
        self.board.set_piece(self)

    def ensure_valid_moves(self, allies):

        if self.valid_moves is None:
            self.generate_validmoves(allies)

    def make_move_surface(self) -> None:
        # if is_king_in_check and self.type != "king":
        #     print("King is in check")
        #     return
        self.ensure_valid_moves(
            self.game_scene.get_current_player().pieces)

        move_surface = pygame.Surface(
            (self.screenWidth, self.screenHeight), pygame.SRCALPHA)
        for rank, file in self.valid_moves:
            move_surface.blit(self.game_scene.next_move_icon,
                              (file * self.width, rank * self.height))
        self.game_scene.next_moves_surface = move_surface

    def filter_moves_to(self, allies, target_moves: set[Tuple[int, int]]):

        if self.valid_moves is None:
            self.generate_validmoves(allies)
        if target_moves:
            self.valid_moves = target_moves & self.valid_moves
            # logging.info(f"Moves of {self.id} filtered to {self.valid_moves}")
            self.game_scene.get_current_player().playable_moves_in_check += len(self.valid_moves)

    def trace_direction(
        self,
        step: tuple[int, int],
        allies: list[str],
        limit: int | None = None,
        stop_on_block: bool = True,
    ) -> tuple[set[tuple[int, int]], set[tuple[int, int]], bool]:
        """
        Trace squares along a given direction.
        Returns (moves, blocks, spotted_king).
        """
        moves, blocks = set(), set()
        spotted_king = False

        if limit is None:
            limit = self.squares

        dy, dx = step
        r, f = self.rank, self.file

        for _ in range(limit):
            r += dy
            f += dx

            if not (0 <= r < len(self.board) and 0 <= f < len(self.board)):
                break
            if spotted_king:
                blocks.add((r, f))
                break
            piece = self.board.get_piece(coords=(r, f))
            if piece:
                if piece.id in allies:
                    blocks.add((r, f))
                else:
                    moves.add((r, f))
                    if piece.type == "king":
                        spotted_king = True
                        continue
                if stop_on_block:
                    break
            else:
                moves.add((r, f))

        return moves, blocks, spotted_king

    def detect_pieces_in_direction(
        self,
        step: Tuple[int, int],
        n_pieces: int,
        limit: int | None = None
    ) -> list[str]:
        """
        Trace along a given direction and return up to n piece IDs.
        """
        found = []

        if limit is None:
            limit = self.squares

        dy, dx = step
        r, f = self.rank, self.file

        for _ in range(limit):
            r += dy
            f += dx

            if not (0 <= r < len(self.board) and 0 <= f < len(self.board)):
                break

            piece = self.board.get_piece(coords=(r, f))
            if piece:
                found.append(piece.id)
                if len(found) >= n_pieces:
                    break

        return found

    def generate_validmoves(self, allies: List[str],  enforce_rules: bool = True) -> Tuple:

        valid_moves = set()
        danger_sqs = set()
        is_king_spotted = False
        checking_piece_id = ""
        directions = self.directions
        pin_status, legal_direction = self.pinned_status.values()

        if pin_status and enforce_rules:
            print(f"{self.id} is pinned, Valid dir is {legal_direction}")
            self.valid_moves = valid_moves
            directions = legal_direction if legal_direction[0] in self.directions else [
            ]

        for direction_name in directions:

            direction = self.game_scene.settings.directions[direction_name]
            directional_valid_moves, directional_danger_sqs, is_king_spotted = self.trace_direction(
                direction, allies)
            if is_king_spotted:
                checking_piece_id = self.id

            valid_moves.update(directional_valid_moves)
            danger_sqs.update(directional_danger_sqs)
        if enforce_rules:
            self.valid_moves = valid_moves
            return ()

        valid_moves.update(danger_sqs)
        return valid_moves, checking_piece_id

    def highlight_piece(self):
        rect_y = self.rank*self.height
        rect_x = self.file*self.width
        rect_w = self.width
        rect_h = self.height
        pygame.draw.rect(
            self.game_scene.screen,
            (255, 255, 0),  # Yellow color
            pygame.Rect(rect_x, rect_y, rect_w, rect_h),
            4  # Thickness of the border
        )

    def render_piece(self) -> None:

        self.game_scene.screen.blit(
            self.texture, (self.file*self.width+self.padding-2, self.rank*self.height+self.padding))
        if self.selected:
            self.highlight_piece()

    def move_piece(self, pos: tuple[int, int], allies: List[str], enforce_rules: bool = True) -> bool:

        rank, file = pos

        self.ensure_valid_moves(allies)

        if pos not in self.valid_moves and enforce_rules:
            return False

        self.board.move_piece_on_board(self.id, (rank, file))
        self.has_moved = True

        self.selected = False
        self.valid_moves = None
        self.game_scene.get_current_player().turn_complete = True
        self.game_scene.next_moves_surface = None

        return True

    def capture(self, pos: tuple[int, int], allies: List[str], ) -> bool:

        self.ensure_valid_moves(allies)
        rank, file = pos
        if (rank, file) not in self.valid_moves:
            return False

        if self.board.get_piece_id(
                (rank, file)) not in allies:
            target_piece = self.board.get_piece_id(
                (rank, file))
            if not target_piece:
                return False
            self.board.remove_piece(target_piece)
            self.game_scene.players[(self.game_scene.current_player + 1) %
                                    2].pieces.remove(target_piece)
            self.move_piece(pos, allies)

        return True

    @property
    def pos(self) -> Tuple[int, int]:
        return self.rank, self.file


class Pawn(Piece):
    def __init__(self, coords, size, screen_size,  texture_url, padding, piece_id, color, game):
        directions = ["up", "up_left", "up_right"]
        if piece_id.split('_')[0] == 'black':
            directions = ["down", "down_left", "down_right"]
        super().__init__(coords, size, screen_size,
                         texture_url, padding, piece_id, color, directions, 2, game)

        self.type = "pawn"
        self.category = "stepping"

    def generate_validmoves(self, allies: List[str],  enforce_rules: bool = True) -> Tuple:
        moves = set()
        is_pinned, pin_dir = self.pinned_status.values()

        if is_pinned and enforce_rules:

            y_dir, x_dir = pin_dir[0].split(
                "_") if "_" in pin_dir[0] else (pin_dir[0], "")

            print(f"{self.id} is pinned")
            if not self.directions[0].startswith(y_dir):
                self.valid_moves = moves

                return ()
            if x_dir:
                moves.update(self.get_pawn_capture_moves(allies)[0])
                self.valid_moves = moves
                return ()

        direction = -1 if self.id.startswith("white") else 1
        next_rank = self.rank + direction
        if 0 <= next_rank < len(self.board):
            # Forward move
            if self.board.get_piece_id((next_rank, self.file)) is None:
                moves.add((next_rank, self.file))
                # Two squares forward from starting position
                if not self.has_moved:
                    next_rank2 = self.rank + 2 * direction
                    if 0 <= next_rank2 < len(self.board) and self.board.get_piece_id((next_rank2, self.file)) is None:
                        moves.add((next_rank2, self.file))
                self.squares = 1

        if not is_pinned:
            moves.update(self.get_pawn_capture_moves(allies)[0])

        if enforce_rules:
            self.valid_moves = moves
            return ()
        return moves,

    def get_pawn_capture_moves(self, allies, enforce_rules: bool = True) -> Tuple[set[Tuple[int, int]], str]:
        captures = set()
        threatened = set()
        delivers_check = ""

        is_pinned, pin_dirs = self.pinned_status.values()
        pin_dir = pin_dirs[0]

        # If pinned, only allow captures in the pin direction
        x_steps = [-1, 1]
        if is_pinned and enforce_rules:
            x_steps = [1] if pin_dir.endswith("right") else [-1]

        step = -1 if self.id.startswith("white") else 1
        forward_rank = self.rank + step

        for dx in x_steps:
            target_file = self.file + dx
            if 0 <= target_file < len(self.board):
                piece = self.board.get_piece(
                    coords=(forward_rank, target_file))
                if piece and piece.id not in allies:
                    if piece.type == "king":
                        delivers_check = self.id
                    captures.add((forward_rank, target_file))
                threatened.add((forward_rank, target_file))

        if enforce_rules:
            return captures, delivers_check
        return threatened, delivers_check

    def promote(self):
        rank, file = self.rank, self.file
        piece_id = self.id.split('_')
        self.board.remove_piece(self.id)
        self.game_scene.get_current_player().pieces.remove(self.id)
        p_type = "queen"
        logging.info(f"Promoting {self.id} on {self.pos} to a {p_type}")
        self.board.create_piece(p_type, (rank, file),
                                piece_id, self.color, self.game_scene)

    def move_piece(self, pos: tuple[int, int], allies: List[str], enforce_rules: bool = True) -> bool:
        super().move_piece(pos, allies)
        if self.rank == 0 or self.rank == 7:
            self.promote()

        return True


class Queen(Piece):
    def __init__(self, coords, size, screen_size,  texture_url, padding, piece_id, color, game):
        super().__init__(coords, size, screen_size,
                         texture_url, padding, piece_id, color, ["up", "down", "left", "right",
                                                                 "up_left", "up_right", "down_left", "down_right"], len(game.board), game)

        self.type = "queen"
        self.category = "sliding"


class Rook(Piece):
    def __init__(self, coords, size, screen_size,  texture_url, padding, piece_id, color, game):
        super().__init__(coords, size, screen_size,
                         texture_url, padding, piece_id, color, ["up", "down", "left", "right"], len(game.board), game)
        self.directions = ["up", "down", "left", "right"]
        self.squares = len(game.board)
        self.type = "rook"
        self.category = "sliding"


class Bishop(Piece):
    def __init__(self, coords, size, screen_size,  texture_url, padding, piece_id, color, game):
        super().__init__(coords, size, screen_size,
                         texture_url, padding, piece_id, color, ["up_left", "up_right", "down_left", "down_right"], len(game.board), game)
        self.type = "bishop"
        self.category = "sliding"


class King(Piece):
    def __init__(self, coords, size, screen_size,  texture_url, padding, piece_id, color, game):
        super().__init__(coords, size, screen_size,
                         texture_url, padding, piece_id, color, ["up", "down", "left", "right", "up-left", "up-right", "down-left", "down-right"], 1, game)
        self.directions = ["up", "down", "left", "right",
                           "up_left", "up_right", "down_left", "down_right"]
        self.squares = 1
        self.type = "king"
        self.category = "stepping"
        self.checked = False
        self.checking_pieces = []
        self.castle_moves = set()

    def filter_moves_to(self, *_, **__):
        logging.debug(f"This method is deleted for king")

    def register_check(self, checking_piece_id):
        if checking_piece_id:
            self.checked = True
            self.checking_pieces.append(checking_piece_id)

    def generate_safe_king_moves(self, allies):
        logging.debug(f"Generating Safe King Moves...")

        self.generate_validmoves(allies)
        king_moves = self.valid_moves
        castle_moves = {(self.rank, self.file - 2), (self.rank, self.file + 2)}
        unsafe_sqs = set()

        for enemy_moves, attacker_id in self.game_scene.get_next_player().get_all_valid_moves():
            overlap = (king_moves | castle_moves) & enemy_moves
            logging.debug(
                f"{overlap}, Current Piece is  {attacker_id}")
            unsafe_sqs.update(overlap)
            self.register_check(attacker_id)

        self.valid_moves -= unsafe_sqs
        castle_moves -= unsafe_sqs
        self.generate_castle_moves(castle_moves)

        logging.info(f"{self.color} Kings Final Moves:{self.valid_moves}")

        self.game_scene.get_current_player().playable_moves_in_check += len(self.valid_moves)

    def generate_check_defenses(self, allies: List[str]) -> None:
        """Restrict ally moves to block or capture the checking piece."""

        if (attackers := len(self.checking_pieces)) >= 2:
            logging.debug(
                f"King is threatened by {attackers} pieces. No blocks possible — king must move."
            )
            return

        attacker = self.game_scene.board.get_piece(self.checking_pieces[0])
        attacker_pos = attacker.pos

        logging.info(f"Checking piece at {attacker_pos}")

        blocks = set()
        if attacker.category == "sliding":
            logging.debug("Generating block squares...")
            blocks = self.generate_check_block_path(attacker_pos)

        defense_squares = blocks | {attacker_pos}

        for p_id in allies:
            piece = self.game_scene.board.get_piece(p_id)
            piece.filter_moves_to(allies, defense_squares)

    def generate_check_block_path(self, threat_piece_coord: Tuple[int, int]) -> Set[Tuple[int, int]]:
        ky, kx = self.pos
        hy, hx = threat_piece_coord
        logging.debug(f"Making safe path for the piece on {hy, hx}")

        dx = hx - kx
        dy = hy - ky

        step_x = 0 if dx == 0 else (1 if hx < kx else -1)
        step_y = 0 if dy == 0 else (1 if hy < ky else -1)

        curr_x = hx
        curr_y = hy

        legal_moves = set()

        while (curr_x != kx or curr_y != ky) and (0 <= curr_x <= 7 and 0 <= curr_y <= 7):
            curr_x += step_x
            curr_y += step_y

            if (curr_y, curr_x) != (ky, kx):
                legal_moves.add((curr_y, curr_x))

        return legal_moves

    def generate_castle_moves(self, safe_castle_sqs: Set[Tuple[int, int]]) -> None:

        if self.checked or self.has_moved or not safe_castle_sqs:
            return

        for step in safe_castle_sqs:
            x_dir = 1 if step[1] > self.file else -1
            ray_piece_id = self.detect_pieces_in_direction(
                (0, x_dir), 1, len(self.board))[0]
            if not "rook" in ray_piece_id:
                continue
            ray_piece = self.board.get_piece(piece_id=ray_piece_id)

            if ray_piece.color == self.color and not ray_piece.has_moved and (self.rank, step[1] - x_dir) in self.valid_moves:
                self.valid_moves.add(step)
                self.castle_moves.add(step)

    def move_piece(self, pos: Tuple[int, int], allies: List[str], enforce_rules: bool = True) -> bool:
        x_dir = 1 if pos[1] > self.file else -1
        super().move_piece(pos, allies)
        if pos in self.castle_moves:
            rook_id = self.detect_pieces_in_direction(
                (0, x_dir), 1, len(self.board))[0]
            rook = self.board.get_piece(piece_id=rook_id)
            rook.move_piece((self.rank, self.file-x_dir),
                            allies, enforce_rules=False)
            self.castle_moves.clear()

        return True

    def detect_pins(self, allies: List[str]) -> None:
        """Detect pinned pieces by tracing along directions from this piece."""

        for dir_name in self.directions:
            step = self.game_scene.settings.directions[dir_name]

            # Find reverse direction’s name
            reverse_step = (-step[0], -step[1])
            reverse_name = next(
                name for name, vec in self.game_scene.settings.directions.items()
                if vec == reverse_step
            )

            # Collect pieces in this line (up to 2 potential targets)
            seen_pieces = self.detect_pieces_in_direction(
                step=step, n_pieces=2, limit=len(self.board) * 2)
            print(seen_pieces)

            if len(seen_pieces) != 2:
                continue

            pinned_id, attacker_id = seen_pieces

            # Skip if attacker is friendly or "pinned" piece is a king
            if attacker_id in allies or "king" in pinned_id:
                continue

            attacker = self.board.get_piece(piece_id=attacker_id)

            if reverse_name in attacker.directions and attacker.category == "sliding":
                print("Pinning the piece", pinned_id)
                pinned = self.board.get_piece(piece_id=pinned_id)
                pinned.pinned_status["pinned"] = True
                pinned.pinned_status["allowed_dir"] = [dir_name]

    def highlight_check(self):

        if not self.checked:
            return

        rect_y = self.rank*self.height
        rect_x = self.file*self.width
        rect_w = self.width
        rect_h = self.height
        overlay = pygame.Surface((rect_w, rect_h), pygame.SRCALPHA)
        overlay.fill((255, 0, 0, 100))  # Last value is alpha (transparency)
        self.game_scene.screen.blit(overlay, (rect_x, rect_y))

    def render_piece(self) -> None:
        super().render_piece()
        self.highlight_check()


class Knight(Piece):
    def __init__(self, coords, size, screen_size,  texture_url, padding, piece_id, color, game):
        super().__init__(coords, size, screen_size,
                         texture_url, padding, piece_id, color, ["knight"], 1, game)

        self.type = "knight"
        self.category = "stepping"

    def generate_validmoves(self, allies: List[str], enforce_rules: bool = True) -> Tuple:
        """Generate knight moves, respecting pins if legal=True."""

        moves = set()
        threatened = set()
        delivers_check = ""

        # Knights can’t move if pinned
        if self.pinned_status["pinned"] and enforce_rules:
            self.valid_moves = moves
            return ()

        for dy, dx in self.game_scene.settings.directions["knight"]:
            r, f = self.rank + dy, self.file + dx

            if not (0 <= r < len(self.board)) and (0 <= f < len(self.board)):
                continue

            threatened.add((r, f))
            piece = self.board.get_piece(coords=(r, f))

            if piece:
                if piece.id not in allies:
                    if piece.type == "king":
                        delivers_check = self.id
                    moves.add((r, f))
            else:
                moves.add((r, f))

        if enforce_rules:
            self.valid_moves = moves
            return ()
        return threatened, delivers_check
