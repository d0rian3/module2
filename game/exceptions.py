class GameOverPlayerDead(Exception):
    @staticmethod
    def player_dead():
        print("Увы, игрок погиб")


class GameOverEnemyDead(Exception):
    @staticmethod
    def enemy_dead():
        print("Ты победил, продвигаешься на следующий уровень")

