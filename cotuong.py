import pygame
import sys

# Khởi tạo Pygame
pygame.init()

# Kích thước cửa sổ
width, height = 800, 800
rows, columns = 10, 9
cell_size = min(width // columns, height // rows)  # Chọn kích thước ô sao cho chúng vừa với cửa sổ
cell_size = min(cell_size, height // rows)  # Chọn kích thước ô sao cho chúng cân xứng theo chiều cao

# Đổi logo của cửa sổ
pygame.display.set_icon(pygame.image.load('tuong_r.png'))

# Đổi tiêu đề của cửa sổ
pygame.display.set_caption('Cờ Tướng')

# Giảm kích thước của các ô cờ
cell_size = min(cell_size, 70)  # Đặt giá trị 50 làm kích thước tối thiểu

screen = pygame.display.set_mode((width, height))

# Tính toán offset để bàn cờ nằm ở giữa
offset_x = (width - columns * cell_size) // 2 + 35
offset_y = (height - rows * cell_size) // 2 + 35

# Đảm bảo bàn cờ không vượt quá kích thước cửa sổ
offset_x = max(offset_x, 0)
offset_y = max(offset_y, 0)

# Kích thước của đường ngăn cách giữa các ô cờ
border_size = 4

# Danh sách các quân cờ và vị trí tương ứng trên bàn cờ, bao gồm màu của quân cờ
pieces = [
    ("xe_b.png", (0, 0)), ("ma_b.png", (1, 0)), ("tinh_b.png", (2, 0)), ("sy_b.png", (3, 0)), ("tuong_b.png", (4, 0)),
    ("xe_b.png", (8, 0)), ("ma_b.png", (7, 0)), ("tinh_b.png", (6, 0)), ("sy_b.png", (5, 0)),
    ("phao_b.png", (1, 2)), ("phao_b.png", (7, 2)),
    ("tot_b.png", (0, 3)), ("tot_b.png", (2, 3)), ("tot_b.png", (4, 3)), ("tot_b.png", (6, 3)), ("tot_b.png", (8, 3)),
    ("xe_r.png", (0, 9)), ("ma_r.png", (1, 9)), ("tinh_r.png", (2, 9)), ("sy_r.png", (3, 9)), ("tuong_r.png", (4, 9)),
    ("xe_r.png", (8, 9)), ("ma_r.png", (7, 9)), ("tinh_r.png", (6, 9)), ("sy_r.png", (5, 9)),
    ("phao_r.png", (1, 7)), ("phao_r.png", (7, 7)),
    ("tot_r.png", (0, 6)), ("tot_r.png", (2, 6)), ("tot_r.png", (4, 6)), ("tot_r.png", (6, 6)), ("tot_r.png", (8, 6)),
]

# Biến để lưu trữ vị trí của quân cờ được chọn
selected_piece = None
captured_piece = None

# Biến để lưu trữ thông tin của quân cờ được chọn
selected_info = None

# Lưu trạng thái của bàn cờ để hỗ trợ undo
board_states = []

# Vòng lặp chính
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            # Chuyển đổi tọa độ chuột sang tọa độ ô cờ trong bàn cờ
            selected_col = (mouse_x - offset_x) // cell_size
            selected_row = (mouse_y - offset_y) // cell_size
            # Kiểm tra xem có phải là một ô cờ hợp lệ hay không
            if 0 <= selected_col < columns and 0 <= selected_row < rows:
                selected_piece = (selected_col, selected_row)
                # Kiểm tra xem quân cờ ở vị trí chọn có phải là quân cờ đang bị ăn không
                for piece, position in pieces:
                    if position == selected_piece:
                        selected_info = {"image": piece, "position": position}
                        captured_piece = (piece, position)
                        break
            # Lưu trạng thái của bàn cờ trước khi thực hiện nước đi mới
            board_states.append(list(pieces))
        elif event.type == pygame.MOUSEBUTTONUP:
            if selected_piece and captured_piece:
                mouse_x, mouse_y = event.pos
                target_col = (mouse_x - offset_x) // cell_size
                target_row = (mouse_y - offset_y) // cell_size
                if 0 <= target_col < columns and 0 <= target_row < rows:
                    target_position = (target_col, target_row)
                    for piece, position in pieces:
                        if position == target_position:
                            pieces.remove((piece, position))
                            break
                    if captured_piece in pieces:
                        pieces.remove(captured_piece)
                        captured_piece_last_move = captured_piece
                    pieces.append((captured_piece[0], target_position))
                selected_piece = None
                captured_piece = None
                selected_info = None  # Reset selected_info khi quân cờ được di chuyển
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_z:  # Phím "z" để undo
                if board_states:
                    pieces = list(board_states.pop())
                    selected_piece = None
                    captured_piece = None
                    selected_info = None  # Reset selected_info khi undo

    # Xóa màn hình
    screen.fill((192, 192, 192))

    # Tô màu nền xám cho bàn cờ
    pygame.draw.rect(screen, (255, 255, 255), (offset_x, offset_y, 8 * cell_size, 9 * cell_size))

    # Vẽ đường phía trên
    pygame.draw.rect(screen, (0, 0, 0),
                     (offset_x - border_size, offset_y - border_size, 8 * cell_size + 2 * border_size, border_size))

    # Vẽ đường bên trái
    pygame.draw.rect(screen, (0, 0, 0), (offset_x - border_size, offset_y - border_size, border_size, 9 * cell_size + 2 * border_size))

    # Vẽ đường phía dưới (lớn hơn cho hàng 3)
    pygame.draw.rect(screen, (0, 0, 0), (
        offset_x - border_size, offset_y + 4 * cell_size, 8 * cell_size + 2 * border_size, 1))

    # Vẽ đường phía trên (lớn hơn cho hàng 5)
    pygame.draw.rect(screen, (0, 0, 0), (
        offset_x - border_size, offset_y + 5 * cell_size, 8 * cell_size + 2 * border_size, 2))

    # Vẽ đường bên trái cho hàng 4
    pygame.draw.rect(screen, (0, 0, 0),
                     (offset_x - border_size, offset_y + 4 * cell_size, 5, cell_size + border_size))

    # Vẽ đường bên phải cho cột thứ 7 (tô đậm sang bên trái)
    pygame.draw.rect(screen, (0, 0, 0),
                     (offset_x + 8 * cell_size - 1, offset_y, 5, 9 * cell_size + border_size))

    # Vẽ đường phía dưới (lớn hơn cho hàng 8)
    pygame.draw.rect(screen, (0, 0, 0), (
        offset_x - border_size, offset_y + 9 * cell_size, 8 * cell_size + 2 * border_size, border_size))

    # Danh sách các giao điểm cần vẽ dấu chấm đậm
    dot_positions = [(1, 2), (7, 2), (2, 3), (4, 3), (6, 3), (2, 6), (4, 6), (6, 6), (1, 7), (7, 7)]

    # Vẽ dấu chấm đậm tại các giao điểm
    for dot_col, dot_row in dot_positions:
        dot_x = dot_col * cell_size + offset_x
        dot_y = dot_row * cell_size + offset_y
        pygame.draw.circle(screen, (0, 0, 0), (dot_x, dot_y), 5)  # 5 là bán kính của dấu chấm

    # Vẽ bàn cờ và đường ngăn cách
    for row in range(rows - 1):
        for col in range(columns - 1):  # Loại bỏ cột cuối cùng
            # Kiểm tra điều kiện để vẽ các đường ngăn cách
            if row != 4:
                pygame.draw.rect(screen, (0, 0, 0),
                                 (col * cell_size + offset_x, row * cell_size + offset_y, cell_size, cell_size), 1)

    # Xác định danh sách ô cần vẽ đường chéo
    selected_cells = [(0, 4), (1, 3), (8, 3), (7, 4)]

    # Vẽ đường chéo cho mỗi ô trong danh sách
    for selected_row, selected_col in selected_cells:
        # Tính toán tọa độ của ô trong hệ tọa độ của cửa sổ
        cell_x = selected_col * cell_size + offset_x
        cell_y = selected_row * cell_size + offset_y

        # Tính toán tọa độ của góc trên cùng bên phải của ô
        corner_top_right = (cell_x + cell_size, cell_y)

        # Tính toán tọa độ của góc dưới cùng bên trái của ô
        corner_bottom_left = (cell_x, cell_y + cell_size)

        # Vẽ đường chéo
        pygame.draw.line(screen, (0, 0, 0), corner_top_right, corner_bottom_left, 3)

    # Xác định danh sách ô cần vẽ đường chéo dấu huyền
    selected_cells = [(0, 3), (1, 4), (7, 3), (8, 4)]

    # Vẽ đường chéo dấu huyền cho mỗi ô trong danh sách
    for selected_row, selected_col in selected_cells:
        # Tính toán tọa độ của ô trong hệ tọa độ của cửa sổ
        cell_x = selected_col * cell_size + offset_x
        cell_y = selected_row * cell_size + offset_y

        # Tính toán tọa độ của góc trên cùng bên trái của ô
        corner_top_left = (cell_x, cell_y)

        # Tính toán tọa độ của góc dưới cùng bên phải của ô
        corner_bottom_right = (cell_x + cell_size, cell_y + cell_size)

        # Vẽ đường chéo dấu huyền
        pygame.draw.line(screen, (0, 0, 0), corner_top_left, corner_bottom_right, 3)

    # Vẽ quân cờ lên bàn cờ và xử lý vị trí khi di chuyển
    for piece, position in pieces:
        piece_image = pygame.image.load(piece)
        piece_image = pygame.transform.scale(piece_image, (cell_size, cell_size))
        piece_rect = piece_image.get_rect()
        piece_rect.center = (
            (position[0]) * cell_size + offset_x,
            (position[1]) * cell_size + offset_y
        )
        screen.blit(piece_image, piece_rect)

        # Kiểm tra xem quân cờ có được chọn không và vẽ hình vuông xung quanh
        if selected_piece == (position[0], position[1]):
            pygame.draw.rect(screen, (0, 128, 0), (piece_rect.left, piece_rect.top, cell_size, cell_size), 3)

    # Nếu có quân cờ được chọn, vẽ ảnh của nó khi di chuyển
    if selected_info:
        selected_image = pygame.image.load(selected_info["image"])
        selected_image = pygame.transform.scale(selected_image, (cell_size, cell_size))
        selected_rect = selected_image.get_rect()
        selected_rect.center = pygame.mouse.get_pos()
        screen.blit(selected_image, selected_rect)

    # Cập nhật màn hình
    pygame.display.flip()

# Kết thúc Pygame
pygame.quit()
sys.exit()
