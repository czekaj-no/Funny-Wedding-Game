import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

PLAYER1_NAME = os.getenv("PLAYER1_NAME", "Przemek")
PLAYER2_NAME = os.getenv("PLAYER2_NAME", "Oliwia")
BABY_HUNT_START = os.getenv("BABY_HUNT_START")

PLAYER1_DESCRIPTION = os.getenv("PLAYER1_DESCRIPTION", "Player 1")
PLAYER2_DESCRIPTION = os.getenv("PLAYER2_DESCRIPTION", "Player 2")


GUNS = [
    (os.getenv("GUNNAME1", "Gun of Destiny"), "gun1.png"),
    (os.getenv("GUNNAME2", "Love Blaster"), "gun2.png"),
    (os.getenv("GUNNAME3", "Seed Cannon"), "gun3.png"),
    (os.getenv("GUNNAME4", "Old Soviet Gun"), "gun4.png"),
    (os.getenv("GUNNAME5", "Mega P Shooter"), "gun5.png"),
]

VEHICLES = [
    (os.getenv("VEHICLENAME1", "Turbo Pig"), "vehicle1.png"),
    (os.getenv("VEHICLENAME2", "Startup Unicorn"), "vehicle2.png"),
    (os.getenv("VEHICLENAME3", "Corporate Scooter"), "vehicle3.png"),
    (os.getenv("VEHICLENAME4", "Escape Boots +5"), "vehicle4.png"),
    (os.getenv("VEHICLENAME5", "Dream Wagon"), "vehicle5.png"),
]

raw_date = os.getenv("WEDDING_DATE", "2024-05-31")

polish_months = {
    1: "stycznia",
    2: "lutego",
    3: "marca",
    4: "kwietnia",
    5: "maja",
    6: "czerwca",
    7: "lipca",
    8: "sierpnia",
    9: "września",
    10: "października",
    11: "listopada",
    12: "grudnia"
}

try:
    date_obj = datetime.strptime(raw_date, "%Y-%m-%d")
    day = date_obj.day
    month = polish_months[date_obj.month]
    year = date_obj.year
    WEDDING_DATE_FORMATTED = f"{day} {month} {year}"  # np. 31 maja 2024
except ValueError:
    WEDDING_DATE_FORMATTED = raw_date  # fallback jeśli format się nie zgadza