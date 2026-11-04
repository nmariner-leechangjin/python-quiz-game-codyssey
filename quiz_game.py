"""메뉴, 게임 진행, 로컬 상태 저장을 관리한다."""

import json
import os
from pathlib import Path
from typing import Callable

from default_quizzes import make_default_quizzes
from quiz import Quiz


class QuizGame:
    MENU = (
        "1. 퀴즈 풀기",
        "2. 퀴즈 추가",
        "3. 퀴즈 목록",
        "4. 최고 점수 확인",
        "5. 종료",
    )

    def __init__(
        self,
        state_path: Path | None = None,
        input_fn: Callable[[str], str] = input,
        output_fn: Callable[[str], None] = print,
    ) -> None:
        self.state_path = state_path or Path(__file__).resolve().parent / "state.json"
        self.input_fn = input_fn
        self.output_fn = output_fn
        self.quizzes: list[Quiz] = make_default_quizzes()
        self.best_score = None
        self.load_state()

    def load_state(self) -> None:
        try:
            data = json.loads(self.state_path.read_text(encoding="utf-8"))
            if not isinstance(data, dict) or "quizzes" not in data or "best_score" not in data:
                raise ValueError("필수 항목이 없습니다.")
            if not isinstance(data["quizzes"], list):
                raise ValueError("퀴즈 목록 형식이 올바르지 않습니다.")
            score = data["best_score"]
            if score is not None and (
                isinstance(score, bool) or not isinstance(score, int) or score < 0
            ):
                raise ValueError("최고 점수 형식이 올바르지 않습니다.")
            quizzes = [Quiz.from_dict(item) for item in data["quizzes"]]
        except FileNotFoundError:
            return
        except (OSError, UnicodeError, json.JSONDecodeError, ValueError, TypeError) as error:
            self.output_fn(f"데이터 파일을 읽을 수 없어 기본 퀴즈로 시작합니다: {error}")
            return
        self.quizzes = quizzes
        self.best_score = score

    def save_state(self) -> bool:
        data = {
            "quizzes": [quiz.to_dict() for quiz in self.quizzes],
            "best_score": self.best_score,
        }
        temp_path = self.state_path.with_name(self.state_path.name + ".tmp")
        try:
            with temp_path.open("w", encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False, indent=2)
                file.write("\n")
            os.replace(temp_path, self.state_path)
            return True
        except OSError as error:
            self.output_fn(f"데이터 저장에 실패했습니다: {error}")
            try:
                temp_path.unlink(missing_ok=True)
            except OSError:
                pass
            return False

    def prompt_number(self, prompt: str, minimum: int, maximum: int) -> int:
        while True:
            raw = self.input_fn(prompt).strip()
            if not raw:
                self.output_fn("입력값이 비어 있습니다. 다시 입력해 주세요.")
                continue
            try:
                number = int(raw)
            except ValueError:
                self.output_fn("숫자를 입력해 주세요.")
                continue
            if not minimum <= number <= maximum:
                self.output_fn(f"{minimum}~{maximum} 사이의 번호를 입력해 주세요.")
                continue
            return number

    def prompt_text(self, prompt: str) -> str:
        while True:
            value = self.input_fn(prompt).strip()
            if value:
                return value
            self.output_fn("입력값이 비어 있습니다. 다시 입력해 주세요.")

    def show_menu(self) -> None:
        self.output_fn("\n=== 파이썬 콘솔 퀴즈 게임 ===")
        for item in self.MENU:
            self.output_fn(item)

    def run(self) -> None:
        actions = {
            1: self.play,
            2: self.add_quiz,
            3: self.list_quizzes,
            4: self.show_best_score,
        }
        try:
            while True:
                self.show_menu()
                choice = self.prompt_number("선택: ", 1, 5)
                if choice == 5:
                    self.save_state()
                    self.output_fn("게임을 종료합니다.")
                    return
                actions[choice]()
        except (KeyboardInterrupt, EOFError):
            self.output_fn("\n입력이 중단되어 안전하게 종료합니다.")
            self.save_state()

    def play(self) -> None:
        if not self.quizzes:
            self.output_fn("등록된 퀴즈가 없습니다.")
            return
        correct = 0
        for index, quiz in enumerate(self.quizzes, 1):
            self.output_fn(f"\n문제 {index}/{len(self.quizzes)}")
            self.output_fn(quiz.formatted())
            selection = self.prompt_number("정답 번호 (1~4): ", 1, 4)
            if quiz.is_correct(selection):
                correct += 1
                self.output_fn("정답입니다!")
            else:
                self.output_fn(f"오답입니다. 정답은 {quiz.answer}번입니다.")
        self.output_fn(f"결과: {len(self.quizzes)}문제 중 {correct}문제 정답")

    def add_quiz(self) -> None:
        question = self.prompt_text("문제: ")
        choices = [
            self.prompt_text(f"선택지 {index}: ") for index in range(1, 5)
        ]
        answer = self.prompt_number("정답 번호 (1~4): ", 1, 4)
        self.quizzes.append(Quiz(question, choices, answer))
        if self.save_state():
            self.output_fn("퀴즈를 추가하고 저장했습니다.")
        else:
            self.output_fn("퀴즈는 현재 실행에만 추가되었습니다. 저장 상태를 확인해 주세요.")

    def list_quizzes(self) -> None:
        self.output_fn("퀴즈 목록은 준비 중입니다.")

    def show_best_score(self) -> None:
        self.output_fn("점수 확인은 준비 중입니다.")
