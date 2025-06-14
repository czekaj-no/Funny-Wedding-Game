import customtkinter as ctk
from customtkinter import CTkImage
from config import PLAYER1_NAME, PLAYER2_NAME
from sound_manager import play_music, stop_music
from sounds_config import END_MUSIC
from PIL import Image
import os
from end_story import generate_story
import sys


def img_path(name):
    base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))
    return os.path.join(base_path, "assets", "images", name)


def show_end_screen(score, gun_image, vehicle_image):

    player1_score = 5 - score
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("green")

    root = ctk.CTk()
    root.withdraw()

    root.update()
    play_music(END_MUSIC)
    root.title("Wyniki - Plemnikator 3000")
    icon_path = img_path("icon.png")
    root.iconbitmap(default=icon_path)
    window_width = 1280
    window_height = 800
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = int((screen_width / 2) - (window_width / 2))
    y = int((screen_height / 2) - (window_height / 2))
    root.geometry(f"{window_width}x{window_height}+{x}+{y}")
    root.iconbitmap(default=img_path("icon.ico"))
    root.deiconify()

    header_img = Image.open(img_path("end_header.png"))
    header_photo = CTkImage(light_image=header_img, size=(600, 140))
    header_label = ctk.CTkLabel(root, image=header_photo, text="")
    header_label.pack(pady=10)


    frame = ctk.CTkFrame(root)
    frame.pack(pady=10, expand=True, fill="both")

    left_frame = ctk.CTkFrame(frame, width=365)
    left_frame.pack(side="left", padx=20, fill="y")

    center_frame = ctk.CTkFrame(frame)
    center_frame.pack(side="left", padx=20, fill="both", expand=True)

    right_frame = ctk.CTkFrame(frame, width=365)
    right_frame.pack(side="right", padx=20, fill="y")

    # --- Player 1 ---
    p1_name = ctk.CTkLabel(left_frame, text=PLAYER1_NAME.upper(), font=("Arial", 28, "bold"))
    p1_name.pack(pady=(10, 5))

    p1_img = CTkImage(light_image=Image.open(img_path("player1_image.png")), size=(220, 293))
    p1_label = ctk.CTkLabel(left_frame, image=p1_img, text="")
    p1_label.pack(pady=10)

    p1_score = ctk.CTkLabel(left_frame, text=f"UCIECZKA: {player1_score}/5", font=("Arial", 20))
    p1_score.pack(pady=5)

    vehicle_text = ctk.CTkLabel(left_frame, text="POJAZD:", font=("Arial", 20))
    vehicle_text.pack()

    vehicle_preview = CTkImage(light_image=Image.open(img_path(vehicle_image)), size=(180, 150))
    vehicle_label = ctk.CTkLabel(left_frame, image=vehicle_preview, text="")
    vehicle_label.pack(pady=5)

    # --- Player 2 ---
    p2_name = ctk.CTkLabel(right_frame, text=PLAYER2_NAME.upper(), font=("Arial", 28, "bold"))
    p2_name.pack(pady=(10, 5))

    p2_img = CTkImage(light_image=Image.open(img_path("player2_image.png")), size=(220, 293))
    p2_label = ctk.CTkLabel(right_frame, image=p2_img, text="")
    p2_label.pack(pady=10)

    p2_score = ctk.CTkLabel(right_frame, text=f"DZIECI: {score}/5", font=("Arial", 20))
    p2_score.pack(pady=5)

    gun_text = ctk.CTkLabel(right_frame, text="BROŃ:", font=("Arial", 20))
    gun_text.pack()

    gun_preview = CTkImage(light_image=Image.open(img_path(gun_image)), size=(180, 150))
    gun_label = ctk.CTkLabel(right_frame, image=gun_preview, text="")
    gun_label.pack(pady=5)

    # --- Story ---
    story_text, story_img_file = generate_story(score)

    # Images
    story_img = CTkImage(light_image=Image.open(img_path(story_img_file)), size=(300, 225))
    story_img_label = ctk.CTkLabel(center_frame, image=story_img, text="")
    story_img_label.pack(pady=(20, 10))

    # --- Story ---
    story_label = ctk.CTkLabel(center_frame, text=story_text, wraplength=400, font=("Arial", 20), justify="center")
    story_label.pack(pady=(0, 40))

    # --- Buttons ---
    def quit_game():
        stop_music()
        root.destroy()

    def play_again():
        stop_music()
        root.destroy()

        from gui import start_gui
        from game.engine import game_loop
        import pygame

        user_choices = start_gui()

        if user_choices:
            pygame.init()
            game_loop(user_choices)
            pygame.quit()

    play_button = ctk.CTkButton(center_frame, text="ZAGRAJ PONOWNIE", command=play_again,
                                fg_color="#ed1c24", hover_color="#a50f19", font=("Arial", 16, "bold"), width=200, height=50)
    play_button.pack(pady=5)

    exit_button = ctk.CTkButton(center_frame, text="WYJDŹ Z GRY", command=quit_game,  fg_color="#0F0F0F",  hover_color="#000000",
                                font=("Arial", 16), width=200, height=50)
    exit_button.pack(pady=5)

    root.mainloop()