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
            color: Tuple[int, int, int] = (255, 255, 255)
    ) -> None:

        self.text = text
        self.font_size = font_size
        self.color = color
        self.font = pygame.font.Font(font_style, self.font_size)
        self.font.set_bold(bold)
        self.text_surface = self.font.render(self.text, True, self.color)
        self.text_rect = self.text_surface.get_rect(center=pos)

    def draw(self, surface: pygame.Surface):
        surface.blit(self.text_surface, self.text_rect)


# pygame.init()

# screen = pygame.display.set_mode((400, 300))

# # Make a "card" surface
# card = pygame.Surface((200, 120), pygame.SRCALPHA)  # SRCALPHA → allows transparency

# rect = pygame.Rect(0, 0, 200, 120)

# # Background rectangle (filled)
# pygame.draw.rect(card, (30, 30, 30), rect, border_radius=12)

# # Outline rectangle on top
# pygame.draw.rect(card, (200, 200, 200), rect, width=3, border_radius=12)

# # Smaller inner rect (like highlight or section)
# inner = rect.inflate(-20, -20)
# pygame.draw.rect(card, (100, 180, 250), inner, border_radius=8)

# # Game loop
# running = True
# while running:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False

#     screen.fill((0, 0, 0))
#     screen.blit(card, (100, 90))  # slap your card onto the main screen
#     pygame.display.flip()
