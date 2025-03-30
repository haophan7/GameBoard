import PySimpleGUI as sg
import gspread
import subprocess

gc = gspread.service_account("cre.json")

sh = gc.open_by_url("https://docs.google.com/spreadsheets/d/1JmCKm5eu5FwY0nUFfdmVkwIGc4FcWj95ZIArU3CjUb0/edit#gid=0")

worksheet = sh.sheet1

list_of_lists = worksheet.get_all_values()

hand_cursor_button_color = ("#FFFFFF", "#3399FF")

layout = [
    [sg.Text("Tên Đăng Nhập")],
    [sg.Input(key="dangnhap")],
    [sg.Text("Mật Khẩu")],
    [sg.Input(key="matkhau", password_char="*")],
    [sg.Button("Đăng Nhập", button_color=hand_cursor_button_color, key="button_dangnhap")],
    [sg.Text("", key="tinnhan")],
]

window = sg.Window("Đăng Nhập Tài Khoản", layout=layout)

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break
    elif event == "button_dangnhap":  # Changed the event to match the button key
        # Xử lý sự kiện khi di chuyển chuột vào nút
        window["button_dangnhap"].Widget.config(cursor="hand2")
        dktdangnhap = values["dangnhap"]
        dktmatkhau = values["matkhau"]
        for tk, mk in list_of_lists:
            if dktdangnhap == tk and dktmatkhau == mk:
                window.close()
                # Gọi script Python tiếp theo
                subprocess.run(["python", "trochoicoban.py"])
                break
        else:
            window["tinnhan"].update("Đăng Nhập Không Thành Công")

# Đảm bảo đóng cửa sổ trước khi thoát chương trình
window.close()
