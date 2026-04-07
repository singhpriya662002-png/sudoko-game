import random

def is_valid(board, row, col, num):
    for x in range(9):
        if board[row][x] == num:
            return False

    for x in range(9):
        if board[x][col] == num:
            return False

    start_row = row - row % 3
    start_col = col - col % 3
    for i in range(3):
        for j in range(3):
            if board[i + start_row][j + start_col] == num:
                return False

    return True

def solve(board):
    empty = find_empty(board)
    if not empty:
        return True
    
    row, col = empty

    for num in range(1, 10):
        if is_valid(board, row, col, num):
            board[row][col] = num

            if solve(board):
                return True

            board[row][col] = 0

    return False

def find_empty(board):
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                return (i, j)
    return None

def fill_board(board):
    empty = find_empty(board)
    if not empty:
        return True
    
    row, col = empty
    nums = list(range(1, 10))
    random.shuffle(nums)
    
    for num in nums:
        if is_valid(board, row, col, num):
            board[row][col] = num
            if fill_board(board):
                return True
            board[row][col] = 0
    return False

def generate_puzzle(difficulty):
    board = [[0 for _ in range(9)] for _ in range(9)]
    fill_board(board)
    
    # Keep a copy of the full board as the solution
    solution = [row[:] for row in board]
    
    clues = {"Easy": 40, "Medium": 30, "Hard": 20}
    attempts = 81 - clues.get(difficulty, 30)
    
    while attempts > 0:
        row = random.randint(0, 8)
        col = random.randint(0, 8)
        if board[row][col] != 0:
            board[row][col] = 0
            attempts -= 1
            
    return board, solution

def print_board(board):
    for i in range(len(board)):
        if i % 3 == 0 and i != 0:
            print("- - - - - - - - - - - -")

        for j in range(len(board[0])):
            if j % 3 == 0 and j != 0:
                print(" | ", end="")

            if j == 8:
                print(board[i][j])
            else:
                print(str(board[i][j]) + " ", end="")
