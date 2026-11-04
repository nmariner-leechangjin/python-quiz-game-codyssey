# 파이썬 콘솔 퀴즈 게임

Codyssey 「컴퓨터에게 명령 내리는 말(파이썬) 처음 배우기」 미션 프로젝트입니다. 과제의 **최종 결과물 1 → 2 → 3번 순서**로 설명합니다. Python 표준 라이브러리만 사용합니다.

## 1. 동작하는 퀴즈 게임

### 프로젝트 개요

Python으로 터미널에서 실행하는 사지선다 퀴즈 게임입니다. 메뉴에서 퀴즈 풀기, 퀴즈 추가, 퀴즈 목록, 최고 점수 확인, 종료를 선택합니다.

### 퀴즈 주제와 선정 이유

주제는 **파이썬 기초**입니다. 이 미션의 학습 목표인 변수, 자료형, 조건문, 반복문, 함수를 문제를 풀며 다시 설명해 볼 수 있기 때문입니다. 기본 문제 6개를 직접 작성했습니다.

### 실행 방법

Python 3.10 이상을 설치한 뒤 VS Code에서 `python-quiz-game-codyssey.code-workspace`를 열고 터미널에서 다음을 실행합니다.

```powershell
python main.py
```

자동 검증은 다음 명령으로 실행합니다.

```powershell
python -m unittest discover -s tests -v
```

### 기능 목록과 현재 상태

| 기능 | 현재 상태 |
| --- | --- |
| 번호 선택 메뉴와 종료 | 구현·검증 |
| 퀴즈 풀기와 결과 표시 | 구현·검증 |
| 새 퀴즈 등록 | 구현·검증 |
| 저장된 퀴즈 목록 | 구현·검증 |
| 최고 점수 확인과 갱신 | 구현·검증 |
| 잘못된 입력, `Ctrl+C`, EOF 처리 | 구현·검증 |
| 종료 후 재실행 시 퀴즈와 최고 점수 유지 | 구현·검증 |
| 보너스: 문제 순서 랜덤 출제 | 구현·검증 |

## 2. 코드 구조

`Quiz` 클래스는 문제, 4개 선택지, 정답과 정답 판정을 맡습니다. `QuizGame` 클래스는 메뉴, 입력, 게임 진행, 목록, 최고 점수와 JSON 저장·불러오기를 맡습니다. 기본 문제는 `default_quizzes.py`에 분리했습니다. `random.shuffle`은 문제 목록의 복사본에만 적용하므로 저장된 목록 순서는 바뀌지 않습니다.

### 파일 구조

```text
.
├── .gitignore                 # 로컬 데이터와 Python 생성 파일 제외
├── ARCHITECTURE.md            # 역할과 데이터 흐름
├── CHECKLIST.md               # 요구사항별 검증 상태
├── PRODUCT.md                 # 범위와 완료 조건
├── README.md                  # 실행 및 사용자 안내
├── default_quizzes.py         # 기본 문제 6개
├── main.py                    # 실행 진입점
├── python-quiz-game-codyssey.code-workspace
├── quiz.py                    # Quiz 클래스
├── quiz_game.py               # QuizGame 클래스
├── state.json                 # 실행 중 생성, Git 추적 제외
└── tests/test_quiz_game.py    # 자동 검증
```

### 데이터 파일: `state.json`

프로젝트 루트의 UTF-8 JSON 파일입니다. 예시는 다음과 같습니다.

```json
{
  "quizzes": [
    {
      "question": "예시 문제?",
      "choices": ["가", "나", "다", "라"],
      "answer": 2
    }
  ],
  "best_score": 1
}
```

`answer`는 1~4 번호이고 `best_score`는 최고 정답 수입니다. 아직 풀지 않았다면 `null`입니다. 파일이 없으면 기본 문제 6개로 시작하고, 손상되면 안내 후 기본 데이터로 시작합니다. 저장할 때 임시 파일을 먼저 쓴 뒤 교체합니다. 개인 실행 데이터인 `state.json`은 Git 추적에서 제외합니다.

## 3. GitHub 저장소

저장소: [nmariner-leechangjin/python-quiz-game-codyssey](https://github.com/nmariner-leechangjin/python-quiz-game-codyssey)

| 과제 항목 | 현재 상태 |
| --- | --- |
| 로컬 Git 저장소와 첫 커밋 | 완료 |
| GitHub 저장소 생성 | 완료 |
| 프로젝트 코드 업로드 | 완료 (`main` push) |
| 의미 있는 커밋 10개 이상 | 완료 (17개) |
| 추가 브랜치 생성과 `main` 병합 | `codex/quiz-play`에서 개발 후 `main` 병합 |
| 별도 디렉터리에서 `clone`, 변경 후 `push`, 기존 디렉터리에서 `pull` | 완료 및 반영 확인 |

Git 이력과 원격 반영 여부는 실제 명령 결과로 확인했습니다. 제출용 기록은 `docs/evidence/`에 있습니다.

### 제출용 증빙

- `01-vscode-project.png`: VS Code 작업 영역과 파일
- `02-tests.txt`: 자동 테스트 9개 통과
- `03-console-flow.txt`: 메뉴·잘못된 입력·목록·점수·종료
- `06-add-quiz.txt`: 퀴즈 추가
- `07-list-after-restart.txt`: 재실행 후 목록 유지
- `08-play-quiz.txt`: 퀴즈 플레이와 결과
- `09-score-after-restart.txt`: 재실행 후 최고 점수 유지
- `10-git-log.txt`: 브랜치·병합 및 커밋 그래프
- `11-environment.txt`: Python·Git·원격 저장소 설정

복제 실습: 별도 디렉터리에서 README를 수정하고 push한 뒤 원래 디렉터리에서 pull로 반영했습니다.
