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
        self.load_json()

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

    def print_record(self, record):
        print("\n========== 건강정보 ==========")
        print(f"식별번호 : {record.id}")
        print(f"이름     : {record.name}")
        print(f"생년     : {record.birth}")
        print(f"성별     : {record.gender}")
        print(f"키       : {record.height}cm")
        print(f"몸무게   : {record.weight}kg")
        print(f"BMI      : {record.bmi}")
        print(f"비만도   : {record.status}")
        print("==============================")

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

    
    
    def main(self):

        while True:

            print("\n================================")
            print("       건강정보 관리 프로그램")
            print("================================")
            print("1. 건강정보 등록")
            print("2. CSV 파일 불러오기")
            print("3. 전체 목록 조회")
            print("4. 건강정보 검색")
            print("5. 건강정보 수정")
            print("6. 건강정보 삭제")
            print("7. 전체 통계 조회")
            print("0. 프로그램 종료")
            print("================================")

            choice = input("메뉴 선택: ").strip()

            # 1. 건강정보 등록
            if choice == "1":

                name = input("이름: ").strip()
                birth = input("생년: ").strip()
                gender = input("성별: ").strip()
                height = input("키(cm): ").strip()
                weight = input("몸무게(kg): ").strip()

                result = self.add_record(
                    name, birth, gender, height, weight
                )

                if result:
                    print("\n건강정보 등록 성공!")
                    self.print_record(self.records[-1])
                else:
                    print("\n등록 실패! 입력값 또는 중복 여부를 확인하세요.")

            # 2. CSV 파일 불러오기
            elif choice == "2":

                result = self.add_record_CSV()

                if result:
                    print("\nCSV 파일 불러오기가 완료되었습니다.")
                    print(f"현재 등록 인원: {len(self.records)}명")
                else:
                    print("\nCSV 파일을 불러오지 못했습니다.")
                    print("파일 경로와 파일 이름을 확인하세요.")

            # 3. 전체 목록 조회
            elif choice == "3":

                records = self.get_all_records()

                if len(records) == 0:
                    print("\n등록된 건강정보가 없습니다.")

                else:
                    print("\n========== 전체 건강정보 ==========")
                    print(f"전체 등록 인원: {len(records)}명")

                    for record in records:
                        self.print_record(record)

            # 4. 건강정보 검색
            elif choice == "4":

                keyword = input(
                    "이름 또는 식별번호 입력: "
                ).strip()

                if keyword == "":
                    print("\n검색어를 입력하세요.")
                    continue

                results = self.search_records(keyword)

                if len(results) > 0:

                    print(f"\n검색 결과: {len(results)}건")

                    for record in results:
                        self.print_record(record)

                else:
                    print("\n검색 결과가 없습니다.")

            # 5. 건강정보 수정
            elif choice == "5":

                patient_id = input(
                    "수정할 식별번호: "
                ).strip()

                record = self.get_record(patient_id)

                if record is None:
                    print("\n해당 정보를 찾을 수 없습니다.")
                    continue

                print("\n현재 건강정보")
                self.print_record(record)

                height = input("\n새로운 키(cm): ").strip()
                weight = input("새로운 몸무게(kg): ").strip()

                result = self.update_records(
                    patient_id, height, weight
                )

                if result:

                    print("\n건강정보 수정 성공!")

                    updated_record = self.get_record(patient_id)

                    print("\n수정된 건강정보")
                    self.print_record(updated_record)

                else:
                    print("\n수정 실패! 입력값을 확인하세요.")

            # 6. 건강정보 삭제
            elif choice == "6":

                patient_id = input(
                    "삭제할 식별번호: "
                ).strip()

                record = self.get_record(patient_id)

                if record is None:
                    print("\n해당 정보를 찾을 수 없습니다.")
                    continue

                print("\n삭제할 건강정보")
                self.print_record(record)

                confirm = input(
                    "\n정말 삭제하시겠습니까? (y/n): "
                ).strip().lower()

                if confirm == "y":

                    result = self.delete_record(patient_id)

                    if result:
                        print("\n건강정보 삭제 완료!")
                    else:
                        print("\n삭제에 실패했습니다.")

                elif confirm == "n":
                    print("\n삭제를 취소했습니다.")

                else:
                    print("\n잘못된 입력입니다. 삭제를 취소합니다.")

            # 7. 전체 통계 조회
            elif choice == "7":

                statistics = self.get_statistics()

                if statistics is False:

                    print("\n등록된 데이터가 없습니다.")

                else:

                    weightAvg, heightAvg, bmiAvg = statistics

                    print("\n========== 전체 통계 ==========")
                    print(f"전체 인원수 : {len(self.records)}명")
                    print(f"평균 키     : {heightAvg:.1f}cm")
                    print(f"평균 몸무게 : {weightAvg:.1f}kg")
                    print(f"평균 BMI    : {bmiAvg:.1f}")
                    print("===============================")

            # 0. 프로그램 종료
            elif choice == "0":

                print("\n프로그램을 종료합니다.")
                break

            # 잘못된 메뉴 입력
            else:

                print("\n잘못된 메뉴입니다. 다시 선택하세요.")


# 프로그램 시작
if __name__ == "__main__":

    health = HealthLogic()

    health.main()