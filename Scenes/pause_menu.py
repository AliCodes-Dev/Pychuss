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

        # Semi-transparent overlay using PANEL color
        self.overlay = Panel(
            0, 0, self.game.settings.SCREEN_WIDTH, self.game.settings.SCREEN_HEIGHT,
            border_width=0,
            bg_color=(*ColorPalette.PANEL.value, 180)  # consistent with style
        )

        # Title
        self.overlay.add_component(
            "Label",
            text="Paused",
            color=ColorPalette.TEXT.value,
            pos=(self.game.settings.SCREEN_WIDTH // 2, 120),
            font_size=36,
            font_style="assets/font/PressStart2P.ttf",
            
            bold=True
        )

        btn_w, btn_h = 220, 55
        btn_x = self.game.settings.SCREEN_WIDTH // 2
        start_y = 220
        spacing = 80

        buttons = [
            ("Resume", self.game.resume),
            ("Restart", self.game.restart),
            ("Main Menu", self.game.quit_to_menu),
        ]

        for i, (label, callback) in enumerate(buttons):
            self.overlay.add_component(
                "Button",
                x=btn_x, y=start_y + i * spacing,
                width=btn_w, height=btn_h,
                text=label,
                bg_color=ColorPalette.BUTTON.value,
                hover_color=ColorPalette.BUTTON_HOVER.value,
                border_radius=14,
                on_click=callback,
                font_size=20,
                font_style="assets/font/PressStart2P.ttf",
                text_color=ColorPalette.TEXT.value
            )


    def handle_event(self, event):
        self.overlay.handle_event(event)

    def update(self, dt):
        pass

    def draw(self, screen):
        
        self.overlay.draw(screen)
