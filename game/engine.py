import os
import pygame
import sys
import time
import ctypes


from game.items import GUN_STATS, VEHICLE_STATS
from config import PLAYER1_NAME, PLAYER2_NAME, VEHICLE_PLAYER1_IMAGES
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

# CONSTANTS
WIDTH, HEIGHT = 1280, 800

PLAYER2_WIDTH = 112
PLAYER2_HEIGHT = 112

PLAYER1_WIDTH = 100
PLAYER1_HEIGHT = 74


PLAYER_WIDTH, PLAYER_HEIGHT = 48, 64
BULLET_SIZE = 10

MAX_ROUNDS = 5
ROUND_TIME = 45

RED = 255,255,255
BLACK = 0,0,0


def get_path(*parts):
    base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))
    return os.path.join(base_path, *parts)

def load_player2_images(gun_name):
    gun_index = [g[0] for g in GUNS].index(gun_name) + 1
    directions = ["left", "right", "up", "down"]
    images = {}

    for dir in directions:
        filename = f"gun{gun_index}_player2_{dir}.png"
        path = get_path("assets", "images", filename)
        if os.path.exists(path):
            image = pygame.image.load(path).convert_alpha()
            scaled_image = pygame.transform.scale(image, (PLAYER2_WIDTH, PLAYER2_HEIGHT))
            images[dir] = scaled_image
        else:
            images[dir] = None

    return images

def get_start_positions():

    player2 = pygame.Rect(WIDTH - PLAYER2_WIDTH - 20, 100, PLAYER2_WIDTH, PLAYER2_HEIGHT)

    player1 = pygame.Rect(20, HEIGHT - PLAYER1_HEIGHT - 20, PLAYER1_WIDTH, PLAYER1_HEIGHT)

    return player2, player1

def game_loop(user_choices):
    try:
        ctypes.windll.user32.SetProcessDPIAware()
    except:
        pass

    os.environ['SDL_VIDEO_CENTERED'] = '1'

    pygame.init()

    play_music(GAME_MUSIC)
    pygame.display.set_caption("Plemnikator 3000")
    icon_path = get_path("assets", "images", "icon.png")
    if os.path.exists(icon_path):
        pygame.display.set_icon(pygame.image.load(icon_path))

    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SCALED)

    font = pygame.font.SysFont("Arial", 20)
    clock = pygame.time.Clock()

    game_bg = pygame.image.load(get_path("assets", "images", "game_bg.jpg"))
    bullet_img_raw = pygame.image.load(get_path("assets", "images", "bullet.png")).convert_alpha()
    gun_name = user_choices["gun_name"]
    bullet_width, bullet_height = GUN_STATS[gun_name]["size"]
    bullet_img = pygame.transform.scale(bullet_img_raw, (bullet_width, bullet_height))
    baby_bg = pygame.image.load(get_path("assets", "images", "baby_bg.jpg"))
    fail_bg = pygame.image.load(get_path("assets", "images", "fail_bg.jpg"))

    gun_name = user_choices["gun_name"]
    vehicle_name = user_choices["vehicle_name"]
    player1_image_file = VEHICLE_PLAYER1_IMAGES.get(vehicle_name)
    player1_image = pygame.image.load(get_path("assets", "images", player1_image_file)).convert_alpha()

    gun_stats = GUN_STATS.get(gun_name, {"speed": 10, "cooldown": 1.0})
    vehicle_stats = VEHICLE_STATS.get(vehicle_name, {"max_speed": 6, "acceleration": 0.2, "deceleration": 0.2})

    bullet_speed = gun_stats["speed"]
    gun_cooldown = gun_stats["cooldown"]

    player1_max_speed = vehicle_stats["max_speed"]
    player1_acc = vehicle_stats["acceleration"]
    player1_dec = vehicle_stats["deceleration"]

    player2_score = 0
    player1_score = 0
    round_number = 1
    bullets = []
    last_shot_time = 0
    direction = "left"
    player1_velocity = [0, 0]

    player2, player1 = get_start_positions()

    gun_name = user_choices["gun_name"]
    player2_imgs = load_player2_images(gun_name)
    current_player2_image = player2_imgs["left"]

    while round_number <= MAX_ROUNDS:
        round_start_time = time.time()
        bullets.clear()
        player2, player1 = get_start_positions()
        player1_velocity = [0, 0]
        last_shot_time = 0
        direction = "left"

        screen.blit(game_bg, (0, 0))
        if current_player2_image:
            screen.blit(current_player2_image, (player2.x, player2.y))
        else:
            pygame.draw.rect(screen, RED, player2)
        screen.blit(player1_image, player1)


        timer_text = font.render(f"Zegar tyka: {ROUND_TIME} s", True, BLACK)
        screen.blit(timer_text, (WIDTH // 2 - 150, 30))

        score_text = font.render(f"{PLAYER2_NAME}, masz {player2_score} z możliwych {MAX_ROUNDS} bejbików", True, BLACK)
        screen.blit(score_text, (30, 30))

        pygame.display.update()

        play_sound(ROUND_START)
        time.sleep(4.2)

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

            if keys[pygame.K_LEFT]:
                player2.x -= 5
                direction = "left"
            if keys[pygame.K_RIGHT]:
                player2.x += 5
                direction = "right"
            if keys[pygame.K_UP]:
                player2.y -= 5
                direction = "up"
            if keys[pygame.K_DOWN]:
                player2.y += 5
                direction = "down"

            if direction in player2_imgs and player2_imgs [direction]:
                current_player2_image = player2_imgs[direction]
            else:
                current_player2_image = None

            player2.x = max(0, min(player2.x, WIDTH - player2.width))
            player2.y = max(0, min(player2.y, HEIGHT - player2.height))

            if keys[pygame.K_SPACE] and time.time() - last_shot_time >= gun_cooldown:
                play_sound(GUN_SHOT)
                last_shot_time = time.time()
                bullet = {
                    "rect": pygame.Rect(player2.centerx, player2.centery, bullet_width, bullet_height),
                    "dir": direction
                }
                bullets.append(bullet)

            target_vel = [0, 0]
            if keys[pygame.K_a]: target_vel[0] = -player1_max_speed
            if keys[pygame.K_d]: target_vel[0] = player1_max_speed
            if keys[pygame.K_w]: target_vel[1] = -player1_max_speed
            if keys[pygame.K_s]: target_vel[1] = player1_max_speed

            player1.x = max(0, min(player1.x, WIDTH - player1.width))
            player1.y = max(0, min(player1.y, HEIGHT - player1.height))

            for i in range(2):
                if player1_velocity[i] < target_vel[i]:
                    player1_velocity[i] = min(player1_velocity[i] + player1_acc, target_vel[i])
                elif player1_velocity[i] > target_vel[i]:
                    player1_velocity[i] = max(player1_velocity[i] - player1_dec, target_vel[i])

            player1.x += int(player1_velocity[0])
            player1.y += int(player1_velocity[1])

            for bullet in bullets[:]:
                dx, dy = 0, 0
                if bullet["dir"] == "left": dx = -bullet_speed
                if bullet["dir"] == "right": dx = bullet_speed
                if bullet["dir"] == "up": dy = -bullet_speed
                if bullet["dir"] == "down": dy = bullet_speed

                bullet["rect"].x += dx
                bullet["rect"].y += dy

                screen.blit(bullet_img, bullet["rect"])

                if bullet["rect"].colliderect(player1):
                    player2_score += 1
                    play_sound(HIT_HURRA)
                    time.sleep(2)
                    play_sound(BABY)
                    screen.blit(baby_bg, (0, 0))
                    pygame.display.update()
                    time.sleep(3)
                    running = False

                elif bullet["rect"].x < 0 or bullet["rect"].x > WIDTH or bullet["rect"].y < 0 or bullet["rect"].y > HEIGHT:
                    bullets.remove(bullet)

            if elapsed_time >= ROUND_TIME:
                player1_score += 1
                play_sound(FAIL_LAUGH)
                screen.blit(fail_bg, (0, 0))
                time.sleep (5)
                pygame.display.update()
                time.sleep(3)
                running = False

            if current_player2_image:
                screen.blit(current_player2_image, (player2.x, player2.y))
            else:
                pygame.draw.rect(screen, RED, player2)

            screen.blit(player1_image, player1)
            timer_text = font.render(f"Zegar tyka: {remaining_time} s", True, BLACK)
            screen.blit(timer_text, (WIDTH // 2 - 150, 30))

            score_text = font.render(f"{PLAYER2_NAME}, masz {player2_score} z możliwych {MAX_ROUNDS} bejbików", True, BLACK)
            screen.blit(score_text, (30, 30))

            pygame.display.update()

        round_number += 1

    stop_music()
    pygame.display.quit()

    from end_screen import show_end_screen
    show_end_screen(
        score=player2_score,
        gun_image=user_choices["gun_image"],
        vehicle_image=user_choices["vehicle_image"]
    )