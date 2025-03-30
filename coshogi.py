import pygame as p
import sys

WIDTH = HEIGHT = 810  # Giảm kích thước để loại bỏ viền phải và dưới
DIMENSION = 9
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

def loadImages():
    pieces = ['wShogi_fuhyo', 'wShogi_hisha', 'wShogi_kakugyo', 'wShogi_kyosha', 'wShogi_keima', 'wShogi_ginsho',
              'wShogi_kinsho', 'wShogi_gyokusho', 'wShogi_tokin', 'wShogi_narikyo', 'wShogi_narikei', 'wShogi_narigin',
              'wShogi_ryuma', 'wShogi_ryuo',
              'bShogi_fuhyo', 'bShogi_hisha', 'bShogi_kakugyo', 'bShogi_kyosha', 'bShogi_keima', 'bShogi_ginsho',
              'bShogi_kinsho', 'bShogi_gyokusho', 'bShogi_tokin', 'bShogi_narikyo', 'bShogi_narikei', 'bShogi_narigin',
              'bShogi_ryuma', 'bShogi_ryuo']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load(piece + ".png"), (SQ_SIZE - 10, SQ_SIZE - 10))

def main():
    p.init()
    p.display.set_caption('Cờ Shogi')
    p.display.set_icon(p.image.load('wShogi_gyokusho.png'))
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = GameState()
    loadImages()
    running = True
    sqSelected = ()  # no square is selected initially, this will keep track of the last click of the user (tuple(row,col))
    playerClicks = []  # this will keep track of player clicks (two tuples)
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()  # (x, y) location of the mouse
                col = location[0] // SQ_SIZE
                row = location[1] // SQ_SIZE
                if sqSelected == (row, col):
                    sqSelected = ()  # deselect
                    playerClicks = []  # clear clicks
                else:
                    sqSelected = (row, col)
                    playerClicks.append(sqSelected)  # append for both 1st and 2nd click
                if len(playerClicks) == 2:  # after 2nd click
                    move = Move(playerClicks[0], playerClicks[1], gs.board)
                    if move.isValidFuhyoMove(gs.board):  # Kiểm tra nước đi của quân tốt có hợp lệ không
                        gs.makeMove(move)
                    elif move.isValidKakugyoMove(gs.board):  # Kiểm tra nước đi của quân tượng có hợp lệ không
                        gs.makeMove(move)
                    elif move.isValidHishaMove(gs.board):  # Kiểm tra nước đi của quân xe có hợp lệ không
                        gs.makeMove(move)
                    elif move.isValidKyoshaMove(gs.board):  # Kiểm tra nước đi của quân thương có hợp lệ không
                        gs.makeMove(move)
                    elif move.isValidKeimaMove(gs.board):  # Kiểm tra nước đi của quân mã có hợp lệ không
                        gs.makeMove(move)
                    elif move.isValidGinshoMove(gs.board):  # Kiểm tra nước đi của quân bạc có hợp lệ không
                        gs.makeMove(move)
                    elif move.isValidKinshoMove(gs.board):  # Kiểm tra nước đi của quân vàng có hợp lệ không
                        gs.makeMove(move)
                    elif move.isValidGyokushoMove(gs.board):  # Kiểm tra nước đi của quân vua có hợp lệ không
                        gs.makeMove(move)
                    elif move.isValidTokinMove(gs.board):  # Kiểm tra nước đi của quân tốt phong cấp có hợp lệ không
                        gs.makeMove(move)
                    elif move.isValidNarikyoMove(gs.board):  # Kiểm tra nước đi của quân thương phong cấp có hợp lệ không
                        gs.makeMove(move)
                    elif move.isValidNarikeiMove(gs.board):  # Kiểm tra nước đi của quân mã phong cấp có hợp lệ không
                        gs.makeMove(move)
                    elif move.isValidNariginMove(gs.board):  # Kiểm tra nước đi của quân bạc phong cấp có hợp lệ không
                        gs.makeMove(move)
                    elif move.isValidRyumaMove(gs.board):  # Kiểm tra nước đi của quân tượng rồng có hợp lệ không
                        gs.makeMove(move)
                    elif move.isValidRyuoMove(gs.board):  # Kiểm tra nước đi của quân xe rồng có hợp lệ không
                        gs.makeMove(move)
                    else:
                        print("Invalid move")
                    sqSelected = ()  # reset user clicks
                    playerClicks = []

            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:
                    gs.undoMove()

        drawGameState(screen, gs, sqSelected)
        clock.tick(MAX_FPS)
        p.display.flip()

    p.quit()

def hasOpponentPiece(board, row, col, pieceColor):
    # Kiểm tra xem có quân đối phương ở ô được chỉ định hay không
    return board[row][col] != "--" and board[row][col][0] != pieceColor[0]

def getValidMoves(board, row, col, piece):
    moves = []
    if piece.endswith("fuhyo"):
        direction = 1 if piece.startswith("b") else -1
        # Kiểm tra nước đi tiến
        if board[row + direction][col] == "--":
            moves.append((row + direction, col))
        # Kiểm tra nếu có quân đối thủ đứng phía trước
        elif hasOpponentPiece(board, row + direction, col, piece):
            moves.append((row + direction, col))
    elif piece.endswith("kakugyo"):
        # Di chuyển quân tượng
        for d_row, d_col in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
            r, c = row + d_row, col + d_col
            while 0 <= r < DIMENSION and 0 <= c < DIMENSION:
                if board[r][c] == "--" or hasOpponentPiece(board, r, c, piece):
                    moves.append((r, c))
                    if board[r][c] != "--":
                        break
                else:
                    break
                r += d_row
                c += d_col
    elif piece.endswith("hisha"):
        # Di chuyển quân xe
        # Di chuyển ngang
        for d_col in range(col + 1, DIMENSION):
            if board[row][d_col] == "--":
                moves.append((row, d_col))
            elif hasOpponentPiece(board, row, d_col, piece):
                moves.append((row, d_col))
                break
            else:
                break
        for d_col in range(col - 1, -1, -1):
            if board[row][d_col] == "--":
                moves.append((row, d_col))
            elif hasOpponentPiece(board, row, d_col, piece):
                moves.append((row, d_col))
                break
            else:
                break
        # Di chuyển dọc
        for d_row in range(row + 1, DIMENSION):
            if board[d_row][col] == "--":
                moves.append((d_row, col))
            elif hasOpponentPiece(board, d_row, col, piece):
                moves.append((d_row, col))
                break
            else:
                break
        for d_row in range(row - 1, -1, -1):
            if board[d_row][col] == "--":
                moves.append((d_row, col))
            elif hasOpponentPiece(board, d_row, col, piece):
                moves.append((d_row, col))
                break
            else:
                break
    elif piece.endswith("kyosha"):
        # Di chuyển quân thương
        direction = 1 if piece.startswith("b") else -1
        # Di chuyển tiến cho đến khi gặp quân cản
        for i in range(1, DIMENSION):
            if 0 <= row + i * direction < DIMENSION:
                if board[row + i * direction][col] == "--":
                    moves.append((row + i * direction, col))
                else:
                    if hasOpponentPiece(board, row + i * direction, col, piece):
                        moves.append((row + i * direction, col))
                    break
            else:
                break
    elif piece.endswith("keima"):
        # Di chuyển quân mã
        directions = [(2, 1), (2, -1)] if piece.startswith("b") else [(-2, 1), (-2, -1)]
        for d_row, d_col in directions:
            r, c = row + d_row, col + d_col
            # Kiểm tra xem nước đi có hợp lệ không
            if 0 <= r < DIMENSION and 0 <= c < DIMENSION and (
                    board[r][c] == "--" or hasOpponentPiece(board, r, c, piece)):
                moves.append((r, c))
    elif piece.endswith("ginsho"):
        # Di chuyển quân bạc
        direction = 1 if piece.startswith("b") else -1
        # Di chuyển tiến cho đến khi gặp quân cản
        directions = [(1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
        for d_row, d_col in directions:
            r, c = row + direction * d_row, col + d_col
            # Kiểm tra xem nước đi có hợp lệ không
            if 0 <= r < DIMENSION and 0 <= c < DIMENSION and (
                    board[r][c] == "--" or hasOpponentPiece(board, r, c, piece)):
                moves.append((r, c))
    elif piece.endswith("kinsho"):
        # Di chuyển quân vàng
        direction = 1 if piece.startswith("b") else -1
        # Di chuyển tiến cho đến khi gặp quân cản
        directions = [(1, 0), (1, 1), (1, -1), (-1, 0), (0, 1), (0, -1)]
        for d_row, d_col in directions:
            r, c = row + direction * d_row, col + d_col
            # Kiểm tra xem nước đi có hợp lệ không
            if 0 <= r < DIMENSION and 0 <= c < DIMENSION and (
                    board[r][c] == "--" or hasOpponentPiece(board, r, c, piece)):
                moves.append((r, c))
    elif piece.endswith("gyokusho"):
        # Di chuyển quân vua
        direction = 1 if piece.startswith("b") else -1
        # Di chuyển tiến cho đến khi gặp quân cản
        directions = [(1, 0), (1, 1), (1, -1), (-1, 0), (-1, 1), (-1, -1), (0, 1), (0, -1)]
        for d_row, d_col in directions:
            r, c = row + direction * d_row, col + d_col
            # Kiểm tra xem nước đi có hợp lệ không
            if 0 <= r < DIMENSION and 0 <= c < DIMENSION and (
                    board[r][c] == "--" or hasOpponentPiece(board, r, c, piece)):
                moves.append((r, c))
    elif piece.endswith("tokin"):
        # Di chuyển quân tốt phong cấp
        direction = 1 if piece.startswith("b") else -1
        # Di chuyển tiến cho đến khi gặp quân cản
        directions = [(1, 0), (1, 1), (1, -1), (-1, 0), (0, 1), (0, -1)]
        for d_row, d_col in directions:
            r, c = row + direction * d_row, col + d_col
            # Kiểm tra xem nước đi có hợp lệ không
            if 0 <= r < DIMENSION and 0 <= c < DIMENSION and (
                    board[r][c] == "--" or hasOpponentPiece(board, r, c, piece)):
                moves.append((r, c))
    elif piece.endswith("narikyo"):
        # Di chuyển quân thương phong cấp
        direction = 1 if piece.startswith("b") else -1
        # Di chuyển tiến cho đến khi gặp quân cản
        directions = [(1, 0), (1, 1), (1, -1), (-1, 0), (0, 1), (0, -1)]
        for d_row, d_col in directions:
            r, c = row + direction * d_row, col + d_col
            # Kiểm tra xem nước đi có hợp lệ không
            if 0 <= r < DIMENSION and 0 <= c < DIMENSION and (
                    board[r][c] == "--" or hasOpponentPiece(board, r, c, piece)):
                moves.append((r, c))
    elif piece.endswith("narikei"):
        # Di chuyển quân mã phong cấp
        direction = 1 if piece.startswith("b") else -1
        # Di chuyển tiến cho đến khi gặp quân cản
        directions = [(1, 0), (1, 1), (1, -1), (-1, 0), (0, 1), (0, -1)]
        for d_row, d_col in directions:
            r, c = row + direction * d_row, col + d_col
            # Kiểm tra xem nước đi có hợp lệ không
            if 0 <= r < DIMENSION and 0 <= c < DIMENSION and (
                    board[r][c] == "--" or hasOpponentPiece(board, r, c, piece)):
                moves.append((r, c))
    elif piece.endswith("narigin"):
        # Di chuyển quân bạc phong cấp
        direction = 1 if piece.startswith("b") else -1
        # Di chuyển tiến cho đến khi gặp quân cản
        directions = [(1, 0), (1, 1), (1, -1), (-1, 0), (0, 1), (0, -1)]
        for d_row, d_col in directions:
            r, c = row + direction * d_row, col + d_col
            # Kiểm tra xem nước đi có hợp lệ không
            if 0 <= r < DIMENSION and 0 <= c < DIMENSION and (
                    board[r][c] == "--" or hasOpponentPiece(board, r, c, piece)):
                moves.append((r, c))
    elif piece.endswith("ryuma"):
        # Di chuyển quân tượng
        for d_row, d_col in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
            r, c = row + d_row, col + d_col
            while 0 <= r < DIMENSION and 0 <= c < DIMENSION:
                if board[r][c] == "--" or hasOpponentPiece(board, r, c, piece):
                    moves.append((r, c))
                    if board[r][c] != "--":
                        break
                else:
                    break
                r += d_row
                c += d_col
        # Di chuyển quân vua
        direction = 1 if piece.startswith("b") else -1
        # Di chuyển tiến cho đến khi gặp quân cản
        directions = [(1, 0), (1, 1), (1, -1), (-1, 0), (-1, 1), (-1, -1), (0, 1), (0, -1)]
        for d_row, d_col in directions:
            r, c = row + direction * d_row, col + d_col
            # Kiểm tra xem nước đi có hợp lệ không
            if 0 <= r < DIMENSION and 0 <= c < DIMENSION and (
                    board[r][c] == "--" or hasOpponentPiece(board, r, c, piece)):
                moves.append((r, c))
    elif piece.endswith("ryuo"):
        # Di chuyển quân xe
        # Di chuyển ngang
        for d_col in range(col + 1, DIMENSION):
            if board[row][d_col] == "--":
                moves.append((row, d_col))
            elif hasOpponentPiece(board, row, d_col, piece):
                moves.append((row, d_col))
                break
            else:
                break
        for d_col in range(col - 1, -1, -1):
            if board[row][d_col] == "--":
                moves.append((row, d_col))
            elif hasOpponentPiece(board, row, d_col, piece):
                moves.append((row, d_col))
                break
            else:
                break
        # Di chuyển dọc
        for d_row in range(row + 1, DIMENSION):
            if board[d_row][col] == "--":
                moves.append((d_row, col))
            elif hasOpponentPiece(board, d_row, col, piece):
                moves.append((d_row, col))
                break
            else:
                break
        for d_row in range(row - 1, -1, -1):
            if board[d_row][col] == "--":
                moves.append((d_row, col))
            elif hasOpponentPiece(board, d_row, col, piece):
                moves.append((d_row, col))
                break
            else:
                break
        # Di chuyển quân vua
        direction = 1 if piece.startswith("b") else -1
        # Di chuyển tiến cho đến khi gặp quân cản
        directions = [(1, 0), (1, 1), (1, -1), (-1, 0), (-1, 1), (-1, -1), (0, 1), (0, -1)]
        for d_row, d_col in directions:
            r, c = row + direction * d_row, col + d_col
            # Kiểm tra xem nước đi có hợp lệ không
            if 0 <= r < DIMENSION and 0 <= c < DIMENSION and (
                    board[r][c] == "--" or hasOpponentPiece(board, r, c, piece)):
                moves.append((r, c))
    return moves

def drawGameState(screen, gs, sqSelected):
    draw_board(screen)
    drawPieces(screen, gs.board, sqSelected)
    if sqSelected:
        row, col = sqSelected
        piece = gs.board[row][col]
        validMoves = getValidMoves(gs.board, row, col, piece)
        highlightMoves(screen, validMoves, gs.board, piece)

def highlightMoves(screen, moves, board, pieceColor):
    for move in moves:
        row, col = move
        if hasOpponentPiece(board, row, col, pieceColor):
            p.draw.rect(screen, (255, 0, 255), (col * SQ_SIZE + 2, row * SQ_SIZE + 2, SQ_SIZE - 2, SQ_SIZE - 2), 4)
        else:
            p.draw.rect(screen, (0, 255, 0), (col * SQ_SIZE + 2, row * SQ_SIZE + 2, SQ_SIZE - 2, SQ_SIZE - 2), 4)

def draw_board(screen):
    yellow = (255, 250, 205)
    board_size = 9
    cell_size = HEIGHT // board_size

    for row in range(board_size):
        for col in range(board_size):
            p.draw.rect(screen, yellow, (col * cell_size, row * cell_size, cell_size, cell_size))

    for i in range(1, board_size):
        p.draw.line(screen, (0, 0, 0), (i * cell_size, 0), (i * cell_size, HEIGHT), 2)
        p.draw.line(screen, (0, 0, 0), (0, i * cell_size), (WIDTH, i * cell_size), 2)

    p.draw.line(screen, (0, 0, 0), (0, 0), (WIDTH, 0), 2)
    p.draw.line(screen, (0, 0, 0), (0, HEIGHT - 2), (WIDTH, HEIGHT - 2), 2)  # Loại bỏ đường dưới

    p.draw.line(screen, (0, 0, 0), (0, 0), (0, HEIGHT), 2)
    p.draw.line(screen, (0, 0, 0), (WIDTH - 2, 0), (WIDTH - 2, HEIGHT), 2)

    p.draw.circle(screen, (0, 0, 0), (3 * cell_size, 3 * cell_size), 5)
    p.draw.circle(screen, (0, 0, 0), (3 * cell_size, 6 * cell_size), 5)
    p.draw.circle(screen, (0, 0, 0), (6 * cell_size, 3 * cell_size), 5)
    p.draw.circle(screen, (0, 0, 0), (6 * cell_size, 6 * cell_size), 5)

def drawPieces(screen, board, sqSelected):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":
                # Tính toán vị trí của quân cờ để đảm bảo nó nằm ở giữa ô cờ
                x_pos = c * SQ_SIZE + (SQ_SIZE - IMAGES[piece].get_width()) // 2
                y_pos = r * SQ_SIZE + (SQ_SIZE - IMAGES[piece].get_height()) // 2

                if (r, c) == sqSelected:
                    # Vẽ hình chữ nhật đỏ xung quanh quân cờ đã chọn
                    rect = p.Rect(c * SQ_SIZE + 2, r * SQ_SIZE + 2, SQ_SIZE - 2, SQ_SIZE - 2)
                    p.draw.rect(screen, p.Color('red'), rect, 4)

                screen.blit(IMAGES[piece], (x_pos, y_pos))

if __name__ == "__main__":
    class GameState:
        def __init__(self):
            self.board = [
                ["bShogi_kyosha", "bShogi_keima", "bShogi_ginsho", "bShogi_kinsho", "bShogi_gyokusho", "bShogi_kinsho",
                 "bShogi_ginsho", "bShogi_keima", "bShogi_kyosha"],
                ["--", "bShogi_hisha", "--", "--", "--", "--", "--", "bShogi_kakugyo", "--"],
                ["bShogi_fuhyo", "bShogi_fuhyo", "bShogi_fuhyo", "bShogi_fuhyo", "bShogi_fuhyo", "bShogi_fuhyo",
                 "bShogi_fuhyo", "bShogi_fuhyo", "bShogi_fuhyo"],
                ["--", "--", "--", "--", "--", "--", "--", "--", "--"],
                ["--", "--", "--", "--", "--", "--", "--", "--", "--"],
                ["--", "--", "--", "--", "--", "--", "--", "--", "--"],
                ["wShogi_fuhyo", "wShogi_fuhyo", "wShogi_fuhyo", "wShogi_fuhyo", "wShogi_fuhyo", "wShogi_fuhyo",
                 "wShogi_fuhyo", "wShogi_fuhyo", "wShogi_fuhyo"],
                ["--", "wShogi_kakugyo", "--", "--", "--", "--", "--", "wShogi_hisha", "--"],
                ["wShogi_kyosha", "wShogi_keima", "wShogi_ginsho", "wShogi_kinsho", "wShogi_gyokusho", "wShogi_kinsho",
                 "wShogi_ginsho", "wShogi_keima", "wShogi_kyosha"]]
            self.whiteToMove = True
            self.moveLog = []
            p.init()
            self.screen = p.display.set_mode((810, 810))
            self.font = p.font.Font('arial-unicode-ms.ttf', 32)
            self.clock = p.time.Clock()
            self.time_since_win = 0
            self.win_displayed = False

        def makeMove(self, move):
            # Thực hiện nước đi được chọn và cập nhật trạng thái trò chơi
            self.board[move.startRow][move.startCol] = "--"

            # Kiểm tra nếu quân tốt đã đi đến hàng ngang cuối cùng
            if move.endRow == 2 or move.endRow == DIMENSION - 3:
                # Kiểm tra nếu là quân Mã (Shogi_keima) và đến hàng ngang thứ 2 hoặc thứ 6
                if move.pieceMoved.endswith("keima"):
                    if (move.pieceMoved == "wShogi_keima" and move.endRow == 2) or (
                            move.pieceMoved == "bShogi_keima" and move.endRow == DIMENSION - 3):
                        # Phong cấp thành quân Mã thần (Shogi_narikei)
                        self.board[move.endRow][move.endCol] = move.pieceMoved.replace("keima", "narikei")
                    else:
                        # Giữ nguyên quân Mã (Shogi_keima)
                        self.board[move.endRow][move.endCol] = move.pieceMoved
                # Kiểm tra nếu là quân Bạc (Shogi_ginsho) và đến hàng ngang thứ 2 hoặc thứ 6
                elif move.pieceMoved.endswith("ginsho"):
                    if (move.pieceMoved == "wShogi_ginsho" and move.endRow == 2) or (
                            move.pieceMoved == "bShogi_ginsho" and move.endRow == DIMENSION - 3):
                        # Phong cấp thành quân Bạc thần (Shogi_narigin)
                        self.board[move.endRow][move.endCol] = move.pieceMoved.replace("ginsho", "narigin")
                    else:
                        # Giữ nguyên quân Bạc (Shogi_ginsho)
                        self.board[move.endRow][move.endCol] = move.pieceMoved
                # Nếu là quân tốt của người chơi đang đi và đến hàng ngang cuối cùng
                elif move.pieceMoved.endswith("fuhyo"):
                    # Thay đổi quân từ tốt thành Tốt thần
                    if move.pieceMoved.startswith("b"):
                        self.board[move.endRow][move.endCol] = "bShogi_tokin"
                    else:
                        self.board[move.endRow][move.endCol] = "wShogi_tokin"
                # Kiểm tra nếu là quân Tượng và đến hàng ngang cuối cùng
                elif move.pieceMoved.endswith("kakugyo"):
                    # Nếu là quân Tượng và đến hàng ngang cuối cùng
                    if move.pieceMoved.startswith("w") and move.endRow == DIMENSION - 3:
                        # Không phong cấp khi Tượng trắng đi đến hàng 6
                        self.board[move.endRow][move.endCol] = move.pieceMoved
                    elif move.pieceMoved.startswith("b") and move.endRow == 2:
                        # Không phong cấp khi Tượng đen đi đến hàng 2
                        self.board[move.endRow][move.endCol] = move.pieceMoved
                    else:
                        # Phong cấp thành quân Tượng rồng (Shogi_ryuma)
                        self.board[move.endRow][move.endCol] = "bShogi_ryuma" if move.pieceMoved.startswith(
                            "b") else "wShogi_ryuma"
                # Kiểm tra nếu là quân Xe và đến hàng ngang cuối cùng
                elif move.pieceMoved.endswith("hisha"):
                    # Nếu là quân Xe và đến hàng ngang cuối cùng
                    if move.pieceMoved.startswith("w") and move.endRow == DIMENSION - 3:
                        # Không phong cấp khi Xe trắng đi đến hàng 6
                        self.board[move.endRow][move.endCol] = move.pieceMoved
                    elif move.pieceMoved.startswith("b") and move.endRow == 2:
                        # Không phong cấp khi Xe đen đi đến hàng 2
                        self.board[move.endRow][move.endCol] = move.pieceMoved
                    else:
                        # Phong cấp thành quân Xe rồng (Shogi_ryuo)
                        self.board[move.endRow][move.endCol] = "bShogi_ryuo" if move.pieceMoved.startswith(
                            "b") else "wShogi_ryuo"
                # Kiểm tra nếu là quân Thương và đến hàng ngang cuối cùng
                elif move.pieceMoved.endswith("kyosha"):
                    # Nếu là quân Thương của người chơi đang đi và đến hàng ngang cuối cùng
                    if move.pieceMoved.startswith("b") and move.endRow >= DIMENSION - 3:
                        # Thay đổi quân từ Thương thành Thương thần
                        self.board[move.endRow][move.endCol] = "bShogi_narikyo"
                    elif move.pieceMoved.startswith("w") and move.endRow <= 2:
                        # Thay đổi quân từ Thương thành Thương thần
                        self.board[move.endRow][move.endCol] = "wShogi_narikyo"
                    else:
                        self.board[move.endRow][move.endCol] = "bShogi_kyosha" if move.pieceMoved.startswith(
                            "b") else "wShogi_kyosha"
                else:
                    self.board[move.endRow][move.endCol] = move.pieceMoved
            elif move.endRow == 0 and move.pieceMoved.startswith("w"):
                # Kiểm tra nếu là quân Thương trắng và đến hàng ngang cuối cùng
                if move.pieceMoved.endswith("kyosha"):
                    # Thay đổi quân từ Thương thành Thương thần
                    self.board[move.endRow][move.endCol] = "wShogi_narikyo"
                elif move.pieceMoved.endswith("kakugyo"):
                    # Thay đổi quân từ Tượng thành Tượng rồng
                    self.board[move.endRow][move.endCol] = "wShogi_ryuma"
                elif move.pieceMoved.endswith("hisha"):
                    # Thay đổi quân từ Xe thành Xe rồng
                    self.board[move.endRow][move.endCol] = "wShogi_ryuo"
                else:
                    self.board[move.endRow][move.endCol] = move.pieceMoved
            elif move.endRow == DIMENSION - 1 and move.pieceMoved.startswith("b"):
                # Kiểm tra nếu là quân Thương đen và đến hàng ngang cuối cùng
                if move.pieceMoved.endswith("kyosha"):
                    # Thay đổi quân từ Thương thành Thương thần
                    self.board[move.endRow][move.endCol] = "bShogi_narikyo"
                elif move.pieceMoved.endswith("kakugyo"):
                    # Thay đổi quân từ Tượng thành Tượng rồng
                    self.board[move.endRow][move.endCol] = "bShogi_ryuma"
                elif move.pieceMoved.endswith("hisha"):
                    # Thay đổi quân từ Xe thành Xe rồng
                    self.board[move.endRow][move.endCol] = "bShogi_ryuo"
                else:
                    self.board[move.endRow][move.endCol] = move.pieceMoved
            elif move.endRow == 1 and move.pieceMoved.startswith("w"):
                # Kiểm tra nếu là quân Thương trắng và đến hàng ngang cuối cùng
                if move.pieceMoved.endswith("kyosha"):
                    # Thay đổi quân từ Thương thành Thương thần
                    self.board[move.endRow][move.endCol] = "wShogi_narikyo"
                elif move.pieceMoved.endswith("kakugyo"):
                    # Thay đổi quân từ Tượng thành Tượng rồng
                    self.board[move.endRow][move.endCol] = "wShogi_ryuma"
                elif move.pieceMoved.endswith("hisha"):
                    # Thay đổi quân từ Xe thành Xe rồng
                    self.board[move.endRow][move.endCol] = "wShogi_ryuo"
                else:
                    self.board[move.endRow][move.endCol] = move.pieceMoved
            elif move.endRow == DIMENSION - 2 and move.pieceMoved.startswith("b"):
                # Kiểm tra nếu là quân Thương đen và đến hàng ngang cuối cùng
                if move.pieceMoved.endswith("kyosha"):
                    # Thay đổi quân từ Thương thành Thương thần
                    self.board[move.endRow][move.endCol] = "bShogi_narikyo"
                elif move.pieceMoved.endswith("kakugyo"):
                    # Thay đổi quân từ Tượng thành Tượng rồng
                    self.board[move.endRow][move.endCol] = "bShogi_ryuma"
                elif move.pieceMoved.endswith("hisha"):
                    # Thay đổi quân từ Xe thành Xe rồng
                    self.board[move.endRow][move.endCol] = "bShogi_ryuo"
                else:
                    self.board[move.endRow][move.endCol] = move.pieceMoved
            else:
                self.board[move.endRow][move.endCol] = move.pieceMoved

            # Kiểm tra nếu quân Vua bị ăn
            if move.pieceCaptured.endswith("gyokusho"):
                # Gọi hàm để hiển thị thông báo chiến thắng
                self.displayWinMessage(move.pieceCaptured)

            self.moveLog.append(move)
            self.whiteToMove = not self.whiteToMove

        def displayWinMessage(self, winner):
            if winner.startswith("b"):
                winner_message = "Sente"
                text_color = (255, 255, 255)  # Màu trắng cho người chơi Đen thắng
            else:
                winner_message = "Gote"
                text_color = (0, 0, 0)  # Màu đen cho người chơi Trắng thắng

            message = winner_message + " chiến thắng!"
            text = self.font.render(message, True, text_color)
            text_rect = text.get_rect(center=(405, 405))

            # Vẽ lại bàn cờ sau khi hiển thị thông báo chiến thắng
            self.draw_board()

            # Vẽ thông báo chiến thắng
            self.screen.blit(text, text_rect)
            p.display.flip()

            # Đặt timer cho việc đóng cửa sổ sau 20 giây
            p.time.set_timer(p.USEREVENT, 20000)

            # Vòng lặp chờ cho đến khi người chơi đóng cửa sổ
            while not self.win_displayed:
                for event in p.event.get():
                    if event.type == p.QUIT:
                        p.quit()
                        sys.exit()
                    elif event.type == p.USEREVENT:
                        # Đóng cửa sổ Pygame khi hết thời gian
                        p.quit()
                        sys.exit()

                self.clock.tick(60)

        def run(self):
            # Khởi chạy trò chơi ở đây
            # Gọi phương thức displayWinMessage khi một người chơi chiến thắng
            self.displayWinMessage("Sente")  # Ví dụ: Chiến thắng của người chơi trắng

        def draw_board(self):
            yellow = (255, 222, 173)
            board_size = 9
            cell_size = HEIGHT // board_size

            for row in range(board_size):
                for col in range(board_size):
                    p.draw.rect(self.screen, yellow, (col * cell_size, row * cell_size, cell_size, cell_size))

            for i in range(1, board_size):
                p.draw.line(self.screen, (0, 0, 0), (i * cell_size, 0), (i * cell_size, HEIGHT), 2)
                p.draw.line(self.screen, (0, 0, 0), (0, i * cell_size), (WIDTH, i * cell_size), 2)

            p.draw.line(self.screen, (0, 0, 0), (0, 0), (WIDTH, 0), 2)
            p.draw.line(self.screen, (0, 0, 0), (0, HEIGHT - 2), (WIDTH, HEIGHT - 2), 2)  # Loại bỏ đường dưới

            p.draw.line(self.screen, (0, 0, 0), (0, 0), (0, HEIGHT), 2)
            p.draw.line(self.screen, (0, 0, 0), (WIDTH - 2, 0), (WIDTH - 2, HEIGHT), 2)

            p.draw.circle(self.screen, (0, 0, 0), (3 * cell_size, 3 * cell_size), 5)
            p.draw.circle(self.screen, (0, 0, 0), (3 * cell_size, 6 * cell_size), 5)
            p.draw.circle(self.screen, (0, 0, 0), (6 * cell_size, 3 * cell_size), 5)
            p.draw.circle(self.screen, (0, 0, 0), (6 * cell_size, 6 * cell_size), 5)

        def undoMove(self):
            if len(self.moveLog) != 0:
                move = self.moveLog.pop()
                self.board[move.startRow][move.startCol] = move.pieceMoved
                self.board[move.endRow][move.endCol] = move.pieceCaptured
                self.whiteToMove = not self.whiteToMove

    class Move:
        ranksToRows = {"1": 8, "2": 7, "3": 6, "4": 5,
                         "5": 4, "6": 3, "7": 2, "8": 1, "9": 0}
        rowsToRanks = {v: k for k, v in ranksToRows.items()}
        filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3,
                         "e": 4, "f": 5, "g": 6, "h": 7, "i": 8}
        colsToFiles = {v: k for k, v in filesToCols.items()}

        def __init__(self, startSq, endSq, board):
            self.startRow = startSq[0]
            self.startCol = startSq[1]
            self.endRow = endSq[0]
            self.endCol = endSq[1]
            self.pieceMoved = board[self.startRow][self.startCol]
            self.pieceCaptured = board[self.endRow][self.endCol]
            self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol

        def __eq__(self, other):
            if isinstance(other, Move):
                return self.moveID == other.moveID
            return False

        def isValidFuhyoMove(self, board):
            # Đảm bảo chỉ có thể di chuyển quân tốt tiến hoặc ăn quân ở phía trước
            if self.pieceMoved.endswith("fuhyo"):
                # Xác định hướng di chuyển của quân tốt dựa trên màu sắc
                direction = 1 if self.pieceMoved.startswith("b") else -1
                # Kiểm tra nước đi có là đi tiến hoặc ăn quân ở phía trước không
                if self.startCol != self.endCol:  # Di chuyển sang trái hoặc sang phải
                    return False
                if self.endRow != self.startRow + direction and \
                        self.endRow != self.startRow + 1 * direction:  # Không di chuyển tiến hoặc ăn quân ở phía trước
                    return False
                if board[self.endRow][self.endCol][0] == self.pieceMoved[0]:  # Không thể ăn quân của mình
                    return False
                return True
            return False

        def isValidKakugyoMove(self, board):
            # Đảm bảo chỉ có thể di chuyển quân tượng theo đường chéo
            if self.pieceMoved.endswith("kakugyo"):
                # Kiểm tra nếu quân Tượng đang ở trên bàn cờ
                if self.pieceMoved[0] == "w":
                    playerColor = "w"
                else:
                    playerColor = "b"

                # Kiểm tra xem nước đi có nằm trên đường chéo không
                if abs(self.startRow - self.endRow) != abs(self.startCol - self.endCol):
                    return False

                # Kiểm tra xem có quân cờ nào ở giữa không
                d_row = 1 if self.endRow > self.startRow else -1
                d_col = 1 if self.endCol > self.startCol else -1
                r, c = self.startRow + d_row, self.startCol + d_col
                while r != self.endRow and c != self.endCol:
                    if board[r][c] != "--":
                        return False
                    r += d_row
                    c += d_col

                # Kiểm tra nếu ô đích có quân cờ cùng màu với quân cờ di chuyển
                if board[self.endRow][self.endCol][0] == playerColor:
                    return False

                return True
            return False

        def isValidHishaMove(self, board):
            # Đảm bảo chỉ có thể di chuyển quân xe theo đường ngang hoặc đứng
            if self.pieceMoved.endswith("hisha"):
                # Kiểm tra nếu quân Xe đang ở trên bàn cờ
                if self.pieceMoved[0] == "w":
                    playerColor = "w"
                else:
                    playerColor = "b"

                # Kiểm tra xem nước đi có nằm trên đường ngang hoặc đứng không
                if self.startRow != self.endRow and self.startCol != self.endCol:
                    return False

                # Kiểm tra xem có quân cờ nào ở giữa không
                if self.startRow == self.endRow:  # Di chuyển ngang
                    d_col = 1 if self.endCol > self.startCol else -1
                    for col in range(self.startCol + d_col, self.endCol, d_col):
                        if board[self.startRow][col] != "--":
                            return False
                else:  # Di chuyển dọc
                    d_row = 1 if self.endRow > self.startRow else -1
                    for row in range(self.startRow + d_row, self.endRow, d_row):
                        if board[row][self.startCol] != "--":
                            return False

                # Kiểm tra nếu ô đích có quân cờ cùng màu với quân cờ di chuyển
                if board[self.endRow][self.endCol][0] == playerColor:
                    return False

                return True
            return False

        def isValidKyoshaMove(self, board):
            # Đảm bảo chỉ có thể di chuyển quân thương tiến về phía trước
            if self.pieceMoved.endswith("kyosha"):
                # Kiểm tra nếu quân Thương đang ở trên bàn cờ
                playerColor = self.pieceMoved[0]
                direction = -1 if playerColor == "w" else 1  # Di chuyển tiến về phía trước cho cả quân Đen và Trắng

                # Kiểm tra xem nước đi có nằm trên đường dọc và đi về phía trước không
                if self.startCol != self.endCol or direction * (self.endRow - self.startRow) <= 0:
                    return False

                # Kiểm tra xem có quân cản nào trên đường di chuyển không
                for row in range(self.startRow + direction, self.endRow, direction):
                    if board[row][self.startCol] != "--":
                        return False

                # Kiểm tra nếu ô đích có quân cờ cùng màu với quân cờ di chuyển
                if board[self.endRow][self.endCol][0] == playerColor:
                    return False

                return True
            return False

        def isValidKeimaMove(self, board):
            # Đảm bảo chỉ có thể di chuyển quân mã theo hình chữ L tiến
            if self.pieceMoved.endswith("keima"):
                playerColor = self.pieceMoved[0]
                direction = -1 if playerColor == "w" else 1  # Di chuyển tiến về phía trước cho cả quân Đen và Trắng

                # Kiểm tra xem nước đi có nằm trong hình chữ L tiến không
                valid_moves = [(self.startRow + 2 * direction, self.startCol + 1),
                               (self.startRow + 2 * direction, self.startCol - 1)]

                # Kiểm tra xem ô đích có nằm trong hình chữ L và không có quân cản hoặc là quân đối thủ không
                if (self.endRow, self.endCol) in valid_moves and (board[self.endRow][self.endCol] == "--" or
                                                                  board[self.endRow][self.endCol][0] != playerColor):
                    return True

            return False

        def isValidGinshoMove(self, board):
            # Đảm bảo chỉ có thể di chuyển quân bạc tiến về phía trước
            if self.pieceMoved.endswith("ginsho"):
                playerColor = self.pieceMoved[0]
                direction = -1 if playerColor == "w" else 1  # Di chuyển tiến về phía trước cho cả quân Đen và Trắng

                # Các hướng di chuyển cho quân Bạc (trừ 2 nước đi sang ngang và nước đi lùi thẳng phía sau)
                directions = [(1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]

                # Kiểm tra xem ô đích có nằm trong các ô xung quanh quân Bạc và không có quân cản hoặc là quân đối thủ không
                for d_row, d_col in directions:
                    r, c = self.startRow + direction * d_row, self.startCol + d_col
                    if (self.endRow, self.endCol) == (r, c) and (
                            board[self.endRow][self.endCol] == "--" or board[self.endRow][self.endCol][
                        0] != playerColor):
                        return True

            return False

        def isValidKinshoMove(self, board):
            # Đảm bảo chỉ có thể di chuyển quân Vàng tiến về phía trước hoặc chéo về phía trước
            if self.pieceMoved.endswith("kinsho"):
                playerColor = self.pieceMoved[0]
                direction = -1 if playerColor == "w" else 1  # Di chuyển tiến về phía trước cho cả quân Đen và Trắng

                # Các hướng di chuyển cho quân Vàng (trừ 2 nước đi lùi chéo phía sau)
                directions = [(1, 0), (1, 1), (1, -1), (-1, 0), (0, 1), (0, -1)]

                # Kiểm tra xem ô đích có nằm trong các ô xung quanh quân Vàng và không có quân cản hoặc là quân đối thủ không
                for d_row, d_col in directions:
                    r, c = self.startRow + direction * d_row, self.startCol + d_col
                    if (self.endRow, self.endCol) == (r, c) and (
                            board[self.endRow][self.endCol] == "--" or board[self.endRow][self.endCol][
                        0] != playerColor):
                        return True

            return False

        def isValidGyokushoMove(self, board):
            # Đảm bảo chỉ có thể di chuyển quân Vua tiến về phía trước hoặc chéo về phía trước
            if self.pieceMoved.endswith("gyokusho"):
                playerColor = self.pieceMoved[0]
                direction = -1 if playerColor == "w" else 1  # Di chuyển tiến về phía trước cho cả quân Đen và Trắng

                # Các hướng di chuyển cho quân Vua
                directions = [(1, 0), (1, 1), (1, -1), (-1, 0), (-1, 1), (-1, -1), (0, 1), (0, -1)]

                # Kiểm tra xem ô đích có nằm trong các ô xung quanh quân Vua và không có quân cản hoặc là quân đối thủ không
                for d_row, d_col in directions:
                    r, c = self.startRow + direction * d_row, self.startCol + d_col
                    if (self.endRow, self.endCol) == (r, c) and (
                            board[self.endRow][self.endCol] == "--" or board[self.endRow][self.endCol][
                        0] != playerColor):
                        return True

            return False

        def isValidTokinMove(self, board):
            # Đảm bảo chỉ có thể di chuyển quân Tốt phong cấp tiến về phía trước hoặc chéo về phía trước
            if self.pieceMoved.endswith("tokin"):
                playerColor = self.pieceMoved[0]
                direction = -1 if playerColor == "w" else 1  # Di chuyển tiến về phía trước cho cả quân Đen và Trắng

                # Các hướng di chuyển cho quân Vàng (trừ 2 nước đi lùi chéo phía sau)
                directions = [(1, 0), (1, 1), (1, -1), (-1, 0), (0, 1), (0, -1)]

                # Kiểm tra xem ô đích có nằm trong các ô xung quanh quân Tốt phong cấp và không có quân cản hoặc là quân đối thủ không
                for d_row, d_col in directions:
                    r, c = self.startRow + direction * d_row, self.startCol + d_col
                    if (self.endRow, self.endCol) == (r, c) and (
                            board[self.endRow][self.endCol] == "--" or board[self.endRow][self.endCol][
                        0] != playerColor):
                        return True

            return False

        def isValidNarikyoMove(self, board):
            # Đảm bảo chỉ có thể di chuyển quân Thương phong cấp tiến về phía trước hoặc chéo về phía trước
            if self.pieceMoved.endswith("narikyo"):
                playerColor = self.pieceMoved[0]
                direction = -1 if playerColor == "w" else 1  # Di chuyển tiến về phía trước cho cả quân Đen và Trắng

                # Các hướng di chuyển cho quân Vàng (trừ 2 nước đi lùi chéo phía sau)
                directions = [(1, 0), (1, 1), (1, -1), (-1, 0), (0, 1), (0, -1)]

                # Kiểm tra xem ô đích có nằm trong các ô xung quanh quân Thương phong cấp và không có quân cản hoặc là quân đối thủ không
                for d_row, d_col in directions:
                    r, c = self.startRow + direction * d_row, self.startCol + d_col
                    if (self.endRow, self.endCol) == (r, c) and (
                            board[self.endRow][self.endCol] == "--" or board[self.endRow][self.endCol][
                        0] != playerColor):
                        return True

            return False

        def isValidNarikeiMove(self, board):
            # Đảm bảo chỉ có thể di chuyển quân Mã phong cấp tiến về phía trước hoặc chéo về phía trước
            if self.pieceMoved.endswith("narikei"):
                playerColor = self.pieceMoved[0]
                direction = -1 if playerColor == "w" else 1  # Di chuyển tiến về phía trước cho cả quân Đen và Trắng

                # Các hướng di chuyển cho quân Vàng (trừ 2 nước đi lùi chéo phía sau)
                directions = [(1, 0), (1, 1), (1, -1), (-1, 0), (0, 1), (0, -1)]

                # Kiểm tra xem ô đích có nằm trong các ô xung quanh quân Mã phong cấp và không có quân cản hoặc là quân đối thủ không
                for d_row, d_col in directions:
                    r, c = self.startRow + direction * d_row, self.startCol + d_col
                    if (self.endRow, self.endCol) == (r, c) and (
                            board[self.endRow][self.endCol] == "--" or board[self.endRow][self.endCol][
                        0] != playerColor):
                        return True

            return False

        def isValidNariginMove(self, board):
            # Đảm bảo chỉ có thể di chuyển quân Bạc phong cấp tiến về phía trước hoặc chéo về phía trước
            if self.pieceMoved.endswith("narigin"):
                playerColor = self.pieceMoved[0]
                direction = -1 if playerColor == "w" else 1  # Di chuyển tiến về phía trước cho cả quân Đen và Trắng

                # Các hướng di chuyển cho quân Vàng (trừ 2 nước đi lùi chéo phía sau)
                directions = [(1, 0), (1, 1), (1, -1), (-1, 0), (0, 1), (0, -1)]

                # Kiểm tra xem ô đích có nằm trong các ô xung quanh quân Bạc phong cấp và không có quân cản hoặc là quân đối thủ không
                for d_row, d_col in directions:
                    r, c = self.startRow + direction * d_row, self.startCol + d_col
                    if (self.endRow, self.endCol) == (r, c) and (
                            board[self.endRow][self.endCol] == "--" or board[self.endRow][self.endCol][
                        0] != playerColor):
                        return True

            return False

        def isValidRyumaMove(self, board):
            # Kiểm tra nếu quân Vua
            if self.pieceMoved.endswith("ryuma"):
                playerColor = self.pieceMoved[0]
                direction = -1 if playerColor == "w" else 1  # Di chuyển tiến về phía trước cho cả quân Đen và Trắng

                # Các hướng di chuyển cho quân Vua (bao gồm cả đường chéo và tiến về phía trước)
                directions = [(1, 0), (1, 1), (1, -1), (-1, 0), (-1, 1), (-1, -1), (0, 1), (0, -1)]

                # Kiểm tra xem ô đích có nằm trong các ô xung quanh quân Vua và không có quân cản hoặc là quân đối thủ không
                for d_row, d_col in directions:
                    r, c = self.startRow + direction * d_row, self.startCol + d_col
                    if (self.endRow, self.endCol) == (r, c) and (
                            board[self.endRow][self.endCol] == "--" or board[self.endRow][self.endCol][
                        0] != playerColor):
                        return True

            # Kiểm tra nếu quân là Tượng
            if self.pieceMoved.endswith("ryuma"):
                # Kiểm tra nếu quân Tượng đang ở trên bàn cờ
                if self.pieceMoved[0] == "w":
                    playerColor = "w"
                else:
                    playerColor = "b"

                # Kiểm tra xem nước đi có nằm trên đường chéo không
                if abs(self.startRow - self.endRow) != abs(self.startCol - self.endCol):
                    return False

                # Kiểm tra xem có quân cờ nào ở giữa không
                d_row = 1 if self.endRow > self.startRow else -1
                d_col = 1 if self.endCol > self.startCol else -1
                r, c = self.startRow + d_row, self.startCol + d_col
                while r != self.endRow and c != self.endCol:
                    if board[r][c] != "--":
                        return False
                    r += d_row
                    c += d_col

                # Kiểm tra nếu ô đích có quân cờ cùng màu với quân cờ di chuyển
                if board[self.endRow][self.endCol][0] == playerColor:
                    return False

                return True

            return False

        def isValidRyuoMove(self, board):
            # Kiểm tra nếu quân Vua
            if self.pieceMoved.endswith("ryuo"):
                playerColor = self.pieceMoved[0]
                direction = -1 if playerColor == "w" else 1  # Di chuyển tiến về phía trước cho cả quân Đen và Trắng

                # Các hướng di chuyển cho quân Vua (bao gồm cả đường chéo và tiến về phía trước)
                directions = [(1, 0), (1, 1), (1, -1), (-1, 0), (-1, 1), (-1, -1), (0, 1), (0, -1)]

                # Kiểm tra xem ô đích có nằm trong các ô xung quanh quân Vua và không có quân cản hoặc là quân đối thủ không
                for d_row, d_col in directions:
                    r, c = self.startRow + direction * d_row, self.startCol + d_col
                    if (self.endRow, self.endCol) == (r, c) and (
                            board[self.endRow][self.endCol] == "--" or board[self.endRow][self.endCol][
                        0] != playerColor):
                        return True

            # Kiểm tra nếu quân là Xe
            if self.pieceMoved.endswith("ryuo"):
                # Kiểm tra nếu quân Xe đang ở trên bàn cờ
                if self.pieceMoved[0] == "w":
                    playerColor = "w"
                else:
                    playerColor = "b"

                # Kiểm tra xem nước đi có nằm trên đường ngang hoặc đứng không
                if self.startRow != self.endRow and self.startCol != self.endCol:
                    return False

                # Kiểm tra xem có quân cờ nào ở giữa không
                if self.startRow == self.endRow:  # Di chuyển ngang
                    d_col = 1 if self.endCol > self.startCol else -1
                    for col in range(self.startCol + d_col, self.endCol, d_col):
                        if board[self.startRow][col] != "--":
                            return False
                else:  # Di chuyển dọc
                    d_row = 1 if self.endRow > self.startRow else -1
                    for row in range(self.startRow + d_row, self.endRow, d_row):
                        if board[row][self.startCol] != "--":
                            return False

                # Kiểm tra nếu ô đích có quân cờ cùng màu với quân cờ di chuyển
                if board[self.endRow][self.endCol][0] == playerColor:
                    return False

                return True
            return False

        def getChessNotation(self):
            return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)

        def getRankFile(self, r, c):
            return self.colsToFiles[c] + self.rowsToRanks[r]

    main()
