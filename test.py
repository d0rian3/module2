import unittest
from unittest.mock import patch, MagicMock, mock_open
from game.game import Game
from game.models import Player, Enemy
from game.settings import WIN, LOSE, DRAW, ALLOWED_ATTACKS
from game.score import ScoreHandler
from game.score import GameRecord
from game.score import PlayerRecord
import os

class TestModels(unittest.TestCase):

    def setUp(self):
        self.player = Player("TestPlayer", mode=1)
        self.game = Game(self.player, mode=1)

    def test_game_initialization(self):

        self.assertEqual(self.game.player.name, "TestPlayer")
        self.assertEqual(self.game.mode, 1)
        self.assertIsInstance(self.game.enemy, Enemy)
        self.assertEqual(self.game.enemy.level, 1)
        self.assertEqual(self.game.enemy.lives, 1)

    def test_create_enemy(self):
        self.assertEqual(self.game.enemy.level, 1)
        self.game.enemy.level = 2
        new_enemy = self.game.create_enemy()

        self.assertEqual(new_enemy.level, 3)
        self.assertEqual(new_enemy.lives, 3)

    @patch('game.models.Player.select_attack', return_value=1)
    @patch('game.models.Enemy.select_attack', return_value=2)
    def test_fight_player_wins(self, mock_enemy_attack, mock_player_attack):

        result = self.game.fight()
        self.assertEqual(result, WIN)

    @patch('game.models.Player.select_attack', return_value=2)
    @patch('game.models.Enemy.select_attack', return_value=1)
    def test_fight_player_loses(self, mock_enemy_attack, mock_player_attack):

        result = self.game.fight()
        self.assertEqual(result, LOSE)

    @patch('game.models.Player.select_attack', return_value=1)
    @patch('game.models.Enemy.select_attack', return_value=1)
    def test_fight_draw(self, mock_enemy_attack, mock_player_attack):

        result = self.game.fight()
        self.assertEqual(result, DRAW)

    def test_handle_fight_result_win(self):

        initial_score = self.player.score
        initial_enemy_lives = self.game.enemy.lives

        self.game.handle_fight_result(WIN)


        self.assertGreater(self.player.score, initial_score)

        self.assertLess(self.game.enemy.lives, initial_enemy_lives)

    def test_handle_fight_result_lose(self):

        initial_player_lives = self.player.lives

        self.game.handle_fight_result(LOSE)


        self.assertLess(self.player.lives, initial_player_lives)

    def test_handle_fight_result_draw(self):

        initial_player_lives = self.player.lives
        initial_enemy_lives = self.game.enemy.lives
        initial_score = self.player.score

        self.game.handle_fight_result(DRAW)


        self.assertEqual(self.player.lives, initial_player_lives)
        self.assertEqual(self.game.enemy.lives, initial_enemy_lives)
        self.assertEqual(self.player.score, initial_score)



class TestScoreHandler(unittest.TestCase):
    def setUp(self):
        self.test_file = "test_scores.txt"
        self.score_handler = ScoreHandler(score_file=self.test_file)
        self.score_handler.score_handler = GameRecord()

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    @patch("builtins.open", new_callable=mock_open, read_data="Player1: Normal: 100\nPlayer2: Hard: 200")
    def test_read(self, mock_file):
        self.score_handler.read()
        records = self.score_handler.score_handler.records
        self.assertEqual(len(records), 2)

        self.assertEqual(records[0].name, "Player1")
        self.assertEqual(records[0].mode, "Normal")
        self.assertEqual(records[0].score, 100)

        self.assertEqual(records[1].name, "Player2")
        self.assertEqual(records[1].mode, "Hard")
        self.assertEqual(records[1].score, 200)

    @patch("builtins.open", new_callable=mock_open)
    def test_save(self,mock_file):
        self.score_handler.score_handler.add_record(PlayerRecord("Player1", "Normal", 100))
        self.score_handler.score_handler.add_record(PlayerRecord("Player2", "Hard", 200))

        self.score_handler.save()

        mock_file.assert_called_once_with(self.test_file, "w")

        handle = mock_file()

        expected_calls = [
            unittest.mock.call("Игрок: Player1 | Уровень сложности: Normal | Очки: 100\n"),
            unittest.mock.call("Игрок: Player2 | Уровень сложности: Hard | Очки: 200\n")
        ]
        handle.write.assert_called_once_with(expected_calls, any_order = True)

    @patch("builtins.print")
    def test_display_with_records(self, mock_print):
        self.score_handler.score_handler.add_record("Player1", "Normal", 100)
        self.score_handler.score_handler.add_record("Player2", "Hard", 200)

        self.score_handler.display()
        mock_print.assert_any_calls("\n=== ТАБЛИЦА РЕКОРДОВ ===")

    @patch("builtins.print")
    def test_display_without_records(self, mock_print):

        self.score_handler.display()
        mock_print.assert_called_with("Нет сохраненных результатов.")

class TestPlayerRecord(unittest.TestCase):
    pass

if __name__ == '__main__':
    unittest.main()