import os
import sys

def sound_path(filename):
    base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))
    return os.path.join(base_path, "assets", "sounds", filename)

GUI_MUSIC = sound_path("gui_music.ogg")
GAME_MUSIC = sound_path("game_music.ogg")
END_MUSIC = sound_path("end_music.ogg")

GUN_SHOT = sound_path("gun_shot.wav")
HIT_HURRA = sound_path("hit_hurra.wav")
FAIL_LAUGH = sound_path("fail_laugh.wav")
ROUND_START = sound_path("round_start_beep.wav")
BABY = sound_path("baby.wav")