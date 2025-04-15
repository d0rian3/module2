from module2.game.exceptions import GameOverPlayerDead, GameOverEnemyDead
from module2.game.models import Enemy
from module2.game.settings import ALLOWED_ATTACKS, ATTACK_PAIRS_OUTCOME, MAX_RECORDS_NUMBER
from module2.game.settings import DRAW, WIN, LOSE



class Game:


    def __init__(self, player, mode):
        self.player = player
        self.mode = mode
        self.enemy = self.create_enemy()

    def create_enemy(self):

        if hasattr(self, "enemy") and self.enemy:
            level = self.enemy.level
        else:
            level = 1
        lives = level * self.mode
        return Enemy(lives=lives, level=level)

    def play(self):
        while True:
            try:
                result = self.fight()
                self.handle_fight_result(result)
            except GameOverPlayerDead:
                print("Ты проиграл")
                self.save_score()
                break
            except GameOverEnemyDead:
                print("Ты выиграл")
                self.player.add_score(self.enemy.level)
                self.enemy = self.create_enemy()
                break




    def fight(self):

        player_attack = self.player.select_attack()
        enemy_attack = self.enemy.select_attack()
        """
        Ниже я переопределяю значение 
        введенное пользователем в одно из значений словаря
        ALLOWED_ATTACKS, чтобы потом сделать проверку на результат из словаря 
        ATTACK_PAIRS_OUTCOME
        """
        player_attack = ALLOWED_ATTACKS[player_attack]
        enemy_attack = ALLOWED_ATTACKS[enemy_attack]
        if (player_attack, enemy_attack) in ATTACK_PAIRS_OUTCOME:
            result = ATTACK_PAIRS_OUTCOME[(player_attack, enemy_attack)]
            return result
        else:
            print("Ошибка в атаках. Бой не состоялся.")
            return DRAW

    def handle_fight_result(self, result):

        if result == LOSE:
            self.player.decrease_lives()
        elif result == DRAW:
            print("Ничья! Следующий раунд.")
        elif result == WIN:
            self.player.add_score(self.enemy.level)
            self.enemy.decrease_lives()



    def save_score(self):
        player_name = self.player.name
        player_score = self.player.score
        scores = []
        try:
            with open("../scores.txt", "r") as file:
                scores = file.readlines()
        except FileNotFoundError:
            scores = []

        scores.append(f"{player_name}: {player_score}\n")


        scores.sort(key=lambda x: int(x.split(": ")[1]), reverse=True)
        scores = scores[:MAX_RECORDS_NUMBER]

        with open("../scores.txt", "w") as file:
            file.writelines(scores)


