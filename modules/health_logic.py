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

import csv
from health_db import HealthManager, HealthRecord

class HealthLogic(HealthManager):
    def __init__(self):
        super().__init__()

    '''
        AI 종류: ChatGPT (GPT-6)
        AI 사용 목적: 입력받은 데이터와 기존 데이터 간 비교를 어떻게 해야할 지 어려움을 겪었다.
        사용 날짜: 2026.11.18
    '''
    def check_duplicate(self, name, birth, gender):      # 중복 데이터 검사하는 메소드
        for record in self.records:
            if (record.name == name and
                record.gender == gender and
                record.birth == birth):
                return True
        return False

    def calculate_bmi(self, height, weight):        # BMI 계산
        bmi = weight / (height / 100) ** 2
        return round(bmi, 1)

    def add_record(self, name, birth, gender, height, weight):     # UI에서 건강정보를 추가하는 메소드
        if self.check_duplicate(name, birth, gender):
            print("중복된 정보입니다.")
            return False

        '''
        AI 종류: ChatGPT (GPT-6)
        AI 사용 목적: 생년, 키, 몸무게가 숫자가 아닐 경우 오류를 처리하기 위함.
        사용 날짜: 2026.11.19
        '''
        try:
            birth = int(birth)
            height = float(height)
            weight = float(weight)

        except ValueError:
            print("생년, 키, 몸무게는 숫자로 입력해야 합니다.")
            return False

        if type(height) == float and type(weight) == float:
            bmi = self.calculate_bmi(height, weight)

        if bmi < 18.5:
            status = "저체중"
        elif bmi < 23.0:
            status = "정상"
        elif bmi < 25.0:
            status = "과체중"
        elif bmi < 30.0:
            status = "1단계 비만"
        elif bmi < 35.0:
            status = "2단계 비만"
        else:
            status = "고도비만"

        newID = self.generate_patient_id()
        newRecord = HealthRecord(newID, name, birth, gender, height, weight, bmi, status)
        self.records.append(newRecord)
        
        self.save_json()

        return True        

    def add_record_CSV(self):          # CSV에서 건강정보를 가져오는 메소드
        with open("health_data..csv", 'r', encoding="utf-8") as f:
            reader = csv.reader(f)
            

    def get_all_records(self):      # 전체 목록 반환하는 메소드
        pass

    def get_record(self):           # 식별번호로 상세 조회
        pass

    def search_records(self):       # 이름 및 식별번호 검색
        pass

    def update_records(self):       # 기존 정보 수정
        pass


    def delete_record(self):        # 건강정보 삭제
        pass

    def get_statistics(self):       # 전체 통계 계산
        pass