import pygame
from pygame.locals import *
import sys

# Thiết lập kích thước và các tham số liên quan
GRID_SIZE = 19
CELL_SIZE = 40
WINDOW_SIZE = GRID_SIZE * CELL_SIZE
PLAYER1_COLOR = (0, 0, 0)
PLAYER2_COLOR = (255, 255, 255)
LINE_COLOR = (0, 0, 0)
DISPLAY_COLOR = (0, 255, 255)
WINNING_LENGTH = 6

class Connect6Game:
    def __init__(self):
        # Khởi tạo pygame
        pygame.init()

        # Tạo một mảng 2D để lưu trạng thái của bàn cờ (0 cho ô trống, 1 cho người chơi 1, 2 cho người chơi 2)
        self.board = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

        # Biến lưu trạng thái người chơi hiện tại (1 hoặc 2)
        self.current_player = 1

        # Biến lưu trạng thái trò chơi (True nếu trò chơi đang diễn ra, False nếu trò chơi đã kết thúc)
        self.game_active = True

        # Khởi tạo cửa sổ Pygame
        self.screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
        pygame.display.set_caption("Cờ Connect 6")
        pygame.display.set_icon(pygame.image.load('connect6.png'))

        # Thiết lập thuộc tính Pygame
        self.font = pygame.font.Font('arial-unicode-ms.ttf', 24)
        self.running = True

        # Khởi tạo biến lượt di chuyển ban đầu
        self.moves_left = 1

        # Định nghĩa một số biến để theo dõi trạng thái trò chơi
        self.game_state = {}  # Trạng thái trò chơi

        # Thêm biến current_move để theo dõi số nước đi đã thực hiện
        self.current_move = -1

        # Biến kiểm tra trạng thái hòa
        self.is_draw = False

        # Khởi tạo biến lịch sử di chuyển và lịch sử redo
        self.move_history = []  # Lịch sử di chuyển
        self.move_history = {1: [], 2: []}  # Lịch sử di chuyển của mỗi người chơi

        # Khởi tạo các biến cần thiết, bao gồm move_history
        self.move_history = {}  # Sử dụng một từ điển thay vì danh sách

        # Thêm biến để theo dõi lượt đi của người chơi
        self.current_player_turn = 1  # Ban đầu, lượt đi thuộc về người chơi 1
        self.moves_made = 0  # Số lượt đã di chuyển trong lượt hiện tại
        self.max_moves_per_turn = 2  # Số lượt tối đa mà mỗi người chơi có thể thực hiện

        # Thêm biến để theo dõi người chơi 2 đã đi nước đầu chưa
        self.player2_first_move = False

        # Lượt đi ban đầu của người chơi 1
        self.current_player_turn = 1

        # Thêm thuộc tính trạng thái trò chơi
        self.trang_thai_game = {
            'board': self.board,
            'current_player': self.current_player,
            'moves_left': self.moves_left,
            'move_history': self.move_history,
            # Thêm các thông tin khác mà bạn muốn lưu
        }

    # Hàm vẽ bàn cờ
    def draw_board(self):
        self.screen.fill((238, 232, 170))

        # Vẽ các ô cờ và đường viền
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                pygame.draw.rect(self.screen, LINE_COLOR, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)

                if self.board[row][col] == 1:
                    pygame.draw.circle(self.screen, PLAYER1_COLOR,
                                       (col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2),
                                       CELL_SIZE // 2 - 2)
                elif self.board[row][col] == 2:
                    pygame.draw.circle(self.screen, PLAYER2_COLOR,
                                       (col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2),
                                       CELL_SIZE // 2 - 2)

        # Vẽ các đường trên, dưới, trái và phải bàn cờ
        pygame.draw.line(self.screen, LINE_COLOR, (0, 0), (GRID_SIZE * CELL_SIZE - 1, 0), 2)  # Đường trên
        pygame.draw.line(self.screen, LINE_COLOR, (0, GRID_SIZE * CELL_SIZE - 1),
                         (GRID_SIZE * CELL_SIZE - 1, GRID_SIZE * CELL_SIZE - 1), 3)  # Đường dưới
        pygame.draw.line(self.screen, LINE_COLOR, (0, 0), (0, GRID_SIZE * CELL_SIZE - 1), 2)  # Đường trái
        pygame.draw.line(self.screen, LINE_COLOR, (GRID_SIZE * CELL_SIZE - 1, 0),
                         (GRID_SIZE * CELL_SIZE - 1, GRID_SIZE * CELL_SIZE - 1), 3)  # Đường phải

        pygame.display.flip()

    # Hàm vẽ quân cờ
    def draw_piece(self, row, col, player):
        x = col * CELL_SIZE + CELL_SIZE // 2
        y = row * CELL_SIZE + CELL_SIZE // 2
        color = PLAYER1_COLOR if player == 1 else PLAYER2_COLOR
        pygame.draw.circle(self.screen, color, (x, y), CELL_SIZE // 2 - 2)

    # Hàm kiểm tra chiến thắng
    def check_win(self, player, row, col):
        directions = [(1, 0), (0, 1), (1, 1), (-1, 1)]
        for dr, dc in directions:
            count = 1
            for i in range(1, WINNING_LENGTH):
                r, c = row + i * dr, col + i * dc
                if 0 <= r < GRID_SIZE and 0 <= c < GRID_SIZE and self.board[r][c] == player:
                    count += 1
                else:
                    break
            for i in range(1, WINNING_LENGTH):
                r, c = row - i * dr, col - i * dc
                if 0 <= r < GRID_SIZE and 0 <= c < GRID_SIZE and self.board[r][c] == player:
                    count += 1
                else:
                    break
            if count >= WINNING_LENGTH:
                return True
        return False

    # Hàm xác định người chơi chiến thắng và trả về tên của người chơi đó
    def determine_winner(self, player):
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                if self.board[row][col] == player and self.check_win(player, row, col):
                    return f"Player {player}"
        return None

    # Hàm kiểm tra xem bàn cờ đã đầy chưa
    def is_board_full(self):
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                if self.board[row][col] == 0:
                    return False
        return True

    # Hàm hiển thị thông báo người chơi chiến thắng hoặc kết quả hòa
    def draw_winner(self, player):
        winner = self.determine_winner(player)
        text = ""  # Khởi tạo text trước khi sử dụng
        text_color = (0, 0, 0)  # Khởi tạo một màu sắc mặc định

        if winner is not None:
            if player == 1:
                text_color = (255, 0, 0)  # Màu đỏ cho người chơi 1
                text = f"Đen Chiến Thắng!"
            else:
                text_color = (255, 0, 255)  # Màu hồng cho người chơi 2
                text = f"Trắng Chiến Thắng!"
        elif self.is_board_full():
            text_color = (255, 165, 0)  # Màu cam cho kết quả hòa
            text = f"Hòa!"

        text_surface = self.font.render(text, True, text_color)
        text_rect = text_surface.get_rect(center=(WINDOW_SIZE // 2, WINDOW_SIZE // 2))
        self.screen.blit(text_surface, text_rect)
        pygame.display.flip()

    # Thay đổi phương thức close_game_window để bắt sự kiện đóng cửa sổ
    def close_game_window(self):
        pygame.quit()

    def add_move_to_history(self, row, col):
        player = self.current_player
        moves_made = self.moves_made
        if player in self.move_history:
            self.move_history[player].append((row, col, player, moves_made))
        else:
            self.move_history[player] = [(row, col, player, moves_made)]

    def update_turn_and_moves(self):
        if self.current_player_turn == 2:
            # Nếu lượt của người chơi 2, thì cho người chơi 2 đi 2 quân sau undo
            self.moves_left = 2
        else:
            # Ngược lại, cho người chơi 1 đi 2 quân sau undo
            self.moves_left = 1

    def is_game_active(self):
        # Kiểm tra xem trò chơi có còn hoạt động hay không
        for row in self.board:
            for cell in row:
                if cell == 0:
                    return True
        return False

    def switch_turn(self):
        # Hàm chuyển lượt cho đối thủ
        self.moves_left = 2
        if self.current_player_turn == 1:
            self.current_player_turn = 2
        else:
            self.current_player_turn = 1

    # Thêm hàm pop_last_move để lấy thông tin nước đi cuối cùng trong lịch sử
    def pop_last_move(self):
        if self.move_history:
            return self.move_history[-1]
        else:
            return None

    # Hàm để xác định người chơi hiện tại và số lượt di chuyển của người chơi
    def get_current_player_and_moves_left(self):
        if self.current_move == -1:
            return self.current_player, self.moves_left
        if self.current_move % 2 == 0:
            return self.current_player, self.moves_left
        else:
            return 3 - self.current_player, self.moves_left - 1

    # Hàm để kiểm tra xem trò chơi đã kết thúc chưa
    def check_game_over(self):
        if self.determine_winner(1) or self.determine_winner(2):
            self.game_active = False
            return True
        if self.is_board_full():
            self.is_draw = True
            self.game_active = False
            return True
        return False

    def update_game_state(self):
        # Kiểm tra xem self.move_history có tồn tại và có đủ phần tử để truy cập không
        if self.move_history and self.current_player in self.move_history:
            self.game_state = {
                'board': [row[:] for row in self.board],
                'current_player': self.current_player,
                'moves_left': self.moves_left,
                'move_history': self.move_history[self.current_player][:],
            }
        else:
            # Nếu không có lịch sử di chuyển cho người chơi hiện tại, hãy tạo một danh sách trống
            self.game_state = {
                'board': [row[:] for row in self.board],
                'current_player': self.current_player,
                'moves_left': self.moves_left,
                'move_history': [],
            }

    def make_move(self, row, col):
        if self.board[row][col] == 0 and self.moves_left > 0:
            self.board[row][col] = self.current_player
            self.add_move_to_history(row, col)
            self.move_history[self.current_player].append((row, col))

            if self.moves_made >= self.max_moves_per_turn:
                self.moves_made = 0

            if self.check_win(self.current_player, row, col):
                self.draw_winner(self.current_player)

            if self.is_board_full():
                self.draw_winner(0)  # Set a draw

            if self.moves_left == 0:
                if self.current_player == 1:
                    self.moves_left = 2  # Player 2 takes 2 moves
                else:
                    self.moves_left = 2  # Player 1 takes 1 move

            if not any(0 in row for row in self.board):
                self.is_draw = True
                self.game_active = False

        # Sau mỗi nước đi, cập nhật trạng thái trò chơi
        self.trang_thai_game = {
            'board': self.board,
            'current_player': self.current_player,
            'moves_left': self.moves_left,
            'move_history': self.move_history,
            # Thêm các thông tin khác mà bạn muốn lưu
        }

    # Vòng lặp chính của game
    def run(self):
        self.moves_left = 1

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE: # Phím tắt cửa sổ giao diện (Esc)
                        self.running = False
                    if event.key == K_u and pygame.key.get_mods() & KMOD_CTRL:  # Phím tắt cho Undo (Ctrl + U)
                        self.update_game_state()
                        # Thêm dòng sau để cập nhật trạng thái trò chơi sau Undo
                        self.trang_thai_game = {
                            'board': self.board,
                            'current_player': self.current_player,
                            'moves_left': self.moves_left,
                            'move_history': self.move_history,
                            # Thêm các thông tin khác mà bạn muốn lưu
                        }
                    if event.key == K_r and pygame.key.get_mods() & KMOD_CTRL:  # Phím tắt cho Redo (Ctrl + R)
                        self.update_game_state()
                        # Thêm dòng sau để cập nhật trạng thái trò chơi sau Redo
                        self.trang_thai_game = {
                            'board': self.board,
                            'current_player': self.current_player,
                            'moves_left': self.moves_left,
                            'move_history': self.move_history,
                            # Thêm các thông tin khác mà bạn muốn lưu
                        }
                    elif event.key == pygame.K_n:  # Phím tắt cho Reset (Ctrl + N) hoặc (N)
                        self.game_state = {}  # Đặt lại trạng thái trò chơi về trạng thái ban đầu
                        # Đặt lại trạng thái trò chơi về trạng thái ban đầu
                        self.trang_thai_game = {
                            'board': self.board,
                            'current_player': self.current_player,
                            'moves_left': self.moves_left,
                            'move_history': self.move_history,
                            # Thêm các thông tin khác mà bạn muốn lưu
                        }
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    col = event.pos[0] // CELL_SIZE
                    row = event.pos[1] // CELL_SIZE
                    if 0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE and self.board[row][col] == 0 and self.moves_left > 0:
                        self.make_move(row, col)
                        self.board[row][col] = self.current_player
                        self.draw_piece(row, col, self.current_player)
                        self.add_move_to_history(row, col)  # Thêm nước đi vào lịch sử
                        self.moves_left -= 1
                        self.update_game_state()
                        if self.check_win(self.current_player, row, col):
                            self.draw_winner(self.current_player_turn)
                            pygame.time.delay(20000)
                            pygame.quit()
                            sys.exit()
                        if self.is_board_full():
                            self.draw_winner(self.current_player)
                            pygame.time.delay(20000)
                            pygame.quit()
                            sys.exit()
                        elif self.moves_left == 0:
                            self.current_player = 3 - self.current_player  # Chuyển sang người chơi tiếp theo
                            self.moves_left = 2  # Đặt lại số lượt di chuyển cho người chơi mới
                            if not any(0 in row for row in self.board):
                                self.is_draw = True  # Xác định trạng thái hòa
                                self.game_active = False  # Trò chơi đã kết thúc
                            self.update_game_state()
                            self.check_game_over()

            self.draw_board()
            pygame.display.flip()

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Connect6Game()
    game.run()
