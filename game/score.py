from models import Player
from settings import SCORE_FILE


class ScoreHandler:
    def __init__(self, SCORE_FILE):
        self.SCORE_FILE = SCORE_FILE
        self.score = 0
        self.score_handler = GameRecord()


    def read(self):
        try:
            with open(self.SCORE_FILE, "r") as file:
                for line in file:
                    name, mode,score = line.strip().split(": ")
                    score = int(score)
                    self.score_handler.add_record(PlayerRecord(name, mode, score))
        except FileNotFoundError:
            pass

    def save(self):
        with open(self.SCORE_FILE, "w") as file:
            for record in self.score_handler.records:
                file.write(str(record) + "\n")

    def display(self):
        print(self.score_handler)

class GameRecord:
    def __init__(self):
        self.records = []

    def add_record(self, new_record):
        for i, record in enumerate(self.records):
            if record == new_record:
                if new_record.score > record.score:
                    self.records[i] = new_record
                return
        self.records.append(new_record)

    def __str__(self):
        return "\n".join(str(record) for record in self.records)


class PlayerRecord:

    def __init__(self, name, mode,score):
        self.name = name
        self.mode = mode
        self.score = score

    def __gt__(self, other):
        if not isinstance(other, PlayerRecord):
            return NotImplemented
        return self.score > other.score

    def __eq__(self, other):
        if not isinstance(other, PlayerRecord):
            return False

        return self.name == other.name and self.mode == other.mode

    def __str__(self):
        return f"Игрок: {self.name} | Уровень сложности: {self.mode} | Очки: {self.score}"