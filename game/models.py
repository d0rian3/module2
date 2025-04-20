from game.settings import PLAYER_LIVES, POINTS_FOR_KILLING
from game.settings import ALLOWED_ATTACKS
from game.exceptions import GameOverPlayerDead
from game.exceptions import GameOverEnemyDead
from random import randint


class Player:

    def __init__(self, name):
        self.name = name
        self.lives = PLAYER_LIVES
        self.score = 0

    def select_attack(self):
        while True:
            print("Доступные атаки:")
            for key, attack in ALLOWED_ATTACKS.items():
                print(f"{key} - {attack}")

            try:
                attack_choice = int(input(f"{self.name}, выбери атаку (1, 2 или 3): "))
                if attack_choice in ALLOWED_ATTACKS:
                    return attack_choice
                else:
                    print("Некорректный выбор! Попробуй снова.")
            except ValueError:
                print("Некорректный ввод! Пожалуйста, введите цифру (1, 2 или 3).")

    def decrease_lives(self):
        self.lives -= 1
        if self.lives == 0:
            raise GameOverPlayerDead


    def add_score(self, enemy_level):
        self.score += POINTS_FOR_KILLING * enemy_level



class Enemy:

    def __init__(self, lives, level):
        self.final_attack = None
        self.attack = None
        self.lives = lives
        self.level = level

    def select_attack(self):
        self.attack = randint(1, 3)

        return self.attack
    def decrease_lives(self):
        self.lives -=1
        self.level += 1
        if self.lives == 0:
            raise GameOverEnemyDead
        return True






