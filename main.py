import pygame
import sys
import copy

import config as cfg
from data.digimon_data import PLAYER_DIGIMON, ENEMIES, EVOLUTIONS

pygame.init()

screen = pygame.display.set_mode((cfg.WIDTH, cfg.HEIGHT))
pygame.display.set_caption(cfg.TITLE)

clock = pygame.time.Clock()

scene = "menu"
selected = 0
player = None

options = ["Agumon", "Gabumon", "Tentomon"]


# ===============================
# UTILIDADES
# ===============================
def draw_text(text, font, color, x, y):
    img = font.render(text, True, color)
    screen.blit(img, (x, y))


def draw_center(text, font, color, y):
    img = font.render(text, True, color)
    x = cfg.WIDTH // 2 - img.get_width() // 2
    screen.blit(img, (x, y))


def draw_panel(x, y, w, h, color):
    pygame.draw.rect(screen, color, (x, y, w, h), border_radius=18)


# ===============================
# MENU
# ===============================
def draw_menu():
    screen.fill((25, 35, 65))

    draw_center("DIGIMON BATTLE", cfg.FONT_BIG, cfg.WHITE, 130)
    draw_center("Turn Based Adventure", cfg.FONT_SMALL, (180, 220, 255), 230)

    draw_panel(430, 360, 420, 70, (70, 120, 220))
    draw_center("ENTER - INICIAR", cfg.FONT_MEDIUM, cfg.WHITE, 378)

    draw_panel(430, 460, 420, 70, (120, 70, 70))
    draw_center("ESC - SALIR", cfg.FONT_MEDIUM, cfg.WHITE, 478)


# ===============================
# SELECCION
# ===============================
def draw_selection():
    screen.fill((30, 55, 45))

    # Título superior
    draw_center("ESCOGE TU DIGIMON", cfg.FONT_BIG, cfg.WHITE, 60)

    for i, name in enumerate(options):

        x = 170 + i * 320
        y = 260

        # Tarjeta seleccionada
        color = (220, 80, 80) if i == selected else (70, 90, 110)

        # Panel principal
        draw_panel(x, y, 240, 280, color)

        # Nombre centrado dentro de la tarjeta
        text = cfg.FONT_MEDIUM.render(name, True, cfg.WHITE)
        text_x = x + 120 - text.get_width() // 2
        screen.blit(text, (text_x, y + 20))

        # Stats
        data = PLAYER_DIGIMON[name]

        draw_text(f"HP: {data['hp']}", cfg.FONT_SMALL, cfg.WHITE, x + 30, y + 90)
        draw_text(f"ATQ: {data['atq']}", cfg.FONT_SMALL, cfg.WHITE, x + 30, y + 130)
        draw_text(f"DEF: {data['def']}", cfg.FONT_SMALL, cfg.WHITE, x + 30, y + 170)
        draw_text(f"VEL: {data['vel']}", cfg.FONT_SMALL, cfg.WHITE, x + 30, y + 210)

    # Instrucciones abajo
    draw_center(
        "← → mover | ENTER elegir | ESC volver",
        cfg.FONT_SMALL,
        cfg.WHITE,
        640
    )


# ===============================
# LOOP
# ===============================
running = True

while running:
    clock.tick(cfg.FPS)

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            if scene == "menu":

                if event.key == pygame.K_RETURN:
                    scene = "selection"

                elif event.key == pygame.K_ESCAPE:
                    running = False

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

                    print("DIGIMON ELEGIDO:")
                    print(player)

                    print("ENEMIGOS NIVEL 1:")
                    print(ENEMIES[1])

                    print("EVOLUCIONES:")
                    print(EVOLUTIONS[player["nombre"]])

    if scene == "menu":
        draw_menu()

    elif scene == "selection":
        draw_selection()

    pygame.display.flip()

pygame.quit()
sys.exit()