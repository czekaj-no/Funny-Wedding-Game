import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "assets", "sounds")

GUI_MUSIC = os.path.join(ASSETS_DIR, "gui_music.ogg")
GAME_MUSIC = os.path.join(ASSETS_DIR, "game_music.ogg")
END_MUSIC = os.path.join(ASSETS_DIR, "end_music.ogg")

GUN_SHOT = os.path.join(ASSETS_DIR, "gun_shot.wav")
HIT_HURRA = os.path.join(ASSETS_DIR, "hit_hurra.wav")
FAIL_LAUGH = os.path.join(ASSETS_DIR, "fail_laugh.wav")
ROUND_START = os.path.join(ASSETS_DIR, "round_start_beep.wav")
BABY = os.path.join (ASSETS_DIR, "baby.wav")

