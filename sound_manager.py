import pygame
from sounds_config import *


initialized = False

def ensure_mixer():
    global initialized
    if not initialized:
        pygame.mixer.init()
        initialized = True


def sound_path(filename):
    base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))
    return os.path.join(base_path, "assets", "sounds", filename)

def play_music(filename, loop=True):
    ensure_mixer()
    pygame.mixer.music.load(sound_path(filename))
    pygame.mixer.music.play(-1 if loop else 0)

def stop_music():
    if initialized:
        pygame.mixer.music.stop()


def play_sound(filename):
    ensure_mixer()
    sound = pygame.mixer.Sound(sound_path(filename))
    sound.play()