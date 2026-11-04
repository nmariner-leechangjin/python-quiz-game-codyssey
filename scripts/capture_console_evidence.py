"""격리된 임시 폴더에서 실제 프로그램을 실행해 제출용 기록을 만든다."""

import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "docs" / "evidence"
SOURCE_FILES = ("main.py", "quiz.py", "quiz_game.py", "default_quizzes.py")


def run_game(folder: Path, filename: str, inputs: list[str]) -> str:
    environment = os.environ.copy()
    environment["PYTHONIOENCODING"] = "utf-8"
    result = subprocess.run(
        [sys.executable, "main.py"],
        input=("\n".join(inputs) + "\n").encode("utf-8"),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        cwd=folder,
        env=environment,
        check=False,
    )
    output = result.stdout.decode("utf-8").replace("\r\n", "\n")
    if result.returncode:
        raise RuntimeError(f"{filename}: 프로그램 종료 코드 {result.returncode}\n{output}")
    text = "Command: python main.py\nInput sequence: " + ", ".join(inputs) + "\n\n" + output
    (OUTPUT / filename).write_text(text, encoding="utf-8")
    return output


def main() -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="codyssey-quiz-evidence-") as directory:
        folder = Path(directory)
        for name in SOURCE_FILES:
            shutil.copy2(ROOT / name, folder / name)

        add_output = run_game(
            folder,
            "06-add-quiz.txt",
            ["2", "bool 자료형의 값은?", "True", "문자열만", "리스트만", "딕셔너리만", "1", "5"],
        )
        if "퀴즈를 추가하고 저장했습니다" not in add_output:
            raise AssertionError("퀴즈 추가 확인 실패")

        list_output = run_game(folder, "07-list-after-restart.txt", ["3", "5"])
        if "등록된 퀴즈: 7개" not in list_output or "bool 자료형의 값은?" not in list_output:
            raise AssertionError("재실행 후 퀴즈 목록 확인 실패")

        play_output = run_game(folder, "08-play-quiz.txt", ["1", *(["1"] * 7), "5"])
        if "결과: 7문제 중" not in play_output:
            raise AssertionError("퀴즈 결과 확인 실패")

        score_output = run_game(folder, "09-score-after-restart.txt", ["4", "5"])
        if "최고 점수:" not in score_output:
            raise AssertionError("재실행 후 최고 점수 확인 실패")

    print("4 console evidence files generated and verified")


if __name__ == "__main__":
    main()
