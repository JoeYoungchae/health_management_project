'''
모듈명: health_db.py
작성일: 2026.11.13
작성자: 조영채
주 담당 영역: 데이터 구조화 및 파일 영구 저장

세부 요구사항 내용: 
    - 레코드 모델링: 식별번호, 이름, 생년, 성별, 키, 몸무게, BMI, 비만도 상태를 담는 객체 구조 및
            딕셔너리 변환(to_dict) 지원
    - 식별번호 자동 생성: 신규 레코드 추가 시 고유한 환자식별번호 발급 로직 구현
    - 다중 파일 I/O: JSON, CSV, TXT, Pickle 등 영구 파일 포맷별 저장(save) 및 로드(load) 기능 제공
    - 예외 처리: 파일 부재나 손상 시 예외 처리(try-except) 구현

클래스:
    - HealthRecord: 한 사람의 건강 기록(식별번호, 이름, 생년, 성별, 키, 몸무게, BMI, 비만도 상태)을 저장하고
        딕셔너리로 변환하는 클래스
    - HealthManager: 건강 기록 목록을 관리하고, 식별번호 생성 및 JSON, CSV, TXT, Pickle 파일의
        저장과 불러오기를 담당하는 클래스

** AI 사용한 코드 **
    - AI 종류: ChatGPT (GPT-6)
    - AI 사용 목적: 예외 처리를 해야되는데 사용해야 하는 예외 처리 종류를 파악하지 못하여 사용함.
    - 사용한 AI 프롬프트: 예외처리를 해야 되는데 이 코드에선 뭘 써야될까?
    - 사용한 사람: 조영채
    - 사용 날짜: 2026.11.13
'''

import json
import csv
import pickle
from datetime import datetime

class HealthRecord:
    def __init__(self, id, name, birth, gender,
                 height, weight, bmi, status):   # 객체 생성 및 초기화
        self.id = id
        self.name = name
        self.birth = birth
        self.gender = gender
        self.height = height
        self.weight = weight
        self.bmi = bmi
        self.status = status

    def to_dict(self):      # 객체 딕셔너리 변환
        return{
            "id":self.id,
            "name":self.name,
            "birth":self.birth,
            "gender":self.gender,
            "height":self.height,
            "weight":self.weight,
            "bmi":self.bmi,
            "status":self.status
        }
    
class HealthManager:
    def __init__(self):     # 데이터 목록 초기화
        self.records = []

    def generate_patient_id(self):      # 식별번호 생성
        current_year = datetime.now().year
        max_num = 0
        new_num = 0
        new_id = ""

        '''
        AI 종류: ChatGPT (GPT-6)
        AI 사용 목적: 식별번호 생성에 어려움을 겪어 도움받음.
        사용한 AI 프롬프트: 이렇게 쓰는게 맞아? 전체 코드를 보내줄테니까 잘못된 부분을 알려줘.
        사용한 사람: 조영채
        사용 날짜: 2026.11.13
        '''
        for p in self.records:
            id_parts = p.id.split("-")

            if id_parts[0] == "P" + str(current_year):
                if int(id_parts[1]) > max_num:
                    max_num = int(id_parts[1])

        new_num = max_num + 1

        # zfill()을 이용해 문자열의 왼쪽에 0을 채워 4만큼의 길이로 늘린다.
        new_num = str(new_num).zfill(4)

        new_id = 'P' + str(current_year) + '-' + new_num
        return new_id



    def save_json(self):        # JSON 저장
        try:
            with open("data/health_data.json", "w", encoding="utf-8") as f:
                new_list = []

                for person in self.records:
                    new_list.append(person.to_dict())

                json.dump(new_list, f, ensure_ascii=False)

        except OSError:
            print("JSON 파일 저장 중 오류가 발생했습니다.")

    def load_json(self):        # JSON 불러오기
        try:
            with open("data/health_data.json", "r", encoding="utf-8") as f:
                person_list = json.load(f)
            # new_records를 이용해 데이터를 불러오는 도중 오류 발생 시 기존 데이터를 보호한다.
            new_records = []

            for person_dict in person_list:

                # 딕셔너리에 저장된 데이터를 언패킹(**)하여 HealthRecord 객체를 생성한다.
                person = HealthRecord(**person_dict)
                new_records.append(person)

            # 불러오기 성공 시 기존 기록을 교체
            self.records = new_records

        except FileNotFoundError:
            print("JSON 파일을 찾을 수 없습니다.")

        except json.JSONDecodeError:
            print("JSON 파일의 데이터 형식이 잘못되었습니다.")

        except (TypeError, KeyError):
            print("JSON 파일의 데이터 구조가 올바르지 않습니다.")


    def save_csv(self):         # CSV 저장
        try:
            with open("data/health_data.csv", "w", encoding="utf-8", newline="") as f:
                # csv.DictWriter()를 사용하면 딕셔너리 형태의 데이터를 편하게 저장 가능하다.
                writer = csv.DictWriter(f, fieldnames=["id", "name", "birth", "gender",
                                                    "height", "weight", "bmi", "status"])
                writer.writeheader()

                for person in self.records:
                    person_dict = person.to_dict()
                    # 변환한 딕셔너리 데이터를 CSV 파일에 한 행씩 작성한다.
                    writer.writerow(person_dict)

        except OSError:
            print("CSV 파일 저장 중 오류가 발생했습니다.")

    def load_csv(self):         # CSV 불러오기
        try:
            with open("data/health_data.csv", "r", encoding="utf-8", newline="") as f:
                reader = csv.DictReader(f)      # CSV 데이터를 딕셔너리 형태로 읽는다.
                new_records = []

                # 숫자 데이터들은 자료형을 변환해준다.
                for person_dict in reader:
                    person_dict["birth"] = int(person_dict["birth"])
                    person_dict["height"] = float(person_dict["height"])
                    person_dict["weight"] = float(person_dict["weight"])
                    person_dict["bmi"] = float(person_dict["bmi"])

                    # 딕셔너리에 저장된 데이터를 언패킹(**)하여 HealthRecord 객체를 생성한다.
                    person = HealthRecord(**person_dict)
                    new_records.append(person)

                self.records = new_records

        except FileNotFoundError:
            print("CSV 파일을 찾을 수 없습니다.")

        except ValueError:
            print("CSV 파일의 숫자 데이터가 올바르지 않습니다.")

        except KeyError:
            print("CSV 파일에 필요한 항목이 없습니다.")

        except OSError:
            print("CSV 파일을 불러오는 중 오류가 발생했습니다.")

    def save_txt(self):         # TXT 저장
        try:
            with open("data/health_data.txt", "w", encoding="utf-8") as f:
                for person in self.records:
                    # 환자 객체의 각 속성을 문자열로 변환하여 리스트에 저장한다.
                    person_data = [
                        str(person.id),
                        str(person.name),
                        str(person.birth),
                        str(person.gender),
                        str(person.height),
                        str(person.weight),
                        str(person.bmi),
                        str(person.status)
                    ]

                    person_text = ",".join(person_data)
                    f.write(person_text + "\n")

        except OSError:
            print("TXT 파일 저장 중 오류가 발생했습니다.")

    def load_txt(self):         # TXT 불러오기
        try:
            with open("data/health_data.txt", "r", encoding="utf-8") as f:
                new_records = []

                for line in f:
                    person_data = line.strip().split(',')       # 공백, 줄바꿈 제거 후 쉼표를 기준하여 분리한다.
                    
                    # 데이터의 개수가 8개가 아니면 ValueError 예외를 직접 발생시킨다.
                    if len(person_data) != 8:
                        raise ValueError
                    
                    # 문자열로 읽어온 숫자 데이터를 정수형, 실수형으로 변환한다.
                    person_data[2] = int(person_data[2])
                    person_data[4] = float(person_data[4])
                    person_data[5] = float(person_data[5])
                    person_data[6] = float(person_data[6])

                    person = HealthRecord(*person_data)     # *는 "리스트" 값을 순서대로 매개 변수에 전달
                    new_records.append(person)

                self.records = new_records

        except FileNotFoundError:
            print("TXT 파일을 찾을 수 없습니다.")

        except ValueError:
            print("TXT 파일의 데이터 형식이 잘못되었습니다.")

        except IndexError:
            print("TXT 파일의 데이터 항목이 부족합니다.")

        except OSError:
            print("TXT 파일을 불러오는 중 오류가 발생했습니다.")


    def save_pkl(self):         # Pickle 저장
        try:
            with open("data/health_data.pkl", "wb") as f:
                # self.records에 저장된 환자 객체 리스트를 Pickle 형식으로 파일에 저장한다.
                pickle.dump(self.records, f)

        except OSError:
            print("Pickle 파일 저장 중 오류가 발생했습니다.")

        except pickle.PickleError:
            print("Pickle 파일 저장 중 오류가 발생했습니다.")

    def load_pkl(self):         # Pickle 불러오기
        try:
            with open("data/health_data.pkl", "rb") as f:
                new_records = pickle.load(f)
                
            # 불러온 데이터가 리스트 형태인지 확인한다.
            if not isinstance(new_records, list):
                raise ValueError
            
            # 리스트 안의 모든 데이터가 HealthRecord 객체인지 확인한다.
            if not all(isinstance(person, HealthRecord)
                       for person in new_records):
                raise ValueError

            self.records = new_records

        except FileNotFoundError:
            print("Pickle 파일을 찾을 수 없습니다.")

        except (pickle.UnpicklingError, EOFError):
            print("Pickle 파일의 데이터가 손상되었습니다.")

        except ValueError:
            print("Pickle 파일의 데이터 구조가 올바르지 않습니다.")

        except OSError:
            print("Pickle 파일을 불러오는 중 오류가 발생했습니다.")
