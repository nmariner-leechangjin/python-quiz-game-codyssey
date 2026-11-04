"""퀴즈 게임의 실제 사용자 흐름과 저장 경계를 확인한다."""

import json
import tempfile
import unittest
from pathlib import Path

from default_quizzes import make_default_quizzes
from quiz import Quiz
from quiz_game import QuizGame


class QuizGameTests(unittest.TestCase):
    def setUp(self) -> None:
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.state_path = Path(self.directory.name) / "state.json"
        self.output: list[str] = []

    def game(self, answers: list[str]) -> QuizGame:
        values = iter(answers)
        return QuizGame(
            self.state_path,
            input_fn=lambda _: next(values),
            output_fn=self.output.append,
        )

    def test_menu_retries_empty_text_and_out_of_range_numbers(self) -> None:
        game = self.game(["", "abc", "9", " 5 "])
        game.run()
        self.assertTrue(any("비어" in line for line in self.output))
        self.assertTrue(any("숫자" in line for line in self.output))
        self.assertTrue(any("1~5" in line for line in self.output))
        self.assertTrue(self.state_path.exists())

    def test_add_quiz_survives_restart(self) -> None:
        game = self.game(["", "추가 문제?", "가", "나", "다", "라", "0", "2"])
        game.add_quiz()
        restored = QuizGame(self.state_path, output_fn=self.output.append)
        self.assertEqual(7, len(restored.quizzes))
        self.assertEqual("추가 문제?", restored.quizzes[-1].question)
        self.assertEqual(2, restored.quizzes[-1].answer)

    def test_play_result_and_best_score_survive_restart(self) -> None:
        answers = [str(quiz.answer) for quiz in make_default_quizzes()]
        game = self.game(answers)
        game.play()
        self.assertEqual(6, game.best_score)
        self.assertIn("결과: 6문제 중 6문제 정답", self.output)
        restored = QuizGame(self.state_path, output_fn=self.output.append)
        self.assertEqual(6, restored.best_score)
        restored.show_best_score()
        self.assertIn("6문제", self.output[-1])

    def test_empty_quiz_list_and_unplayed_score(self) -> None:
        self.state_path.write_text(
            json.dumps({"quizzes": [], "best_score": None}), encoding="utf-8"
        )
        game = QuizGame(self.state_path, output_fn=self.output.append)
        game.play()
        game.list_quizzes()
        game.show_best_score()
        self.assertEqual(2, sum("등록된 퀴즈가 없습니다" in x for x in self.output))
        self.assertIn("아직", self.output[-1])

    def test_corrupt_or_invalid_state_uses_default_quizzes(self) -> None:
        for content in ("{broken", json.dumps({"quizzes": [{}], "best_score": 0})):
            with self.subTest(content=content):
                self.state_path.write_text(content, encoding="utf-8")
                game = QuizGame(self.state_path, output_fn=self.output.append)
                self.assertEqual(6, len(game.quizzes))
        self.assertTrue(any("기본 퀴즈" in x for x in self.output))

    def test_keyboard_interrupt_and_eof_save_before_exit(self) -> None:
        for error in (KeyboardInterrupt, EOFError):
            with self.subTest(error=error):
                if self.state_path.exists():
                    self.state_path.unlink()
                game = QuizGame(
                    self.state_path,
                    input_fn=lambda _: (_ for _ in ()).throw(error()),
                    output_fn=self.output.append,
                )
                game.run()
                self.assertTrue(self.state_path.exists())
        self.assertTrue(any("안전하게 종료" in x for x in self.output))

    def test_write_failure_is_reported(self) -> None:
        missing_parent = self.state_path.parent / "missing" / "state.json"
        game = QuizGame(missing_parent, output_fn=self.output.append)
        self.assertFalse(game.save_state())
        self.assertTrue(any("저장에 실패" in x for x in self.output))

    def test_quiz_rejects_invalid_schema(self) -> None:
        with self.assertRaises(ValueError):
            Quiz("질문", ["가", "나", "다", "라"], True)
        with self.assertRaises(ValueError):
            Quiz.from_dict({"question": "질문", "choices": ["가"]})


if __name__ == "__main__":
    unittest.main()
