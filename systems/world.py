import random


WORLD_ZONES = {
    1: {
        "name": "Bosque Inicial",
        "enemy_level": 1
    },

    2: {
        "name": "Cueva Digital",
        "enemy_level": 2
    },

    3: {
        "name": "Montaña Binaria",
        "enemy_level": 3
    }
}


TILE_SIZE = 50

WORLD_MAP = [

    ["tree","tree","tree","tree","tree","tree","tree","tree","tree","tree"],

    ["tree","grass","grass","path","grass","grass","grass","grass","grass","tree"],

    ["tree","grass","path","path","path","grass","grass","rock","grass","tree"],

    ["tree","grass","grass","grass","path","grass","grass","grass","grass","tree"],

    ["tree","rock","grass","grass","path","grass","rock","grass","grass","tree"],

    ["tree","grass","grass","grass","path","grass","grass","grass","grass","tree"],

    ["tree","grass","grass","grass","path","grass","grass","grass","grass","tree"],

    ["tree","tree","tree","tree","tree","tree","tree","tree","tree","tree"]

]


def can_move(tile):

    blocked = ["tree", "rock"]

    return tile not in blocked


def random_encounter(chance=0.03):
    return random.random() < chance


def get_zone_name(zone):
    return WORLD_ZONES[zone]["name"]


def get_enemy_level(zone):
    return WORLD_ZONES[zone]["enemy_level"]


def update_zone(player_level):

    if player_level >= 10:
        return 3

    if player_level >= 5:
        return 2

    return 1