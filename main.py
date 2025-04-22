from game.game import Game
from game.models import Player
from game.score import ScoreHandler
from game.settings import MODES


def main():
    def play_game():
        name = input("Введите имя: ")

        print("Выберите сложность:")
        for key, mode_name in MODES.items():
            print(f"{key} - {mode_name}")

        mode_choice = input("Ваш выбор: ")


        try:
            mode = int(mode_choice)
            if mode not in [1, 2, 3]:
                print("Некорректный ввод, режим будет выставлен на 1")
                mode = 1
        except ValueError:
            print("Некорректный ввод, режим будет выставлен на 1")
            mode = 1

        player = Player(name, mode)
        game = Game(player, mode)
        game.play()

    def show_score():
        handler = ScoreHandler()

        handler.display()

    while True:
        first_choice = input("Выберите действие: \n 1 - Запуск игры\n 2 - Посмотреть очки\n 3 - Выйти из игры\n")

        match first_choice:
            case "1":
                play_game()
            case "2":
                show_score()
            case "3":
                print("Выход из игры...")
                break
            case _:
                print("Ошибка: Некорректный ввод. Попробуйте снова.")


if __name__ == "__main__":
    main()