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
        '''
        AI 종류: ChatGPT (GPT-6)
        AI 사용 목적: 생년, 키, 몸무게가 숫자가 아닐 경우 오류를 처리하기 위함.
        사용 날짜: 2026.11.19
        '''
        try:
            birth = int(birth)
            height = float(height)
            weight = float(weight)

        except (ValueError, TypeError):
            return False

        if height <= 0 or weight <= 0:
            return False

        if self.check_duplicate(name, birth, gender):       # 중복된 정보면 False 반환
            return False

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
        try:
            with open("data/health_data.csv", 'r', encoding="utf-8") as f:
                reader = csv.reader(f)
                next(reader, None)       # 열 이름이 저장된 첫 번째 행을 건너뛴다.

                for element in reader:
                    if len(element) < 8:       # 데이터 항목이 부족한 행은 건너뛴다.
                        continue

                    if not element[0]:       # 식별번호가 없는 행은 건너뛴다.
                        continue

                    if self.get_record(element[0]):       # 기존 식별번호와 중복되면 건너뛴다.
                        continue

                    try:
                        birth = int(element[2])
                        height = float(element[4])
                        weight = float(element[5])
                        bmi = float(element[6])
                    except (ValueError, TypeError):
                        continue       # 숫자 변환에 실패하면 해당 행 건너뛰기

                    if height <= 0 or weight <= 0:
                        continue

                    duplicate = self.check_duplicate(element[1], birth, element[3])

                    if duplicate:
                        continue

                    newRecord = HealthRecord(element[0], element[1], birth, element[3],
                                           height, weight, bmi, element[7])
                    self.records.append(newRecord)

            self.save_json()
            return True

        except FileNotFoundError:
            return False

    def get_all_records(self):      # 전체 목록 반환하는 메소드
        return self.records

    def get_record(self, id):           # 식별번호로 상세 조회
        for record in self.records:
            if id == record.id:
                return record
        return None

    def search_records(self, keyword):       # 이름 및 식별번호 검색
        results = []

        for record in self.records:
            if keyword in record.name or keyword in record.id:
                results.append(record)
        return results

    def update_records(self, id, height, weight):       # 기존 정보 수정
        try:
            height = float(height)
            weight = float(weight)
        except (ValueError, TypeError):
            return False

        if height <= 0 or weight <= 0:
            return False

        record = self.get_record(id)      # get_record는 레코드 객체를 반환함

        if record == None:
            return False

        record.height = height
        record.weight = weight
        record.bmi = self.calculate_bmi(height, weight)

        if record.bmi < 18.5:
            record.status = "저체중"
        elif record.bmi < 23.0:
            record.status = "정상"
        elif record.bmi < 25.0:
            record.status = "과체중"
        elif record.bmi < 30.0:
            record.status = "1단계 비만"
        elif record.bmi < 35.0:
            record.status = "2단계 비만"
        else:
            record.status = "고도비만"

        self.save_json()

        return True

    def delete_record(self, id):        # 건강정보 삭제
        record = self.get_record(id)

        if record == None:
            return False

        self.records.remove(record)
        self.save_json()

        return True

    def get_statistics(self):       # 전체 통계 계산
        if len(self.records) == 0:
            return False

        count = len(self.records)

        sumWeight = 0
        sumHeight = 0
        sumBMI = 0

        for record in self.records:
            sumWeight += record.weight
            sumHeight += record.height
            sumBMI += record.bmi

        weightAvg = sumWeight / count
        heightAvg = sumHeight / count
        bmiAvg = sumBMI / count

        return weightAvg, heightAvg, bmiAvg