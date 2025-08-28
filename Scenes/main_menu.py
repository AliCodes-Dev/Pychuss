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
        self.main_panel = Panel(
            0, 0, self.game.settings.SCREEN_WIDTH, self.game.settings.SCREEN_HEIGHT,
            border_width=3, border_color=ColorPalette.BACKGROUND.value, bg_color=ColorPalette.BACKGROUND.value)
        self.main_panel.add_component(
            "Label",
            text="Main Menu",
            color=ColorPalette.TEXT.value,
            pos=(self.game.settings.SCREEN_WIDTH // 2, 100),
            font_size=32,

            font_style="assets/font/PressStart2P.ttf"
        )
        self.name = "Main Menu"
        self.main_panel.add_component(
            "Button",
            x=self.game.settings.SCREEN_WIDTH // 2, y=200, width=150, height=50,
            text="Play",
            bg_color=ColorPalette.BUTTON.value,
            border_radius=10,
            on_click=self.game.play,
            font_size=32,
            font_style="assets/font/PressStart2P.ttf",
            text_color=ColorPalette.TEXT_SECONDARY.value

        )
        self.main_panel.add_component(
            "Button",
            x=self.game.settings.SCREEN_WIDTH // 2, y=300, width=150, height=50,
            text="Quit",
            bg_color=ColorPalette.BUTTON.value,
            border_radius=10,
            on_click=self.game.quit,
            font_size=32,
            font_style="assets/font/PressStart2P.ttf",
            text_color=ColorPalette.TEXT_SECONDARY.value

        )

    def handle_event(self, event):
        self.main_panel.handle_event(event)

    def update(self, dt):
        pass

    def draw(self, screen):
        self.main_panel.draw(screen)
