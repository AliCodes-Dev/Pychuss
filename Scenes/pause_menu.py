from UI.panel import Panel
from Scenes.scene import Scene
import pygame
from typing import TYPE_CHECKING
from settings import ColorPalette

if TYPE_CHECKING:
    from ..main import Game


class PauseMenu(Scene):
    def __init__(self, game: "Game"):
        super().__init__(game)
        self.name = "Paused"

        # Semi-transparent overlay panel
        self.overlay = Panel(
            0, 0, self.game.settings.SCREEN_WIDTH, self.game.settings.SCREEN_HEIGHT,
            border_width=0,
            bg_color=(0, 0, 0, 180)  # black with alpha for dim effect
        )

        # Title
        self.overlay.add_component(
            "Label",
            text="Paused",
            color=ColorPalette.TEXT.value,
            pos=(self.game.settings.SCREEN_WIDTH // 2, 120),
            font_size=28,
            font_style="assets/font/PressStart2P.ttf"
        )

        # Resume button
        self.overlay.add_component(
            "Button",
            x=self.game.settings.SCREEN_WIDTH // 2, y=220,
            width=200, height=50,
            text="Resume",
            bg_color=ColorPalette.BUTTON.value,
            border_radius=12,
            on_click=self.game.resume,
            font_size=24,
            font_style="assets/font/PressStart2P.ttf",
            text_color=ColorPalette.TEXT_SECONDARY.value
        )

        # Restart button
        self.overlay.add_component(
            "Button",
            x=self.game.settings.SCREEN_WIDTH // 2, y=300,
            width=200, height=50,
            text="Restart",
            bg_color=ColorPalette.BUTTON.value,
            border_radius=12,
            on_click=self.game.restart,
            font_size=24,
            font_style="assets/font/PressStart2P.ttf",
            text_color=ColorPalette.TEXT_SECONDARY.value
        )

        # Quit to main menu
        self.overlay.add_component(
            "Button",
            x=self.game.settings.SCREEN_WIDTH // 2, y=380,
            width=250, height=50,
            text="Main Menu",
            bg_color=ColorPalette.BUTTON.value,
            border_radius=12,
            on_click=self.game.quit_to_menu,
            font_size=24,
            font_style="assets/font/PressStart2P.ttf",
            text_color=ColorPalette.TEXT_SECONDARY.value
        )

        pygame.display.set_caption("Paused")

    def handle_event(self, event):
        self.overlay.handle_event(event)

    def update(self, dt):
        pass

    def draw(self, screen):
        # Instead of clearing, we just draw the overlay panel on top
        self.overlay.draw(screen)
