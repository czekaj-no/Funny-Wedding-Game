import os
import pygame
import sys
import time

from game.items import GUN_STATS, VEHICLE_STATS
from config import PLAYER1_NAME, PLAYER2_NAME
from sound_manager import play_music, stop_music, play_sound

from sounds_config import (
    GAME_MUSIC,
    END_MUSIC,
    GUN_SHOT,
    HIT_HURRA,
    HIT_GOODJOB,
    FAIL_LAUGH,
    ROUND_START,
    BABY
)



os.environ['SDL_VIDEO_CENTERED'] = '1'

# Stałe
WIDTH, HEIGHT = 1400, 1000
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (220, 50, 50)
BLUE = (50, 50, 255)

PLAYER_WIDTH, PLAYER_HEIGHT = 60, 80
BULLET_SIZE = 12

MAX_ROUNDS = 5
ROUND_TIME = 3  # sekundy

pygame.init()
play_music(GAME_MUSIC)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Plemnikator 3000")

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
    przemek = pygame.Rect(WIDTH - 100, 100, PLAYER_WIDTH, PLAYER_HEIGHT)
    oliwia = pygame.Rect(100, HEIGHT - 150, PLAYER_WIDTH, PLAYER_HEIGHT)
    return przemek, oliwia

def game_loop(user_choices):

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

    while round_number <= MAX_ROUNDS:
        round_start_time = time.time()
        bullets.clear()
        przemek, oliwia = get_start_positions()
        oliwia_velocity = [0, 0]
        last_shot_time = 0
        direction = "left"

        # --- Pokaż planszę i zagraj efekt odliczania
        screen.blit(game_bg, (0, 0))
        pygame.draw.rect(screen, RED, przemek)
        pygame.draw.rect(screen, BLUE, oliwia)

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

                pygame.draw.rect(screen, BLACK, bullet["rect"])

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
            pygame.draw.rect(screen, RED, przemek)
            pygame.draw.rect(screen, BLUE, oliwia)

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

