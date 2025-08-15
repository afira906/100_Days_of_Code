# There is no block scope in python!

game_level = 3
enemies = ["skeleton", "zombies", "aliens"]

def create_enemy():
    new_enemy = ""
    if game_level < 5:
        new_enemy = enemies[1]

    print(new_enemy)

create_enemy()
