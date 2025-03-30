import tkinter as tk
import subprocess
from PIL import Image, ImageTk

# Tạo cửa sổ chính
root = tk.Tk()
root.title("Trò Chơi Cờ Bàn")

# Thiết lập kích thước cửa sổ là 700x700
root.geometry("700x700")

# Tạo font với kích thước lớn hơn
custom_font = ("Helvetica", 16)

# Mở hình ảnh "home.jpg" sử dụng thư viện Pillow
image = Image.open("home.jpg")

# Chuyển đổi hình ảnh thành định dạng Tkinter PhotoImage
photo = ImageTk.PhotoImage(image)

# Tạo nhãn để hiển thị hình ảnh nền
background_label = tk.Label(image=photo)
background_label.place(relwidth=1, relheight=1)

# Tạo một khung để chứa các nút
button_container = tk.Frame(root, bg='SystemButtonFace')
button_container.pack(expand=True)

# Hàm game Cờ Caro
def game_CoCaRo():
    subprocess.Popen(["python", "cocaro.py"])

# Hàm game Cờ Hoang Dã
def game_CoHoangDa():
    subprocess.Popen(["python", "cohoangda.py"])

# Hàm game Cờ Thú
def game_CoThu():
    subprocess.Popen(["python", "cothu.py"])

# Hàm game Cờ Connect 6
def game_CoConnect6():
    subprocess.Popen(["python", "coconnect6.py"])

# Hàm game Cờ Vây
def game_CoVay():
    subprocess.Popen(["python", "covay.py"])

# Hàm game Cờ Lật
def game_CoLat():
    subprocess.Popen(["python", "colat.py"])

# Hàm game Cờ Vua
def game_CoVua():
    subprocess.Popen(["python", "covua.py"])

# Hàm game Cờ Connect 4
def game_CoConnect4():
    subprocess.Popen(["python", "coconnect4.py"])

# Hàm game Cờ Tướng
def game_CoTuong():
    subprocess.Popen(["python", "cotuong.py"])

# Hàm game Cờ Shogi
def game_CoShogi():
    subprocess.Popen(["python", "coshogi.py"])

# Hàm game Cờ Gánh
def game_CoGanh():
    subprocess.Popen(["python", "CoGanhByPython/main.py"])

# Tạo danh sách các nút cho từng hàng
buttons_row1 = [
    ("Cờ Thú", game_CoThu),
    ("Cờ Lật", game_CoLat),
    ("Cờ Gánh", game_CoGanh),
    ("Cờ Hoang Dã", game_CoHoangDa),
]

buttons_row2 = [
    ("Cờ Vây", game_CoVay),
    ("Cờ Vua", game_CoVua),
    ("Cờ Tướng", game_CoTuong),
    ("Cờ Shogi", game_CoShogi),
]

buttons_row3 = [
    ("Cờ Connect 4", game_CoConnect4),
    ("Cờ Caro", game_CoCaRo),
    ("Cờ Connect 6", game_CoConnect6),
]

# Tạo nút cho hàng thứ nhất
for text, command in buttons_row1:
    button = tk.Button(button_container, text=text, command=command, width=20, height=2, font=custom_font)
    button.grid(row=0, column=buttons_row1.index((text, command)), padx=10, pady=10)

# Tạo nút cho hàng thứ hai
for text, command in buttons_row2:
    button = tk.Button(button_container, text=text, command=command, width=20, height=2, font=custom_font)
    button.grid(row=1, column=buttons_row2.index((text, command)), padx=10, pady=10)

# Tạo nút cho hàng thứ ba
for text, command in buttons_row3:
    button = tk.Button(button_container, text=text, command=command, width=20, height=2, font=custom_font)
    column_position = buttons_row3.index((text, command))  # Đặt nút vào giữa hai cột
    button.grid(row=2, column=column_position, columnspan=2, padx=10, pady=10)

# Vòng lặp chính
root.mainloop()
