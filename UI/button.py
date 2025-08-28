import pygame
from typing import Callable, Tuple

from UI.label import Label


class Button:
    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        text: str,
        font_size: int = 36,
        font_style: str | None = None,
        on_click: Callable | None = None,
        border_width: int = 0,
        border_radius: int = 0,
        offset_x: int = 0,
        offset_y: int = 0,
        hover_color: Tuple[int, int, int] | None = None,
        active_color: Tuple[int, int, int] | None = None,
        border_color: Tuple[int, int, int] | None = None,
        bg_color: Tuple[int, int, int] = (50, 50, 50),
        text_color: Tuple[int, int, int] = (255, 255, 255)
    ) -> None:
        print(locals())

        self.rect = pygame.Rect(x, y, width, height)

        self.rect.center = x, y
        self.bg_color = bg_color
        self.border_width = border_width
        self.border_radius = border_radius
        self.offset_x = offset_x
        self.offset_y = offset_y

        self.border_color = border_color
        self.hover_color = hover_color or tuple(
            min(c+30, 255) for c in self.bg_color)
        self.active_color = active_color or tuple(
            max(c-30, 0) for c in self.bg_color)

        self.on_click = on_click

        # surface for the button itself
        self.surface = pygame.Surface((width, height), pygame.SRCALPHA)
        self.surface_rect = self.surface.get_rect()

        # label
        self.label = Label(
            text, font_size,  (width // 2, height // 2), color=text_color,  font_style=font_style)

    def handle_click(self):
        if self.on_click:
            self.on_click()
            return True
        return False

    def was_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.is_hover():
            self.handle_click()

            return True

        return False

    def is_hover(self):
        mouse_pos = pygame.mouse.get_pos()
        x, y = mouse_pos[0] - self.offset_x, mouse_pos[1] - self.offset_y

        if self.rect.collidepoint(x, y):
            return True

        return False

    def is_active(self):
        mouse_btns = pygame.mouse.get_pressed()
        if mouse_btns[0]:
            return True
        return False

    def draw(self, target_surface):
        bg_color = self.bg_color
        if self.is_hover():
            bg_color = self.hover_color if not self.is_active() else self.active_color

        pygame.draw.rect(
            self.surface,
            bg_color,
            self.surface_rect,
            border_radius=self.border_radius
        )

        if self.border_color is not None and self.border_width > 0:

            pygame.draw.rect(
                self.surface,
                self.border_color,
                self.surface_rect,
                width=self.border_width,
                border_radius=self.border_radius
            )

        self.label.draw(self.surface)

        target_surface.blit(self.surface, (self.rect.x, self.rect.y))
