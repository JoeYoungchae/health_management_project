# health_management_project

건강 상태를 관리하고 BMI를 확인할 수 있는 프로젝트입니다.
사람들의 건강 정보를 기록하고 관리할 수 있습니다.

## 주요 기능


## 기술 스택


## 저장소 구조

```text
health_management_project/
├── assets/
│   └── esult_screenshot.png    # 프로그램 실행 결과 캡처 화면
├── data/                       # 영구 데이터 저장 폴더 (File I/O 대상)
│   ├── health_data.csv         # CSV 포맷 저장 파일(엑셀 일괄 등록용 포함)
│   ├── health_data.json        # JSON 포맷 저장 파일
│   ├── health_data.pkl         # Pickle 이진 객체 파일
│   └── health_data.txt         # 일반 텍스트 포맷 파일
├── modules/                    # 소스 코드 모듈 디렉토리
│   ├── __init__.py             # 패키지 초기화 파일
│   ├── health_db.py            # 모듈 1: 데이터 구조화 및 파일 I/O, 클래스, 파일입출력
│   ├── health_gui.py           # 모듈 2: 핵심 비즈니스 로직 및 CRUD, 통계 연산, 클래스 내 메소드 추가, 테스트
│   └── health_logic.py         # 모듈 3: Tkinter 기반 GUI 및 이벤트 바인딩
├── main.py                     # 프로그램 실행 진입점
└── README.md                   # 프로젝트 소개, 실행 방법 명시
```
