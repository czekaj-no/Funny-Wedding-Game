import customtkinter as ctk
from customtkinter import CTkImage
from config import (
    PLAYER1_NAME,
    PLAYER2_NAME,
    PLAYER1_DESCRIPTION,
    PLAYER2_DESCRIPTION,
    WEDDING_DATE_FORMATTED,
    GUNS,
    VEHICLES
)
import os
import sys
from PIL import Image
import tkinter.messagebox as mbox
from sound_manager import play_music, stop_music
from sounds_config import GUI_MUSIC



# Image path helper
def img_path(name):
    base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))
    return os.path.join(base_path, "assets", "images", name)


def load_intro_text():
    base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))
    intro_path = os.path.join(base_path, "assets", "intro.txt")

    with open(intro_path, "r", encoding="utf-8") as file:
        text = file.read()
        return text.format(
            WEDDING_DATE_FORMATTED=WEDDING_DATE_FORMATTED,
            PLAYER1_NAME=PLAYER1_NAME,
            PLAYER2_NAME=PLAYER2_NAME,
            PLAYER1_DESCRIPTION=PLAYER1_DESCRIPTION,
            PLAYER2_DESCRIPTION=PLAYER2_DESCRIPTION
        )


def start_gui():
    selected_data = {}
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("green")

    root = ctk.CTk()
    play_music(GUI_MUSIC)
    root.title("Plemnikator 3000: Nasienie Przeznaczenia")
    window_width = 1400
    window_height = 1000

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = int((screen_width / 2) - (window_width / 2))
    y = int((screen_height / 2) - (window_height / 2))

    root.geometry(f"{window_width}x{window_height}+{x}+{y}")
    icon_path = img_path("icon.ico")
    root.iconbitmap(default=icon_path)

    # Title
    title_img = Image.open(img_path("title.png"))
    title_photo = CTkImage(light_image=title_img, size=(350, 140))
    title_label = ctk.CTkLabel(root, image=title_photo, text="")
    title_label.pack(pady=10)

    # Subtitle
    subtitle_img = Image.open(img_path("subtitle.png"))
    subtitle_photo = CTkImage(light_image=subtitle_img, size=(300, 60))
    subtitle_label = ctk.CTkLabel(root, image=subtitle_photo, text="")
    subtitle_label.pack(pady=5)

    # Main container
    frame = ctk.CTkFrame(root)
    frame.pack(pady=10, expand=True, fill="both")

    left_frame = ctk.CTkFrame(frame, width=400)
    left_frame.pack(side="left", padx=20, fill="y")

    center_frame = ctk.CTkFrame(frame)
    center_frame.pack(side="left", padx=20, fill="both", expand=True)

    right_frame = ctk.CTkFrame(frame, width=400)
    right_frame.pack(side="right", padx=20, fill="y")

    # --- Player 1 (Oliwia) ---
    player1_label = ctk.CTkLabel(left_frame, text=PLAYER1_DESCRIPTION.upper(), font=("Arial", 18, "bold"))
    player1_label.pack(pady=(10, 5))

    oliwia_img = CTkImage(
        light_image=Image.open(img_path("oliwia.png")),
        size=(300, 400)
    )
    oliwia_label = ctk.CTkLabel(left_frame, image=oliwia_img, text="")
    oliwia_label.pack(pady=10)

    vehicle_label = ctk.CTkLabel(left_frame, text="Wybierz pojazd:", font=("Arial", 14, "bold"))
    vehicle_label.pack(pady=(10, 0))

    vehicle_var = ctk.StringVar()
    vehicle_dropdown = ctk.CTkComboBox(left_frame, values=[v[0] for v in VEHICLES], variable=vehicle_var, cursor="hand2")
    vehicle_dropdown.pack(pady=5)

    default_preview = CTkImage(
        light_image=Image.open(img_path("questionmark.png")),
        size=(240, 180)
    )

    vehicle_preview = ctk.CTkLabel(left_frame, image=default_preview, text="")
    vehicle_preview.image = default_preview
    vehicle_preview.pack(pady=5)

    # --- Player 2 (Przemek) ---
    player2_label = ctk.CTkLabel(right_frame, text=PLAYER2_DESCRIPTION.upper(), font=("Arial", 18, "bold"))
    player2_label.pack(pady=(10, 5))

    przemek_img = CTkImage(
        light_image=Image.open(img_path("przemek.png")),
        size=(300, 400)
    )
    przemek_label = ctk.CTkLabel(right_frame, image=przemek_img, text="")
    przemek_label.pack(pady=10)

    gun_label = ctk.CTkLabel(right_frame, text="Wybierz broń:", font=("Arial", 14, "bold"))
    gun_label.pack(pady=(10, 0))

    gun_var = ctk.StringVar()
    gun_dropdown = ctk.CTkComboBox(right_frame, values=[g[0] for g in GUNS], variable=gun_var, cursor="hand2")
    gun_dropdown.pack(pady=5)

    gun_preview = ctk.CTkLabel(right_frame, image=default_preview, text="")
    gun_preview.image = default_preview
    gun_preview.pack(pady=5)

    # --- Center section ---
    intro_label = ctk.CTkLabel(
        center_frame,
        text=load_intro_text(),
        font=("Arial", 16),
        justify="center",
        wraplength=400
    )
    intro_label.pack(pady=30)

    def start_game():
        nonlocal selected_data
        gun = gun_var.get()
        vehicle = vehicle_var.get()

        if not gun and not vehicle:
            mbox.showerror("Hola, hola!", "Wybierz broń i pojazd!")
            return
        elif not gun:
            mbox.showerror("Hola, hola!", "Wybierz broń dla Przemka!")
            return
        elif not vehicle:
            mbox.showerror("Hola, hola!", "Wybierz pojazd dla Oliwii!")
            return


        selected_data["gun_name"] = gun
        selected_data["vehicle_name"] = vehicle

        # Dodajemy ID broni i pojazdu (np. gun5, vehicle3)
        selected_data["gun_id"] = next((f"gun{i + 1}" for i, g in enumerate(GUNS) if g[0] == gun), None)
        selected_data["vehicle_id"] = next((f"vehicle{i + 1}" for i, v in enumerate(VEHICLES) if v[0] == vehicle), None)

        selected_data["gun_image"] = next((g[1] for g in GUNS if g[0] == gun), None)
        selected_data["vehicle_image"] = next((v[1] for v in VEHICLES if v[0] == vehicle), None)
        stop_music()
        root.quit()

    start_button = ctk.CTkButton(
        center_frame,
        text="START GAME",
        command=start_game,
        fg_color="#ed1c24",
        hover_color="#a50f19",
        font=("Arial", 20, "bold"),
        width=250,
        height=60
    )
    start_button.pack(pady=10)

    # --- Preview updates ---
    def update_vehicle_preview(choice):
        for name, filename in VEHICLES:
            if name == choice:
                img = CTkImage(
                    light_image=Image.open(img_path(filename)),
                    size=(240, 180)
                )
                vehicle_preview.configure(image=img)
                vehicle_preview.image = img

    def update_gun_preview(choice):
        for name, filename in GUNS:
            if name == choice:
                img = CTkImage(
                    light_image=Image.open(img_path(filename)),
                    size=(240, 180)
                )
                gun_preview.configure(image=img)
                gun_preview.image = img

    vehicle_dropdown.configure(command=update_vehicle_preview)
    gun_dropdown.configure(command=update_gun_preview)

    # --- Show GUI ---
    root.mainloop()
    root.destroy()
    return selected_data
