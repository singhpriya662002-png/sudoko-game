from sudoku_logic import solve, is_valid

def test_solve():
    board = [
        [3, 0, 6, 5, 0, 8, 4, 0, 0],
        [5, 2, 0, 0, 0, 0, 0, 0, 0],
        [0, 8, 7, 0, 0, 0, 0, 3, 1],
        [0, 0, 3, 0, 1, 0, 0, 8, 0],
        [9, 0, 0, 8, 6, 3, 0, 0, 5],
        [0, 5, 0, 0, 9, 0, 6, 0, 0],
        [1, 3, 0, 0, 0, 0, 2, 5, 0],
        [0, 0, 0, 0, 0, 0, 0, 7, 4],
        [0, 0, 5, 2, 0, 6, 3, 0, 0]
    ]

    print("Original Board:")
    for row in board:
        print(row)

    if solve(board):
        print("\nSolved Board:")
        for row in board:
            print(row)
        return True
    else:
        print("\nNo solution exists.")
        return False

if __name__ == "__main__":
    if test_solve():
        print("\nTest Passed!")
    else:
        print("\nTest Failed!")
