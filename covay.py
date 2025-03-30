import pygame
import sys

# Constants
BOARD_SIZE = 20
GRID_SIZE = 30
SCREEN_WIDTH = BOARD_SIZE * GRID_SIZE
SCREEN_HEIGHT = BOARD_SIZE * GRID_SIZE
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Cờ Vây")
pygame.display.set_icon(pygame.image.load('covay.jpg'))

# Create the initial Go board
initial_board = [[0] * BOARD_SIZE for _ in range(BOARD_SIZE)]

def draw_board(board):
    screen.fill((236, 171, 83))

    # Draw horizontal and vertical grid lines within the actual board area
    for x in range(BOARD_SIZE):
        pygame.draw.line(screen, BLACK, ((x + 1) * GRID_SIZE, GRID_SIZE), ((x + 1) * GRID_SIZE, SCREEN_HEIGHT - GRID_SIZE), 2)
        pygame.draw.line(screen, BLACK, (GRID_SIZE, (x + 1) * GRID_SIZE), (SCREEN_WIDTH - GRID_SIZE + 1, (x + 1) * GRID_SIZE), 2)

    # Danh sách các tọa độ để vẽ dấu chấm đậm
    dot_coordinates = [(3, 3), (9, 3), (3, 9), (9, 9), (3, 15), (9, 15), (15, 3), (15, 9), (15, 15)]  # Thay đổi các giá trị này bằng các tọa độ mong muốn

    # Vẽ dấu chấm đậm ở các tọa độ đã chọn
    for coord in dot_coordinates:
        row, col = coord
        pygame.draw.circle(screen, BLACK, ((col + 1) * GRID_SIZE, (row + 1) * GRID_SIZE), 4)

    # Draw stones on the board
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if board[i][j] == 1:
                pygame.draw.circle(screen, BLACK, ((j + 1) * GRID_SIZE, (i + 1) * GRID_SIZE), GRID_SIZE // 2 - 2)
            elif board[i][j] == 2:
                pygame.draw.circle(screen, WHITE, ((j + 1) * GRID_SIZE, (i + 1) * GRID_SIZE), GRID_SIZE // 2 - 2)

    pygame.display.flip()

def is_valid_move(board, row, col, player):
    if 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE:
        if board[row][col] == 0 or (board[row][col] == -1 and count_adjacent_stones(board, row, col, player) == 4):
            # Kiểm tra nếu bước đi hợp lệ (ô trống hoặc quân vây đi vào vị trí đã bị vây)
            return True
    return False

def count_adjacent_stones(board, row, col, player):
    count = 0
    if row > 0 and board[row - 1][col] == player:
        count += 1
    if row < BOARD_SIZE - 1 and board[row + 1][col] == player:
        count += 1
    if col > 0 and board[row][col - 1] == player:
        count += 1
    if col < BOARD_SIZE - 1 and board[row][col + 1] == player:
        count += 1
    return count

def is_surrounded(board, row, col, player):
    # Kiểm tra nếu quân đối thủ đã bị vây bởi chính xác 4 quân của người chơi
    opponent = 3 - player

    # Kiểm tra tất cả các hướng xung quanh
    up = row > 0 and board[row - 1][col] == opponent and count_adjacent_stones(board, row - 1, col, player) == 4
    down = row < BOARD_SIZE - 1 and board[row + 1][col] == opponent and count_adjacent_stones(board, row + 1, col, player) == 4
    left = col > 0 and board[row][col - 1] == opponent and count_adjacent_stones(board, row, col - 1, player) == 4
    right = col < BOARD_SIZE - 1 and board[row][col + 1] == opponent and count_adjacent_stones(board, row, col + 1, player) == 4

    # Kiểm tra xem có ít nhất một quân đối thủ từ cả bốn hướng khác nhau
    return up or down or left or right

def capture_opponent_stones(board, row, col, player):
    # Xác định và ăn quân đối thủ bị bao quanh
    opponent = 3 - player
    captured_stones = []  # Danh sách các quân cờ bị ăn

    def capture_group(r, c):
        nonlocal captured_stones
        if 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE and board[r][c] == opponent:
            if count_adjacent_stones(board, r, c, player) == 4:
                captured_stones.append((r, c))
                board[r][c] = 0
                capture_group(r - 1, c)
                capture_group(r + 1, c)
                capture_group(r, c - 1)
                capture_group(r, c + 1)

    if row > 0 and board[row - 1][col] == opponent:
        capture_group(row - 1, col)
    if row < BOARD_SIZE - 1 and board[row + 1][col] == opponent:
        capture_group(row + 1, col)
    if col > 0 and board[row][col - 1] == opponent:
        capture_group(row, col - 1)
    if col < BOARD_SIZE - 1 and board[row][col + 1] == opponent:
        capture_group(row, col + 1)

    return captured_stones

def main():
    current_board = [row[:] for row in initial_board]
    current_player = 1  # 1 for black, 2 for white
    black_score = 0
    white_score = 0
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                col = mouse_x // GRID_SIZE
                row = mouse_y // GRID_SIZE

                if is_valid_move(current_board, row, col, current_player):
                    current_board[row][col] = current_player

                    captured_stones = []  # Danh sách quân cờ bị ăn
                    if is_surrounded(current_board, row, col, current_player):
                        captured_stones = capture_opponent_stones(current_board, row, col, current_player)
                        if current_player == 1:
                            black_score += len(captured_stones)
                            print("Điểm số cho đen:", black_score)
                        else:
                            white_score += len(captured_stones)
                            print("Điểm số cho trắng:", white_score)

                        # Cập nhật bàn cờ và giữ vị trí đã vây có thể đi vào
                        for r, c in captured_stones:
                            current_board[r][c] = -1

                    current_player = 3 - current_player  # Toggle between 1 and 2

        draw_board(current_board)
        pygame.display.update()

    # Tính tổng số quân trên bàn cờ để xác định người chiến thắng
    total_black_stones = sum(row.count(1) for row in current_board)
    total_white_stones = sum(row.count(2) for row in current_board)

    if total_black_stones > total_white_stones:
        print("Người chơi đen chiến thắng!")
    elif total_black_stones < total_white_stones:
        print("Người chơi trắng chiến thắng!")
    else:
        print("Hòa!")

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
