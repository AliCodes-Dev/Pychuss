from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..main import Game


class Scene:
    def __init__(self, game: "Game"):
        self.game = game  # reference to main Game manager

    def handle_event(self, event):
        pass

    def update(self, dt):
        pass

    def draw(self, screen):
        pass
