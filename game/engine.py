import os
import pygame
import sys
import time

from game.items import GUN_STATS, VEHICLE_STATS
from config import PLAYER1_NAME, PLAYER2_NAME, VEHICLE_OLIWIA_IMAGES
from sound_manager import play_music, stop_music, play_sound
from config import GUNS


from sounds_config import (
    GAME_MUSIC,
    GUN_SHOT,
    HIT_HURRA,
    FAIL_LAUGH,
    ROUND_START,
    BABY
)

os.environ['SDL_VIDEO_CENTERED'] = '1'

# Stałe
WIDTH, HEIGHT = 1400, 1000
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

PRZEMEK_WIDTH = 140
PRZEMEK_HEIGHT = 140

OLIWIA_WIDTH = 132
OLIWIA_HEIGHT = 99


PLAYER_WIDTH, PLAYER_HEIGHT = 60, 80
BULLET_SIZE = 12

MAX_ROUNDS = 5
ROUND_TIME = 2 # sekundy

pygame.init()
play_music(GAME_MUSIC)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Plemnikator 3000")

# Wczytanie obrazków Przemka z bronią dla każdej broni i kierunku

def load_przemek_images(gun_name):
    gun_index = [g[0] for g in GUNS].index(gun_name) + 1
    directions = ["left", "right", "up", "down"]
    images = {}

    for dir in directions:
        filename = f"gun{gun_index}_przemek_{dir}.png"
        path = os.path.join("assets", "images", filename)
        if os.path.exists(path):
            image = pygame.image.load(path).convert_alpha()
            scaled_image = pygame.transform.scale(image, (PRZEMEK_WIDTH, PRZEMEK_HEIGHT))
            images[dir] = scaled_image
        else:
            images[dir] = None  # lub: pygame.Surface((PRZEMEK_WIDTH, PRZEMEK_HEIGHT))

    return images


# Ikonka
icon_path = os.path.join("assets", "images", "icon-png.png")
if os.path.exists(icon_path):
    pygame.display.set_icon(pygame.image.load(icon_path))

font = pygame.font.SysFont("Arial", 25)
clock = pygame.time.Clock()


def draw_text_centered(text, size=36, color=BLACK, duration=2):
    font_obj = pygame.font.SysFont("Arial", size)
    rendered = font_obj.render(text, True, color)
    rect = rendered.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(rendered, rect)
    pygame.display.update()
    time.sleep(duration)

def get_start_positions():

    # Przemek po prawej stronie
    przemek = pygame.Rect(WIDTH - PRZEMEK_WIDTH - 20, 100, PRZEMEK_WIDTH, PRZEMEK_HEIGHT)

    # Oliwia po lewej stronie
    oliwia = pygame.Rect(20, HEIGHT - OLIWIA_HEIGHT - 20, OLIWIA_WIDTH, OLIWIA_HEIGHT)

    return przemek, oliwia

def game_loop(user_choices):
    bullet_img_raw = pygame.image.load("assets/images/bullet.png").convert_alpha()
    bullet_img = pygame.transform.scale(bullet_img_raw, (BULLET_SIZE, BULLET_SIZE))

    baby_bg = pygame.image.load(os.path.join("assets", "images", "baby_bg.jpg"))
    fail_bg = pygame.image.load(os.path.join("assets", "images", "fail_bg.jpg"))
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    game_bg = pygame.image.load(os.path.join("assets", "images", "game_bg.jpg"))
    play_music(GAME_MUSIC)
    icon_path = os.path.join("assets", "images", "icon.png")
    pygame.display.set_icon(pygame.image.load(icon_path))
    pygame.display.set_caption("Plemnikator 3000")

    gun_name = user_choices["gun_name"]
    vehicle_name = user_choices["vehicle_name"]
    oliwia_image_file = VEHICLE_OLIWIA_IMAGES.get(vehicle_name)
    oliwia_image = pygame.image.load(os.path.join("assets", "images", oliwia_image_file)).convert_alpha()

    gun_stats = GUN_STATS.get(gun_name, {"speed": 10, "cooldown": 1.0})
    vehicle_stats = VEHICLE_STATS.get(vehicle_name, {"max_speed": 6, "acceleration": 0.2, "deceleration": 0.2})

    bullet_speed = gun_stats["speed"]
    gun_cooldown = gun_stats["cooldown"]

    oliwia_max_speed = vehicle_stats["max_speed"]
    oliwia_acc = vehicle_stats["acceleration"]
    oliwia_dec = vehicle_stats["deceleration"]

    przemek_score = 0
    oliwia_score = 0
    round_number = 1
    bullets = []
    last_shot_time = 0
    direction = "left"  # startowa orientacja Przemka

    oliwia_velocity = [0, 0]

    przemek, oliwia = get_start_positions()

    gun_name = user_choices["gun_name"]
    przemek_imgs = load_przemek_images(gun_name)
    current_przemek_image = przemek_imgs["left"]

    while round_number <= MAX_ROUNDS:
        round_start_time = time.time()
        bullets.clear()
        przemek, oliwia = get_start_positions()
        oliwia_velocity = [0, 0]
        last_shot_time = 0
        direction = "left"

        # --- Pokaż planszę i zagraj efekt odliczania
        screen.blit(game_bg, (0, 0))
        if current_przemek_image:
            screen.blit(current_przemek_image, (przemek.x, przemek.y))
        else:
            pygame.draw.rect(screen, RED, przemek)
        screen.blit(oliwia_image, oliwia)


        timer_text = font.render(f"Zegar tyka: {ROUND_TIME} s", True, BLACK)
        screen.blit(timer_text, (WIDTH // 2 - 150, 30))

        score_text = font.render(f"{PLAYER2_NAME}, masz {przemek_score} z możliwych {MAX_ROUNDS} bejbików", True, BLACK)
        screen.blit(score_text, (30, 30))

        pygame.display.update()

        play_sound(ROUND_START)
        time.sleep(4.2)

        # ⏱️ Dopiero teraz startujemy czas rundy!
        round_start_time = time.time()

        running = True
        while running:
            dt = clock.tick(60) / 1000
            screen.blit(game_bg, (0, 0))
            elapsed_time = time.time() - round_start_time
            remaining_time = max(0, int(ROUND_TIME - elapsed_time))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            keys = pygame.key.get_pressed()

            # --- Ruch Przemka (strzałki)
            if keys[pygame.K_LEFT]:
                przemek.x -= 5
                direction = "left"
            if keys[pygame.K_RIGHT]:
                przemek.x += 5
                direction = "right"
            if keys[pygame.K_UP]:
                przemek.y -= 5
                direction = "up"
            if keys[pygame.K_DOWN]:
                przemek.y += 5
                direction = "down"

            if direction in przemek_imgs and przemek_imgs [direction]:
                current_przemek_image = przemek_imgs[direction]
            else:
                current_przemek_image = None

            # Ograniczenie pozycji Przemka do granic okna gry
            przemek.x = max(0, min(przemek.x, WIDTH - przemek.width))
            przemek.y = max(0, min(przemek.y, HEIGHT - przemek.height))

            # --- Strzał (spacja)
            if keys[pygame.K_SPACE] and time.time() - last_shot_time >= gun_cooldown:
                play_sound(GUN_SHOT)
                last_shot_time = time.time()
                bullet = {
                    "rect": pygame.Rect(przemek.centerx, przemek.centery, BULLET_SIZE, BULLET_SIZE),
                    "dir": direction
                }
                bullets.append(bullet)

            # --- Ruch Oliwii (WASD) z rozpędzaniem
            target_vel = [0, 0]
            if keys[pygame.K_a]: target_vel[0] = -oliwia_max_speed
            if keys[pygame.K_d]: target_vel[0] = oliwia_max_speed
            if keys[pygame.K_w]: target_vel[1] = -oliwia_max_speed
            if keys[pygame.K_s]: target_vel[1] = oliwia_max_speed

            # Ograniczenie pozycji Oliwii do granic okna gry
            oliwia.x = max(0, min(oliwia.x, WIDTH - oliwia.width))
            oliwia.y = max(0, min(oliwia.y, HEIGHT - oliwia.height))

            # Przyspieszanie i hamowanie
            for i in range(2):
                if oliwia_velocity[i] < target_vel[i]:
                    oliwia_velocity[i] = min(oliwia_velocity[i] + oliwia_acc, target_vel[i])
                elif oliwia_velocity[i] > target_vel[i]:
                    oliwia_velocity[i] = max(oliwia_velocity[i] - oliwia_dec, target_vel[i])

            oliwia.x += int(oliwia_velocity[0])
            oliwia.y += int(oliwia_velocity[1])

            # --- Poruszanie się pocisków
            for bullet in bullets[:]:
                dx, dy = 0, 0
                if bullet["dir"] == "left": dx = -bullet_speed
                if bullet["dir"] == "right": dx = bullet_speed
                if bullet["dir"] == "up": dy = -bullet_speed
                if bullet["dir"] == "down": dy = bullet_speed

                bullet["rect"].x += dx
                bullet["rect"].y += dy

                screen.blit(bullet_img, bullet["rect"])

                if bullet["rect"].colliderect(oliwia):
                    przemek_score += 1
                    play_sound(HIT_HURRA)
                    time.sleep(2)
                    play_sound(BABY)
                    screen.blit(baby_bg, (0, 0))
                    pygame.display.update()
                    time.sleep(3)
                    running = False

                elif bullet["rect"].x < 0 or bullet["rect"].x > WIDTH or bullet["rect"].y < 0 or bullet["rect"].y > HEIGHT:
                    bullets.remove(bullet)

            # --- Koniec rundy przez czas
            if elapsed_time >= ROUND_TIME:
                oliwia_score += 1
                play_sound(FAIL_LAUGH)
                screen.blit(fail_bg, (0, 0))
                time.sleep (5)
                pygame.display.update()
                time.sleep(3)
                running = False

            # Rysowanie graczy i czasu
            if current_przemek_image:
                screen.blit(current_przemek_image, (przemek.x, przemek.y))
            else:
                pygame.draw.rect(screen, RED, przemek)

            screen.blit(oliwia_image, oliwia)
            timer_text = font.render(f"Zegar tyka: {remaining_time} s", True, BLACK)
            screen.blit(timer_text, (WIDTH // 2 - 150, 30))

            score_text = font.render(f"{PLAYER2_NAME}, masz {przemek_score} z możliwych {MAX_ROUNDS} bejbików", True, BLACK)
            screen.blit(score_text, (30, 30))

            pygame.display.update()

        round_number += 1

    stop_music()
    pygame.display.quit()

    from end_screen import show_end_screen
    show_end_screen(
        score=przemek_score,
        gun_name=user_choices["gun_name"],
        vehicle_name=user_choices["vehicle_name"],
        gun_image=user_choices["gun_image"],
        vehicle_image=user_choices["vehicle_image"]
    )

