from data.digimon_data import EVOLUTIONS


def check_evolution(player):
    name = player["nombre"]
    level = player["nivel"]

    if name not in EVOLUTIONS:
        return False

    evolutions = EVOLUTIONS[name]

    # evolución nivel 16 (prioridad alta)
    if level >= 16 and 16 in evolutions:
        evolve(player, evolutions[16])
        return True

    # evolución nivel 8
    if level >= 8 and 8 in evolutions:
        evolve(player, evolutions[8])
        return True

    return False


def evolve(player, new_name):
    player["nombre"] = new_name

    # buff base simple al evolucionar
    player["hp_max"] += 20
    player["atq"] += 5
    player["def"] += 3
    player["vel"] += 2

    player["hp"] = player["hp_max"]