from UI.panel import Panel
from Scenes.scene import Scene
import pygame
from enum import Enum
from typing import TYPE_CHECKING
from settings import ColorPalette
if TYPE_CHECKING:
    from ..main import Game



class MainMenu(Scene):
    def __init__(self, game: "Game"):
        super().__init__(game)
        self.name = "Main Menu"

        # Full-screen dark background panel
        self.main_panel = Panel(
            0, 0, self.game.settings.SCREEN_WIDTH, self.game.settings.SCREEN_HEIGHT,
            border_width=0, 
            border_color=ColorPalette.BACKGROUND.value, 
            bg_color=ColorPalette.BACKGROUND.value
        )

        # Title at top
        self.main_panel.add_component(
            "Label",
            text="PY Chuss",
            color=ColorPalette.TEXT.value,
            pos=(self.game.settings.SCREEN_WIDTH // 2, 120),
            font_size=48,
            bold=True,
            font_style="assets/font/PressStart2P.ttf"
        )

        # Play button
        self.main_panel.add_component(
            "Button",
            x=self.game.settings.SCREEN_WIDTH // 2, y=250, width=220, height=60,
            text="Start",
            bg_color=ColorPalette.BUTTON.value,
            hover_color=ColorPalette.BUTTON_HOVER.value,
            border_radius=12,
            on_click=self.game.play,
            font_size=28,
            font_style="assets/font/PressStart2P.ttf",
            text_color=ColorPalette.TEXT.value
        )

        # Quit button
        self.main_panel.add_component(
            "Button",
            x=self.game.settings.SCREEN_WIDTH // 2, y=350, width=220, height=60,
            text="QUIT",
            bg_color=ColorPalette.BUTTON.value,
            hover_color=ColorPalette.BUTTON_HOVER.value,
            border_radius=12,
            on_click=self.game.quit,
            font_size=28,
            font_style="assets/font/PressStart2P.ttf",
            text_color=ColorPalette.TEXT.value
        )

        # Footer note
        self.main_panel.add_component(
            "Label",
            text="Press Start to Begin",
            color=ColorPalette.TEXT_SECONDARY.value,
            pos=(self.game.settings.SCREEN_WIDTH // 2, self.game.settings.SCREEN_HEIGHT - 60),
            font_size=16,
            font_style="assets/font/PressStart2P.ttf"
        )
    def handle_event(self, event):
        self.main_panel.handle_event(event)

    def update(self, dt):
        pass

    def draw(self, screen):
        self.main_panel.draw(screen)
