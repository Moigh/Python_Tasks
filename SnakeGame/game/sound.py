import pygame
import os


class SoundManager:
    def __init__(self):
        pygame.mixer.init()
        self.sounds = {}
        self._load_sounds()

    def _load_sounds(self):
        """Загружает все звуковые файлы"""
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(current_dir)
        sounds_path = os.path.join(project_root, "assets", "sounds")

        # Загружаем звуки
        self.sounds = {
            'eat': pygame.mixer.Sound(os.path.join(sounds_path, 'eat_apple.mp3')),
            'collision': pygame.mixer.Sound(os.path.join(sounds_path, 'collision.mp3')),
            'victory': pygame.mixer.Sound(os.path.join(sounds_path, 'victory.mp3')),
            'button': pygame.mixer.Sound(os.path.join(sounds_path, 'menu.mp3'))
        }

    def play_background_music(self):
        """Запускает фоновую музыку"""
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(current_dir)
        music_path = os.path.join(
            project_root,
            "assets",
            "sounds",
            "background_music.mp3")

        pygame.mixer.music.load(music_path)
        pygame.mixer.music.play(-1)  # -1 означает бесконечный повтор

    def stop_background_music(self):
        """Останавливает фоновую музыку"""
        pygame.mixer.music.stop()

    def play_sound(self, sound_name):
        """Проигрывает звуковой эффект"""
        if sound_name in self.sounds:
            self.sounds[sound_name].play()
