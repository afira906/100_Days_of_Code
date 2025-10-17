import tkinter as tk
from tkinter import messagebox


class TicTacToe:

    def __init__(self, window):
        self.window = window
        self.window.title("Tic Tac Toe")
        self.window.config(padx=100, pady=100)

        # Game Variables
        self.current_player = "X"
        self.board = ["", "", "", "", "", "", "", "", ""]
        self.game_over = False

        # Create Buttons
        self.buttons = []
        for i in range(9):
            btn = tk.Button(
                window,
                text="",
                font=('Arial', 20),
                height=1,
                width=3,
                command=lambda idx=i: self.on_click(idx)
            )
            btn.grid(row=i // 3, column=i % 3)
            self.buttons.append(btn)

        # Reset Button
        self.reset_btn = tk.Button(
            window,
            text="Reset Game",
            font=('Arial', 12),
            command=self.reset_game
        )
        self.reset_btn.grid(row=3, column=0, columnspan=3, sticky="nsew")

    def check_winner(self):
        # Check Rows
        for i in range(0, 9, 3):
            if self.board[i] == self.board[i + 1] == self.board[i + 2] != "":
                self.highlight_winning_buttons(i, i + 1, i + 2)
                return True

        # Check Columns
        for i in range(3):
            if self.board[i] == self.board[i + 3] == self.board[i + 6] != "":
                self.highlight_winning_buttons(i, i + 3, i + 6)
                return True

        # Check Diagonals
        if self.board[0] == self.board[4] == self.board[8] != "":
            self.highlight_winning_buttons(0, 4, 8)
            return True
        if self.board[2] == self.board[4] == self.board[6] != "":
            self.highlight_winning_buttons(2, 4, 6)
            return True

        return False

    def highlight_winning_buttons(self, *indices):
        for i in indices:
            self.buttons[i].config(bg="light green")

    def on_click(self, index):
        if self.board[index] == "" and not self.game_over:
            self.board[index] = self.current_player
            self.buttons[index].config(text=self.current_player)

            if self.check_winner():
                messagebox.showinfo("Game Over", f"Player {self.current_player} wins!")
                self.game_over = True
            elif "" not in self.board:
                messagebox.showinfo("Game Over", "It's a tie!")
                self.game_over = True
            else:
                self.current_player = "0" if self.current_player == "X" else "X"

    def reset_game(self):
        self.current_player = "X"
        self.board = ["", "", "", "", "", "", "", "", ""]
        self.game_over = False
        for button in self.buttons:
            button.config(text="", bg="SystemButtonFace")


window = tk.Tk()
game = TicTacToe(window)
window.mainloop()
