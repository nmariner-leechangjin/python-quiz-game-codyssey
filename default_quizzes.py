"""파이썬 기초 주제의 직접 작성한 기본 문제."""

from quiz import Quiz


def make_default_quizzes() -> list[Quiz]:
    return [
        Quiz(
            "변수를 사용하는 주된 이유는 무엇일까요?",
            ["값에 이름을 붙여 다시 사용하기 위해", "화면을 지우기 위해", "파일을 삭제하기 위해", "Python을 설치하기 위해"],
            1,
        ),
        Quiz(
            "문자열을 나타내는 Python 자료형은 무엇일까요?",
            ["int", "bool", "str", "list"],
            3,
        ),
        Quiz(
            "여러 값을 순서대로 담는 자료형은 무엇일까요?",
            ["list", "bool", "int", "str"],
            1,
        ),
        Quiz(
            "조건이 참일 때와 거짓일 때 다른 동작을 고르는 문법은 무엇일까요?",
            ["for", "if/else", "def", "import"],
            2,
        ),
        Quiz(
            "횟수가 정해진 반복에서 보통 사용하는 문장은 무엇일까요?",
            ["try", "return", "for", "class"],
            3,
        ),
        Quiz(
            "함수에서 계산한 값을 호출한 곳으로 돌려주는 키워드는 무엇일까요?",
            ["print", "return", "input", "pass"],
            2,
        ),
    ]
