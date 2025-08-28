import pygame
from typing import Type, List, Tuple
from UI.button import Button
from UI.label import Label


components = {
    "Button": Button,
    "Label": Label
}


class Panel:
    def __init__(
            self,
            x: int,
            y: int,
            width: int,
            height: int,
            border_width: int = 0,
            border_radius: int = 0,
            bg_color: Tuple[int, int, int] | Tuple[int,
                                                   int, int, int] = (50, 50, 50),
            border_color: Tuple[int, int, int] | None = None,


    ) -> None:
        self.rect = pygame.Rect(x, y, width, height)
        self.surface = pygame.Surface((width, height), pygame.SRCALPHA)
        self.components: List = []
        self.hovering = False
        self.border_width = border_width
        self.border_radius = border_radius
        self.border_color = border_color
        self.bg_color = bg_color

    def add_component(self, component_type: str, **kwargs):
        component_cls = components.get(component_type, None)
        if not component_cls:
            return

        kwargs["offset_x"] = self.rect.x
        kwargs["offset_y"] = self.rect.y

        comp = component_cls(**kwargs)
        self.components.append(comp)

    def draw(self, screen):
        self.surface.fill((0, 0, 0, 0))  # transparent

        pygame.draw.rect(
            self.surface,
            self.bg_color,
            self.surface.get_rect(),
            border_radius=self.border_radius
        )

        if self.border_color and self.border_width:
            pygame.draw.rect(
                self.surface,
                self.border_color,
                self.surface.get_rect(),
                border_radius=self.border_radius,
                width=self.border_width

            )
        for comp in self.components:
            comp.draw(self.surface)
        screen.blit(self.surface, self.rect.topleft)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            for comp in self.components:

                if hasattr(comp, "was_clicked"):
                    comp.was_clicked(event)

        hovering = any(btn.is_hover()
                       for btn in self.components if isinstance(btn, Button))

        if self.hovering != hovering:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND) if hovering else pygame.mouse.set_cursor(
                pygame.SYSTEM_CURSOR_ARROW)
            self.hovering = hovering
