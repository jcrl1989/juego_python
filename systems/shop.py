POTIONS = {

    "small": {
        "name": "Poción pequeña",
        "heal": 20,
        "price": 10
    },

    "medium": {
        "name": "Poción mediana",
        "heal": 50,
        "price": 25
    },

    "large": {
        "name": "Poción grande",
        "heal": 9999,
        "price": 50
    }

}


def buy_potion(player, potion_key):

    potion = POTIONS[potion_key]

    if player["monedas"] < potion["price"]:
        return False

    player["monedas"] -= potion["price"]

    player["inventory"][potion_key] += 1

    return True


def use_potion(player, potion_key):

    if player["hp"] >= player["hp_max"]:
        return "full_hp"

    if player["inventory"][potion_key] <= 0:
        return "empty"

    potion = POTIONS[potion_key]

    heal = potion["heal"]

    player["hp"] = min(
        player["hp"] + heal,
        player["hp_max"]
    )

    player["inventory"][potion_key] -= 1

    return "used"