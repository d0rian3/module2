class GameOverPlayerDead(Exception):
    def player_dead(self):
        print("Увы, игрок погиб")


class GameOverEnemyDead(Exception):
    def enemy_dead(self):
        print("Ты победил, продвигаешься на следующий уровень")

