"""한 개의 사지선다 문제를 표현한다."""


class Quiz:
    def __init__(self, question: str, choices: list[str], answer: int) -> None:
        if not isinstance(question, str) or not question.strip():
            raise ValueError("문제는 비어 있지 않은 문자열이어야 합니다.")
        if (
            not isinstance(choices, list)
            or len(choices) != 4
            or any(not isinstance(choice, str) or not choice.strip() for choice in choices)
        ):
            raise ValueError("선택지는 비어 있지 않은 문자열 4개여야 합니다.")
        if isinstance(answer, bool) or not isinstance(answer, int) or not 1 <= answer <= 4:
            raise ValueError("정답은 1~4 사이의 번호여야 합니다.")
        self.question = question.strip()
        self.choices = [choice.strip() for choice in choices]
        self.answer = answer

    def formatted(self) -> str:
        lines = [self.question]
        lines.extend(f"{index}. {choice}" for index, choice in enumerate(self.choices, 1))
        return "\n".join(lines)

    def is_correct(self, selection: int) -> bool:
        return selection == self.answer

    def to_dict(self) -> dict:
        return {"question": self.question, "choices": self.choices, "answer": self.answer}

    @classmethod
    def from_dict(cls, data: dict) -> "Quiz":
        if not isinstance(data, dict):
            raise ValueError("문제 데이터는 JSON 객체여야 합니다.")
        try:
            return cls(data["question"], data["choices"], data["answer"])
        except KeyError as error:
            raise ValueError(f"문제 데이터에 {error.args[0]} 항목이 없습니다.") from error
