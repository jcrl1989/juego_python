import pygame
import os


def load_sprite(name, width=180, height=180):

    path = os.path.join(
        "assets",
        "img",
        "digimon",
        f"{name}.png"
    )

    image = pygame.image.load(path).convert_alpha()

    image = pygame.transform.scale(
        image,
        (width, height)
    )

    return image