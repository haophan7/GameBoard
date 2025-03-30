import pygame
import sys
import time

# Khai báo các hằng số
WIDTH, HEIGHT = 600, 640
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH // COLS

# Màu sắc
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 128, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)

# Khởi tạo bảng
board = [[0] * COLS for _ in range(ROWS)]
board[3][3] = board[4][4] = 1  # Quân cờ trắng
board[3][4] = board[4][3] = -1  # Quân cờ đen

# Khởi tạo Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cờ Lật")
pygame.display.set_icon(pygame.image.load('colat.png'))

# Hàm vẽ bảng
def draw_board():
    for row in range(ROWS):
        for col in range(COLS):
            pygame.draw.rect(
                screen,
                GREEN if (row + col) % 2 == 0 else GREEN,
                (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE),
            )

            # Vẽ đường ngang và dọc
            pygame.draw.line(screen, BLACK, (col * SQUARE_SIZE, row * SQUARE_SIZE),
                             ((col + 1) * SQUARE_SIZE, row * SQUARE_SIZE))
            pygame.draw.line(screen, BLACK, (col * SQUARE_SIZE, row * SQUARE_SIZE),
                             (col * SQUARE_SIZE, (row + 1) * SQUARE_SIZE))

            # Vẽ đường ngang và dọc (cuối cửa sổ)
            if col == COLS - 1:
                pygame.draw.line(
                    screen, BLACK, ((col + 1) * SQUARE_SIZE, row * SQUARE_SIZE),
                    ((col + 1) * SQUARE_SIZE, (row + 1) * SQUARE_SIZE)
                )
            if row == ROWS - 1:
                pygame.draw.line(
                    screen, BLACK, (col * SQUARE_SIZE, (row + 1) * SQUARE_SIZE),
                    ((col + 1) * SQUARE_SIZE, (row + 1) * SQUARE_SIZE)
                )

            if board[row][col] == 1:
                pygame.draw.circle(
                    screen,
                    WHITE,
                    (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2),
                    SQUARE_SIZE // 2 - 5,
                )
            elif board[row][col] == -1:
                pygame.draw.circle(
                    screen,
                    BLACK,
                    (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2),
                    SQUARE_SIZE // 2 - 5,
                )

    # Tô màu nền xanh lá cây cho phần bên dưới bàn cờ và giảm xuống 10 đơn vị
    pygame.draw.rect(screen, GREEN, (0, ROWS * SQUARE_SIZE + 1, WIDTH, HEIGHT - ROWS * SQUARE_SIZE - 2))

    # Vẽ đường dọc bên trái cửa sổ (ngoài cùng)
    pygame.draw.line(screen, BLACK, (0, 0), (0, HEIGHT))

    # Vẽ đường dọc bên phải cửa sổ (ngoài cùng)
    pygame.draw.line(screen, BLACK, (WIDTH - 1, 0), (WIDTH - 1, HEIGHT))

# Hàm kiểm tra nước đi hợp lệ
def is_valid_move(row, col, player):
    if 0 <= row < ROWS and 0 <= col < COLS and board[row][col] == 0:
        for dr in range(-1, 2):
            for dc in range(-1, 2):
                if dr == 0 and dc == 0:
                    continue
                r, c = row + dr, col + dc
                while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == -player:
                    r, c = r + dr, c + dc
                    if 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == player:
                        return True
    return False

# Hàm đảo quân cờ khi thực hiện nước đi
def flip_tiles(row, col, player):
    for dr in range(-1, 2):
        for dc in range(-1, 2):
            if dr == 0 and dc == 0:
                continue
            r, c = row + dr, col + dc
            to_flip = []
            while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == -player:
                to_flip.append((r, c))
                r, c = r + dr, c + dc
                if 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == player:
                    for flip_row, flip_col in to_flip:
                        board[flip_row][flip_col] = player

# Hàm kiểm tra kết thúc trò chơi
def is_game_over():
    return all(all(cell != 0 for cell in row) for row in board)

# Hàm đếm số quân cờ của mỗi người chơi
def count_pieces():
    count_white = sum(row.count(1) for row in board)
    count_black = sum(row.count(-1) for row in board)
    return count_white, count_black

# Hàm vẽ số quân cờ của mỗi người chơi
def draw_score(count_white, count_black):
    font = pygame.font.Font(None, 36)
    text_white = font.render(f"White: {count_white}", True, YELLOW)
    text_black = font.render(f"Black: {count_black}", True, RED)
    screen.blit(text_white, (10, HEIGHT - 60))
    screen.blit(text_black, (10, HEIGHT - 30))

# Hàm kiểm tra có nước đi hợp lệ cho người chơi không
def has_valid_move(player):
    for row in range(ROWS):
        for col in range(COLS):
            if is_valid_move(row, col, player):
                return True
    return False

# Hàm vẽ số quân cờ của mỗi người chơi và lượt chơi
def draw_score_and_turn(count_white, count_black, player):
    font = pygame.font.Font(None, 36)
    text_white = font.render(f"White: {count_white}", True, YELLOW)
    text_black = font.render(f"Black: {count_black}", True, RED)
    screen.blit(text_white, (25, HEIGHT - 30))
    screen.blit(text_black, (255, HEIGHT - 30))

    # Hiển thị lượt chơi
    turn_text = font.render("Turn: White" if player == 1 else "Turn: Black", True, BLUE)
    screen.blit(turn_text, (WIDTH - 145, HEIGHT - 30))

# Hàm main
def main():
    player = 1  # 1: Quân cờ trắng, -1: Quân cờ đen
    game_over = False
    countdown_timer = 20  # Đếm ngược 20 giây trước khi đóng cửa sổ
    no_valid_moves_for_both = False  # Biến để kiểm tra khi không còn nước đi hợp lệ cho cả hai bên

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if not game_over and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouseX, mouseY = event.pos
                clicked_row, clicked_col = mouseY // SQUARE_SIZE, mouseX // SQUARE_SIZE

                if is_valid_move(clicked_row, clicked_col, player):
                    board[clicked_row][clicked_col] = player
                    flip_tiles(clicked_row, clicked_col, player)
                    player *= -1  # Đổi lượt người chơi

                    # Reset biến no_valid_moves_for_both nếu có nước đi hợp lệ cho bất kỳ người chơi nào
                    no_valid_moves_for_both = False

        screen.fill(BLACK)
        draw_board()
        count_white, count_black = count_pieces()
        draw_score_and_turn(count_white, count_black, player)

        # Kiểm tra kết thúc khi không còn nước đi hợp lệ cho cả hai người chơi
        if not game_over and no_valid_moves_for_both:
            game_over = True
            winner = "White" if count_white > count_black else "Black" if count_black > count_white else "Tie"
            font = pygame.font.Font('arial-unicode-ms.ttf', 24)

            if winner == "White":
                text_winner = font.render(f"Trắng Chiến Thắng!", True, YELLOW)
            elif winner == "Black":
                text_winner = font.render(f"Đen Chiến Thắng!", True, RED)
            else:
                text_winner = font.render(f"Hòa!", True, CYAN)

            screen.blit(text_winner, (WIDTH // 2 - 100, HEIGHT // 2 - 25))
            pygame.display.flip()
            time.sleep(20)  # Hiển thị thông báo trong 20 giây
            countdown_timer = 20  # Reset đếm ngược

        if not game_over:
            # Kiểm tra xem có nước đi hợp lệ cho người chơi hiện tại không
            if not has_valid_move(player):
                player *= -1  # Đổi lượt người chơi

                # Kiểm tra xem có nước đi hợp lệ cho người chơi mới không
                if not has_valid_move(player):
                    game_over = True
                    winner = "White" if count_white > count_black else "Black" if count_black > count_white else "Tie"
                    font = pygame.font.Font('arial-unicode-ms.ttf', 24)

                    if winner == "White":
                        text_winner = font.render(f"Trắng Chiến Thắng!", True, YELLOW)
                    elif winner == "Black":
                        text_winner = font.render(f"Đen Chiến Thắng!", True, RED)
                    else:
                        text_winner = font.render(f"    Hòa!        ", True, CYAN)

                    screen.blit(text_winner, (WIDTH // 2 - 100, HEIGHT // 2 - 25))
                    pygame.display.flip()
                    time.sleep(20)  # Hiển thị thông báo trong 20 giây
                    countdown_timer = 20  # Reset đếm ngược

        if game_over:
            countdown_timer -= 1
            if countdown_timer <= 0:
                pygame.quit()
                sys.exit()

        pygame.display.flip()
        pygame.time.Clock().tick(60)  # Đặt tốc độ vòng lặp

if __name__ == "__main__":
    main()
