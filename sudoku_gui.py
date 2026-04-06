import tkinter as tk
from tkinter import messagebox
from sudoku_logic import solve, is_valid, generate_puzzle

class SudokuGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku Solver Game - Premium")
        self.root.geometry("500x700")
        self.root.configure(bg="#1A120B")
        self.cells = {}
        self.elapsed_seconds = 0
        self.timer_running = False
        self.current_difficulty = "Easy"
        
        self.create_status_bar()
        self.create_levels()
        self.create_grid()
        self.create_buttons()

    def create_status_bar(self):
        self.status_frame = tk.Frame(self.root, bg="#3C2A21", padx=20, pady=10)
        self.status_frame.pack(fill=tk.X)
        
        self.level_label = tk.Label(self.status_frame, text=f"LEVEL: {self.current_difficulty.upper()}", 
                                   font=("Arial", 12, "bold"), bg="#3C2A21", fg="#E5E5CB")
        self.level_label.pack(side=tk.LEFT)
        
        self.timer_label = tk.Label(self.status_frame, text="TIME: 00:00", 
                                   font=("Arial", 12, "bold"), bg="#3C2A21", fg="#D5CEA3")
        self.timer_label.pack(side=tk.RIGHT)

    def update_timer(self):
        if self.timer_running:
            self.elapsed_seconds += 1
            minutes = self.elapsed_seconds // 60
            seconds = self.elapsed_seconds % 60
            self.timer_label.config(text=f"TIME: {minutes:02d}:{seconds:02d}")
            self.root.after(1000, self.update_timer)

    def start_timer(self):
        self.elapsed_seconds = 0
        self.timer_running = True
        self.update_timer()

    def stop_timer(self):
        self.timer_running = False

    def create_grid(self):
        frame = tk.Frame(self.root, bg="#3C2A21", padx=10, pady=10)
        frame.pack(pady=20)
        
        for r in range(9):
            for c in range(9):
                padx = (1, 1)
                pady = (1, 1)
                if c % 3 == 0 and c != 0: padx = (5, 1)
                if r % 3 == 0 and r != 0: pady = (5, 1)
                
                entry = tk.Entry(frame, width=2, font=('Arial', 24, 'bold'), 
                                justify='center', borderwidth=0, relief="flat",
                                bg="#1A120B", fg="#E5E5CB", insertbackground="#E5E5CB")
                entry.grid(row=r, column=c, padx=padx, pady=pady, sticky="nsew")
                self.cells[(r, c)] = entry

    def create_levels(self):
        level_frame = tk.Frame(self.root, bg="#1A120B")
        level_frame.pack(pady=10)
        
        tk.Label(level_frame, text="CHOOSE DIFFICULTY", font=("Arial", 10, "bold"), 
                 bg="#1A120B", fg="#D5CEA3").pack()
                 
        diff_frame = tk.Frame(level_frame, bg="#1A120B")
        diff_frame.pack()
        
        levels = [("Easy", "#D2B48C"), ("Medium", "#D2B48C"), ("Hard", "#D2B48C")]
        for text, color in levels:
            btn = tk.Button(diff_frame, text=text, font=("Arial", 10, "bold"),
                            bg=color, fg="black", highlightbackground=color, width=8,
                            command=lambda t=text: self.new_game(t))
            btn.pack(side=tk.LEFT, padx=5, pady=5)

    def new_game(self, difficulty):
        self.current_difficulty = difficulty
        self.level_label.config(text=f"LEVEL: {difficulty.upper()}")
        board = generate_puzzle(difficulty)
        self.clear_grid()
        self.set_board(board)
        self.start_timer()

    def create_buttons(self):
        btn_frame = tk.Frame(self.root, bg="#1A120B")
        btn_frame.pack(pady=20)

        # Light brown shades for utility buttons
        solve_btn = tk.Button(btn_frame, text="Solve", command=self.solve_clicked, 
                              font=("Arial", 11, "bold"), bg="#B8860B", fg="black", 
                              highlightbackground="#B8860B", padx=10, pady=5)
        solve_btn.grid(row=0, column=0, padx=5)

        clear_btn = tk.Button(btn_frame, text="Clear", command=self.clear_grid, 
                               font=("Arial", 11, "bold"), bg="#D2B48C", fg="black", 
                               highlightbackground="#D2B48C", padx=10, pady=5)
        clear_btn.grid(row=0, column=1, padx=5)
        
        sample_btn = tk.Button(btn_frame, text="Sample", command=self.load_sample, 
                                font=("Arial", 11, "bold"), bg="#BC8F8F", fg="black", 
                                highlightbackground="#BC8F8F", padx=10, pady=5)
        sample_btn.grid(row=0, column=2, padx=5)

        submit_btn = tk.Button(self.root, text="SUBMIT GAME", command=self.submit_clicked,
                                font=("Arial", 14, "bold"), bg="#A67B5B", fg="black",
                                highlightbackground="#A67B5B", padx=20, pady=10)
        submit_btn.pack(pady=10)

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

        # 1. Check if board is full
        full = True
        for r in range(9):
            for c in range(9):
                if board[r][c] == 0:
                    full = False
                    break
            if not full: break
        
        if not full:
            messagebox.showwarning("Incomplete", "Please fill the entire board first. You can only use 'Solve' if your full solution is wrong.")
            return

        # 2. Check if the full board is already valid
        valid = True
        for r in range(9):
            for c in range(9):
                val = board[r][c]
                board[r][c] = 0
                if not is_valid(board, r, c, val):
                    valid = False
                    board[r][c] = val
                    break
                board[r][c] = val
            if not valid: break
        
        if valid:
            messagebox.showinfo("Already Correct", "Great job! Your solution is already correct.")
            return

        # 3. If full and invalid, run backtracking
        if solve(board):
            self.set_board(board)
            messagebox.showinfo("Solved", "Your logic had some errors, so I corrected it using Backtracking!")
        else:
            messagebox.showerror("No Solution", "This Sudoku is unsolvable with these numbers.")

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
        self.start_timer()

    def submit_clicked(self):
        board = self.get_board()
        if board is None: return

        # Check if board is full
        for r in range(9):
            for c in range(9):
                if board[r][c] == 0:
                    messagebox.showwarning("Incomplete", "Please fill all cells before submitting!")
                    return

        # Validate board
        for r in range(9):
            for c in range(9):
                val = board[r][c]
                board[r][c] = 0
                if not is_valid(board, r, c, val):
                    board[r][c] = val
                    messagebox.showerror("Error", f"Wrong value at row {r+1}, column {c+1}!")
                    return
                board[r][c] = val

        self.stop_timer()
        minutes = self.elapsed_seconds // 60
        seconds = self.elapsed_seconds % 60
        time_str = f"{minutes}m {seconds}s"
        
        res = messagebox.askyesno("Victory!", f"Congratulations! You solved it in {time_str}.\nDo you want to play the next puzzle?")
        if res:
            self.new_game(self.current_difficulty)

if __name__ == "__main__":
    root = tk.Tk()
    SudokuGUI(root)
    root.mainloop()
