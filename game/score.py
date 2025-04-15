from models import Player


class ScoreHandler:
    def __init__(self):
        self.score = 0

class GameRecord:
    def __str__(self):
        self.records = []

    def add_record(self, new_record):
        for i, record in enumerate(self.records):
            if record > new_record:
                self.records.insert(i, new_record)
                return
        self.records.append(new_record)


class PlayerRecord:

    def __init__(self, name, mode,score):
        self.name = name
        self.mode = mode
        self.score = score

    def __gt__(self, other):
        if not isinstance(other, Player):
            return NotImplemented
        return self.score > other.score

    def __str__(self):
        return f"Игрок: {self.name} | Уровень сложности: {self.mode} | Очки: {self.score}"
