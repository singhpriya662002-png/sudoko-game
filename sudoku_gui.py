import tkinter as tk
from tkinter import messagebox
from sudoku_logic import solve, is_valid, generate_puzzle
from PIL import Image, ImageTk
import os

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
        self.game_started = False
        self.assets_path = os.path.join(os.path.dirname(__file__), "assets")
        self.load_assets()
        
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

    def load_assets(self):
        try:
            # Banner sticker at the top
            banner_img = Image.open(os.path.join(self.assets_path, "banner.png"))
            banner_img = banner_img.resize((150, 60), Image.LANCZOS)
            self.banner_photo = ImageTk.PhotoImage(banner_img)

            # Pencil sticker at the bottom corner
            pencil_img = Image.open(os.path.join(self.assets_path, "pencil.png"))
            pencil_img = pencil_img.resize((60, 60), Image.LANCZOS)
            self.pencil_photo = ImageTk.PhotoImage(pencil_img)

            # Trophy sticker (shown later or somewhere)
            trophy_img = Image.open(os.path.join(self.assets_path, "trophy.png"))
            trophy_img = trophy_img.resize((60, 60), Image.LANCZOS)
            self.trophy_photo = ImageTk.PhotoImage(trophy_img)
        except Exception as e:
            print(f"Error loading stickers: {e}")
            self.banner_photo = None
            self.pencil_photo = None
            self.trophy_photo = None

    def create_grid(self):
        # Add decorative sticker before grid
        if hasattr(self, 'banner_photo') and self.banner_photo:
            tk.Label(self.root, image=self.banner_photo, bg="#1A120B").pack(pady=5)
            
        frame = tk.Frame(self.root, bg="#3C2A21", padx=10, pady=10)
        frame.pack(pady=10)
        
        for r in range(9):
            for c in range(9):
                padx = (1, 1)
                pady = (1, 1)
                if c % 3 == 0 and c != 0: padx = (5, 1)
                if r % 3 == 0 and r != 0: pady = (5, 1)
                
                entry = tk.Entry(frame, width=2, font=('Arial', 24, 'bold'), 
                                justify='center', borderwidth=0, relief="flat",
                                bg="#1A120B", fg="#E5E5CB", insertbackground="#E5E5CB",
                                state='disabled', disabledbackground="#1A120B", disabledforeground="#D5CEA3")
                entry.grid(row=r, column=c, padx=padx, pady=pady, sticky="nsew")
                entry.bind("<Key>", lambda e: self.reset_cell_colors())
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

    def reset_cell_colors(self):
        for r in range(9):
            for c in range(9):
                self.cells[(r, c)].config(bg="#1A120B", fg="#E5E5CB", disabledbackground="#1A120B")

    def new_game(self, difficulty):
        self.current_difficulty = difficulty
        self.game_started = False
        self.level_label.config(text=f"LEVEL: {difficulty.upper()}")
        self.timer_label.config(text="TIME: 00:00")
        self.elapsed_seconds = 0
        self.stop_timer()
        self.reset_cell_colors()
        
        board = generate_puzzle(difficulty)
        self.clear_grid()
        self.set_board(board)
        self.reset_cell_colors()
        
        if hasattr(self, 'start_btn'):
            self.start_btn.config(state='normal', text="START GAME", bg="#8B4513", fg="black")

    def create_buttons(self):
        # Main Start Button
        self.start_btn = tk.Button(self.root, text="START GAME", command=self.start_game,
                                  font=("Arial", 14, "bold"), bg="#8B4513", fg="black",
                                  highlightbackground="#8B4513", padx=20, pady=10)
        self.start_btn.pack(pady=5)

        util_frame = tk.Frame(self.root, bg="#1A120B")
        util_frame.pack(pady=10)

        # Light brown shades for utility buttons
        solve_btn = tk.Button(util_frame, text="Solve", command=self.solve_clicked, 
                              font=("Arial", 11, "bold"), bg="#B8860B", fg="black", 
                              highlightbackground="#B8860B", padx=10, pady=5)
        solve_btn.grid(row=0, column=0, padx=5)

        clear_btn = tk.Button(util_frame, text="Clear", command=self.clear_grid, 
                               font=("Arial", 11, "bold"), bg="#D2B48C", fg="black", 
                               highlightbackground="#D2B48C", padx=10, pady=5)
        clear_btn.grid(row=0, column=1, padx=5)
        
        sample_btn = tk.Button(util_frame, text="Sample", command=self.load_sample, 
                                font=("Arial", 11, "bold"), bg="#BC8F8F", fg="black", 
                                highlightbackground="#BC8F8F", padx=10, pady=5)
        sample_btn.grid(row=0, column=2, padx=5)

        self.submit_btn = tk.Button(self.root, text="SUBMIT GAME", command=self.submit_clicked,
                                font=("Arial", 14, "bold"), bg="#A67B5B", fg="black",
                                highlightbackground="#A67B5B", padx=20, pady=5)
        self.submit_btn.pack(pady=5)

        # Quit Button
        self.quit_btn = tk.Button(self.root, text="QUIT GAME", command=self.quit_game,
                                 font=("Arial", 12, "bold"), bg="#5C4033", fg="black",
                                 highlightbackground="#5C4033", padx=20, pady=5)
        self.quit_btn.pack(pady=5)

        # Footer stickers
        footer_frame = tk.Frame(self.root, bg="#1A120B")
        footer_frame.pack(fill=tk.X, side=tk.BOTTOM, pady=5)
        
        if hasattr(self, 'pencil_photo') and self.pencil_photo:
            tk.Label(footer_frame, image=self.pencil_photo, bg="#1A120B").pack(side=tk.LEFT, padx=20)
        
        if hasattr(self, 'trophy_photo') and self.trophy_photo:
            tk.Label(footer_frame, image=self.trophy_photo, bg="#1A120B").pack(side=tk.RIGHT, padx=20)

    def quit_game(self):
        if messagebox.askyesno("Quit Game", "Are you sure you want to exit?"):
            self.root.destroy()

    def start_game(self):
        if self.game_started:
            return
            
        self.game_started = True
        self.start_btn.config(text="GAME RUNNING", state='disabled', bg="#3C2A21", disabledforeground="black")
        
        # Unlock grid
        for cell in self.cells.values():
            cell.config(state='normal')
            
        self.start_timer()

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
                self.cells[(r, c)].config(state='normal')
                self.cells[(r, c)].delete(0, tk.END)
                if board[r][c] != 0:
                    self.cells[(r, c)].insert(0, str(board[r][c]))
                if not self.game_started:
                    self.cells[(r, c)].config(state='disabled')

    def solve_clicked(self):
        if not self.game_started:
            messagebox.showwarning("Not Started", "Please click 'START GAME' first!")
            return
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
            self.reset_cell_colors()
            messagebox.showinfo("Solved", "Your logic had some errors, so I corrected it using Backtracking!")
        else:
            messagebox.showerror("No Solution", "This Sudoku is unsolvable with these numbers.")

    def clear_grid(self):
        for r in range(9):
            for c in range(9):
                self.cells[(r, c)].config(state='normal')
                self.cells[(r, c)].delete(0, tk.END)
                if not self.game_started:
                    self.cells[(r, c)].config(state='disabled')

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
        self.game_started = False
        self.timer_label.config(text="TIME: 00:00")
        self.elapsed_seconds = 0
        self.stop_timer()
        
        self.clear_grid()
        self.set_board(sample)
        self.reset_cell_colors()
        
        if hasattr(self, 'start_btn'):
            self.start_btn.config(state='normal', text="START GAME", bg="#8B4513", fg="black")

    def submit_clicked(self):
        if not self.game_started:
            messagebox.showwarning("Not Started", "The game hasn't started yet!")
            return
            
        self.reset_cell_colors()
        board = self.get_board()
        if board is None: return

        # Check if board is full
        full = True
        for r in range(9):
            for c in range(9):
                if board[r][c] == 0:
                    full = False
                    break
            if not full: break

        if not full:
            messagebox.showwarning("Incomplete", "Please fill all cells before submitting!")
            return

        # Validate board and find all errors
        errors = []
        for r in range(9):
            for c in range(9):
                val = board[r][c]
                board[r][c] = 0
                if not is_valid(board, r, c, val):
                    errors.append((r, c))
                board[r][c] = val

        if errors:
            for r, c in errors:
                # Highlight incorrect cell with red background
                self.cells[(r, c)].config(bg="#721c24", fg="white")
            messagebox.showerror("Mistakes Found", f"You have {len(errors)} incorrect inputs! These have been highlighted in red.")
            return

        self.stop_timer()
        minutes = self.elapsed_seconds // 60
        seconds = self.elapsed_seconds % 60
        time_str = f"{minutes:02d}:{seconds:02d}"
        
        self.show_victory_screen(time_str, self.elapsed_seconds)

    def show_victory_screen(self, time_str, seconds):
        # Calculate score
        base_scores = {"Easy": 1000, "Medium": 2500, "Hard": 5000}
        mult = {"Easy": 1, "Medium": 2, "Hard": 3}
        score = base_scores.get(self.current_difficulty, 1000) - (seconds * mult.get(self.current_difficulty, 1))
        score = max(score, 100)
        
        # Determine feedback
        if seconds < 120: feedback = "Flash Mode! ⚡️ You're legendary!"
        elif seconds < 300: feedback = "Sudoku Pro! 🧠 Excellent logic!"
        else: feedback = "Persistent Winner! 🏆 Great job!"
        
        # Create Victory Window
        vic_win = tk.Toplevel(self.root)
        vic_win.title("Sudoku Champion!")
        vic_win.geometry("400x520")
        vic_win.configure(bg="#1A120B")
        vic_win.transient(self.root)
        vic_win.grab_set()

        # Center window relative to parent
        try:
            self.root.update_idletasks()
            x = self.root.winfo_x() + (self.root.winfo_width() // 2) - 200
            y = self.root.winfo_y() + (self.root.winfo_height() // 2) - 260
            vic_win.geometry(f"+{x}+{y}")
        except: pass
        
        # Main Title
        tk.Label(vic_win, text="VICTORY!", font=("Arial", 32, "bold"), 
                 bg="#1A120B", fg="#D5CEA3").pack(pady=20)
                 
        # Trophy Sticker (reloaded to keep size consistent)
        if hasattr(self, 'trophy_photo') and self.trophy_photo:
            tk.Label(vic_win, image=self.trophy_photo, bg="#1A120B").pack(pady=10)
            
        # Stats Frame
        stats_frame = tk.Frame(vic_win, bg="#3C2A21", padx=30, pady=20)
        stats_frame.pack(fill=tk.X, padx=40, pady=15)
        
        tk.Label(stats_frame, text=f"TIME: {time_str}", font=("Arial", 16, "bold"), 
                 bg="#3C2A21", fg="#E5E5CB").pack()
        tk.Label(stats_frame, text=f"SCORE: {score}", font=("Arial", 18, "bold"), 
                 bg="#3C2A21", fg="#D5CEA3").pack(pady=5)
                 
        # Feedback Line
        tk.Label(vic_win, text=feedback, font=("Arial", 13, "italic bold"), 
                 bg="#1A120B", fg="#BC8F8F", wraplength=350).pack(pady=15)
                 
        # Buttons
        btn_frame = tk.Frame(vic_win, bg="#1A120B")
        btn_frame.pack(pady=20)
        
        # Helper to start new game from dialog
        def restart():
            vic_win.destroy()
            self.new_game(self.current_difficulty)

        next_btn = tk.Button(btn_frame, text="NEXT PUZZLE", 
                             command=restart,
                             font=("Arial", 11, "bold"), bg="#A67B5B", fg="black", padx=15, pady=8)
        next_btn.pack(side=tk.LEFT, padx=10)
        
        close_btn = tk.Button(btn_frame, text="CLOSE", 
                              command=vic_win.destroy,
                              font=("Arial", 11, "bold"), bg="#D2B48C", fg="black", padx=15, pady=8)
        close_btn.pack(side=tk.LEFT, padx=10)

if __name__ == "__main__":
    root = tk.Tk()
    SudokuGUI(root)
    root.mainloop()
