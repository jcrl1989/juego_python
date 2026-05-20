import pygame
import config as cfg


def draw_text(screen, text, font, color, x, y):
    img = font.render(text, True, color)
    screen.blit(img, (x, y))


def draw_center(screen, text, font, color, y):
    img = font.render(text, True, color)
    x = cfg.WIDTH // 2 - img.get_width() // 2
    screen.blit(img, (x, y))


def draw_panel(screen, x, y, w, h, color):
    pygame.draw.rect(screen, color, (x, y, w, h), border_radius=18)

def draw_hp_bar(screen, x, y, width, height, current_hp, max_hp):

    ratio = current_hp / max_hp

    pygame.draw.rect(
        screen,
        (80, 80, 80),
        (x, y, width, height)
    )

    pygame.draw.rect(
        screen,
        (40, 220, 40),
        (x, y, width * ratio, height)
    )

    pygame.draw.rect(
        screen,
        (255, 255, 255),
        (x, y, width, height),
        2
    )