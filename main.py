from gui import start_gui

from game.engine import game_loop

def main():
    user_choices = start_gui()
    game_loop(user_choices)

if __name__ == "__main__":
    main()
