# 구조와 데이터 흐름

## 역할

- `main.py`: 프로그램 시작점과 안전한 종료 코드.
- `quiz.py`: 개별 문제의 데이터 유효성, 출력 형식, 정답 판정.
- `default_quizzes.py`: 선택한 주제의 기본 문제 5개 이상.
- `quiz_game.py`: 메뉴, 입력, 게임 진행, 목록, 최고 점수, JSON 저장·불러오기.

## 흐름

`main.py`가 `QuizGame`을 생성하면 `quiz_game.py`가 프로젝트 루트의 `state.json`을 읽는다. 파일이 없거나 손상되면 `default_quizzes.py`의 문제로 시작한다. 메뉴에서 문제를 추가하거나 게임을 마치면 상태를 JSON으로 저장한다. 저장은 임시 파일을 쓴 다음 교체하여 중간에 끊긴 쓰기로 원본을 손상시키지 않도록 한다.

## 데이터 경계

`state.json`은 UTF-8이며 `quizzes` 배열과 `best_score`를 가진다. `best_score`는 아직 플레이하지 않았으면 `null`, 이후에는 최고 정답 수이다. 추가 문제와 점수는 로컬 실행 데이터로 Git에서 제외한다.

## 오류 경계

입력 변환 오류는 입력 메서드에서 재시도한다. 빈 입력은 `입력값이 비어 있습니다`, 숫자 변환 실패는 `숫자를 입력해 주세요`, 범위 오류는 `1~N 사이의 번호를 입력해 주세요`로 안내한다. JSON 읽기 오류·스키마 오류는 기본 데이터로 복구한다. 쓰기 오류는 사용자에게 경고하고 다음 저장 시 재시도한다(숨은 무한 재시도는 하지 않는다). `KeyboardInterrupt`와 `EOFError`는 게임 최상위 루프에서 받아 안전하게 저장·종료하며 저장 위치와 현재 상태 요약을 출력한다.

## 클래스 인터페이스와 선택 이유

- `Quiz`: `formatted()`, `is_correct(selection)`, `to_dict()`, `from_dict(data)`를 공개한다. 문제 데이터와 정답 판정을 한 객체에 묶어 잘못된 선택지·정답을 생성 시점에 막는다.
- `QuizGame`: `run()`, `show_menu()`, `play()`, `add_quiz()`, `list_quizzes()`, `show_best_score()`, `load_state()`, `save_state()`, `prompt_number()`, `prompt_text()`를 공개한다. 게임 상태와 입출력 경계를 한 곳에서 관리한다.

작은 일회성 스크립트라면 함수만으로도 충분하지만, 이 과제에서는 퀴즈별 규칙과 게임 전체 상태가 함께 늘어난다. 클래스를 사용하면 데이터와 그 데이터를 다루는 메서드가 가까워져 책임 분리·재사용·테스트가 쉽다. 함수형 대안은 단순하지만 상태를 여러 함수에 반복 전달해야 한다.

## Git 작업 규칙

`main`은 항상 실행 가능한 상태로 유지하고, 기능은 `codex/<기능명>` 브랜치에서 개발한 뒤 테스트가 통과할 때 병합한다. 브랜치 분리는 기능별 변경을 격리하고 리뷰·되돌리기를 쉽게 하며, 병합은 검증된 기능을 main의 통합 이력에 반영한다. 커밋은 한 기능·한 버그·한 문서 단위로 나누고 메시지는 `type: 명령형 요약` 형식을 사용한다(`feat`, `fix`, `docs`, `test`, `chore`).

## JSON 한계와 복구 정책

`state.json`은 매 저장 때 전체를 메모리에 올리고 다시 쓰므로 데이터가 커지면 O(n) 메모리·쓰기 시간이 필요하다. 현재 규모에서는 `indent=2`, UTF-8, `ensure_ascii=False`로 가독성을 우선한다. 대량 데이터에서는 압축보다 SQLite/DB 전환, 페이지 단위 조회를 고려한다. 향후 스키마 확장 시 `schema_version` 키를 추가하고 마이그레이션으로 이전 버전을 읽는다. 현재 교육용 로컬 앱은 자동 백업을 보존하지 않으며, 원자적 임시 파일 교체와 기본 데이터 복구를 사용한다. 운영 데이터라면 교체 전 `state.json.bak` 한 세대 보존을 추가한다.

## 요구사항 변경 시 수정 지점

| 변경 요구 | 수정 파일·메서드 |
| --- | --- |
| 메뉴/종료/입력 안내 | `quiz_game.py`: `MENU`, `show_menu()`, `run()` |
| 숫자·문자 입력 규칙 | `quiz_game.py`: `prompt_number()`, `prompt_text()` |
| 출제·점수·랜덤화 | `quiz_game.py`: `play()` |
| 퀴즈 등록/목록/점수 화면 | `quiz_game.py`: `add_quiz()`, `list_quizzes()`, `show_best_score()` |
| 문제 규칙·JSON 변환 | `quiz.py`: `Quiz`, `to_dict()`, `from_dict()` |
| 기본 문제 | `default_quizzes.py`: `make_default_quizzes()` |
| 저장 스키마·복구 | `quiz_game.py`: `load_state()`, `save_state()` |
| 실행법·증빙·검증 | `README.md`, `CHECKLIST.md`, `docs/evidence/` |
