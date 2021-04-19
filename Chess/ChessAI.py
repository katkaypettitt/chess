import random

# Depth of the algorithm determining AI moves. Higher set_depth == harder AI. Lower if engine is too slow.
set_depth = 4

# Positive values are good for white, negative for black. i.e. black checkmate = -1000
checkmate_points = 1000
stalemate_points = 0

piece_scores = {'K': 200.0, 'Q': 9.0, 'R': 5.0, 'B': 3.3, 'N': 3.2, 'P': 1.0}
piece_positions = {
    'wP': [
        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        [5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0],
        [1.0, 1.0, 2.0, 3.0, 3.0, 2.0, 1.0, 1.0],
        [0.5, 0.5, 1.0, 2.5, 2.5, 1.0, 0.5, 0.5],
        [0.0, 0.0, 0.0, 2.0, 2.0, 0.0, 0.0, 0.0],
        [0.5, -0.5, -1.0, 0.0, 0.0, -1.0, -0.5, 0.5],
        [0.5, 1.0, 1.0, -2.0, -2.0, 1.0, 1.0, 0.5],
        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]],
    'bP': [
        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        [0.5, 1.0, 1.0, -2.0, -2.0, 1.0, 1.0, 0.5],
        [0.5, -0.5, -1.0, 0.0, 0.0, -1.0, -0.5, 0.5],
        [0.0, 0.0, 0.0, 2.0, 2.0, 0.0, 0.0, 0.0],
        [0.5, 0.5, 1.0, 2.5, 2.5, 1.0, 0.5, 0.5],
        [1.0, 1.0, 2.0, 3.0, 3.0, 2.0, 1.0, 1.0],
        [5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0],
        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]],
    'wN': [
        [-5.0, -4.0, -3.0, -3.0, -3.0, -3.0, -4.0, -5.0],
        [-4.0, -2.0, 0.0, 0.0, 0.0, 0.0, -2.0, -4.0],
        [-3.0, 0.0, 1.0, 1.5, 1.5, 1.0, 0.0, -3.0],
        [-3.0, 0.5, 1.5, 2.0, 2.0, 1.5, 5.0, -30],
        [-3.0, 0.0, 1.5, 2.0, 2.0, 1.5, 0, -3.0],
        [-3.0, 0.5, 1.0, 1.5, 1.5, 1.0, 5.0, -30],
        [-4.0, -2.0, 0.0, 0.5, 0.5, 0.0, -2.0, -4.0],
        [-5.0, -4.0, -3.0, -3.0, -3.0, -3.0, -4.0, -5.0]],
    'bN': [
        [-5.0, -4.0, -3.0, -3.0, -3.0, -3.0, -4.0, -5.0],
        [-.0, -2.0, 0.0, 0.5, 0.5, 0.0, -2.0, -4.0],
        [-3.0, 0.5, 1.0, 1.5, 1.5, 1.0, 0.5, -3.0],
        [-3.0, 0.0, 1.5, 2.0, 2.0, 1.5, 0.0, -3.0],
        [-3.0, 0.5, 1.5, 2.0, 2.0, 1.5, 0.5, -3.0],
        [-3.0, 0.0, 1.0, 1.5, 1.5, 1.0, 0.0, -3.0],
        [-4.0, -2.0, 0.0, 0.0, 0.0, 0.0, -2.0, -4.0],
        [-5.0, -4.0, -3.0, -3.0, -3.0, -3.0, -4.0, -5.0]],
    'wB': [
        [-2.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -2.0],
        [-1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -1.0],
        [-1.0, 0.0, 0.5, 1.0, 1.0, 0.5, 0.0, -1.0],
        [-1.0, 0.5, 0.5, 1.0, 1.0, 0.5, 0.5, -1.0],
        [-1.0, 0.0, 1.0, 1.0, 1.0, 1.0, 0.0, -1.0],
        [-1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, -1.0],
        [-1.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.5, -1.0],
        [-2.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -2.0]],
    'bB': [
        [-2.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -2.0],
        [-1.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.5, -1.0],
        [-1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, -1.0],
        [-1.0, 0.0, 1.0, 1.0, 1.0, 1.0, 0.0, -1.0],
        [-1.0, 0.5, 0.5, 1.0, 1.0, 0.5, 0.5, -1.0],
        [-1.0, 0.0, 0.5, 1.0, 1.0, 0.5, 0.0, -1.0],
        [-1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -1.0],
        [-2.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -2.0]],
    'wR': [
        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        [0.5, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.5],
        [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
        [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
        [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
        [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
        [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
        [0.0, 0.0, 0.0, 0.5, 0.5, 0.0, 0.0, 0.0]],
    'bR': [
        [0.0, 0.0, 0.0, 0.5, 0.5, 0.0, 0.0, 0.0],
        [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
        [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
        [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
        [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
        [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
        [0.5, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.5],
        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]],
    'wQ': [
        [-2.0, -1.0, -1.0, -0.5, -0.5, -1.0, -1.0, -2.0],
        [-1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -1.0],
        [-1.0, 0.0, 0.5, 0.5, 0.5, 0.5, 0.0, -1.0],
        [-0.5, 0.0, 0.5, 0.5, 0.5, 0.5, 0.0, -0.5],
        [0.0, 0.0, 0.5, 0.5, 0.5, 0.5, 0.0, -0.5],
        [-1.0, 0.5, 0.5, 0.5, 0.5, 0.5, 0.0, -1.0],
        [-1.0, 0.0, 0.5, 0.0, 0.0, 0.0, 0.0, -1.0],
        [-2.0, -1.0, -1.0, -0.5, -0.5, -1.0, -1.0, -2.0]],
    "bQ": [
        [-2.0, -1.0, -1.0, -0.5, -0.5, -1.0, -1.0, -2.0],
        [-1.0, 0.0, 0.5, 0.0, 0.0, 0.0, 0.0, -1.0],
        [-1.0, 0.5, 0.5, 0.5, 0.5, 0.5, 0.0, -1.0],
        [0.0, 0.0, 0.5, 0.5, 0.5, 0.5, 0.0, -0.5],
        [-0.5, 0.0, 0.5, 0.5, 0.5, 0.5, 0.0, -0.5],
        [-1.0, 0.0, 0.5, 0.5, 0.5, 0.5, 0.0, -1.0],
        [-1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -1.0],
        [-2.0, -1.0, -1.0, -0.5, -0.5, -1.0, -1.0, -2.0]],
    'wK': [  # Uses chessprogramming.org King middle game values
        [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
        [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
        [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
        [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
        [-2.0, -3.0, -3.0, -4.0, -4.0, -3.0, -3.0, -2.0],
        [-1.0, -2.0, -2.0, -2.0, -2.0, -2.0, -2.0, -1.0],
        [2.0, 2.0, 0.0, 0.0, 0.0, 0.0, 2.0, 2.0],
        [2.0, 3.0, 1.0, 0.0, 0.0, 1.0, 3.0, 2.0]],
    'bK': [  # Uses chessprogramming.org King middle game values
        [2.0, 3.0, 1.0, 0.0, 0.0, 1.0, 3.0, 2.0],
        [2.0, 2.0, 0.0, 0.0, 0.0, 0.0, 2.0, 2.0],
        [-1.0, -2.0, -2.0, -2.0, -2.0, -2.0, -2.0, -1.0],
        [-2.0, -3.0, -3.0, -4.0, -4.0, -3.0, -3.0, -2.0],
        [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
        [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
        [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
        [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0]]}


def find_random_move(valid_moves):
    return random.choice(valid_moves)


def find_best_move(game_state, valid_moves):
    """Helper method to make first recursive call"""
    global next_move
    next_move = None
    random.shuffle(valid_moves)
    find_negamax_move_alphabeta(game_state, valid_moves, set_depth, -checkmate_points, checkmate_points,
                                1 if game_state.white_to_move else -1)
    return next_move


def find_negamax_move_alphabeta(game_state, valid_moves, depth, alpha, beta, turn_multiplier):
    """
    NegaMax algorithm with alpha beta pruning.

    Alpha beta pruning eliminates the need to check all moves within the game_state tree when
    a better branch has been found or a branch has too low of a score.

    alpha: upper bound (max possible); beta: lower bound (min possible)
    If max score is greater than alpha, that becomes the new alpha value.
    If alpha becomes >= beta, break out of branch.

    White is always trying to maximise score and black is always
    trying to minimise score. Once the possibility of a higher max or lower min
    has been eliminated, there is no need to check further branches.
    """
    global next_move
    if depth == 0:
        return turn_multiplier * score_board(game_state)

    max_score = -checkmate_points
    for move in valid_moves:
        game_state.make_move(move)
        next_moves = game_state.get_valid_moves()
        score = -find_negamax_move_alphabeta(game_state, next_moves, depth - 1, -beta, -alpha, -turn_multiplier)
        if score > max_score:
            max_score = score
            if depth == set_depth:
                next_move = move
        game_state.undo_move()

        # Pruning
        if max_score > alpha:
            alpha = max_score
        if alpha >= beta:
            break

    return max_score


def score_board(game_state):
    """Positive score is good for white; negative score is good for black."""
    if game_state.checkmate:
        if game_state.white_to_move:
            return -checkmate_points  # Black wins
        else:
            return checkmate_points  # White wins
    elif game_state.stalemate:
        return stalemate_points

    score = 0
    for row in range(len(game_state.board)):
        for column in range(len(game_state.board)):
            if game_state.board[row][column][0] == 'w':
                score += piece_scores[game_state.board[row][column][1]]
                score += piece_positions[game_state.board[row][column]][row][column]
            elif game_state.board[row][column][0] == 'b':
                score -= piece_scores[game_state.board[row][column][1]]
                score -= piece_positions[game_state.board[row][column]][row][column]
    return score
