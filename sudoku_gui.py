import tkinter as tk
from tkinter import messagebox
from sudoku_logic import solve, is_valid, generate_puzzle

class SudokuGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku Solver Game - Premium")
        self.root.geometry("500x700")
        self.root.configure(bg="#0F0C29")
        self.cells = {}
        
        self.create_levels()
        self.create_grid()
        self.create_buttons()

    def create_grid(self):
        frame = tk.Frame(self.root, bg="#302B63", padx=10, pady=10)
        frame.pack(pady=20)
        
        for r in range(9):
            for c in range(9):
                padx = (1, 1)
                pady = (1, 1)
                if c % 3 == 0 and c != 0: padx = (5, 1)
                if r % 3 == 0 and r != 0: pady = (5, 1)
                
                entry = tk.Entry(frame, width=2, font=('Arial', 24, 'bold'), 
                                justify='center', borderwidth=0, relief="flat",
                                bg="#24243E", fg="#00F2FE", insertbackground="#00F2FE")
                entry.grid(row=r, column=c, padx=padx, pady=pady, sticky="nsew")
                self.cells[(r, c)] = entry

    def create_levels(self):
        level_frame = tk.Frame(self.root, bg="#0F0C29")
        level_frame.pack(pady=10)
        
        tk.Label(level_frame, text="CHOOSE DIFFICULTY", font=("Arial", 12, "bold"), 
                 bg="#0F0C29", fg="#00F2FE").pack()
                 
        diff_frame = tk.Frame(level_frame, bg="#0F0C29")
        diff_frame.pack()
        
        levels = [("Easy", "#00F2FE"), ("Medium", "#FF9800"), ("Hard", "#F44336")]
        for text, color in levels:
            btn = tk.Button(diff_frame, text=text, font=("Arial", 10, "bold"),
                            bg=color, fg="black", highlightbackground=color, width=8,
                            command=lambda t=text: self.new_game(t))
            btn.pack(side=tk.LEFT, padx=5, pady=5)

    def new_game(self, difficulty):
        board = generate_puzzle(difficulty)
        self.clear_grid()
        self.set_board(board)

    def create_buttons(self):
        btn_frame = tk.Frame(self.root, bg="#0F0C29")
        btn_frame.pack(pady=20)

        # On macOS, standard button colors don't show well unless we use highlightbackground
        solve_btn = tk.Button(btn_frame, text="Solve", command=self.solve_clicked, 
                              font=("Arial", 11, "bold"), bg="#9D50BB", fg="black", 
                              highlightbackground="#9D50BB", padx=10, pady=5)
        solve_btn.grid(row=0, column=0, padx=5)

        clear_btn = tk.Button(btn_frame, text="Clear", command=self.clear_grid, 
                               font=("Arial", 11, "bold"), bg="#6E48AA", fg="black", 
                               highlightbackground="#6E48AA", padx=10, pady=5)
        clear_btn.grid(row=0, column=1, padx=5)
        
        sample_btn = tk.Button(btn_frame, text="Sample", command=self.load_sample, 
                                font=("Arial", 11, "bold"), bg="#00F2FE", fg="black", 
                                highlightbackground="#00F2FE", padx=10, pady=5)
        sample_btn.grid(row=0, column=2, padx=5)

    def get_board(self):
        board = []
        for r in range(9):
            row = []
            for c in range(9):
                val = self.cells[(r, c)].get()
                if val == "":
                    row.append(0)
                else:
                    try:
                        num = int(val)
                        if 1 <= num <= 9:
                            row.append(num)
                        else:
                            raise ValueError
                    except ValueError:
                        messagebox.showwarning("Input Error", f"Invalid character at {r+1},{c+1}")
                        return None
            board.append(row)
        return board

    def set_board(self, board):
        for r in range(9):
            for c in range(9):
                self.cells[(r, c)].delete(0, tk.END)
                if board[r][c] != 0:
                    self.cells[(r, c)].insert(0, str(board[r][c]))

    def solve_clicked(self):
        board = self.get_board()
        if board is None: return

        for r in range(9):
            for c in range(9):
                if board[r][c] != 0:
                    temp_val = board[r][c]
                    board[r][c] = 0
                    if not is_valid(board, r, c, temp_val):
                        messagebox.showwarning("Logic Error", "Duplicate values in current board!")
                        return
                    board[r][c] = temp_val

        if solve(board):
            self.set_board(board)
            messagebox.showinfo("Success", "Sudoku Solved using Backtracking!")
        else:
            messagebox.showerror("Failed", "No solution exists for this puzzle.")

    def clear_grid(self):
        for r in range(9):
            for c in range(9):
                self.cells[(r, c)].delete(0, tk.END)

    def load_sample(self):
        sample = [
            [5, 3, 0, 0, 7, 0, 0, 0, 0],
            [6, 0, 0, 1, 9, 5, 0, 0, 0],
            [0, 9, 8, 0, 0, 0, 0, 6, 0],
            [8, 0, 0, 0, 6, 0, 0, 0, 3],
            [4, 0, 0, 8, 0, 3, 0, 0, 1],
            [7, 0, 0, 0, 2, 0, 0, 0, 6],
            [0, 6, 0, 0, 0, 0, 2, 8, 0],
            [0, 0, 0, 4, 1, 9, 0, 0, 5],
            [0, 0, 0, 0, 8, 0, 0, 7, 9]
        ]
        self.clear_grid()
        self.set_board(sample)

if __name__ == "__main__":
    root = tk.Tk()
    SudokuGUI(root)
    root.mainloop()
