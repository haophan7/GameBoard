import tkinter as tk

def close_window():  # Hàm đóng cửa sổ
    window.destroy()

def admin():
    close_window()  # Đóng cửa sổ hiện tại
    import admin

def login():
    close_window()  # Đóng cửa sổ hiện tại
    import dangky

# Tạo cửa sổ
window = tk.Tk()
window.resizable(False, False)
window.title("Trang Chủ")

# Đặt kích cỡ của cửa sổ
window.geometry("600x600")

# Tạo font với kích thước lớn
custom_font = ("Helvetica", 16)

# Thêm văn bản chọn hình thức phía trên nút Đăng nhập
label_login = tk.Label(window, text="Chọn hình thức đăng nhập", font=("Helvetica", 24, "bold"))
label_login.pack(pady=(20, 0), anchor='center')

# Tạo nút Đăng nhập
login_button = tk.Button(window, text="Admin", command=admin, font=custom_font, width=20, height=2)
login_button.pack(pady=(100, 0), anchor='center')

# Tạo nút Đăng ký
register_button = tk.Button(window, text="Khách", command=login, font=custom_font, width=20, height=2)
register_button.pack(pady=(50, 0), anchor='center')

# Khởi chạy vòng lặp chính của tkinter
window.mainloop()
