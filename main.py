from gui import start_gui
import os
import ctypes

try:
    ctypes.windll.user32.SetProcessDPIAware()
except:
    pass


os.environ['SDL_AUDIODRIVER'] = 'directsound'

from game.engine import game_loop

def main():
    user_choices = start_gui()
    game_loop(user_choices)

if __name__ == "__main__":
    main()
