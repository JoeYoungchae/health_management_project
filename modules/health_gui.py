from tkinter import *
from health_logic import HealthLogic

logic = HealthLogic()
window = Tk()
window.geometry("700x450")

main_frame = Frame(window)
main_frame.pack(fill="both", expand=True)

add_frame = Frame(window)

def open_add():
    main_frame.pack_forget()
    add_frame.pack(fill="both", expand=True)

def go_back():
    add_frame.pack_forget()
    main_frame.pack(fill="both", expand=True)

# 메인 화면 구성
label = Label(main_frame, text="BMI 프로그램입니다.")
label.grid(row=0, column=1)

add_record = Button(main_frame, text="건강 정보 추가하기", bg="white", fg="black", width=50, height=14)
entire_record = Button(main_frame, text="전체 건강 정보 확인하기", bg="white", fg="black", width=50, height=14)
search_record = Button(main_frame, text="이름 및 ID로 검색하기", bg="white", fg="black", width=50, height=14)
edit_record = Button(main_frame, text="정보 수정하기", bg="white", fg="black", width=50, height=14)

add_record.grid(row=1, column=0)
entire_record.grid(row=1, column=1)
search_record.grid(row=2, column=0)
edit_record.grid(row=2, column=1)

# 건강 정보 추가 화면
add_label = Label(add_frame, text="신규 정보를 입력하세요.")
add_label.grid(row=0, column=1)

name_label = Label(add_frame, text="이름")
name_label.grid(row=1, column=0)
name_entry = Entry(add_frame)
name_entry.grid(row=1, column=1)

birth_label = Label(add_frame, text="생년")
birth_label.grid(row=2, column=0)
birth_entry = Entry(add_frame)
birth_entry.grid(row=2, column=1)

gender_button = Checkbutton(add_frame, text)

window.mainloop()