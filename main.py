from game.game import Game
from game.models import Player
from game.score import ScoreHandler


def main():

    def play_game():
        name = input("Введите имя: ")
        mode_opp = input("Выберите сложность (1 - легко,\n 2 - средне,\n 3 - сложно):  ")

        mode_opportunity = {
            "1": 1, # легко
            "2": 2, # средне
            "3": 3 # сложно
        }

        mode = mode_opportunity.get(mode_opp)
        if mode is None:
            print("Некорректный ввод, режим будет выставлен на 1")
            mode = 1

        player = Player(name)
        game = Game(player,mode)
        game.play()



    def show_score():
        handler = ScoreHandler()
        handler.display()



    while True:
        first_choise: str = input("Выберите действие: \n 1 - Запуск игры \n 2 - Посмотреть очки \n 3 - Выйти из игры")

        match first_choise:
            case "1":
                play_game()
            case "2":
                show_score()
            case "3":
                print("Выход из игры...")
                break
            case _:
                print("Ошибка: Некорректный ввод. Попробуйте снова.")