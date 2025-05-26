# sound_manager.py

import pygame
from sounds_config import *

# Inicjalizacja miksera
pygame.mixer.init()

# 🎵 Muzyka
def play_music(path, loop=True):
    pygame.mixer.music.load(path)
    pygame.mixer.music.play(-1 if loop else 0)

def stop_music():
    pygame.mixer.music.stop()

# 🔊 Efekty
def play_sound(path):
    sound = pygame.mixer.Sound(path)
    sound.play()