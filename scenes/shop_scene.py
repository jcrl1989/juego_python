import config as cfg

from utils.helpers import (
    draw_text,
    draw_center,
    draw_panel
)

from systems.shop import POTIONS


def draw_shop(screen, player, selected):

    screen.fill((45,50,90))

    draw_center(
        screen,
        "TIENDA DIGIMON",
        cfg.FONT_BIG,
        cfg.WHITE,
        50
    )

    draw_text(
        screen,
        f"Monedas: {player['monedas']}",
        cfg.FONT_MEDIUM,
        cfg.WHITE,
        70,
        130
    )

    potion_keys=list(POTIONS.keys())

    for i,key in enumerate(potion_keys):

        potion=POTIONS[key]

        color=(220,80,80)

        if i!=selected:
            color=(70,90,120)

        y=220+(i*120)

        draw_panel(
            screen,
            180,
            y,
            900,
            90,
            color
        )

        draw_text(
            screen,
            potion["name"],
            cfg.FONT_MEDIUM,
            cfg.WHITE,
            230,
            y+20
        )

        draw_text(
            screen,
            f"Curación: {potion['heal']}",
            cfg.FONT_SMALL,
            cfg.WHITE,
            600,
            y+20
        )

        draw_text(
            screen,
            f"Costo: {potion['price']}",
            cfg.FONT_SMALL,
            cfg.WHITE,
            850,
            y+20
        )


    draw_center(
        screen,
        "↑ ↓ elegir | ENTER comprar | ESC salir",
        cfg.FONT_SMALL,
        cfg.WHITE,
        680
    )