import math


def make_empty_board():
    return [[" " for _ in range(3)] for _ in range(3)]


def print_board(board):
    print()
    for i in range(3):
        row = ""
        for j in range(3):
            row += board[i][j]
            if j < 2:
                row += " | "
        print("  " + row)
        if i < 2:
            print("  ---------")
    print()


def get_available_moves(board):
    moves = []
    for i in range(3):
        for j in range(3):
            if board[i][j] == " ":
                moves.append((i, j))
    return moves


def check_winner(board, player):
    for row in board:
        if all(cell == player for cell in row):
            return True

    for col in range(3):
        if all(board[row][col] == player for row in range(3)):
            return True

    if all(board[i][i] == player for i in range(3)):
        return True

    if all(board[i][2 - i] == player for i in range(3)):
        return True

    return False


def is_board_full(board):
    return all(board[i][j] != " " for i in range(3) for j in range(3))


def get_board_score(board):
    if check_winner(board, "X"):
        return 10
    elif check_winner(board, "O"):
        return -10
    else:
        return 0


def minimax_alpha_beta(board, depth, is_maximizing, alpha, beta, move_log):
    score = get_board_score(board)

    if score == 10 or score == -10:
        return score

    if is_board_full(board):
        return 0

    available = get_available_moves(board)

    if is_maximizing:
        best_val = -math.inf

        for move in available:
            row, col = move
            board[row][col] = "X"

            val = minimax_alpha_beta(board, depth + 1, False, alpha, beta, move_log)

            board[row][col] = " "

            if val > best_val:
                best_val = val

            if best_val > alpha:
                alpha = best_val

            move_log.append({
                "depth": depth,
                "move": move,
                "player": "MAX (X)",
                "value": val,
                "alpha": alpha,
                "beta": beta,
                "pruned": False
            })

            if beta <= alpha:
                move_log[-1]["pruned"] = True
                move_log[-1]["pruned_reason"] = f"Beta ({beta}) <= Alpha ({alpha}) -- MAX cutoff"
                break

        return best_val

    else:
        best_val = math.inf

        for move in available:
            row, col = move
            board[row][col] = "O"

            val = minimax_alpha_beta(board, depth + 1, True, alpha, beta, move_log)

            board[row][col] = " "

            if val < best_val:
                best_val = val

            if best_val < beta:
                beta = best_val

            move_log.append({
                "depth": depth,
                "move": move,
                "player": "MIN (O)",
                "value": val,
                "alpha": alpha,
                "beta": beta,
                "pruned": False
            })

            if beta <= alpha:
                move_log[-1]["pruned"] = True
                move_log[-1]["pruned_reason"] = f"Alpha ({alpha}) >= Beta ({beta}) -- MIN cutoff"
                break

        return best_val


def max_agent_move(board):
    best_score = -math.inf
    best_move = None
    move_log = []

    print("  MAX agent is thinking...")
    print("  Alpha-Beta search starting:")

    for move in get_available_moves(board):
        row, col = move
        board[row][col] = "X"

        move_log_temp = []
        score = minimax_alpha_beta(board, 0, False, -math.inf, math.inf, move_log_temp)

        board[row][col] = " "

        print(f"    Move {move} -> Score: {score}")

        for entry in move_log_temp:
            if entry["pruned"]:
                print(f"      [CUTOFF at depth {entry['depth']}] {entry['pruned_reason']}")

        move_log.extend(move_log_temp)

        if score > best_score:
            best_score = score
            best_move = move

    return best_move, best_score, move_log


def min_agent_move(board):
    best_score = math.inf
    best_move = None
    move_log = []

    print("  MIN agent is thinking...")
    print("  Alpha-Beta search starting:")

    for move in get_available_moves(board):
        row, col = move
        board[row][col] = "O"

        move_log_temp = []
        score = minimax_alpha_beta(board, 0, True, -math.inf, math.inf, move_log_temp)

        board[row][col] = " "

        print(f"    Move {move} -> Score: {score}")

        for entry in move_log_temp:
            if entry["pruned"]:
                print(f"      [CUTOFF at depth {entry['depth']}] {entry['pruned_reason']}")

        move_log.extend(move_log_temp)

        if score < best_score:
            best_score = score
            best_move = move

    return best_move, best_score, move_log


def play_game():
    board = make_empty_board()

    max_score = 0
    min_score = 0
    move_number = 0

    print("=" * 55)
    print("       TIC TAC TOE  --  MAX (X) vs MIN (O)")
    print("       Algorithm: Minimax with Alpha-Beta Pruning")
    print("=" * 55)

    print_board(board)

    while True:
        move_number += 1

        print(f"\n--- Move #{move_number} ---  MAX (X) is playing")
        print(f"  Current Score -> MAX: {max_score}  |  MIN: {min_score}")

        best_move, score, log = max_agent_move(board)

        row, col = best_move
        board[row][col] = "X"

        max_score = score

        print(f"\n  MAX placed X at position {best_move}")
        print(f"  Utility/Score after move: {score}")
        print_board(board)

        if check_winner(board, "X"):
            max_score = 10
            print("=" * 55)
            print("  RESULT: MAX (X) wins the game!")
            print(f"  Final Score -> MAX: {max_score}  |  MIN: {min_score}")
            print("=" * 55)
            break

        if is_board_full(board):
            print("=" * 55)
            print("  RESULT: Game is a Draw!")
            print(f"  Final Score -> MAX: {max_score}  |  MIN: {min_score}")
            print("=" * 55)
            break

        move_number += 1

        print(f"\n--- Move #{move_number} ---  MIN (O) is playing")
        print(f"  Current Score -> MAX: {max_score}  |  MIN: {min_score}")

        best_move, score, log = min_agent_move(board)

        row, col = best_move
        board[row][col] = "O"

        min_score = score

        print(f"\n  MIN placed O at position {best_move}")
        print(f"  Utility/Score after move: {score}")
        print_board(board)

        if check_winner(board, "O"):
            min_score = -10
            print("=" * 55)
            print("  RESULT: MIN (O) wins the game!")
            print(f"  Final Score -> MAX: {max_score}  |  MIN: {min_score}")
            print("=" * 55)
            break

        if is_board_full(board):
            print("=" * 55)
            print("  RESULT: Game is a Draw!")
            print(f"  Final Score -> MAX: {max_score}  |  MIN: {min_score}")
            print("=" * 55)
            break


play_game()
