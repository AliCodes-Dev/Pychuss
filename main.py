import pygame
import logging
from rich.logging import RichHandler


from  settings import Settings,ColorPalette

from Scenes.main_menu import MainMenu
from Scenes.game_scene import GameScene
from Scenes.pause_menu import PauseMenu

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler()]
)


class Game:
    def __init__(self) -> None:
        pygame.init()

        self.settings = Settings()
        self._set_window()
        self._set_clock()

        self.is_game_over = False
        self.running = True

        # start at main menu
        self.gamescene = GameScene(self)
        self.mainmenu_scene = MainMenu(self)
        self.pausemenu = PauseMenu(self)
        self.current_scene = self.mainmenu_scene
        self.update_title()

    def _set_window(self) -> None:
        self.screen = pygame.display.set_mode(
            (self.settings.SCREEN_WIDTH, self.settings.SCREEN_HEIGHT)
        )
        pygame.display.set_caption(self.settings.title)
        icon = pygame.image.load(self.settings.icon)
        pygame.display.set_icon(icon)


    def switch_scene(self,scene):
        self.current_scene = scene
        self.screen.fill(ColorPalette.BLACK.value)
        self.update_title()


    def update_title(self):
        pygame.display.set_caption(self.current_scene.name)

    def quit(self):
        self.running = False

    def restart(self):
        # self.gamescene.restart()
        # self.switch_scene(self.gamescene)
        logging.info("Restart Method is not implemented yet.")
        

    def resume(self):
        self.current_scene = self.gamescene
        self.switch_scene(self.gamescene)
        

    def pause(self):
        self.switch_scene(self.pausemenu)
        

    def quit_to_menu(self):
        self.switch_scene(self.mainmenu_scene)

    def play(self):
        self.gamescene.restart()

        pygame.mouse.set_cursor(
            pygame.SYSTEM_CURSOR_ARROW)
        self.switch_scene(self.gamescene)

    def _set_clock(self) -> None:
        self.clock = pygame.time.Clock()

    def _tick_clock(self) -> float:
        dt = self.clock.tick(self.settings.frame_rate)
        return dt / 1000  # convert to seconds

    def run(self) -> None:
        while self.running:
            dt = self._tick_clock()

            # global events (like quitting)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                else:
                    # current scene handle your own events!!!
                    self.current_scene.handle_event(event)

            # update + render
            self.current_scene.update(dt)
            self.current_scene.draw(self.screen)

            pygame.display.flip()


if __name__ == "__main__":
    Game().run()
