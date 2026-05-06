import random
import copy


def create_enemy(enemy_pool):
    return copy.deepcopy(random.choice(enemy_pool))


def calculate_damage(attacker, defender):
    damage = attacker["atq"] - defender["def"] // 2
    return max(1, damage)


def player_attack(player, enemy):
    damage = calculate_damage(player, enemy)
    enemy["hp"] -= damage
    enemy["hp"] = max(0, enemy["hp"])
    return damage


def enemy_attack(enemy, player):
    damage = calculate_damage(enemy, player)
    player["hp"] -= damage
    player["hp"] = max(0, player["hp"])
    return damage


def is_defeated(unit):
    return unit["hp"] <= 0