import pygame
import pygame.time
import sys
import math
import textwrap
import pygame.mixer

# Khởi tạo Pygame
pygame.init()

# Khởi tạo âm thanh Pygame
pygame.mixer.init()

# Kích thước cửa sổ
width, height = 631, 811
screen = pygame.display.set_mode((width + 455, height))

# Đổi tiêu đề của cửa sổ
pygame.display.set_caption('Cờ Thú')

# Đổi logo của cửa sổ
pygame.display.set_icon(pygame.image.load('lion.png'))

# Màu sắc
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
blue = (0, 0, 255)
gray = (128, 128, 128)
green = (0, 128, 0)
PaleGoldenrod = (238, 232, 170)

# Kích thước ô cờ
rows, cols = 9, 7
cell_size = width // cols

# Tạo danh sách để theo dõi các ô cờ đã bị ăn
canceled_squares = []

# Khai báo biến để theo dõi quân cờ được chọn và danh sách các nước đi hợp lệ
selected_quan = None
valid_moves = []

# Tạo các đối tượng âm thanh cho di chuyển và ăn quân
move_sound = pygame.mixer.Sound('move.wav')
capture_sound = pygame.mixer.Sound('capture.wav')

# Khởi tạo biến cho số lượt đi hiện tại và số lượt đi tối đa
current_moves = 0
max_moves = 1000  # Số lượt đi tối đa

# Tạo một biến để kiểm tra xem người chơi đã chọn màu hay chưa
da_chon_mau = False

# Trong hàm xử lý sự kiện MOUSEBUTTONDOWN
def handle_mouse_click(event):
    global selected_quan, valid_moves
    x, y = event.pos

    for quan in quans:
        if quan["color"] == current_player:
            if quan["x"] <= x < quan["x"] + cell_size and quan["y"] <= y < quan["y"] + cell_size:
                selected_quan = quan
                valid_moves = nuoc_di_hop_le(selected_quan)
                move_sound.play()  # Phát âm thanh khi quân cờ di chuyển
                break

# Hàm để vẽ bàn cờ 1
def ve_ban_co1():
    for i in range(rows):
        for j in range(cols):
            x = j * cell_size
            y = i * cell_size

            if (i, j) in valid_moves and (i, j) != (0, 0) and selected_quan and selected_quan["color"] == current_player:
                pygame.draw.rect(screen, blue, (x, y, cell_size, cell_size))
            elif (i, j) in valid_moves and (i, j) != (0, 0):
                pygame.draw.rect(screen, red if current_player == "do" else blue, (x, y, cell_size, cell_size))
            else:
                pygame.draw.rect(screen, black, (x, y, cell_size, cell_size), 1)

    # Vẽ đường ngang phía trên
    pygame.draw.line(screen, black, (0, 0), (7 * cell_size, 0), 2)
    # Vẽ đường ngang phía dưới
    pygame.draw.line(screen, black, (0, 9 * cell_size), (9 * cell_size, 9 * cell_size), 1)
    # Vẽ đường dọc bên trái
    pygame.draw.line(screen, black, (0, 0), (0, 7 * cell_size), 2)
    # Vẽ đường dọc bên phải
    pygame.draw.line(screen, black, (7 * cell_size, 0), (7 * cell_size, 9 * cell_size), 1)

# Hàm để vẽ bàn cờ 2
def ve_ban_co2():
    global da_chon_mau  # Sử dụng biến global để kiểm tra trạng thái chọn màu

    for i in range(rows):
        for j in range(cols):
            x = j * cell_size
            y = i * cell_size

            if da_chon_mau:  # Nếu đã chọn màu
                if (i == 1 and j in (3, 4, 5)):
                    pygame.draw.rect(screen, white, (x, y, cell_size, cell_size))  # Sử dụng màu nền để tạo ô trắng
                elif (i == 3 and j == 3):
                    pygame.draw.rect(screen, red, (x, y, cell_size, cell_size))
                elif (i == 5 and j == 3):
                    pygame.draw.rect(screen, blue, (x, y, cell_size, cell_size))
                else:
                    pygame.draw.rect(screen, white, (x, y, cell_size, cell_size))
            else:  # Nếu chưa chọn màu, vẽ bàn cờ với màu trắng
                pygame.draw.rect(screen, white, (x, y, cell_size, cell_size))

    # Vùng riêng để vẽ nền cho văn bản
    x_text = 3 * cell_size
    y_text = 0 * cell_size
    text_rect = pygame.Rect(x_text, y_text, cell_size, cell_size)
    pygame.draw.rect(screen, white, text_rect)

    font = pygame.font.Font('arial-unicode-ms.ttf', 24)
    text_surface = font.render("CHỌN MÀU QUÂN", True, black)
    text_rect = text_surface.get_rect()
    text_rect.center = text_rect.center = (x_text + cell_size / 2, y_text + cell_size / 2)
    screen.blit(text_surface, text_rect.topleft)

# Hàm để ghi văn bản vào ô cờ cụ thể và căn giữa theo chiều ngang và dọc 1
def ghi_van_ban1(x, y, text):
    font = pygame.font.Font('arial-unicode-ms.ttf', 24)  # Chỉnh lại đường dẫn tới font Unicode của bạn và kích thước font
    text_surface = font.render(text, True, black)
    text_rect = text_surface.get_rect()
    text_rect.center = (x + cell_size / 2, y + cell_size / 2)
    screen.blit(text_surface, text_rect.topleft)

# Hàm để ghi văn bản vào ô cờ cụ thể và căn giữa theo chiều ngang và dọc 2
def ghi_van_ban2(x, y, text):
    font = pygame.font.Font('arial-unicode-ms.ttf', 24)  # Chỉnh lại đường dẫn tới font Unicode của bạn và kích thước font
    lines = text.splitlines()
    y_offset = 0
    for line in lines:
        text_surface = font.render(line, True, black)
        text_rect = text_surface.get_rect()
        x_offset = (cell_size - text_rect.width) / 2
        text_rect.center = (x + x_offset + text_rect.width / 2, y + cell_size / 2 - text_surface.get_height() / 2 + y_offset)
        screen.blit(text_surface, text_rect.topleft)
        y_offset += text_surface.get_height()

# Hàm để chèn hình ảnh quân cờ vào ô cờ cụ thể
def chen_quan_co(x, y, image_path):
    image = pygame.image.load(image_path)
    image = pygame.transform.scale(image, (cell_size, cell_size))
    screen.blit(image, (x, y))

# Kiểm tra xem có quân cờ ở vị trí x, y hay không
def co_quan_co_tai_vi_tri(x, y):
    for quan in quans:
        if quan["x"] == x and quan["y"] == y:
            return quan
    return None

# Lấy khoảng cách giữa hai điểm
def khoang_cach(x1, y1, x2, y2):
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

# Kiểm tra xem ô cờ có phải là "VỰC HẲM" không
def la_o_vuc_ham(x, y):
    vuc_ham_positions_xanh = [(3 * cell_size, 0 * cell_size), (2 * cell_size, 8 * cell_size), (4 * cell_size, 8 * cell_size), (3 * cell_size, 7 * cell_size)]
    vuc_ham_positions_do = [(3 * cell_size, 8 * cell_size), (2 * cell_size, 0 * cell_size), (4 * cell_size, 0 * cell_size), (3 * cell_size, 1 * cell_size)]

    if current_player == "xanh":
        return (x, y) in vuc_ham_positions_do
    elif current_player == "do":
        return (x, y) in vuc_ham_positions_xanh

    return False

# Kiểm tra xem quân cờ có thể di chuyển đến vị trí mới không
def co_the_di_chuyen(x1, y1, x2, y2):
    if la_o_vuc_ham(x2, y2):
        return False

    # Kiểm tra nếu đích là ổ thú của đối thủ
    la_ow_cua_doi_thu = (y2 == 8 * cell_size and x2 == 3 * cell_size) if current_player == "do" else (y2 == 0 and x2 == 3 * cell_size)

    if abs(x1 - x2) == cell_size and abs(y1 - y2) == cell_size:
        return True

    if (abs(x1 - x2) == cell_size and y1 == y2) or (x1 == x2 and abs(y1 - y2) == cell_size):
        return True

    # Cho phép di chuyển vào ổ thú của đối thủ
    if la_ow_cua_doi_thu:
        return True

    return False

# Hàm để vẽ các ô cờ bị ăn với hiệu ứng màu
def hieu_ung_mau():
    for square in canceled_squares:
        x, y, frame = square
        if frame < 10:
            color = red if current_player == "xanh" else blue  # Chọn màu dựa trên màu của người chơi
            pygame.draw.rect(screen, color, (x, y, cell_size, cell_size))
            square[2] += 1
        else:
            canceled_squares.remove(square)

# Thay đổi hàm co_the_an_quan
def co_the_an_quan(x1, y1, x2, y2):
    if la_o_vuc_ham(x2, y2):
        return False

    quan1 = co_quan_co_tai_vi_tri(x1, y1)
    quan2 = co_quan_co_tai_vi_tri(x2, y2)

    if not quan1 or not quan2:
        return False

    # Kiểm tra quy tắc ăn của từng quân
    if quan1["color"] != quan2["color"]:
        if quan1["name"] == "voi" and quan2["name"] in ["sutu", "ho", "bao", "soi", "cho", "meo"]:
            canceled_squares.append([x2, y2, 0])
            capture_sound.play()
            return True
        elif quan1["name"] == "sutu" and quan2["name"] in ["ho", "bao", "soi", "cho", "meo", "chuot"]:
            canceled_squares.append([x2, y2, 0])
            capture_sound.play()
            return True
        elif quan1["name"] == "ho" and quan2["name"] in ["bao", "soi", "cho", "meo", "chuot"]:
            canceled_squares.append([x2, y2, 0])
            capture_sound.play()
            return True
        elif quan1["name"] == "bao" and quan2["name"] in ["soi", "cho", "meo", "chuot"]:
            canceled_squares.append([x2, y2, 0])
            capture_sound.play()
            return True
        elif quan1["name"] == "soi" and quan2["name"] in ["cho", "meo", "chuot"]:
            canceled_squares.append([x2, y2, 0])
            capture_sound.play()
            return True
        elif quan1["name"] == "cho" and quan2["name"] in ["meo", "chuot"]:
            canceled_squares.append([x2, y2, 0])
            capture_sound.play()
            return True
        elif quan1["name"] == "meo" and quan2["name"] == "chuot":
            canceled_squares.append([x2, y2, 0])
            capture_sound.play()
            return True
        elif quan1["name"] == "chuot" and quan2["name"] == "voi":
            canceled_squares.append([x2, y2, 0])
            capture_sound.play()
            return True

    return False

ket_qua = None

def kiem_tra_ket_qua():
    for quan in quans:
        if quan["name"] == "voi" or quan["name"] == "sutu" or quan["name"] == "ho" or quan["name"] == "bao" or quan["name"] == "soi" or quan["name"] == "cho" or quan["name"] == "meo" or quan["name"] == "chuot":
            if quan["x"] == 3 * cell_size and quan["y"] == 0 * cell_size and quan["color"] == "xanh":
                return "Xanh chiến thắng!"
            elif quan["x"] == 3 * cell_size and quan["y"] == 8 * cell_size and quan["color"] == "do":
                return "Đỏ chiến thắng!"

    if current_moves >= max_moves:
        return "Hòa!"

    return None

# Vùng riêng để vẽ luật chơi
x_luat_choi = 10  # Đặt vị trí bên phải bàn cờ cho luật chơi
y_luat_choi = 0

# Hàm để vẽ luật chơi
def ve_luat_choi():
    if not da_hien_thi_huong_dan:  # Chỉ vẽ luật chơi nếu trò chơi chưa kết thúc
        font = pygame.font.Font('arial-unicode-ms.ttf', 22)

        luat_choi = [
            'HƯỚNG DẪN CHƠI CỜ THÚ:',
            '. Mỗi quân thú chỉ được di chuyển 1 ô: ngang, dọc hoặc chéo tùy ý.',
            '. Các quân thú được phép ra vào ô "VỰC HẲM" bên phía mình nhưng không được phép đi vào ô "VỰC HẲM" của đối thủ.',
            '. CHÓ và CHUỘT được phép bơi qua "SÔNG".',
            '. Cách ăn quân: các quân thú ăn theo cấp bậc từ cao đến thấp như sau:',
            '. VOI > SƯ TỬ > HỔ > BÁO > SÓI > CHÓ > MÈO > CHUỘT',
            '* Lưu ý: CHUỘT > VOI',
            '. Khi quân thú nào từ phía 2 bên đi được vào ô "Ổ THÚ" của đối thủ trước thì xem như là giành được chiến thắng trong ván cờ đó.',
            '  ~~~~~~~~~~         *        ~~~~~~~~~~',
            '                             HẾT                          ',
            'CỜ THÚ:',
            '. Tên tiếng Anh: Animal Chess.',
            '. Xuất xứ: Trung Quốc.'
        ]

        y_text = y_luat_choi
        for line in luat_choi:
            lines = textwrap.wrap(line, 40)  # 40 là độ dài tối đa của mỗi dòng
            for text_line in lines:
                text_surface = font.render(text_line, True, (0, 0, 0))  # Màu đen
                text_rect = text_surface.get_rect()
                text_rect.topleft = (width, y_text)  # Đặt vị trí phía bên phải của bàn cờ
                screen.blit(text_surface, text_rect.topleft)
                y_text += text_rect.height

# Khởi tạo vị trí ban đầu cho các quân cờ
quans = [
    {"name": "sutu", "image_path": "sutudo.png", "x": 0 * cell_size, "y": 0 * cell_size, "color": "do"},
    {"name": "ho", "image_path": "hodo.png", "x": 6 * cell_size, "y": 0 * cell_size, "color": "do"},
    {"name": "cho", "image_path": "chodo.png", "x": 1 * cell_size, "y": 1 * cell_size, "color": "do"},
    {"name": "meo", "image_path": "meodo.png", "x": 5 * cell_size, "y": 1 * cell_size, "color": "do"},
    {"name": "chuot", "image_path": "chuotdo.png", "x": 0 * cell_size, "y": 2 * cell_size, "color": "do"},
    {"name": "bao", "image_path": "baodo.png", "x": 2 * cell_size, "y": 2 * cell_size, "color": "do"},
    {"name": "soi", "image_path": "soido.png", "x": 4 * cell_size, "y": 2 * cell_size, "color": "do"},
    {"name": "voi", "image_path": "voido.png", "x": 6 * cell_size, "y": 2 * cell_size, "color": "do"},

    {"name": "sutu", "image_path": "sutuxanh.png", "x": 6 * cell_size, "y": 8 * cell_size, "color": "xanh"},
    {"name": "ho", "image_path": "hoxanh.png", "x": 0 * cell_size, "y": 8 * cell_size, "color": "xanh"},
    {"name": "cho", "image_path": "choxanh.png", "x": 5 * cell_size, "y": 7 * cell_size, "color": "xanh"},
    {"name": "meo", "image_path": "meoxanh.png", "x": 1 * cell_size, "y": 7 * cell_size, "color": "xanh"},
    {"name": "chuot", "image_path": "chuotxanh.png", "x": 6 * cell_size, "y": 6 * cell_size, "color": "xanh"},
    {"name": "bao", "image_path": "baoxanh.png", "x": 4 * cell_size, "y": 6 * cell_size, "color": "xanh"},
    {"name": "soi", "image_path": "soixanh.png", "x": 2 * cell_size, "y": 6 * cell_size, "color": "xanh"},
    {"name": "voi", "image_path": "voixanh.png", "x": 0 * cell_size, "y": 6 * cell_size, "color": "xanh"},
]

choosing_color = True
selected_color = None

# Vòng lặp chính
while choosing_color:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            # Kiểm tra xem người chơi đã click vào ô màu đỏ hay xanh không
            if 3 * cell_size <= x < 4 * cell_size and 3 * cell_size <= y < 6 * cell_size:
                if 3 * cell_size <= y < 4 * cell_size:
                    selected_color = "do"
                    choosing_color = False
                elif 5 * cell_size <= y < 6 * cell_size:
                    selected_color = "xanh"
                    choosing_color = False

    # Vẽ bàn cờ với ô màu đỏ và xanh
    ve_ban_co2()

    # Vẽ ô màu đỏ và xanh
    pygame.draw.rect(screen, red, (3 * cell_size, 3 * cell_size, cell_size, cell_size))
    pygame.draw.rect(screen, blue, (3 * cell_size, 5 * cell_size, cell_size, cell_size))

    pygame.display.flip()

# Gán màu cờ đã chọn cho người chơi
starting_color = selected_color
current_player = starting_color

# Trước vòng lặp chính, bạn có thể đặt biến kiểm tra đã hiển thị hướng dẫn hay chưa
da_hien_thi_huong_dan = False

# Tạo biến để theo dõi trạng thái kết thúc game
game_over = False

# Vùng riêng để vẽ luật chơi và kết quả
def ve_huong_dan_va_ket_qua():
    # Xóa vùng bên phải của bàn cờ
    pygame.draw.rect(screen, white, (width, 0, 200, height))

    # Vẽ hướng dẫn
    ve_luat_choi()

    # Nếu trò chơi đã kết thúc, hiển thị kết quả
    if ket_qua:
        if current_moves >= 1000 and ket_qua == "Xanh chiến thắng!":
            font_color = blue  # Sử dụng màu xanh khi kết quả là chiến thắng của Xanh
        elif current_moves >= 1000 and ket_qua == "Đỏ chiến thắng!":
            font_color = red  # Sử dụng màu đỏ khi kết quả là chiến thắng của Đỏ
        elif current_moves >= 1000:
            font_color = black  # Sử dụng màu đen khi kết quả là Hòa
        elif ket_qua == "Xanh chiến thắng!":
            font_color = blue  # Sử dụng màu xanh mặc định
        else:
            font_color = red  # Sử dụng màu đỏ mặc định

        font = pygame.font.Font('arial-unicode-ms.ttf', 32)
        text_surface = font.render(ket_qua, True, font_color)
        text_rect = text_surface.get_rect()
        text_rect.center = (width // 2, height // 2)
        screen.blit(text_surface, text_rect.topleft)
        pygame.display.update()  # Cập nhật màn hình để hiển thị thông báo
        pygame.time.delay(20000)  # Dừng màn hình trong 20 giây (20000 miliseconds)

# Hàm để xác định tất cả các nước đi hợp lệ của quân cờ
def nuoc_di_hop_le(quan):
    x, y = quan["x"], quan["y"]
    hop_le = []

    for dx in [-cell_size, 0, cell_size]:
        for dy in [-cell_size, 0, cell_size]:
            if dx == 0 and dy == 0:
                continue  # Bỏ qua trường hợp hiện tại

            new_x, new_y = x + dx, y + dy

            quan_hien_tai = co_quan_co_tai_vi_tri(x, y)
            quan_dich = co_quan_co_tai_vi_tri(new_x, new_y)

            if quan_hien_tai and quan_dich and quan_hien_tai["color"] == quan_dich["color"]:
                continue  # Bỏ qua trường hợp quân cùng màu

            if quan_hien_tai and quan_dich and quan_hien_tai["name"] == quan_dich["name"]:
                continue  # Bỏ qua trường hợp quân cùng tên

            # Kiểm tra nếu là quân chó hoặc chuột
            if quan["name"] in ["cho", "chuot"]:
                # Cho phép ăn quân bên ngoài sông hoặc di chuyển bình thường
                if 0 <= new_x < width and 0 <= new_y < height and (
                        co_quan_co_tai_vi_tri(new_x, new_y) and not (
                                1 * cell_size <= new_x <= 2 * cell_size and 3 * cell_size <= new_y <= 5 * cell_size or 4 * cell_size <= new_x <= 5 * cell_size and 3 * cell_size <= new_y <= 5 * cell_size)):
                    hop_le.append((new_x, new_y))
                # Cho phép di chuyển bình thường nếu không nằm trong sông và quân đối phương nhỏ hơn
                elif co_the_di_chuyen(x, y, new_x, new_y) and not co_quan_co_tai_vi_tri(new_x, new_y):
                    hop_le.append((new_x, new_y))
            else:
                # Kiểm tra xem các quân khác có thể di chuyển không (không nằm trong vùng sông) và quân đối phương nhỏ hơn
                if co_the_di_chuyen(x, y, new_x, new_y) and not (
                        1 * cell_size <= new_x <= 2 * cell_size and 3 * cell_size <= new_y <= 5 * cell_size or 4 * cell_size <= new_x <= 5 * cell_size and 3 * cell_size <= new_y <= 5 * cell_size):
                    hop_le.append((new_x, new_y))

            # Kiểm tra nếu là quân chó hoặc chuột
            if quan["name"] in ["cho", "chuot"]:
                # Cho phép ăn quân bên ngoài sông hoặc di chuyển bình thường
                if 0 <= new_x < width and 0 <= new_y < height:
                    # Kiểm tra nếu quân đối phương là chuột và đang trên sông hoặc bờ sông, cho phép chó ăn chuột
                    if co_quan_co_tai_vi_tri(new_x, new_y):
                        quan_dich = co_quan_co_tai_vi_tri(new_x, new_y)
                        if quan["name"] == "cho" and quan_dich["name"] == "chuot" and (
                                1 * cell_size <= new_x <= 2 * cell_size and 3 * cell_size <= new_y <= 5 * cell_size or
                                4 * cell_size <= new_x <= 5 * cell_size and 3 * cell_size <= new_y <= 5 * cell_size):
                            hop_le.append((new_x, new_y))
                        elif quan["name"] == "chuot" and quan_dich["name"] == "cho" and (
                                1 * cell_size <= new_x <= 2 * cell_size and 3 * cell_size <= new_y <= 5 * cell_size or
                                4 * cell_size <= new_x <= 5 * cell_size and 3 * cell_size <= new_y <= 5 * cell_size):
                            hop_le.append((new_x, new_y))
                    # Cho phép di chuyển bình thường nếu không nằm trong sông và quân đối phương nhỏ hơn
                    elif co_the_di_chuyen(x, y, new_x, new_y) and not co_quan_co_tai_vi_tri(new_x, new_y):
                        hop_le.append((new_x, new_y))
                # Cho phép quân chuột di chuyển xuống dưới nước và chó ăn chuột
                elif quan["name"] == "chuot" and (
                        1 * cell_size <= new_x <= 2 * cell_size and 3 * cell_size <= new_y <= 5 * cell_size or
                        4 * cell_size <= new_x <= 5 * cell_size and 3 * cell_size <= new_y <= 5 * cell_size):
                    hop_le.append((new_x, new_y))
            else:
                # Kiểm tra xem các quân khác có thể di chuyển không (không nằm trong vùng sông) và quân đối phương nhỏ hơn
                if co_the_di_chuyen(x, y, new_x, new_y) and not (
                        1 * cell_size <= new_x <= 2 * cell_size and 3 * cell_size <= new_y <= 5 * cell_size or 4 * cell_size <= new_x <= 5 * cell_size and 3 * cell_size <= new_y <= 5 * cell_size):
                    hop_le.append((new_x, new_y))

    return hop_le

def to_mau_nuoc_di(x, y, color):
    pygame.draw.rect(screen, color, (x, y, cell_size, cell_size))

# Vòng lặp chính
running = True
selected_quan = None
offset_x, offset_y = 0, 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            handle_mouse_click(event)
            if current_player:
                if selected_quan is None:
                    x, y = event.pos
                    for quan in quans:
                        if quan["color"] == current_player:
                            if quan["x"] <= x < quan["x"] + cell_size and quan["y"] <= y < quan["y"] + cell_size:
                                selected_quan = quan
                                offset_x = x - quan["x"]
                                offset_y = y - quan["y"]
                                valid_moves = nuoc_di_hop_le(selected_quan)  # Cập nhật danh sách các nước đi hợp lệ

        elif event.type == pygame.MOUSEBUTTONUP:
            if selected_quan and current_player:
                x, y = event.pos
                new_x = (x // cell_size) * cell_size
                new_y = (y // cell_size) * cell_size
                # Kiểm tra vị trí mới của quân cờ
                if 0 <= new_x < width and 0 <= new_y < height and (new_x, new_y) in valid_moves:
                    if co_the_di_chuyen(selected_quan["x"], selected_quan["y"], new_x, new_y):
                        target_quan = co_quan_co_tai_vi_tri(new_x, new_y)
                        if not target_quan:
                            selected_quan["x"] = new_x
                            selected_quan["y"] = new_y
                            current_moves += 1  # Tăng biến đếm số lượt đi
                            current_player = "xanh" if current_player == "do" else "do"
                        elif co_the_an_quan(selected_quan["x"], selected_quan["y"], new_x, new_y):
                            quans.remove(target_quan)
                            selected_quan["x"] = new_x
                            selected_quan["y"] = new_y
                            current_moves += 1  # Tăng biến đếm số lượt đi
                            current_player = "xanh" if current_player == "do" else "do"
                selected_quan = None

                # Kiểm tra điều kiện kết thúc trò chơi
                ket_qua = kiem_tra_ket_qua()
                if ket_qua:
                    game_over = True

    # Xóa màn hình
    screen.fill((255, 255, 255))

    # Vẽ bàn cờ
    ve_ban_co1()

    # Ghi văn bản vào ô cờ cụ thể
    ghi_van_ban2(3 * cell_size, 0 * cell_size, "Ổ\nTHÚ")
    ghi_van_ban2(0 * cell_size, 0 * cell_size, "SƯ\nTỬ")
    ghi_van_ban1(6 * cell_size, 0 * cell_size, "HỔ")
    ghi_van_ban1(1 * cell_size, 1 * cell_size, "CHÓ")
    ghi_van_ban1(5 * cell_size, 1 * cell_size, "MÈO")
    ghi_van_ban1(0 * cell_size, 2 * cell_size, "CHUỘT")
    ghi_van_ban1(2 * cell_size, 2 * cell_size, "BÁO")
    ghi_van_ban1(4 * cell_size, 2 * cell_size, "SÓI")
    ghi_van_ban1(6 * cell_size, 2 * cell_size, "VOI")
    ghi_van_ban2(2 * cell_size, 0 * cell_size, "VỰC\nHẲM")
    ghi_van_ban2(4 * cell_size, 0 * cell_size, "VỰC\nHẲM")
    ghi_van_ban2(3 * cell_size, 1 * cell_size, "VỰC\nHẲM")

    ghi_van_ban2(3 * cell_size, 8 * cell_size, "Ổ\nTHÚ")
    ghi_van_ban2(6 * cell_size, 8 * cell_size, "SƯ\nTỬ")
    ghi_van_ban1(0 * cell_size, 8 * cell_size, "HỔ")
    ghi_van_ban1(5 * cell_size, 7 * cell_size, "CHÓ")
    ghi_van_ban1(1 * cell_size, 7 * cell_size, "MÈO")
    ghi_van_ban1(6 * cell_size, 6 * cell_size, "CHUỘT")
    ghi_van_ban1(4 * cell_size, 6 * cell_size, "BÁO")
    ghi_van_ban1(2 * cell_size, 6 * cell_size, "SÓI")
    ghi_van_ban1(0 * cell_size, 6 * cell_size, "VOI")
    ghi_van_ban2(2 * cell_size, 8 * cell_size, "VỰC\nHẲM")
    ghi_van_ban2(4 * cell_size, 8 * cell_size, "VỰC\nHẲM")
    ghi_van_ban2(3 * cell_size, 7 * cell_size, "VỰC\nHẲM")

    ghi_van_ban1(1 * cell_size, 3 * cell_size, "SÔNG")
    ghi_van_ban1(2 * cell_size, 3 * cell_size, "SÔNG")
    ghi_van_ban1(1 * cell_size, 4 * cell_size, "SÔNG")
    ghi_van_ban1(2 * cell_size, 4 * cell_size, "SÔNG")
    ghi_van_ban1(1 * cell_size, 5 * cell_size, "SÔNG")
    ghi_van_ban1(2 * cell_size, 5 * cell_size, "SÔNG")
    ghi_van_ban2(4 * cell_size, 3 * cell_size, "SÔNG")
    ghi_van_ban2(5 * cell_size, 3 * cell_size, "SÔNG")
    ghi_van_ban2(4 * cell_size, 4 * cell_size, "SÔNG")
    ghi_van_ban2(5 * cell_size, 4 * cell_size, "SÔNG")
    ghi_van_ban2(4 * cell_size, 5 * cell_size, "SÔNG")
    ghi_van_ban2(5 * cell_size, 5 * cell_size, "SÔNG")

    # Chèn hình ảnh quân cờ vào ô cờ
    for quan in quans:
        chen_quan_co(quan["x"], quan["y"], quan["image_path"])

    # Vẽ các nước đi hợp lệ của quân cờ hiện tại
    if selected_quan and current_player:
        for nuoc_di in nuoc_di_hop_le(selected_quan):
            x, y = nuoc_di[0], nuoc_di[1]
            quan_hien_tai = co_quan_co_tai_vi_tri(selected_quan["x"], selected_quan["y"])
            quan_dich = co_quan_co_tai_vi_tri(x, y)

            move_color = gray

            is_an_quan = False

            # Kiểm tra xem có phải nước đi là ăn quân hay không
            if quan_hien_tai and quan_dich:
                if quan_hien_tai["color"] != quan_dich["color"] or quan_hien_tai["name"] < quan_dich["name"]:
                    is_an_quan = True

            # Tô màu vàng cho nước đi là ăn quân của cả hai bên
            if is_an_quan:
                move_color = red if current_player == "do" else blue  # Tô màu viền cho các nước đi ăn quân
            else:
                to_mau_nuoc_di(x, y, PaleGoldenrod)  # Tô màu xám cho các nước đi không ăn quân

            pygame.draw.rect(screen, move_color, (x, y, cell_size, cell_size), 2)

    # Hiển thị hướng dẫn và kết quả
    ve_huong_dan_va_ket_qua()

    # Vùng trắng bên phải bàn cờ
    pygame.draw.rect(screen, white, (width, 0, 200, height))

    # Vẽ luật chơi
    ve_luat_choi()

    # Vẽ các ô cờ bị ăn với hiệu ứng nhấp nháy màu
    hieu_ung_mau()

    # Cập nhật màn hình
    pygame.display.flip()

    if game_over:
        pygame.quit()
        sys.exit()

# Kết thúc Pygame
pygame.quit()
sys.exit()
