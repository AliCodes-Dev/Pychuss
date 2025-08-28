import pygame
from typing import Tuple


class Label:
    def __init__(
            self,
            text: str,
            font_size: int,
            pos: Tuple[int, int],
            offset_x: int = 0,
            offset_y: int = 0,
            bold: bool = False,
            font_style: str | None = None,
            color: Tuple[int, int, int] = (255, 255, 255),
            line_spacing: int = 4
    ) -> None:

        self.text = text
        self.font_size = font_size
        self.color = color
        self.font = pygame.font.Font(font_style, self.font_size)
        self.font.set_bold(bold)
        self.text_surface = self.font.render(self.text, True, self.color)
        self.text_rect = self.text_surface.get_rect(center=pos)
        self.line_spacing = line_spacing
        self.lines = []

        if "/b/" in self.text:
            for i, line in enumerate(self.text.split("/b/")):
                new_line_surf = self.font.render(line, True, self.color)
                rect = new_line_surf.get_rect()

                rect.midtop = pos[0], pos[1] + i * \
                    (self.font_size + self.line_spacing)

                self.lines.append((new_line_surf, rect))
        else:
            self.text_surface = self.font.render(self.text, True, self.color)

    def draw(self, surface: pygame.Surface):
        if self.lines:
            for surf, rect in self.lines:
                surface.blit(surf, rect)
            return
        surface.blit(self.text_surface, self.text_rect)
