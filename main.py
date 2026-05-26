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
    update_zone,
    WORLD_MAP,
    TILE_SIZE,
    can_move
)

from systems.shop import (
    buy_potion,
    use_potion,
    POTIONS
)

from scenes.shop_scene import draw_shop

from utils.helpers import (
    draw_text,
    draw_center,
    draw_panel,
    draw_hp_bar
)

from utils.loader import load_sprite


pygame.init()

screen = pygame.display.set_mode(
    (cfg.WIDTH, cfg.HEIGHT)
)

pygame.display.set_caption(cfg.TITLE)

clock = pygame.time.Clock()


# ==================================
# ESTADO DEL JUEGO
# ==================================

scene = "menu"

selected = 0
shop_selected = 0

player = None
enemy = None

player_sprite = None
enemy_sprite = None

options = [
    "Agumon",
    "Gabumon",
    "Tentomon"
]

battle_log = ""
turn = "player"

# WORLD

player_row = 2
player_col = 2

current_zone = 1


# ==================================
# MENU
# ==================================

def draw_menu():

    screen.fill((25,35,65))

    draw_center(
        screen,
        "DIGIMON BATTLE",
        cfg.FONT_BIG,
        cfg.WHITE,
        130
    )

    draw_center(
        screen,
        "ENTER - INICIAR",
        cfg.FONT_MEDIUM,
        cfg.WHITE,
        380
    )

    draw_center(
        screen,
        "ESC - SALIR",
        cfg.FONT_MEDIUM,
        cfg.WHITE,
        470
    )


# ==================================
# SELECCION
# ==================================

def draw_selection():

    screen.fill((30,55,45))

    draw_center(
        screen,
        "ESCOGE TU DIGIMON",
        cfg.FONT_BIG,
        cfg.WHITE,
        60
    )

    for i,name in enumerate(options):

        x=170+(i*320)
        y=260

        color=(220,80,80)

        if i!=selected:
            color=(70,90,110)

        draw_panel(
            screen,
            x,
            y,
            240,
            280,
            color
        )

        draw_text(
            screen,
            name,
            cfg.FONT_MEDIUM,
            cfg.WHITE,
            x+40,
            y+20
        )

        data=PLAYER_DIGIMON[name]

        draw_text(
            screen,
            f"HP: {data['hp']}",
            cfg.FONT_SMALL,
            cfg.WHITE,
            x+30,
            y+90
        )

        draw_text(
            screen,
            f"ATQ: {data['atq']}",
            cfg.FONT_SMALL,
            cfg.WHITE,
            x+30,
            y+130
        )

        draw_text(
            screen,
            f"DEF: {data['def']}",
            cfg.FONT_SMALL,
            cfg.WHITE,
            x+30,
            y+170
        )

        draw_text(
            screen,
            f"VEL: {data['vel']}",
            cfg.FONT_SMALL,
            cfg.WHITE,
            x+30,
            y+210
        )


# ==================================
# WORLD
# ==================================

def draw_world():

    screen.fill((50,80,50))

    colors = {

        "tree": (20,90,20),
        "grass": (80,170,80),
        "path": (180,150,90),
        "rock": (120,120,120)

    }


    # Dibujar mapa
    for row in range(len(WORLD_MAP)):

        for col in range(len(WORLD_MAP[row])):

            tile = WORLD_MAP[row][col]

            x = col*TILE_SIZE + 350
            y = row*TILE_SIZE + 150

            pygame.draw.rect(

                screen,
                colors[tile],
                (x,y,TILE_SIZE,TILE_SIZE)
            )

            pygame.draw.rect(

                screen,
                (0,0,0),
                (x,y,TILE_SIZE,TILE_SIZE),
                1
            )


    # Avatar jugador

    px = player_col*TILE_SIZE + 350
    py = player_row*TILE_SIZE + 150


    # cabeza
    pygame.draw.circle(

        screen,
        (255,220,180),
        (px+25,py+15),
        12
    )


    # cuerpo
    pygame.draw.rect(

        screen,
        (50,120,255),
        (px+15,py+25,20,20)
    )


    # ojos
    pygame.draw.circle(
        screen,
        (0,0,0),
        (px+21,py+12),
        2
    )

    pygame.draw.circle(
        screen,
        (0,0,0),
        (px+29,py+12),
        2
    )

if player:

    draw_text(
        screen,
        f"Digimon: {player['nombre']}",
        cfg.FONT_SMALL,
        cfg.WHITE,
        40,
        150
    )

    draw_text(
        screen,
        f"Nivel: {player['nivel']}",
        cfg.FONT_SMALL,
        cfg.WHITE,
        40,
        190
    )

    draw_text(
        screen,
        f"Monedas: {player['monedas']}",
        cfg.FONT_SMALL,
        cfg.WHITE,
        40,
        230
    )


    draw_text(
        screen,
        f"Zona: {get_zone_name(current_zone)}",
        cfg.FONT_SMALL,
        cfg.WHITE,
        40,
        270
    )


    draw_center(
        screen,
        "WASD mover | T tienda | ESC menu",
        cfg.FONT_SMALL,
        cfg.WHITE,
        680
    )

# ==================================
# BATALLA
# ==================================

def draw_battle():

    screen.fill((45,45,65))

    draw_center(
        screen,
        "BATALLA DIGIMON",
        cfg.FONT_BIG,
        cfg.WHITE,
        30
    )

    if player_sprite:
        screen.blit(
            player_sprite,
            (180,280)
        )

    if enemy_sprite:
        screen.blit(
            enemy_sprite,
            (850,220)
        )

    draw_text(
        screen,
        player["nombre"],
        cfg.FONT_MEDIUM,
        cfg.WHITE,
        100,
        180
    )

    draw_hp_bar(
        screen,
        100,
        230,
        250,
        25,
        player["hp"],
        player["hp_max"]
    )

    draw_text(
        screen,
        enemy["nombre"],
        cfg.FONT_MEDIUM,
        cfg.WHITE,
        800,
        180
    )

    draw_hp_bar(
        screen,
        800,
        230,
        250,
        25,
        enemy["hp"],
        enemy["hp_max"]
    )

    draw_center(
        screen,
        battle_log,
        cfg.FONT_SMALL,
        cfg.WHITE,
        650
    )

    draw_text(
    screen,
    f"P:{player['inventory']['small']} "
    f"O:{player['inventory']['medium']} "
    f"I:{player['inventory']['large']}",
    cfg.FONT_SMALL,
    cfg.WHITE,
    80,
    600
    )

    draw_center(
    screen,
    "ENTER atacar | P/O/I usar poción",
    cfg.FONT_SMALL,
    cfg.WHITE,
    680
    )


# ==================================
# LOOP
# ==================================

running = True

while running:

    clock.tick(cfg.FPS)

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False


        elif event.type == pygame.KEYDOWN:

            # ======================
            # MENU
            # ======================

            if scene == "menu":

                if event.key == pygame.K_RETURN:
                    scene = "selection"

                elif event.key == pygame.K_ESCAPE:
                    running = False


            # ======================
            # SELECCION
            # ======================

            elif scene == "selection":

                if event.key == pygame.K_LEFT:
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

                    player["inventory"] = {

                        "small":0,
                        "medium":0,
                        "large":0
                    }

                    player_sprite = load_sprite(
                        player["nombre"]
                    )

                    scene = "world"


            # ======================
            # WORLD
            # ======================

            elif scene == "world":

                new_row = player_row
                new_col = player_col


                if event.key == pygame.K_w:
                    new_row -= 1

                elif event.key == pygame.K_s:
                    new_row += 1

                elif event.key == pygame.K_a:
                    new_col -= 1

                elif event.key == pygame.K_d:
                    new_col += 1

                elif event.key == pygame.K_t:
                    scene = "shop"

                elif event.key == pygame.K_ESCAPE:
                    scene = "menu"


                if (
                    0 <= new_row < len(WORLD_MAP)
                    and
                    0 <= new_col < len(WORLD_MAP[0])
                ):

                    tile = WORLD_MAP[
                        new_row
                    ][
                        new_col
                    ]

                    if can_move(tile):

                        player_row = new_row
                        player_col = new_col


                        if player:

                            current_zone = update_zone(
                                player["nivel"]
                            )


                            if (
                                tile == "grass"
                                and random_encounter()
                            ):

                                enemy = create_enemy(

                                    ENEMIES[
                                        get_enemy_level(
                                            current_zone
                                        )
                                    ]
                                )

                                enemy_sprite = load_sprite(
                                    enemy["nombre"]
                                )

                                player_sprite = load_sprite(
                                    player["nombre"]
                                )

                                turn = "player"

                                battle_log = (
                                    "¡Un Digimon salvaje apareció!"
                                )

                                scene = "battle"


            # ======================
            # SHOP
            # ======================

            elif scene == "shop":

                keys = list(
                    POTIONS.keys()
                )

                if event.key == pygame.K_ESCAPE:
                    scene = "world"

                elif event.key == pygame.K_UP:

                    shop_selected = (
                        shop_selected - 1
                    ) % len(keys)

                elif event.key == pygame.K_DOWN:

                    shop_selected = (
                        shop_selected + 1
                    ) % len(keys)

                elif event.key == pygame.K_RETURN:

                    buy_potion(
                        player,
                        keys[shop_selected]
                    )


            # ======================
            # BATALLA
            # ======================

            elif scene == "battle":

                if event.key == pygame.K_ESCAPE:
                    scene = "world"


                elif event.key == pygame.K_p:

                    result = use_potion(
                        player,
                        "small"
                    )

                    if result == "used":
                        battle_log = "Poción pequeña usada"

                    elif result == "empty":
                        battle_log = "No tienes pociones"

                    elif result == "full_hp":
                        battle_log = "HP completo"


                elif event.key == pygame.K_o:

                    result = use_potion(
                        player,
                        "medium"
                    )

                    if result == "used":
                        battle_log = "Poción mediana usada"

                    elif result == "empty":
                        battle_log = "No tienes pociones"

                    elif result == "full_hp":
                        battle_log = "HP completo"


                elif event.key == pygame.K_i:

                    result = use_potion(
                        player,
                        "large"
                    )

                    if result == "used":
                        battle_log = "Poción grande usada"

                    elif result == "empty":
                        battle_log = "No tienes pociones"

                    elif result == "full_hp":
                        battle_log = "HP completo"


                elif event.key == pygame.K_RETURN:

                    if turn == "player":

                        dmg = player_attack(
                            player,
                            enemy
                        )

                        battle_log = (
                            f"{player['nombre']} hizo "
                            f"{dmg} daño"
                        )

                        if is_defeated(enemy):

                            add_exp(
                                player,
                                30
                            )

                            player["monedas"] += 15

                            battle_log = (
                                f"{enemy['nombre']} derrotado"
                            )

                            scene = "world"

                        else:
                            turn = "enemy"


                    else:

                        dmg = enemy_attack(
                            enemy,
                            player
                        )

                        battle_log = (
                            f"{enemy['nombre']} hizo "
                            f"{dmg} daño"
                        )

                        if is_defeated(player):

                            battle_log = (
                                f"{player['nombre']} derrotado"
                            )

                            scene = "menu"

                        else:
                            turn = "player"

    # ======================
    # DIBUJADO
    # ======================

    if scene=="menu":
        draw_menu()

    elif scene=="selection":
        draw_selection()

    elif scene=="world":
        draw_world()

    elif scene=="battle":
        draw_battle()

    elif scene=="shop":

        draw_shop(
            screen,
            player,
            shop_selected
        )

    pygame.display.flip()

pygame.quit()
sys.exit()