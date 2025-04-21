from game.exceptions import GameOverPlayerDead, GameOverEnemyDead
from game.models import Enemy
from game.settings import ALLOWED_ATTACKS, ATTACK_PAIRS_OUTCOME, MAX_RECORDS_NUMBER
from game.settings import DRAW, WIN, LOSE, SCORE_FILE, MODES


class Game:

    def __init__(self, player, mode):
        self.player = player
        self.player.mode = mode
        self.mode = mode
        self.enemy = self.create_enemy()
        self.mode_name = MODES.get(str(mode), "Custom")

    def create_enemy(self):
        if hasattr(self, "enemy") and self.enemy:
            level = self.enemy.level + 1
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
                print(f"Ты победил врага уровня {self.enemy.level}!")

                self.enemy = self.create_enemy()
                print(f"Новый враг уровня {self.enemy.level} появился!")

    def fight(self):
        player_attack = self.player.select_attack()
        enemy_attack = self.enemy.select_attack()

        print(f"Ты выбрал: {ALLOWED_ATTACKS[player_attack]}")
        print(f"Враг выбрал: {ALLOWED_ATTACKS[enemy_attack]}")

        player_attack_name = ALLOWED_ATTACKS[player_attack]
        enemy_attack_name = ALLOWED_ATTACKS[enemy_attack]

        if (player_attack_name, enemy_attack_name) in ATTACK_PAIRS_OUTCOME:
            result = ATTACK_PAIRS_OUTCOME[(player_attack_name, enemy_attack_name)]

            if result == WIN:
                print("Ты выиграл этот раунд!")
            elif result == LOSE:
                print("Ты проиграл этот раунд!")
            else:
                print("Ничья в этом раунде!")

            return result
        else:
            print("Ошибка в атаках. Бой не состоялся.")
            return DRAW

    def handle_fight_result(self, result):
        if result == LOSE:
            print(f"Ты потерял жизнь! Осталось жизней: {self.player.lives - 1}")
            self.player.decrease_lives()
        elif result == DRAW:
            print("Ничья! Следующий раунд.")
        elif result == WIN:
            self.player.add_score(self.enemy.level)
            print(f"Ты нанес урон врагу! Текущий счет: {self.player.score}")
            self.enemy.decrease_lives()

    def save_score(self):
        player_name = self.player.name
        player_score = self.player.score

        scores = []
        try:
            with open(SCORE_FILE, "r") as file:
                scores = file.readlines()
        except FileNotFoundError:
            scores = []


        scores.append(f"{player_name}: {self.mode_name}: {player_score}\n")


        scores.sort(key=lambda x: int(x.strip().split(": ")[2]), reverse=True)
        scores = scores[:MAX_RECORDS_NUMBER]

        with open(SCORE_FILE, "w") as file:
            file.writelines(scores)

        print(f"Твой финальный счет: {player_score}")
        print("Результат сохранен!")