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
from utils.helpers import draw_text, draw_center, draw_panel

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

options = ["Agumon", "Gabumon", "Tentomon"]

battle_log = ""
turn = "player"


# ==================================
# MENU
# ==================================
def draw_menu():
    screen.fill((25, 35, 65))

    draw_center(screen, "DIGIMON BATTLE", cfg.FONT_BIG, cfg.WHITE, 130)
    draw_center(screen, "Turn Based Adventure", cfg.FONT_SMALL, (180, 220, 255), 230)

    draw_panel(screen, 430, 360, 420, 70, (70, 120, 220))
    draw_center(screen, "ENTER - INICIAR", cfg.FONT_MEDIUM, cfg.WHITE, 378)

    draw_panel(screen, 430, 460, 420, 70, (120, 70, 70))
    draw_center(screen, "ESC - SALIR", cfg.FONT_MEDIUM, cfg.WHITE, 478)


# ==================================
# SELECCIÓN
# ==================================
def draw_selection():
    screen.fill((30, 55, 45))

    draw_center(screen, "ESCOGE TU DIGIMON", cfg.FONT_BIG, cfg.WHITE, 60)

    for i, name in enumerate(options):

        x = 170 + i * 320
        y = 260

        color = (220, 80, 80) if i == selected else (70, 90, 110)

        draw_panel(screen, x, y, 240, 280, color)

        text = cfg.FONT_MEDIUM.render(name, True, cfg.WHITE)
        text_x = x + 120 - text.get_width() // 2
        screen.blit(text, (text_x, y + 20))

        data = PLAYER_DIGIMON[name]

        draw_text(screen, f"HP: {data['hp']}", cfg.FONT_SMALL, cfg.WHITE, x + 30, y + 90)
        draw_text(screen, f"ATQ: {data['atq']}", cfg.FONT_SMALL, cfg.WHITE, x + 30, y + 130)
        draw_text(screen, f"DEF: {data['def']}", cfg.FONT_SMALL, cfg.WHITE, x + 30, y + 170)
        draw_text(screen, f"VEL: {data['vel']}", cfg.FONT_SMALL, cfg.WHITE, x + 30, y + 210)

    draw_center(
        screen,
        "← → mover | ENTER elegir | ESC volver",
        cfg.FONT_SMALL,
        cfg.WHITE,
        640
    )


# ==================================
# BATALLA
# ==================================
def draw_battle():
    screen.fill((45, 45, 65))

    draw_center(screen, "BATALLA DIGIMON", cfg.FONT_BIG, cfg.WHITE, 40)

    # PLAYER
    draw_panel(screen, 90, 180, 420, 260, (70, 110, 180))

    draw_text(screen, player["nombre"], cfg.FONT_MEDIUM, cfg.WHITE, 120, 210)
    draw_text(
        screen,
        f"HP: {player['hp']} / {player['hp_max']}",
        cfg.FONT_SMALL,
        cfg.WHITE,
        120,
        280
    )
    draw_text(screen, f"ATQ: {player['atq']}", cfg.FONT_SMALL, cfg.WHITE, 120, 330)
    draw_text(screen, f"DEF: {player['def']}", cfg.FONT_SMALL, cfg.WHITE, 120, 370)
    draw_text(screen, f"EXP: {player['exp']}", cfg.FONT_SMALL, cfg.WHITE, 120, 410)
    draw_text(screen, f"FORMA: {player['nombre']}", cfg.FONT_SMALL, cfg.WHITE, 120, 500)
    draw_text(screen, f"NIVEL: {player['nivel']}", cfg.FONT_SMALL, cfg.WHITE, 120, 440)
    draw_text(screen, f"MONEDAS: {player['monedas']}", cfg.FONT_SMALL, cfg.WHITE, 120, 470)

    # ENEMY
    draw_panel(screen, 770, 180, 420, 260, (180, 80, 80))

    draw_text(screen, enemy["nombre"], cfg.FONT_MEDIUM, cfg.WHITE, 800, 210)
    draw_text(
        screen,
        f"HP: {enemy['hp']} / {enemy['hp_max']}",
        cfg.FONT_SMALL,
        cfg.WHITE,
        800,
        280
    )
    draw_text(screen, f"ATQ: {enemy['atq']}", cfg.FONT_SMALL, cfg.WHITE, 800, 330)
    draw_text(screen, f"DEF: {enemy['def']}", cfg.FONT_SMALL, cfg.WHITE, 800, 370)

    # LOG DE COMBATE
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
        660
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

            # ================= MENU =================
            if scene == "menu":

                if event.key == pygame.K_RETURN:
                    scene = "selection"

                elif event.key == pygame.K_ESCAPE:
                    running = False

            # ============== SELECCIÓN ==============
            elif scene == "selection":

                if event.key == pygame.K_ESCAPE:
                    scene = "menu"

                elif event.key == pygame.K_LEFT:
                    selected = (selected - 1) % len(options)

                elif event.key == pygame.K_RIGHT:
                    selected = (selected + 1) % len(options)

                elif event.key == pygame.K_RETURN:

                    player = copy.deepcopy(
                        PLAYER_DIGIMON[options[selected]]
                    )

                    player["nombre"] = options[selected]

                    enemy = create_enemy(ENEMIES[1])

                    battle_log = "¡Comienza la batalla!"
                    turn = "player"

                    scene = "battle"

            # ================ BATALLA ================
            elif scene == "battle":

                if event.key == pygame.K_ESCAPE:
                    scene = "menu"

                elif event.key == pygame.K_RETURN:

                    # TURNO JUGADOR
                    if turn == "player":

                        dmg = player_attack(player, enemy)
                        battle_log = f"{player['nombre']} hace {dmg} daño"

                        if is_defeated(enemy):

                           leveled = add_exp(player, 30)
                           player["monedas"] += 15

                           if leveled:
                             battle_log = f"¡VICTORIA! {player['nombre']} ha mejorado o evolucionado"
                           else:
                             battle_log = "¡VICTORIA!"

                           continue

                        turn = "enemy"

                    # TURNO ENEMIGO
                    elif turn == "enemy":

                        dmg = enemy_attack(enemy, player)
                        battle_log = f"{enemy['nombre']} hace {dmg} daño"

                        if is_defeated(player):
                            battle_log = "¡DERROTA! pierdes 5 monedas"
                            player["monedas"] = max(0, player["monedas"] - 5)
                            continue

                        turn = "player"

    # ==================================
    # RENDER
    # ==================================
    if scene == "menu":
        draw_menu()

    elif scene == "selection":
        draw_selection()

    elif scene == "battle":
        draw_battle()

    pygame.display.flip()

pygame.quit()
sys.exit()