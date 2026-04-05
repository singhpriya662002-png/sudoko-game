from sudoku_logic import generate_puzzle, solve, print_board

def test_difficulty(level):
    print(f"\nTesting {level} Difficulty...")
    board = generate_puzzle(level)
    
    clues = 0
    for row in board:
        for val in row:
            if val != 0:
                clues += 1
    
    print(f"Clues provided: {clues}")
    
    print("Generated Puzzle:")
    print_board(board)
    
    if solve([row[:] for row in board]):
        print(f"Verification: {level} board is solvable!")
        return True
    else:
        print(f"Verification: {level} board failed to solve!")
        return False

if __name__ == "__main__":
    success = True
    for lvl in ["Easy", "Medium", "Hard"]:
        if not test_difficulty(lvl):
            success = False
    
    if success:
        print("\nAll Generator Tests Passed!")
    else:
        print("\nSome Generator Tests Failed!")
