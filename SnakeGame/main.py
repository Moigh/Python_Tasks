import pygame
import sys
from game.screens import MenuScreen
from game.sound import SoundManager


def main():
    pygame.init()

    # Создаем менеджер звуков
    sound_manager = SoundManager()

    WIDTH, HEIGHT = 800, 600
    FPS = 60

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Змейка")
    clock = pygame.time.Clock()

    current_screen = MenuScreen(WIDTH, HEIGHT, sound_manager)
    running = True

    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False

        new_screen = current_screen.handle_events(events)

        if new_screen is None:
            running = False
        elif new_screen != current_screen:
            current_screen = new_screen
        else:
            new_screen = current_screen.update()
            if new_screen is not None and new_screen != current_screen:
                current_screen = new_screen

        current_screen.update()
        current_screen.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
