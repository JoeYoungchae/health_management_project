'''
모듈명: health_logic.py
작성일: 2026.11.17
작성자: 조영채
주 담당 영역: 데이터 구조화 및 파일 영구 저장

세부 요구사항 내용: 
    - 신규 등록 및 중복 체크: UI 및 엑셀 파일로부터 데이터를 받아 중복 검사 후 리스트 및 파일에 추가
    - 조회 및 검색: 전체 목록 조회 및 이름·식별번호 기반 상세 검색 기능 제공
    - 수정 및 BMI 자동 재계산: 특정 레코드의 키·몸무게 수정 시 공식에 따른 BMI 및 비만도 재산출 연동
    - 삭제: 선택된 레코드의 안전한 제거 및 파일 동기
    - 통계 산출: 전체 인원수, 평균 키, 평균 몸무게, 평균 BMI 등의 유용한 통계 데이터 연산

클래스:
    - HealthLogic
'''

from health_db import HealthManager

class HealthLogic(HealthManager):
    def __init__(self, id, name, birth, gender, height, weight):
        super().__init__()
        self.id = id
        self.name = name
        self.birth = birth
        self.gender = gender
        self.height = height
        self.weight = weight

    def add_record(self, id, name, birth, gender, height, weight):     # 건강정보를 추가하는 메소드
        pass

    '''
    AI 사용
    '''
    def check_duplicate(self):      # 중복 데이터 검사하는 메소드
        for existing in self.records:
            if existing.id == records.id:
                return True

            if (existing.name == records.name and
                existing.birth_year == records.birth_year and
                existing.gender == records.gender):
                return True
            return False

    def get_all_records(self):      # 전체 목록 반환하는 메소드
        pass

    def get_record(self):           # 식별번호로 상세 조회
        pass

    def search_records(self):       # 이름 및 식별번호 검색
        pass

    def update_records(self):       # 기존 정보 수정
        pass

    def calculate_bmi(self):        # BMI 계산
        pass

    def delete_record(self):        # 건강정보 삭제
        pass

    def get_statistics(self):       # 전체 통계 계산
        pass