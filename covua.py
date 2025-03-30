import pygame as p
import sys
import random

BOARD_WIDTH = BOARD_HEIGHT = 800
DIMENSION = 8 # số hàng,cột trên bàn cờ
SQUARE_SIZE = BOARD_HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}

def loadImages():
   # Hàm dùng để tải hình ảnh các quân cờ từ thư mục image có sẵn
    pieces = ['wp', 'wR', 'wN', 'wB', 'wK', 'wQ', 'bp', 'bR', 'bN', 'bB', 'bK', 'bQ']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load(piece + ".png"), (SQUARE_SIZE, SQUARE_SIZE))

# transform.scale : điều chỉnh kích thước hình ảnh theo hình vuông
def main():
    """
    The main driver for our code.
    This will handle user input and updating the graphics.
    """
    p.init() #Khởi tạo pygame
    p.display.set_caption('Cờ Vua') # đổi tên cửa sổ
    p.display.set_icon(p.image.load('bK.png')) # đổi logo cửa sổ
    p.mixer.init()
    screen = p.display.set_mode((BOARD_WIDTH, BOARD_HEIGHT)) # tạo cửa sổ trò chơi
    clock = p.time.Clock() # > kiểm soát tốc độ khung hình và thời gian
    screen.fill(p.Color("white")) #để board full white
    game_state = GameState()
    valid_moves = game_state.getValidMoves() # lấy list nước đi hợp lệ cho lượt hiên tại
    move_made = False  # flag variable xem nước đi mới đã thực hiện chưa
    animate = False  # flag variable for when we should animate a move
    loadImages()  # do this only once before while loop
    running = True
    square_selected = ()  # no square is selected initially, this will keep track of the last click of the user (tuple(row,col))
    player_clicks = []  # this will keep track of player clicks (two tuples)
    game_over = False
    player_one = True  # if a human is playing white, then this will be True, else False
    player_two = True  # if a human is playing black, then this will be True, else False

    while running:
        human_turn = (game_state.white_to_move and player_one) or (not game_state.white_to_move and player_two)
        for e in p.event.get():
            if e.type == p.QUIT:
                p.quit()
                sys.exit()
            elif e.type == p.MOUSEBUTTONDOWN:
                if not game_over:
                    location = p.mouse.get_pos()  # (x, y) location of the mouse
                    col = location[0] // SQUARE_SIZE
                    row = location[1] // SQUARE_SIZE
                    if square_selected == (row, col) or col >= 8:  # user clicked the same square twice
                        square_selected = ()  # deselect
                        player_clicks = []  # clear clicks
                    else:
                        square_selected = (row, col)
                        player_clicks.append(square_selected)  # append for both 1st and 2nd click
                    if len(player_clicks) == 2 and human_turn:  # after 2nd click
                        move = Move(player_clicks[0], player_clicks[1], game_state.board)
                        for i in range(len(valid_moves)):
                            if move == valid_moves[i]:
                                game_state.makeMove(valid_moves[i])
                                move_made = True
                                animate = True
                                square_selected = ()  # reset user clicks
                                player_clicks = []
                        if not move_made:
                            player_clicks = [square_selected]

        if move_made:
            if animate:
                animateMove(game_state.move_log[-1], screen, game_state.board, clock)
            valid_moves = game_state.getValidMoves()
            move_made = False
            animate = False

        drawGameState(screen, game_state, valid_moves, square_selected)

        if game_state.checkmate:
            game_over = True
            if game_state.white_to_move:
                drawEndGameText(screen, "Đen Chiến Thắng!", 'red')
            else:
                drawEndGameText(screen, "Trắng Chiến Thắng!", 'green')
            p.display.flip()
            p.time.wait(20000)
            break

        elif game_state.stalemate:
            game_over = True
            drawEndGameText(screen, "Hòa!", 'orange')
            p.display.flip()
            p.time.wait(20000)
            break

        clock.tick(MAX_FPS)
        p.display.flip()

    p.quit()
    sys.exit()

def drawGameState(screen, game_state, valid_moves, square_selected):
    """
    Responsible for all the graphics within current game state.
    """
    drawBoard(screen)  # draw squares on the board
    highlightSquares(screen, game_state, valid_moves, square_selected)
    drawPieces(screen, game_state.board)  # draw pieces on top of those squares

def drawBoard(screen):
    """
    Draw the squares on the board.
    The top left square is always light.
    """
    global colors
    colors = [p.Color("white"), p.Color("gray")]
    for row in range(DIMENSION):
        for column in range(DIMENSION):
            color = colors[((row + column) % 2)]
            p.draw.rect(screen, color, p.Rect(column * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

def highlightSquares(screen, game_state, valid_moves, square_selected):
    """
    Highlight square selected and moves for piece selected.
    """
    if (len(game_state.move_log)) > 0:
        last_move = game_state.move_log[-1]
        s = p.Surface((SQUARE_SIZE, SQUARE_SIZE))
        s.set_alpha(100)
        s.fill(p.Color('green'))
        screen.blit(s, (last_move.end_col * SQUARE_SIZE, last_move.end_row * SQUARE_SIZE))
    if square_selected != ():
        row, col = square_selected
        if game_state.board[row][col][0] == (
                'w' if game_state.white_to_move else 'b'):  # square_selected is a piece that can be moved
            # highlight selected square
            s = p.Surface((SQUARE_SIZE, SQUARE_SIZE))
            s.set_alpha(100)  # transparency value 0 -> transparent, 255 -> opaque
            s.fill(p.Color('blue'))
            screen.blit(s, (col * SQUARE_SIZE, row * SQUARE_SIZE))
            # highlight moves from that square
            s.fill(p.Color('yellow'))
            for move in valid_moves:
                if move.start_row == row and move.start_col == col:
                    screen.blit(s, (move.end_col * SQUARE_SIZE, move.end_row * SQUARE_SIZE))

def drawPieces(screen, board):
    """
    Draw the pieces on the board using the current game_state.board
    """
    for row in range(DIMENSION):
        for column in range(DIMENSION):
            piece = board[row][column]
            if piece != "--":
                screen.blit(IMAGES[piece], p.Rect(column * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

def drawEndGameText(screen, text, color):
    font = p.font.Font('arial-unicode-ms.ttf', 36)
    text_object = font.render(text, False, p.Color('brown'))
    text_location = p.Rect(0, 0, BOARD_WIDTH, BOARD_HEIGHT).move(BOARD_WIDTH / 2 - text_object.get_width() / 2,
                                                                 BOARD_HEIGHT / 2 - text_object.get_height() / 2)
    screen.blit(text_object, text_location)
    text_object = font.render(text, False, p.Color(color))
    screen.blit(text_object, text_location.move(2, 2))

def animateMove(move, screen, board, clock):
    """
    Animating a move
    """
    global colors
    d_row = move.end_row - move.start_row
    d_col = move.end_col - move.start_col
    frames_per_square = 10  # frames to move one square
    frame_count = (abs(d_row) + abs(d_col)) * frames_per_square
    for frame in range(frame_count + 1):
        row, col = (move.start_row + d_row * frame / frame_count, move.start_col + d_col * frame / frame_count)
        drawBoard(screen)
        drawPieces(screen, board)
        # erase the piece moved from its ending square
        color = colors[(move.end_row + move.end_col) % 2]
        end_square = p.Rect(move.end_col * SQUARE_SIZE, move.end_row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
        p.draw.rect(screen, color, end_square)
        # draw captured piece onto rectangle
        if move.piece_captured != '--':
            if move.is_enpassant_move:
                enpassant_row = move.end_row + 1 if move.piece_captured[0] == 'b' else move.end_row - 1
                end_square = p.Rect(move.end_col * SQUARE_SIZE, enpassant_row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
            screen.blit(IMAGES[move.piece_captured], end_square)
        # draw moving piece
        screen.blit(IMAGES[move.piece_moved], p.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
        p.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    class GameState:
        def __init__(self):
            self.board = [
                ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
                ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
                ["--", "--", "--", "--", "--", "--", "--", "--"],
                ["--", "--", "--", "--", "--", "--", "--", "--"],
                ["--", "--", "--", "--", "--", "--", "--", "--"],
                ["--", "--", "--", "--", "--", "--", "--", "--"],
                ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
                ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]]
            self.moveFunctions = {"p": self.getPawnMoves, "R": self.getRookMoves, "N": self.getKnightMoves,
                                  "B": self.getBishopMoves, "Q": self.getQueenMoves, "K": self.getKingMoves}
            self.white_to_move = True
            self.move_log = []
            self.white_king_location = (7, 4)
            self.black_king_location = (0, 4)
            self.checkmate = False
            self.stalemate = False
            self.in_check = False
            self.pins = []
            self.checks = []
            self.enpassant_possible = ()  # coordinates for the square where en-passant capture is possible
            self.enpassant_possible_log = [self.enpassant_possible]
            self.current_castling_rights = CastleRights(True, True, True, True)
            self.castle_rights_log = [CastleRights(self.current_castling_rights.wks, self.current_castling_rights.bks,
                                                   self.current_castling_rights.wqs, self.current_castling_rights.bqs)]
            self.move_sound = p.mixer.Sound("move.wav")
            self.capture_sound = p.mixer.Sound("capture.wav")

        def makeMove(self, move):
            # Thực hiện nước đi được chọn và cập nhật trạng thái trò chơi
            self.board[move.start_row][move.start_col] = "--"
            self.board[move.end_row][move.end_col] = move.piece_moved
            self.move_log.append(move)
            self.white_to_move = not self.white_to_move
            # update king's location if moved
            if move.piece_moved == "wK":
                self.white_king_location = (move.end_row, move.end_col)
            elif move.piece_moved == "bK":
                self.black_king_location = (move.end_row, move.end_col)

            # pawn promotion
            if move.is_pawn_promotion:
                # if not is_AI:
                #    promoted_piece = input("Promote to Q, R, B, or N:") #take this to UI later
                #    self.board[move.end_row][move.end_col] = move.piece_moved[0] + promoted_piece
                # else:
                promoted_piece = random.choice(["Q", "R", "B", "N"])
                self.board[move.end_row][move.end_col] = move.piece_moved[0] + promoted_piece

            # enpassant move
            if move.is_enpassant_move:
                self.board[move.start_row][move.end_col] = "--"  # capturing the pawn

            # update enpassant_possible variable
            if move.piece_moved[1] == "p" and abs(move.start_row - move.end_row) == 2:  # only on 2 square pawn advance
                self.enpassant_possible = ((move.start_row + move.end_row) // 2, move.start_col)
            else:
                self.enpassant_possible = ()

            # castle move
            if move.is_castle_move:
                if move.end_col - move.start_col == 2:  # king-side castle move
                    self.board[move.end_row][move.end_col - 1] = self.board[move.end_row][
                        move.end_col + 1]  # moves the rook to its new square
                    self.board[move.end_row][move.end_col + 1] = '--'  # erase old rook
                else:  # queen-side castle move
                    self.board[move.end_row][move.end_col + 1] = self.board[move.end_row][
                        move.end_col - 2]  # moves the rook to its new square
                    self.board[move.end_row][move.end_col - 2] = '--'  # erase old rook

            self.enpassant_possible_log.append(self.enpassant_possible)

            # update quyền được phép nhập thành
            self.updateCastleRights(move)
            self.castle_rights_log.append(
                CastleRights(self.current_castling_rights.wks, self.current_castling_rights.bks,
                             self.current_castling_rights.wqs, self.current_castling_rights.bqs))

            # Play sound effects based on move type
            if move.is_capture:
                self.capture_sound.play()
            else:
                self.move_sound.play()

        def updateCastleRights(self, move):
            """
            Update the castle rights given the move
            """
            if move.piece_captured == "wR":
                if move.end_col == 0:  # left rook
                    self.current_castling_rights.wqs = False
                elif move.end_col == 7:  # right rook
                    self.current_castling_rights.wks = False
            elif move.piece_captured == "bR":
                if move.end_col == 0:  # left rook
                    self.current_castling_rights.bqs = False
                elif move.end_col == 7:  # right rook
                    self.current_castling_rights.bks = False

            if move.piece_moved == 'wK':
                self.current_castling_rights.wqs = False
                self.current_castling_rights.wks = False
            elif move.piece_moved == 'bK':
                self.current_castling_rights.bqs = False
                self.current_castling_rights.bks = False
            elif move.piece_moved == 'wR':
                if move.start_row == 7:
                    if move.start_col == 0:  # left rook
                        self.current_castling_rights.wqs = False
                    elif move.start_col == 7:  # right rook
                        self.current_castling_rights.wks = False
            elif move.piece_moved == 'bR':
                if move.start_row == 0:
                    if move.start_col == 0:  # left rook
                        self.current_castling_rights.bqs = False
                    elif move.start_col == 7:  # right rook
                        self.current_castling_rights.bks = False

        def getValidMoves(self):
            """
            All moves considering checks.
            """
            temp_castle_rights = CastleRights(self.current_castling_rights.wks, self.current_castling_rights.bks,
                                              self.current_castling_rights.wqs, self.current_castling_rights.bqs)
            # advanced algorithm
            moves = []
            self.in_check, self.pins, self.checks = self.checkForPinsAndChecks()

            if self.white_to_move:
                king_row = self.white_king_location[0]
                king_col = self.white_king_location[1]
            else:
                king_row = self.black_king_location[0]
                king_col = self.black_king_location[1]
            if self.in_check:
                if len(self.checks) == 1:  # only 1 check, block the check or move the king
                    moves = self.getAllPossibleMoves()
                    # to block the check you must put a piece into one of the squares between the enemy piece and your king
                    check = self.checks[0]  # check information
                    check_row = check[0]
                    check_col = check[1]
                    piece_checking = self.board[check_row][check_col]
                    valid_squares = []  # squares that pieces can move to
                    # if knight, must capture the knight or move your king, other pieces can be blocked
                    if piece_checking[1] == "N":
                        valid_squares = [(check_row, check_col)]
                    else:
                        for i in range(1, 8):
                            valid_square = (king_row + check[2] * i,
                                            king_col + check[3] * i)  # check[2] and check[3] are the check directions
                            valid_squares.append(valid_square)
                            if valid_square[0] == check_row and valid_square[
                                1] == check_col:  # once you get to piece and check
                                break
                    # get rid of any moves that don't block check or move king
                    for i in range(len(moves) - 1, -1, -1):  # iterate through the list backwards when removing elements
                        if moves[i].piece_moved[1] != "K":  # move doesn't move king so it must block or capture
                            if not (moves[i].end_row,
                                    moves[i].end_col) in valid_squares:  # move doesn't block or capture piece
                                moves.remove(moves[i])
                else:  # double check, king has to move
                    self.getKingMoves(king_row, king_col, moves)
            else:  # not in check - all moves are fine
                moves = self.getAllPossibleMoves()
                if self.white_to_move:
                    self.getCastleMoves(self.white_king_location[0], self.white_king_location[1], moves)
                else:
                    self.getCastleMoves(self.black_king_location[0], self.black_king_location[1], moves)

            if len(moves) == 0:
                if self.inCheck():
                    self.checkmate = True
                else:
                    # TODO stalemate on repeated moves
                    self.stalemate = True
            else:
                self.checkmate = False
                self.stalemate = False

            self.current_castling_rights = temp_castle_rights
            return moves

        def inCheck(self):
            """
            Determine if a current player is in check
            """
            if self.white_to_move:
                return self.squareUnderAttack(self.white_king_location[0], self.white_king_location[1])
            else:
                return self.squareUnderAttack(self.black_king_location[0], self.black_king_location[1])

        def squareUnderAttack(self, row, col):
            """
            Determine if enemy can attack the square row col
            """
            self.white_to_move = not self.white_to_move  # switch to opponent's point of view
            opponents_moves = self.getAllPossibleMoves()
            self.white_to_move = not self.white_to_move
            for move in opponents_moves:
                if move.end_row == row and move.end_col == col:  # square is under attack
                    return True
            return False

        def getAllPossibleMoves(self):
            """
            All moves without considering checks.
            """
            moves = []
            for row in range(len(self.board)):
                for col in range(len(self.board[row])):
                    turn = self.board[row][col][0]
                    if (turn == "w" and self.white_to_move) or (turn == "b" and not self.white_to_move):
                        piece = self.board[row][col][1]
                        self.moveFunctions[piece](row, col,
                                                  moves)  # calls appropriate move function based on piece type
            return moves

        def checkForPinsAndChecks(self):
            pins = []  # squares pinned and the direction its pinned from
            checks = []  # squares where enemy is applying a check
            in_check = False
            if self.white_to_move:
                enemy_color = "b"
                ally_color = "w"
                start_row = self.white_king_location[0]
                start_col = self.white_king_location[1]
            else:
                enemy_color = "w"
                ally_color = "b"
                start_row = self.black_king_location[0]
                start_col = self.black_king_location[1]
            # check outwards from king for pins and checks, keep track of pins
            directions = ((-1, 0), (0, -1), (1, 0), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1))
            for j in range(len(directions)):
                direction = directions[j]
                possible_pin = ()  # reset possible pins
                for i in range(1, 8):
                    end_row = start_row + direction[0] * i
                    end_col = start_col + direction[1] * i
                    if 0 <= end_row <= 7 and 0 <= end_col <= 7:
                        end_piece = self.board[end_row][end_col]
                        if end_piece[0] == ally_color and end_piece[1] != "K":
                            if possible_pin == ():  # first allied piece could be pinned
                                possible_pin = (end_row, end_col, direction[0], direction[1])
                            else:  # 2nd allied piece - no check or pin from this direction
                                break
                        elif end_piece[0] == enemy_color:
                            enemy_type = end_piece[1]
                            # 5 possibilities in this complex conditional
                            # 1.) orthogonally away from king and piece is a rook
                            # 2.) diagonally away from king and piece is a bishop
                            # 3.) 1 square away diagonally from king and piece is a pawn
                            # 4.) any direction and piece is a queen
                            # 5.) any direction 1 square away and piece is a king
                            if (0 <= j <= 3 and enemy_type == "R") or (4 <= j <= 7 and enemy_type == "B") or (
                                    i == 1 and enemy_type == "p" and (
                                    (enemy_color == "w" and 6 <= j <= 7) or (enemy_color == "b" and 4 <= j <= 5))) or (
                                    enemy_type == "Q") or (i == 1 and enemy_type == "K"):
                                if possible_pin == ():  # no piece blocking, so check
                                    in_check = True
                                    checks.append((end_row, end_col, direction[0], direction[1]))
                                    break
                                else:  # piece blocking so pin
                                    pins.append(possible_pin)
                                    break
                            else:  # enemy piece not applying checks
                                break
                    else:
                        break  # off board
            # check for knight checks
            knight_moves = ((-2, -1), (-2, 1), (-1, 2), (1, 2), (2, -1), (2, 1), (-1, -2), (1, -2))
            for move in knight_moves:
                end_row = start_row + move[0]
                end_col = start_col + move[1]
                if 0 <= end_row <= 7 and 0 <= end_col <= 7:
                    end_piece = self.board[end_row][end_col]
                    if end_piece[0] == enemy_color and end_piece[1] == "N":  # enemy knight attacking a king
                        in_check = True
                        checks.append((end_row, end_col, move[0], move[1]))
            return in_check, pins, checks

        def getPawnMoves(self, row, col, moves):

            piece_pinned = False
            pin_direction = ()
            for i in range(len(self.pins) - 1, -1, -1):
                if self.pins[i][0] == row and self.pins[i][1] == col:
                    piece_pinned = True
                    pin_direction = (self.pins[i][2], self.pins[i][3])
                    self.pins.remove(self.pins[i])
                    break

            if self.white_to_move:
                move_amount = -1
                start_row = 6
                enemy_color = "b"
                king_row, king_col = self.white_king_location
            else:
                move_amount = 1
                start_row = 1
                enemy_color = "w"
                king_row, king_col = self.black_king_location

            if self.board[row + move_amount][col] == "--":  # 1 square pawn advance
                if not piece_pinned or pin_direction == (move_amount, 0):
                    moves.append(Move((row, col), (row + move_amount, col), self.board))
                    if row == start_row and self.board[row + 2 * move_amount][col] == "--":  # 2 square pawn advance
                        moves.append(Move((row, col), (row + 2 * move_amount, col), self.board))
            if col - 1 >= 0:  # capture to the left
                if not piece_pinned or pin_direction == (move_amount, -1):
                    if self.board[row + move_amount][col - 1][0] == enemy_color:
                        moves.append(Move((row, col), (row + move_amount, col - 1), self.board))
                    if (row + move_amount, col - 1) == self.enpassant_possible:
                        attacking_piece = blocking_piece = False
                        if king_row == row:
                            if king_col < col:  # king is left of the pawn
                                # inside: between king and the pawn;
                                # outside: between pawn and border;
                                inside_range = range(king_col + 1, col - 1)
                                outside_range = range(col + 1, 8)
                            else:  # king right of the pawn
                                inside_range = range(king_col - 1, col, -1)
                                outside_range = range(col - 2, -1, -1)
                            for i in inside_range:
                                if self.board[row][i] != "--":  # some piece beside en-passant pawn blocks
                                    blocking_piece = True
                            for i in outside_range:
                                square = self.board[row][i]
                                if square[0] == enemy_color and (square[1] == "R" or square[1] == "Q"):
                                    attacking_piece = True
                                elif square != "--":
                                    blocking_piece = True
                        if not attacking_piece or blocking_piece:
                            moves.append(
                                Move((row, col), (row + move_amount, col - 1), self.board, is_enpassant_move=True))
            if col + 1 <= 7:  # capture to the right
                if not piece_pinned or pin_direction == (move_amount, +1):
                    if self.board[row + move_amount][col + 1][0] == enemy_color:
                        moves.append(Move((row, col), (row + move_amount, col + 1), self.board))
                    if (row + move_amount, col + 1) == self.enpassant_possible:
                        attacking_piece = blocking_piece = False
                        if king_row == row:
                            if king_col < col:  # king is left of the pawn
                                # inside: between king and the pawn;
                                # outside: between pawn and border;
                                inside_range = range(king_col + 1, col)
                                outside_range = range(col + 2, 8)
                            else:  # king right of the pawn
                                inside_range = range(king_col - 1, col + 1, -1)
                                outside_range = range(col - 1, -1, -1)
                            for i in inside_range:
                                if self.board[row][i] != "--":  # some piece beside en-passant pawn blocks
                                    blocking_piece = True
                            for i in outside_range:
                                square = self.board[row][i]
                                if square[0] == enemy_color and (square[1] == "R" or square[1] == "Q"):
                                    attacking_piece = True
                                elif square != "--":
                                    blocking_piece = True
                        if not attacking_piece or blocking_piece:
                            moves.append(
                                Move((row, col), (row + move_amount, col + 1), self.board, is_enpassant_move=True))

        def getRookMoves(self, row, col, moves):
            """
            Get all the rook moves for the rook located at row, col and add the moves to the list.
            """
            piece_pinned = False
            pin_direction = ()
            for i in range(len(self.pins) - 1, -1, -1):
                if self.pins[i][0] == row and self.pins[i][1] == col:
                    piece_pinned = True
                    pin_direction = (self.pins[i][2], self.pins[i][3])
                    if self.board[row][col][
                        1] != "Q":  # can't remove queen from pin on rook moves, only remove it on bishop moves
                        self.pins.remove(self.pins[i])
                    break

            directions = ((-1, 0), (0, -1), (1, 0), (0, 1))  # up, left, down, right
            enemy_color = "b" if self.white_to_move else "w"
            for direction in directions:
                for i in range(1, 8):
                    end_row = row + direction[0] * i
                    end_col = col + direction[1] * i
                    if 0 <= end_row <= 7 and 0 <= end_col <= 7:  # check for possible moves only in boundaries of the board
                        if not piece_pinned or pin_direction == direction or pin_direction == (
                                -direction[0], -direction[1]):
                            end_piece = self.board[end_row][end_col]
                            if end_piece == "--":  # empty space is valid
                                moves.append(Move((row, col), (end_row, end_col), self.board))
                            elif end_piece[0] == enemy_color:  # capture enemy piece
                                moves.append(Move((row, col), (end_row, end_col), self.board))
                                break
                            else:  # friendly piece
                                break
                    else:  # off board
                        break

        def getKnightMoves(self, row, col, moves):
            """
            Get all the knight moves for the knight located at row col and add the moves to the list.
            """
            piece_pinned = False
            for i in range(len(self.pins) - 1, -1, -1):
                if self.pins[i][0] == row and self.pins[i][1] == col:
                    piece_pinned = True
                    self.pins.remove(self.pins[i])
                    break

            knight_moves = ((-2, -1), (-2, 1), (-1, 2), (1, 2), (2, -1), (2, 1), (-1, -2),
                            (1, -2))  # up/left up/right right/up right/down down/left down/right left/up left/down
            ally_color = "w" if self.white_to_move else "b"
            for move in knight_moves:
                end_row = row + move[0]
                end_col = col + move[1]
                if 0 <= end_row <= 7 and 0 <= end_col <= 7:
                    if not piece_pinned:
                        end_piece = self.board[end_row][end_col]
                        if end_piece[0] != ally_color:  # so its either enemy piece or empty square
                            moves.append(Move((row, col), (end_row, end_col), self.board))

        def getBishopMoves(self, row, col, moves):
            """
            Get all the bishop moves for the bishop located at row col and add the moves to the list.
            """
            piece_pinned = False
            pin_direction = ()
            for i in range(len(self.pins) - 1, -1, -1):
                if self.pins[i][0] == row and self.pins[i][1] == col:
                    piece_pinned = True
                    pin_direction = (self.pins[i][2], self.pins[i][3])
                    self.pins.remove(self.pins[i])
                    break

            directions = ((-1, -1), (-1, 1), (1, 1), (1, -1))  # diagonals: up/left up/right down/right down/left
            enemy_color = "b" if self.white_to_move else "w"
            for direction in directions:
                for i in range(1, 8):
                    end_row = row + direction[0] * i
                    end_col = col + direction[1] * i
                    if 0 <= end_row <= 7 and 0 <= end_col <= 7:  # check if the move is on board
                        if not piece_pinned or pin_direction == direction or pin_direction == (
                                -direction[0], -direction[1]):
                            end_piece = self.board[end_row][end_col]
                            if end_piece == "--":  # empty space is valid
                                moves.append(Move((row, col), (end_row, end_col), self.board))
                            elif end_piece[0] == enemy_color:  # capture enemy piece
                                moves.append(Move((row, col), (end_row, end_col), self.board))
                                break
                            else:  # friendly piece
                                break
                    else:  # off board
                        break

        def getQueenMoves(self, row, col, moves):
            """
            Get all the queen moves for the queen located at row col and add the moves to the list.
            """
            self.getBishopMoves(row, col, moves)
            self.getRookMoves(row, col, moves)

        def getKingMoves(self, row, col, moves):
            """
            Get all the king moves for the king located at row col and add the moves to the list.
            """
            row_moves = (-1, -1, -1, 0, 0, 1, 1, 1)
            col_moves = (-1, 0, 1, -1, 1, -1, 0, 1)
            ally_color = "w" if self.white_to_move else "b"
            for i in range(8):
                end_row = row + row_moves[i]
                end_col = col + col_moves[i]
                if 0 <= end_row <= 7 and 0 <= end_col <= 7:
                    end_piece = self.board[end_row][end_col]
                    if end_piece[0] != ally_color:  # not an ally piece - empty or enemy
                        # place king on end square and check for checks
                        if ally_color == "w":
                            self.white_king_location = (end_row, end_col)
                        else:
                            self.black_king_location = (end_row, end_col)
                        in_check, pins, checks = self.checkForPinsAndChecks()
                        if not in_check:
                            moves.append(Move((row, col), (end_row, end_col), self.board))
                        # place king back on original location
                        if ally_color == "w":
                            self.white_king_location = (row, col)
                        else:
                            self.black_king_location = (row, col)

        def getCastleMoves(self, row, col, moves):
            """
            Generate all valid castle moves for the king at (row, col) and add them to the list of moves.
            """
            if self.squareUnderAttack(row, col):
                return  # can't castle while in check
            if (self.white_to_move and self.current_castling_rights.wks) or (
                    not self.white_to_move and self.current_castling_rights.bks):
                self.getKingsideCastleMoves(row, col, moves)
            if (self.white_to_move and self.current_castling_rights.wqs) or (
                    not self.white_to_move and self.current_castling_rights.bqs):
                self.getQueensideCastleMoves(row, col, moves)

        def getKingsideCastleMoves(self, row, col, moves):
            if self.board[row][col + 1] == '--' and self.board[row][col + 2] == '--':
                if not self.squareUnderAttack(row, col + 1) and not self.squareUnderAttack(row, col + 2):
                    moves.append(Move((row, col), (row, col + 2), self.board, is_castle_move=True))

        def getQueensideCastleMoves(self, row, col, moves):
            if self.board[row][col - 1] == '--' and self.board[row][col - 2] == '--' and self.board[row][col - 3] == '--':
                if not self.squareUnderAttack(row, col - 1) and not self.squareUnderAttack(row, col - 2):
                    moves.append(Move((row, col), (row, col - 2), self.board, is_castle_move=True))

    class CastleRights:
        def __init__(self, wks, bks, wqs, bqs):
            self.wks = wks
            self.bks = bks
            self.wqs = wqs
            self.bqs = bqs

    class Move:
        # in chess, fields on the board are described by two symbols, one of them being number between 1-8 (which is corresponding to rows)
        # and the second one being a letter between a-f (corresponding to columns), in order to use this notation we need to map our [row][col] coordinates
        # to match the ones used in the original chess game
        ranks_to_rows = {"1": 7, "2": 6, "3": 5, "4": 4,
                         "5": 3, "6": 2, "7": 1, "8": 0}
        rows_to_ranks = {v: k for k, v in ranks_to_rows.items()}
        files_to_cols = {"a": 0, "b": 1, "c": 2, "d": 3,
                         "e": 4, "f": 5, "g": 6, "h": 7}
        cols_to_files = {v: k for k, v in files_to_cols.items()}

        def __init__(self, start_square, end_square, board, is_enpassant_move=False, is_castle_move=False):
            self.start_row = start_square[0]
            self.start_col = start_square[1]
            self.end_row = end_square[0]
            self.end_col = end_square[1]
            self.piece_moved = board[self.start_row][self.start_col]
            self.piece_captured = board[self.end_row][self.end_col]
            # pawn promotion
            self.is_pawn_promotion = (self.piece_moved == "wp" and self.end_row == 0) or (
                    self.piece_moved == "bp" and self.end_row == 7)
            # en passant
            self.is_enpassant_move = is_enpassant_move
            if self.is_enpassant_move:
                self.piece_captured = "wp" if self.piece_moved == "bp" else "bp"
            # castle move
            self.is_castle_move = is_castle_move

            self.is_capture = self.piece_captured != "--"
            self.moveID = self.start_row * 1000 + self.start_col * 100 + self.end_row * 10 + self.end_col

        def __eq__(self, other):
            """
            Overriding the equals method.
            """
            if isinstance(other, Move):
                return self.moveID == other.moveID
            return False

        def getChessNotation(self):
            if self.is_pawn_promotion:
                return self.getRankFile(self.end_row, self.end_col) + "Q"
            if self.is_castle_move:
                if self.end_col == 1:
                    return "0-0-0"
                else:
                    return "0-0"
            if self.is_enpassant_move:
                return self.getRankFile(self.start_row, self.start_col)[0] + "x" + self.getRankFile(self.end_row,
                                                                                                    self.end_col) + " e.p."
            if self.piece_captured != "--":
                if self.piece_moved[1] == "p":
                    return self.getRankFile(self.start_row, self.start_col)[0] + "x" + self.getRankFile(self.end_row,
                                                                                                        self.end_col)
                else:
                    return self.piece_moved[1] + "x" + self.getRankFile(self.end_row, self.end_col)
            else:
                if self.piece_moved[1] == "p":
                    return self.getRankFile(self.end_row, self.end_col)
                else:
                    return self.piece_moved[1] + self.getRankFile(self.end_row, self.end_col)

            # TODO Disambiguating moves

        def getRankFile(self, row, col):
            return self.cols_to_files[col] + self.rows_to_ranks[row]

        def __str__(self):
            if self.is_castle_move:
                return "0-0" if self.end_col == 6 else "0-0-0"

            end_square = self.getRankFile(self.end_row, self.end_col)

            if self.piece_moved[1] == "p":
                if self.is_capture:
                    return self.cols_to_files[self.start_col] + "x" + end_square
                else:
                    return end_square + "Q" if self.is_pawn_promotion else end_square

            move_string = self.piece_moved[1]
            if self.is_capture:
                move_string += "x"
            return move_string + end_square

    main()
