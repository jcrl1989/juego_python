import pygame
import sys
import copy

import config as cfg

from data.digimon_data import PLAYER_DIGIMON, ENEMIES

from systems.battle import (
    create_enemy,
    player_attack,
    enemy_attack,
    is_defeated
)

from systems.leveling import add_exp

from systems.world import (
    random_encounter,
    get_zone_name,
    get_enemy_level,
    update_zone
)

from utils.helpers import (
    draw_text,
    draw_center,
    draw_panel,
    draw_hp_bar
)

from utils.loader import load_sprite

pygame.init()

screen = pygame.display.set_mode((cfg.WIDTH, cfg.HEIGHT))
pygame.display.set_caption(cfg.TITLE)

clock = pygame.time.Clock()

# ==================================
# ESTADO DEL JUEGO
# ==================================
scene = "menu"

selected = 0

player = None
enemy = None

player_sprite = None
enemy_sprite = None

options = ["Agumon", "Gabumon", "Tentomon"]

battle_log = ""

turn = "player"

# WORLD
world_x = 600
world_y = 350

current_zone = 1


# ==================================
# MENU
# ==================================
def draw_menu():

    screen.fill((25, 35, 65))

    draw_center(
        screen,
        "DIGIMON BATTLE",
        cfg.FONT_BIG,
        cfg.WHITE,
        130
    )

    draw_center(
        screen,
        "Turn Based Adventure",
        cfg.FONT_SMALL,
        (180, 220, 255),
        230
    )

    draw_panel(
        screen,
        430,
        360,
        420,
        70,
        (70, 120, 220)
    )

    draw_center(
        screen,
        "ENTER - INICIAR",
        cfg.FONT_MEDIUM,
        cfg.WHITE,
        378
    )

    draw_panel(
        screen,
        430,
        460,
        420,
        70,
        (120, 70, 70)
    )

    draw_center(
        screen,
        "ESC - SALIR",
        cfg.FONT_MEDIUM,
        cfg.WHITE,
        478
    )


# ==================================
# SELECCION
# ==================================
def draw_selection():

    screen.fill((30, 55, 45))

    draw_center(
        screen,
        "ESCOGE TU DIGIMON",
        cfg.FONT_BIG,
        cfg.WHITE,
        60
    )

    for i, name in enumerate(options):

        x = 170 + i * 320
        y = 260

        color = (
            (220, 80, 80)
            if i == selected
            else (70, 90, 110)
        )

        draw_panel(
            screen,
            x,
            y,
            240,
            280,
            color
        )

        text = cfg.FONT_MEDIUM.render(
            name,
            True,
            cfg.WHITE
        )

        text_x = x + 120 - text.get_width() // 2

        screen.blit(
            text,
            (text_x, y + 20)
        )

        data = PLAYER_DIGIMON[name]

        draw_text(
            screen,
            f"HP: {data['hp']}",
            cfg.FONT_SMALL,
            cfg.WHITE,
            x + 30,
            y + 90
        )

        draw_text(
            screen,
            f"ATQ: {data['atq']}",
            cfg.FONT_SMALL,
            cfg.WHITE,
            x + 30,
            y + 130
        )

        draw_text(
            screen,
            f"DEF: {data['def']}",
            cfg.FONT_SMALL,
            cfg.WHITE,
            x + 30,
            y + 170
        )

        draw_text(
            screen,
            f"VEL: {data['vel']}",
            cfg.FONT_SMALL,
            cfg.WHITE,
            x + 30,
            y + 210
        )

    draw_center(
        screen,
        "← → mover | ENTER elegir | ESC volver",
        cfg.FONT_SMALL,
        cfg.WHITE,
        640
    )


# ==================================
# WORLD
# ==================================
def draw_world():

    screen.fill((40, 120, 70))

    draw_center(
        screen,
        "MUNDO DIGITAL",
        cfg.FONT_BIG,
        cfg.WHITE,
        30
    )

    pygame.draw.rect(
        screen,
        (255, 220, 80),
        (world_x, world_y, 40, 40)
    )

    draw_text(
        screen,
        f"Digimon: {player['nombre']}",
        cfg.FONT_SMALL,
        cfg.WHITE,
        40,
        140
    )

    draw_text(
        screen,
        f"Nivel: {player['nivel']}",
        cfg.FONT_SMALL,
        cfg.WHITE,
        40,
        180
    )

    draw_text(
        screen,
        f"HP: {player['hp']} / {player['hp_max']}",
        cfg.FONT_SMALL,
        cfg.WHITE,
        40,
        220
    )

    draw_text(
        screen,
        f"Monedas: {player['monedas']}",
        cfg.FONT_SMALL,
        cfg.WHITE,
        40,
        260
    )

    draw_text(
        screen,
        f"Zona: {get_zone_name(current_zone)}",
        cfg.FONT_SMALL,
        cfg.WHITE,
        40,
        300
    )

    draw_center(
        screen,
        "WASD mover | ESC menu",
        cfg.FONT_SMALL,
        cfg.WHITE,
        680
    )


# ==================================
# BATALLA
# ==================================
def draw_battle():

    screen.fill((45, 45, 65))

    draw_center(
        screen,
        "BATALLA DIGIMON",
        cfg.FONT_BIG,
        cfg.WHITE,
        40
    )

    # PANEL PLAYER
    draw_panel(
        screen,
        70,
        160,
        500,
        420,
        (70, 110, 180)
    )

    # PANEL ENEMIGO
    draw_panel(
        screen,
        720,
        160,
        500,
        360,
        (180, 80, 80)
    )

    # SPRITES
    if player_sprite:
        screen.blit(player_sprite, (200, 260))

    if enemy_sprite:
        screen.blit(enemy_sprite, (860, 240))

    # NOMBRE PLAYER
    draw_text(
        screen,
        player["nombre"],
        cfg.FONT_MEDIUM,
        cfg.WHITE,
        120,
        190
    )

    # HP PLAYER
    draw_hp_bar(
        screen,
        120,
        240,
        260,
        22,
        player["hp"],
        player["hp_max"]
    )

    draw_text(
        screen,
        f"{player['hp']} / {player['hp_max']}",
        cfg.FONT_SMALL,
        cfg.WHITE,
        390,
        240
    )

    draw_text(
        screen,
        f"Nivel: {player['nivel']}",
        cfg.FONT_SMALL,
        cfg.WHITE,
        120,
        290
    )

    draw_text(
        screen,
        f"EXP: {player['exp']}",
        cfg.FONT_SMALL,
        cfg.WHITE,
        120,
        330
    )

    draw_text(
        screen,
        f"Monedas: {player['monedas']}",
        cfg.FONT_SMALL,
        cfg.WHITE,
        120,
        370
    )

    # NOMBRE ENEMIGO
    draw_text(
        screen,
        enemy["nombre"],
        cfg.FONT_MEDIUM,
        cfg.WHITE,
        760,
        190
    )

    # HP ENEMIGO
    draw_hp_bar(
        screen,
        760,
        240,
        260,
        22,
        enemy["hp"],
        enemy["hp_max"]
    )

    draw_text(
        screen,
        f"{enemy['hp']} / {enemy['hp_max']}",
        cfg.FONT_SMALL,
        cfg.WHITE,
        1030,
        240
    )

    draw_text(
        screen,
        f"ATQ: {enemy['atq']}",
        cfg.FONT_SMALL,
        cfg.WHITE,
        760,
        290
    )

    draw_text(
        screen,
        f"DEF: {enemy['def']}",
        cfg.FONT_SMALL,
        cfg.WHITE,
        760,
        330
    )

    # LOG
    draw_center(
        screen,
        battle_log,
        cfg.FONT_SMALL,
        cfg.WHITE,
        620
    )

    draw_center(
        screen,
        "ENTER atacar | ESC salir",
        cfg.FONT_SMALL,
        cfg.WHITE,
        670
    )


# ==================================
# LOOP PRINCIPAL
# ==================================
running = True

while running:

    clock.tick(cfg.FPS)

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            # MENU
            if scene == "menu":

                if event.key == pygame.K_RETURN:
                    scene = "selection"

                elif event.key == pygame.K_ESCAPE:
                    running = False

            # SELECCION
            elif scene == "selection":

                if event.key == pygame.K_ESCAPE:
                    scene = "menu"

                elif event.key == pygame.K_LEFT:
                    selected = (selected - 1) % len(options)

                elif event.key == pygame.K_RIGHT:
                    selected = (selected + 1) % len(options)

                elif event.key == pygame.K_RETURN:

                    player = copy.deepcopy(
                        PLAYER_DIGIMON[
                            options[selected]
                        ]
                    )

                    player["nombre"] = options[selected]

                    battle_log = "Explora el mundo"

                    scene = "world"

            # WORLD
            elif scene == "world":

                speed = 15

                if event.key == pygame.K_w:
                    world_y -= speed

                elif event.key == pygame.K_s:
                    world_y += speed

                elif event.key == pygame.K_a:
                    world_x -= speed

                elif event.key == pygame.K_d:
                    world_x += speed

                elif event.key == pygame.K_ESCAPE:
                    scene = "menu"

                current_zone = update_zone(
                    player["nivel"]
                )

                if random_encounter():

                    enemy_level = get_enemy_level(
                        current_zone
                    )

                    enemy = create_enemy(
                        ENEMIES[enemy_level]
                    )

                    player_sprite = load_sprite(
                        player["nombre"]
                    )

                    enemy_sprite = load_sprite(
                        enemy["nombre"]
                    )

                    battle_log = (
                        "¡Un Digimon salvaje apareció!"
                    )

                    turn = "player"

                    scene = "battle"

            # BATALLA
            elif scene == "battle":

                if event.key == pygame.K_ESCAPE:
                    scene = "world"

                elif event.key == pygame.K_RETURN:

                    # PLAYER
                    if turn == "player":

                        dmg = player_attack(
                            player,
                            enemy
                        )

                        battle_log = (
                            f"{player['nombre']} hace "
                            f"{dmg} daño"
                        )

                        if is_defeated(enemy):

                            leveled = add_exp(
                                player,
                                30
                            )

                            player["monedas"] += 15

                            if leveled:
                                battle_log = (
                                    f"¡{player['nombre']} "
                                    f"mejoró!"
                                )
                            else:
                                battle_log = "¡VICTORIA!"

                            scene = "world"
                            continue

                        turn = "enemy"

                    # ENEMIGO
                    elif turn == "enemy":

                        dmg = enemy_attack(
                            enemy,
                            player
                        )

                        battle_log = (
                            f"{enemy['nombre']} hace "
                            f"{dmg} daño"
                        )

                        if is_defeated(player):

                            player["monedas"] = max(
                                0,
                                player["monedas"] - 5
                            )

                            battle_log = (
                                "¡DERROTA! "
                                "Pierdes 5 monedas"
                            )

                            scene = "menu"
                            continue

                        turn = "player"

    # ==================================
    # RENDER
    # ==================================
    if scene == "menu":
        draw_menu()

    elif scene == "selection":
        draw_selection()

    elif scene == "world":
        draw_world()

    elif scene == "battle":
        draw_battle()

    pygame.display.flip()

pygame.quit()
sys.exit()