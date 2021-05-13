from Chess import ChessMain


class GameState:
    """
    Class responsible for storing information about the current state of the game.
    The functions within this class are responsible for how moves are made, undone,
    determining valid moves given the current state, and keeping a move log.
    """

    def __init__(self):
        """
        The board is a 8x8 2d list. Each element has 2 characters.
        1st character represents the colour of the piece (b/w).
        2nd character represents the type of the piece.
        "--" represents an empty space with no piece.
        """
        self.board = [
            ['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
            ['bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
            ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR']]
        self.move_functions = {'P': self.get_pawn_moves, 'R': self.get_rook_moves, 'N': self.get_knight_moves,
                               'B': self.get_bishop_moves, 'Q': self.get_queen_moves, 'K': self.get_king_moves}
        self.white_to_move = True
        self.move_log = []
        self.white_king_location = (7, 4)
        self.black_king_location = (0, 4)
        self.checkmate = False
        self.stalemate = False
        self.in_check = False
        self.pins = []
        self.checks = []

        # En passant
        self.en_passant_possible = ()  # Coordinates for square where en passant possible
        self.en_passant_possible_log = [self.en_passant_possible]

        # Castling
        self.white_castle_king_side = True
        self.white_castle_queen_side = True
        self.black_castle_king_side = True
        self.black_castle_queen_side = True
        self.castle_rights_log = [CastleRights(self.white_castle_king_side, self.black_castle_king_side,
                                               self.white_castle_queen_side, self.black_castle_queen_side)]

    def make_move(self, move):
        """Takes a move as a parameter, executes it, and updates move log"""
        global promoted_piece

        self.board[move.start_row][move.start_column] = '--'  # When a piece is moved, the square it leaves is blank
        self.board[move.end_row][move.end_column] = move.piece_moved  # Moves piece to new location
        self.move_log.append(move)  # Logs move

        if move.piece_moved == 'wK':
            self.white_king_location = (move.end_row, move.end_column)
        elif move.piece_moved == 'bK':
            self.black_king_location = (move.end_row, move.end_column)

        # Pawn promotion
        if move.is_pawn_promotion:

            # Player turn
            if (self.white_to_move and ChessMain.player_one) or (not self.white_to_move and ChessMain.player_two):
                promoted_piece = input('Promote to Q(ueen), R(ook), B(ishop), or (k)N(ight):').upper()

            else:  # AI turn
                promoted_piece = 'Q'

            self.board[move.end_row][move.end_column] = move.piece_moved[0] + promoted_piece

        # En passant
        if move.is_en_passant_move:
            self.board[move.start_row][move.end_column] = '--'  # Capturing the pawn

        # Updates the en_passant_possible variable
        if move.piece_moved[1] == 'P' and abs(move.start_row - move.end_row) == 2:  # Only valid for 2 square pawn moves
            self.en_passant_possible = ((move.start_row + move.end_row) // 2, move.start_column)
        else:
            self.en_passant_possible = ()

        self.en_passant_possible_log.append(self.en_passant_possible)

        # Castling
        if move.is_castle_move:
            if move.end_column - move.start_column == 2:  # King side castle
                self.board[move.end_row][move.end_column - 1] = self.board[move.end_row][
                    move.end_column + 1]  # Moves rook
                self.board[move.end_row][move.end_column + 1] = '--'  # Erases old rook
            else:  # Queen side castle
                self.board[move.end_row][move.end_column + 1] = self.board[move.end_row][
                    move.end_column - 2]  # Moves rook
                self.board[move.end_row][move.end_column - 2] = '--'  # Erases old rook

        # Updates castling rights
        self.update_castle_rights(move)
        self.castle_rights_log.append(CastleRights(self.white_castle_king_side, self.black_castle_king_side,
                                                   self.white_castle_queen_side, self.black_castle_queen_side))

        self.white_to_move = not self.white_to_move  # Switches turns

    def undo_move(self):
        """Undos last move made"""
        if len(self.move_log) != 0:  # Makes sure that there is a move to undo
            move = self.move_log.pop()
            self.board[move.start_row][move.start_column] = move.piece_moved
            self.board[move.end_row][move.end_column] = move.piece_captured
            self.white_to_move = not self.white_to_move  # Switches turn back

            # Updates king positions
            if move.piece_moved == 'wK':
                self.white_king_location = (move.start_row, move.start_column)
            elif move.piece_moved == 'bK':
                self.black_king_location = (move.start_row, move.start_column)

            # En passant
            if move.is_en_passant_move:
                self.board[move.end_row][move.end_column] = '--'  # Leaves landing square blank
                self.board[move.start_row][move.end_column] = move.piece_captured  # Allows en passant on the next move
            self.en_passant_possible_log.pop()
            self.en_passant_possible = self.en_passant_possible_log[-1]

            # Castling rights
            self.castle_rights_log.pop()  # Gets rid of new castle rights from move undoing
            castle_rights = self.castle_rights_log[-1]
            self.white_castle_king_side = castle_rights.white_king_side
            self.black_castle_king_side = castle_rights.black_king_side
            self.white_castle_queen_side = castle_rights.white_queen_side
            self.black_castle_queen_side = castle_rights.black_queen_side

            # Castling
            if move.is_castle_move:
                if move.end_column - move.start_column == 2:  # King side
                    self.board[move.end_row][move.end_column + 1] = self.board[move.end_row][move.end_column - 1]
                    self.board[move.end_row][move.end_column - 1] = '--'
                else:  # Queen side
                    self.board[move.end_row][move.end_column - 2] = self.board[move.end_row][move.end_column + 1]
                    self.board[move.end_row][move.end_column + 1] = '--'

            self.checkmate = False
            self.stalemate = False

    def get_valid_moves(self):
        """Gets all moves considering checks"""
        valid_moves = []
        self.in_check, self.pins, self.checks = self.check_for_pins_and_checks()

        # Updates king locations
        if self.white_to_move:
            king_row, king_column = self.white_king_location[0], self.white_king_location[1]
        else:
            king_row, king_column = self.black_king_location[0], self.black_king_location[1]

        if self.in_check:
            if len(self.checks) == 1:  # Only 1 check: block check or move king
                valid_moves = self.get_all_possible_moves()
                check = self.checks[0]
                check_row, check_column = check[0], check[1]
                piece_checking = self.board[check_row][check_column]  # Enemy piece causing check
                valid_squares = []
                if piece_checking == 'N':
                    valid_squares = [(check_row, check_column)]
                else:
                    for i in range(1, len(self.board)):
                        valid_square = (king_row + check[2] * i, king_column + check[3] * i)  # 2 & 3 = check directions
                        valid_squares.append(valid_square)
                        if valid_square[0] == check_row and valid_square[1] == check_column:
                            break
                for i in range(len(valid_moves) - 1, -1, -1):  # Gets rid of move not blocking, checking, or moving king
                    if valid_moves[i].piece_moved[1] != 'K':
                        if not (valid_moves[i].end_row, valid_moves[i].end_column) in valid_squares:
                            valid_moves.remove(valid_moves[i])
            else:  # Double check, king must move
                self.get_king_moves(king_row, king_column, valid_moves)
        else:  # Not in check
            valid_moves = self.get_all_possible_moves()

        if len(valid_moves) == 0:  # Either checkmate or stalemate
            if self.in_check:
                self.checkmate = True
            else:
                self.stalemate = True
        else:
            self.checkmate = False
            self.stalemate = False

        return valid_moves

    def get_all_possible_moves(self):
        """Gets all moves without considering checks"""
        moves = []
        for row in range(len(self.board)):  # Number of rows
            for column in range(len(self.board[row])):  # Number of columns in each row
                turn = self.board[row][column][0]
                if (turn == 'w' and self.white_to_move) or (turn == 'b' and not self.white_to_move):
                    piece = self.board[row][column][1]
                    self.move_functions[piece](row, column, moves)  # Calls move function based on piece type
        return moves

    def get_pawn_moves(self, row, column, moves):
        """Gets all pawn moves for the pawn located at (row, column) and adds moves to move log"""
        piece_pinned = False
        pin_direction = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == row and self.pins[i][1] == column:
                piece_pinned = True
                pin_direction = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break

        if self.white_to_move:
            move_amount = -1
            start_row = 6
            back_row = 0
            opponent = 'b'
            king_row, king_column = self.white_king_location
        else:
            move_amount = 1
            start_row = 1
            back_row = 7
            opponent = 'w'
            king_row, king_column = self.black_king_location
        pawn_promotion = False

        if self.board[row + move_amount][column] == '--':  # 1 square move
            if not piece_pinned or pin_direction == (move_amount, 0):
                if row + move_amount == back_row:  # If piece gets to back rank, it is a pawn promotion
                    pawn_promotion = True
                moves.append(
                    Move((row, column), (row + move_amount, column), self.board, pawn_promotion=pawn_promotion))
                if row == start_row and self.board[row + 2 * move_amount][column] == '--':  # 2 square advance
                    moves.append(Move((row, column), (row + 2 * move_amount, column), self.board))
        if column - 1 >= 0:  # Captures left
            if not piece_pinned or pin_direction == (move_amount, -1):
                if self.board[row + move_amount][column - 1][0] == opponent:
                    if row + move_amount == back_row:  # If piece gets to back rank, it is a pawn promotion
                        pawn_promotion = True
                    moves.append(Move((row, column), (row + move_amount, column - 1),
                                      self.board, pawn_promotion=pawn_promotion))
                if (row + move_amount, column - 1) == self.en_passant_possible:
                    attacking_piece = blocking_piece = False
                    if king_row == row:
                        if king_column < column:  # King is left of pawn
                            # inside_range between king and pawn; outside_range between pawn and border
                            inside_range = range(king_column + 1, column - 1)
                            outside_range = range(column + 1, len(self.board))
                        else:  # King is right of pawn
                            inside_range = range(king_column - 1, column, -1)
                            outside_range = range(column - 2, -1, -1)
                        for i in inside_range:
                            if self.board[row][i] != '--':
                                blocking_piece = True
                        for i in outside_range:
                            square = self.board[row][i]
                            if square[0] == opponent and (square[1] == 'R' or square[1] == 'Q'):
                                attacking_piece = True
                            elif square != '--':
                                blocking_piece = True
                    if not attacking_piece or blocking_piece:
                        moves.append(Move((row, column), (row + move_amount, column - 1), self.board, en_passant=True))
        if column + 1 <= len(self.board) - 1:  # Captures right
            if not piece_pinned or pin_direction == (move_amount, 1):
                if self.board[row + move_amount][column + 1][0] == opponent:
                    if row + move_amount == back_row:  # If piece gets to back rank, it is a pawn promotion
                        pawn_promotion = True
                    moves.append(Move((row, column), (row + move_amount, column + 1),
                                      self.board, pawn_promotion=pawn_promotion))
                if (row + move_amount, column + 1) == self.en_passant_possible:
                    attacking_piece = blocking_piece = False
                    if king_row == row:
                        if king_column < column:  # King is left of pawn
                            # inside_range between king and pawn; outside_range between pawn and border
                            inside_range = range(king_column + 1, column)
                            outside_range = range(column + 2, len(self.board))
                        else:  # King is right of pawn
                            inside_range = range(king_column - 1, column + 1, -1)
                            outside_range = range(column - 1, -1, -1)
                        for i in inside_range:
                            if self.board[row][i] != '--':
                                blocking_piece = True
                        for i in outside_range:
                            square = self.board[row][i]
                            if square[0] == opponent and (square[1] == 'R' or square[1] == 'Q'):
                                attacking_piece = True
                            elif square != '--':
                                blocking_piece = True
                    if not attacking_piece or blocking_piece:
                        moves.append(Move((row, column), (row + move_amount, column + 1), self.board, en_passant=True))

    def get_rook_moves(self, row, column, moves):
        """Gets all rook moves for the rook located at (row, column) and adds moves to move log"""
        opponent = 'b' if self.white_to_move else 'w'

        piece_pinned = False
        pin_direction = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == row and self.pins[i][1] == column:
                piece_pinned = True
                pin_direction = (self.pins[i][2], self.pins[i][3])
                if self.board[row][column][1] != 'Q':  # Can't remove queen from pin on rook moves (only bishop moves)
                    self.pins.remove(self.pins[i])
                break

        directions = [(-1, 0), (0, -1), (1, 0), (0, 1)]  # Tuples indicate (row, column) movements possible
        for d in directions:
            for i in range(1, len(self.board)):
                end_row = row + d[0] * i  # Potentially moves up/down to 7 rows
                end_column = column + d[1] * i  # Potentially moves up/down to 7 columns
                if 0 <= end_row < len(self.board) and 0 <= end_column < len(self.board):  # Makes sure on the board
                    if not piece_pinned or pin_direction == d or pin_direction == (-d[0], -d[1]):
                        end_piece = self.board[end_row][end_column]
                        if end_piece == '--':  # Valid move to empty space
                            moves.append(Move((row, column), (end_row, end_column), self.board))
                        elif end_piece[0] == opponent:  # Valid move to capture
                            moves.append(Move((row, column), (end_row, end_column), self.board))
                            break
                        else:  # Cannot take friendly piece
                            break
                else:  # Cannot move off board
                    break

    def get_knight_moves(self, row, column, moves):
        """Gets all knight moves for the knight located at (row, column) and adds moves to move log"""
        opponent = 'b' if self.white_to_move else 'w'

        piece_pinned = False
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == row and self.pins[i][1] == column:
                piece_pinned = True
                self.pins.remove(self.pins[i])
                break

        # Tuples indicate (row, column) movements possible
        directions = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]

        for d in directions:
            end_row = row + d[0]
            end_column = column + d[1]
            if 0 <= end_row < len(self.board) and 0 <= end_column < len(self.board):  # Makes sure on the board
                if not piece_pinned:
                    end_piece = self.board[end_row][end_column]
                    if end_piece[0] == opponent:  # Valid move to capture
                        moves.append(Move((row, column), (end_row, end_column), self.board))
                    elif end_piece == '--':  # Valid move to empty space
                        moves.append(Move((row, column), (end_row, end_column), self.board))

    def get_bishop_moves(self, row, column, moves):
        """Gets all bishop moves for the bishop located at (row, column) and adds moves to move log"""
        opponent = 'b' if self.white_to_move else 'w'

        piece_pinned = False
        pin_direction = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == row and self.pins[i][1] == column:
                piece_pinned = True
                pin_direction = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break

        directions = [(-1, -1), (-1, 1), (1, 1), (1, -1)]  # Tuples indicate (row, column) movements possible
        for d in directions:
            for i in range(1, len(self.board)):

                # See get_rook_moves for explanation; same here but for diagonals
                end_row = row + d[0] * i
                end_column = column + d[1] * i

                if 0 <= end_row < len(self.board) and 0 <= end_column < len(self.board):  # Makes sure on the board
                    if not piece_pinned or pin_direction == d or pin_direction == (-d[0], -d[1]):
                        end_piece = self.board[end_row][end_column]
                        if end_piece == '--':  # Valid move to empty space
                            moves.append(Move((row, column), (end_row, end_column), self.board))
                        elif end_piece[0] == opponent:  # Valid move to capture
                            moves.append(Move((row, column), (end_row, end_column), self.board))
                            break
                        else:  # Cannot take friendly piece
                            break
                else:  # Cannot move off board
                    break

    def get_queen_moves(self, row, column, moves):
        """Gets all queen moves for the queen located at (row, column) and adds moves to move log"""
        self.get_bishop_moves(row, column, moves)
        self.get_rook_moves(row, column, moves)

    def get_king_moves(self, row, column, moves):
        """Gets all king moves for the king located at (row, column) and adds moves to move log"""
        ally = 'w' if self.white_to_move else 'b'
        row_moves = (-1, -1, -1, 0, 0, 1, 1, 1)
        column_moves = (-1, 0, 1, -1, 1, -1, 0, 1)
        for i in range(len(self.board)):
            end_row = row + row_moves[i]
            end_column = column + column_moves[i]
            if 0 <= end_row < len(self.board) and 0 <= end_column < len(self.board):  # Makes sure on the board
                end_piece = self.board[end_row][end_column]
                if end_piece[0] != ally:  # Empty or enemy piece

                    # Places king on end square and checks for checks
                    if ally == 'w':
                        self.white_king_location = (end_row, end_column)
                    else:
                        self.black_king_location = (end_row, end_column)
                    in_check, pins, checks = self.check_for_pins_and_checks()
                    if not in_check:
                        moves.append(Move((row, column), (end_row, end_column), self.board))

                    # Places king back on original location
                    if ally == 'w':
                        self.white_king_location = (row, column)
                    else:
                        self.black_king_location = (row, column)
        self.get_castle_moves(row, column, moves, ally)

    def get_castle_moves(self, row, column, moves, ally):
        """
        Generates all valid castle moves for the king at (row, column).
        Adds valid castle moves to the list of moves.
        """
        if self.square_under_attack(row, column, ally):
            return  # Can't castle while in check
        if (self.white_to_move and self.white_castle_king_side) or \
                (not self.white_to_move and self.black_castle_king_side):
            self.get_king_side_castle_moves(row, column, moves, ally)
        if (self.white_to_move and self.white_castle_queen_side) or \
                (not self.white_to_move and self.black_castle_queen_side):
            self.get_queen_side_castle_moves(row, column, moves, ally)

    def get_king_side_castle_moves(self, row, column, moves, ally):
        if self.board[row][column + 1] == '--' and self.board[row][column + 2] == '--' and \
                not self.square_under_attack(row, column + 1, ally) and not self.square_under_attack(row, column + 2,
                                                                                                     ally):
            moves.append(Move((row, column), (row, column + 2), self.board, castle=True))

    def get_queen_side_castle_moves(self, row, column, moves, ally):
        if self.board[row][column - 1] == '--' and self.board[row][column - 2] == '--' and \
                self.board[row][column - 3] == '--' and not self.square_under_attack(row, column - 1, ally) and \
                not self.square_under_attack(row, column - 2, ally):
            moves.append(Move((row, column), (row, column - 2), self.board, castle=True))

    def update_castle_rights(self, move):
        """Updates castle rights given the move"""

        # If king or rook moved
        if move.piece_moved == 'wK':
            self.white_castle_queen_side = False
            self.white_castle_king_side = False
        elif move.piece_moved == 'bK':
            self.black_castle_queen_side = False
            self.black_castle_king_side = False
        elif move.piece_moved == 'wR':
            if move.start_row == 7:
                if move.start_column == 7:
                    self.white_castle_king_side = False
                elif move.start_column == 0:
                    self.white_castle_queen_side = False
        elif move.piece_moved == 'bR':
            if move.start_row == 0:
                if move.start_column == 7:
                    self.black_castle_king_side = False
                elif move.start_column == 0:
                    self.black_castle_queen_side = False

        # If rook is captured
        if move.piece_captured == 'wR':
            if move.end_row == 7:
                if move.end_column == 0:
                    self.white_castle_queen_side = False
                elif move.end_column == 7:
                    self.white_castle_king_side = False
        elif move.piece_captured == 'bR':
            if move.end_row == 0:
                if move.end_column == 0:
                    self.black_castle_queen_side = False
                elif move.end_column == 7:
                    self.black_castle_king_side = False

    def square_under_attack(self, row, column, ally):
        """Checks outward from a square to see if it is being attacked, thus invalidating castling"""
        opponent = 'b' if self.white_to_move else 'w'
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1))
        for j in range(len(directions)):
            d = directions[j]
            for i in range(1, len(self.board)):
                end_row = row + d[0] * i
                end_column = column + d[1] * i
                if 0 <= end_row < len(self.board) and 0 <= end_column < len(self.board):
                    end_piece = self.board[end_row][end_column]
                    if end_piece[0] == ally:  # no attack from that direction
                        break
                    elif end_piece[0] == opponent:
                        piece_type = end_piece[1]
                        if (0 <= j <= 3 and piece_type == 'R') or (4 <= j <= 7 and piece_type == 'B') or \
                                (i == 1 and piece_type == 'P' and ((opponent == 'w' and 6 <= j <= 7)
                                                                   or (opponent == 'b' and 4 <= j <= 5))) or \
                                (piece_type == 'Q') or (i == 1 and piece_type == 'K'):
                            return True
                        else:  # Enemy piece but not applying check
                            break
                else:  # Off board
                    break
        knight_moves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        for move in knight_moves:
            end_row = row + move[0]
            end_column = column + move[1]
            if 0 <= end_row < len(self.board) and 0 <= end_column < len(self.board):
                end_piece = self.board[end_row][end_column]
                if end_piece[0] == opponent and end_piece[1] == 'N':
                    return True
        return False

    def check_for_pins_and_checks(self):
        """Returns if the player is in check, a list of pins, and a list of checks"""
        pins = []
        checks = []
        in_check = False

        if self.white_to_move:
            opponent = 'b'
            ally = 'w'
            start_row, start_column = self.white_king_location[0], self.white_king_location[1]
        else:
            opponent = 'w'
            ally = 'b'
            start_row, start_column = self.black_king_location[0], self.black_king_location[1]

        directions = ((-1, 0), (0, -1), (1, 0), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1))
        for j in range(len(directions)):
            d = directions[j]
            possible_pin = ()  # Resets possible pins
            for i in range(1, len(self.board)):
                end_row = start_row + d[0] * i
                end_column = start_column + d[1] * i
                if 0 <= end_row < len(self.board) and 0 <= end_column < len(self.board):
                    end_piece = self.board[end_row][end_column]
                    if end_piece[0] == ally and end_piece[1] != 'K':
                        if possible_pin == ():  # 1st ally piece can be pinned
                            possible_pin = (end_row, end_column, d[0], d[1])
                        else:  # 2nd ally piece, so no pin or check possible
                            break
                    elif end_piece[0] == opponent:
                        piece_type = end_piece[1]
                        if (0 <= j <= 3 and piece_type == 'R') or (4 <= j <= 7 and piece_type == 'B') or \
                                (i == 1 and piece_type == 'P' and ((opponent == 'w' and 6 <= j <= 7)
                                                                   or (opponent == 'b' and 4 <= j <= 5))) or \
                                (piece_type == 'Q') or (i == 1 and piece_type == 'K'):
                            if possible_pin == ():  # no piece blocking, so check
                                in_check = True
                                checks.append((end_row, end_column, d[0], d[1]))
                                break
                            else:  # Piece blocking, so pin
                                pins.append(possible_pin)
                                break
                        else:  # Enemy piece but not applying check
                            break
                else:  # Off board
                    break

        knight_moves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        for move in knight_moves:
            end_row = start_row + move[0]
            end_column = start_column + move[1]
            if 0 <= end_row < len(self.board) and 0 <= end_column < len(self.board):
                end_piece = self.board[end_row][end_column]
                if end_piece[0] == opponent and end_piece[1] == 'N':
                    in_check = True
                    checks.append((end_row, end_column, move[0], move[1]))

        return in_check, pins, checks


class CastleRights:
    """Data storage of current states of castling rights"""

    def __init__(self, white_king_side, black_king_side, white_queen_side, black_queen_side):
        self.white_king_side = white_king_side
        self.black_king_side = black_king_side
        self.white_queen_side = white_queen_side
        self.black_queen_side = black_queen_side


class Move:
    """
    Class responsible for storing information about particular moves,
    including starting and ending positions, which pieces were moved and captured,
    and special moves such as en passant, pawn promotion, and castling.
    """
    ranks_to_rows = {'1': 7, '2': 6, '3': 5, '4': 4,
                     '5': 3, '6': 2, '7': 1, '8': 0}
    rows_to_ranks = {v: k for k, v in ranks_to_rows.items()}
    files_to_columns = {'a': 0, 'b': 1, 'c': 2, 'd': 3,
                        'e': 4, 'f': 5, 'g': 6, 'h': 7}
    columns_to_files = {v: k for k, v in files_to_columns.items()}

    def __init__(self, start_square, end_square, board, en_passant=False, pawn_promotion=False, castle=False):
        self.start_row, self.start_column = start_square[0], start_square[1]
        self.end_row, self.end_column = end_square[0], end_square[1]
        self.piece_moved = board[self.start_row][self.start_column]
        self.piece_captured = board[self.end_row][self.end_column]
        self.is_pawn_promotion = pawn_promotion

        # En passant
        self.is_en_passant_move = en_passant
        if self.is_en_passant_move:
            self.piece_captured = 'wP' if self.piece_moved == 'bP' else 'bP'

        self.is_castle_move = castle
        self.is_capture = self.piece_captured != '--'
        self.move_id = self.start_row * 1000 + self.start_column * 100 + self.end_row * 10 + self.end_column

    def __eq__(self, other):
        """Overrides the equals method because a Class is used"""
        if isinstance(other, Move):
            return self.move_id == other.move_id
        return False

    def get_chess_notation(self):
        """Creates a rank and file chess notation"""
        return self.get_rank_file(self.start_row, self.start_column) + self.get_rank_file(self.end_row, self.end_column)

    def get_rank_file(self, rank, column):
        return self.columns_to_files[column] + self.rows_to_ranks[rank]

    def __str__(self):
        """
        Overrides string function to improve chess notation.
        Does not 1) specify checks, 2) checkmate, or 3) when
        multiple same-type pieces can capture the same square.
        """
        # Castling
        if self.is_castle_move:
            return 'O-O' if self.end_column == 6 else 'O-O-O'

        end_square = self.get_rank_file(self.end_row, self.end_column)

        # Pawn moves
        if self.piece_moved[1] == 'P':
            if self.is_capture and self.is_pawn_promotion:  # Pawn promotion
                return f'{end_square}={promoted_piece}'
            elif self.is_capture and not self.is_pawn_promotion:  # Capture move
                return f'{self.columns_to_files[self.start_column]}x{end_square}'
            else:  # Normal movement
                return end_square

        # Other piece moves
        move_string = self.piece_moved[1]
        if self.is_capture:
            move_string += 'x'

        return f'{move_string}{end_square}'
