from systems.evolution import check_evolution


def exp_needed(level):
    return 50 + (level * 25)


def add_exp(player, amount):
    player["exp"] += amount

    leveled_up = False
    evolved = False

    while player["exp"] >= exp_needed(player["nivel"]):
        player["exp"] -= exp_needed(player["nivel"])
        level_up(player)
        leveled_up = True

        #  revisar evolución en cada level up
        if check_evolution(player):
            evolved = True

    return leveled_up or evolved


def level_up(player):
    player["nivel"] += 1

    player["hp_max"] += 5
    player["atq"] += 2
    player["def"] += 1
    player["vel"] += 1

    player["hp"] = player["hp_max"]