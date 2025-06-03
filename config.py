import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

PLAYER1_NAME = os.getenv("PLAYER1_NAME", "Ucieka")
PLAYER2_NAME = os.getenv("PLAYER2_NAME", "Goni")

PLAYER1_DESCRIPTION = os.getenv("PLAYER1_DESCRIPTION", "Player 1")
PLAYER2_DESCRIPTION = os.getenv("PLAYER2_DESCRIPTION", "Player 2")


GUNS = [
    (os.getenv("GUNNAME1", "Miotacz Spermy"), "gun1.png"),
    (os.getenv("GUNNAME2", "Bazooka Płodności"), "gun2.png"),
    (os.getenv("GUNNAME3", "Armata Rozkoszy"), "gun3.png"),
    (os.getenv("GUNNAME4", "Karabin Rozrodczy"), "gun4.png"),
    (os.getenv("GUNNAME5", "Katapulta Namiętności"), "gun5.png"),
]

VEHICLES = [
    (os.getenv("VEHICLENAME1", "Świnia"), "vehicle1.png"),
    (os.getenv("VEHICLENAME2", "Widlak"), "vehicle2.png"),
    (os.getenv("VEHICLENAME3", "Szambiarka"), "vehicle3.png"),
    (os.getenv("VEHICLENAME4", "Foka"), "vehicle4.png"),
    (os.getenv("VEHICLENAME5", "Taczka"), "vehicle5.png"),
]

VEHICLE_PLAYER1_IMAGES = {
    "Świnia": "player1_vehicle1.png",
    "Widlak": "player1_vehicle2.png",
    "Szambiarka": "player1_vehicle3.png",
    "Foka": "player1_vehicle4.png",
    "Taczka": "player1_vehicle5.png"
}

raw_date = os.getenv("WEDDING_DATE", "2025-06-15")

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
    WEDDING_DATE_FORMATTED = f"{day} {month} {year}"
except ValueError:
    WEDDING_DATE_FORMATTED = raw_date