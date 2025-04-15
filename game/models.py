
from module2.game.settings import PLAYER_LIVES, POINTS_FOR_KILLING
from module2.game.settings import ALLOWED_ATTACKS
from module2.game.exceptions import GameOverPlayerDead
from module2.game.exceptions import GameOverEnemyDead
from random import randint

class Player:

    def __init__(self, name):
        self.name = name
        self.lives = PLAYER_LIVES
        self.score = 0


    def select_attack(self):
        while True:
            attack = input(f"{self.name}, выбери атаку {ALLOWED_ATTACKS}: ")
            if attack in ALLOWED_ATTACKS:
                return attack
            else:
                print("Некорректный выбор! Попробуй снова.")


    def decrease_lives(self):
        self.lives -= 1
        if self.lives == 0:
            raise GameOverPlayerDead


    def add_score(self, enemy_level):
        self.score += POINTS_FOR_KILLING * enemy_level



class Enemy:

    def __init__(self, lives, level):
        self.attack = None
        self.lives = lives
        self.level = level

    def select_attack(self):
        self.attack = randint(1, 3)
    def decrease_lives(self):
        self.lives -=1
        self.level += 1
        if self.lives == 0:
            raise GameOverEnemyDead
        return True






