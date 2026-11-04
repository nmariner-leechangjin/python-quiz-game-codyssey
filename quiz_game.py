"""메뉴와 게임 진행을 관리한다."""

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
                    self.output_fn("게임을 종료합니다.")
                    return
                actions[choice]()
        except (KeyboardInterrupt, EOFError):
            self.output_fn("\n입력이 중단되어 안전하게 종료합니다.")

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
        self.output_fn("퀴즈 추가는 준비 중입니다.")

    def list_quizzes(self) -> None:
        self.output_fn("퀴즈 목록은 준비 중입니다.")

    def show_best_score(self) -> None:
        self.output_fn("점수 확인은 준비 중입니다.")
