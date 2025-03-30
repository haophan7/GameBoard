import pygame
import sys

# Khai báo các hằng số
WIDTH, HEIGHT = 761, 761
BOARD_SIZE = 19
CELL_SIZE = WIDTH // BOARD_SIZE

# Khai báo màu sắc
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
PINK = (255, 0, 255)
MAROON = (128, 0, 0)

# Khởi tạo mảng chứa trạng thái của bàn cờ
board = [[0] * BOARD_SIZE for _ in range(BOARD_SIZE)]

# Khởi tạo Pygame
pygame.init()

# Tạo cửa sổ game
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cờ Caro")
pygame.display.set_icon(pygame.image.load('caro.png'))

# Khởi tạo biến lưu nước đi mới nhất
last_move = None

def draw_board():
    for i in range(1, BOARD_SIZE):
        # Vẽ các đường dọc
        pygame.draw.line(screen, BLACK, (i * CELL_SIZE, 0), (i * CELL_SIZE, HEIGHT), 1)
        # Vẽ các đường ngang
        pygame.draw.line(screen, BLACK, (0, i * CELL_SIZE), (WIDTH, i * CELL_SIZE), 1)

    # Vẽ đường ngang phía trên
    pygame.draw.line(screen, BLACK, (0, 0), (WIDTH, 0), 1)
    # Vẽ đường ngang phía dưới
    pygame.draw.line(screen, BLACK, (0, HEIGHT - 1), (WIDTH, HEIGHT - 1), 1)
    # Vẽ đường dọc bên trái
    pygame.draw.line(screen, BLACK, (0, 0), (0, HEIGHT), 1)
    # Vẽ đường dọc bên phải
    pygame.draw.line(screen, BLACK, (WIDTH - 1, 0), (WIDTH - 1, HEIGHT), 1)

def draw_pieces():
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if board[row][col] == 1:
                pygame.draw.line(screen, RED, (col * CELL_SIZE + CELL_SIZE // 4, row * CELL_SIZE + CELL_SIZE // 4),
                                 (col * CELL_SIZE + 3 * CELL_SIZE // 4, row * CELL_SIZE + 3 * CELL_SIZE // 4), 5)
                pygame.draw.line(screen, RED, (col * CELL_SIZE + CELL_SIZE // 4, row * CELL_SIZE + 3 * CELL_SIZE // 4),
                                 (col * CELL_SIZE + 3 * CELL_SIZE // 4, row * CELL_SIZE + CELL_SIZE // 4), 5)
            elif board[row][col] == 2:
                pygame.draw.circle(screen, GREEN, (col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 3, 3)

    # Tô màu ô vuông của nước đi hiện tại cho cả hai người chơi
    if last_move is not None:
        x, y = last_move
        pygame.draw.rect(screen, YELLOW, (x * CELL_SIZE + 1, y * CELL_SIZE + 1, CELL_SIZE - 1, CELL_SIZE - 1))
        if board[y][x] == 1:
            pygame.draw.line(screen, RED, (x * CELL_SIZE + CELL_SIZE // 4, y * CELL_SIZE + CELL_SIZE // 4),
                             (x * CELL_SIZE + 3 * CELL_SIZE // 4, y * CELL_SIZE + 3 * CELL_SIZE // 4), 5)
            pygame.draw.line(screen, RED, (x * CELL_SIZE + CELL_SIZE // 4, y * CELL_SIZE + 3 * CELL_SIZE // 4),
                             (x * CELL_SIZE + 3 * CELL_SIZE // 4, y * CELL_SIZE + CELL_SIZE // 4), 5)
        elif board[y][x] == 2:
            pygame.draw.circle(screen, GREEN, (x * CELL_SIZE + CELL_SIZE // 2, y * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 3, 3)

    # Tô màu vàng cho 5 quân cờ chiến thắng
    if last_move is not None:
        player = board[last_move[1]][last_move[0]]
        for direction in [(1, 0), (0, 1), (1, 1), (1, -1)]:
            count = 1
            winning_moves = []
            for i in range(1, 5):
                x, y = last_move[0] + direction[0] * i, last_move[1] + direction[1] * i
                if 0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE and board[y][x] == player:
                    count += 1
                    winning_moves.append((x, y))
                else:
                    break
            for i in range(1, 5):
                x, y = last_move[0] - direction[0] * i, last_move[1] - direction[1] * i
                if 0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE and board[y][x] == player:
                    count += 1
                    winning_moves.append((x, y))
                else:
                    break
            if count >= 5:
                # Tô màu vàng cho 5 quân cờ chiến thắng
                for i in range(5):
                    if i < len(winning_moves):
                        x, y = winning_moves[i]
                        pygame.draw.rect(screen, YELLOW,
                                (x * CELL_SIZE + 1, y * CELL_SIZE + 1, CELL_SIZE - 1, CELL_SIZE - 1))
                        if player == 1:
                            pygame.draw.line(screen, RED,
                                (x * CELL_SIZE + CELL_SIZE // 4, y * CELL_SIZE + CELL_SIZE // 4),
                                (x * CELL_SIZE + 3 * CELL_SIZE // 4,
                                y * CELL_SIZE + 3 * CELL_SIZE // 4), 5)
                            pygame.draw.line(screen, RED,
                                (x * CELL_SIZE + CELL_SIZE // 4, y * CELL_SIZE + 3 * CELL_SIZE // 4),
                                (x * CELL_SIZE + 3 * CELL_SIZE // 4, y * CELL_SIZE + CELL_SIZE // 4),
                                5)
                        elif player == 2:
                            pygame.draw.circle(screen, GREEN,
                                (x * CELL_SIZE + CELL_SIZE // 2, y * CELL_SIZE + CELL_SIZE // 2),
                                CELL_SIZE // 3, 3)

def check_win(player, row, col):
    # Kiểm tra hàng ngang
    count = 1
    for i in range(1, 5):
        if col + i < BOARD_SIZE and board[row][col + i] == player:
            count += 1
        else:
            break
    for i in range(1, 5):
        if col - i >= 0 and board[row][col - i] == player:
            count += 1
        else:
            break
    if count >= 5:
        return True

    # Kiểm tra hàng dọc
    count = 1
    for i in range(1, 5):
        if row + i < BOARD_SIZE and board[row + i][col] == player:
            count += 1
        else:
            break
    for i in range(1, 5):
        if row - i >= 0 and board[row - i][col] == player:
            count += 1
        else:
            break
    if count >= 5:
        return True

    # Kiểm tra đường chéo chính
    count = 1
    for i in range(1, 5):
        if row + i < BOARD_SIZE and col + i < BOARD_SIZE and board[row + i][col + i] == player:
            count += 1
        else:
            break
    for i in range(1, 5):
        if row - i >= 0 and col - i >= 0 and board[row - i][col - i] == player:
            count += 1
        else:
            break
    if count >= 5:
        return True

    # Kiểm tra đường chéo phụ
    count = 1
    for i in range(1, 5):
        if row + i < BOARD_SIZE and col - i >= 0 and board[row + i][col - i] == player:
            count += 1
        else:
            break
    for i in range(1, 5):
        if row - i >= 0 and col + i < BOARD_SIZE and board[row - i][col + i] == player:
            count += 1
        else:
            break
    if count >= 5:
        return True

    return False

def check_draw():
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if board[row][col] == 0:
                return False
    return True

def main():
    global last_move  # Sử dụng biến toàn cục để theo dõi nước đi mới nhất
    player_turn = 1
    game_over = False
    winner = None

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not game_over:
                col = event.pos[0] // CELL_SIZE
                row = event.pos[1] // CELL_SIZE

                if 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE and board[row][col] == 0:
                    board[row][col] = player_turn

                    last_move = (col, row)  # Cập nhật nước đi mới nhất

                    if check_win(player_turn, row, col):
                        game_over = True
                        winner = player_turn
                    elif check_draw():
                        game_over = True
                        winner = None

                    player_turn = 3 - player_turn

        screen.fill(WHITE)
        draw_board()
        draw_pieces()
        pygame.display.flip()

        if game_over:
            font = pygame.font.Font('arial-unicode-ms.ttf', 24)
            if winner is not None:
                text = font.render("{} Chiến Thắng!".format("Đỏ" if winner == 1 else "Xanh"), True,
                                   PINK if winner == 1 else BLUE)
            else:
                text = font.render("Hòa!", True, MAROON)
            text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            screen.blit(text, text_rect)
            pygame.display.flip()
            pygame.time.wait(20000)
            pygame.quit()
            sys.exit()

if __name__ == "__main__":
    main()
