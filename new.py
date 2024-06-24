import random
import tkinter as tk
from functools import partial
from tkinter import messagebox

# Function to display the board
def display_board(board):
    for row in board:
        print(" ".join(row))
    print()

# Function to check for a winning state
def check_winner(board, player):
    # Rows
    for row in board:
        if all(cell == player for cell in row):
            return True
    # Columns
    for col in range(3):
        if all(board[row][col] == player for row in range(3)):
            return True
    # Diagonals
    if board[0][0] == board[1][1] == board[2][2] == player or board[0][2] == board[1][1] == board[2][0] == player:
        return True
    return False

# to handle player move in the UI
def player_move(row, col):
    if board[row][col] == "_":
        board[row][col] = "X"
        # display_board(board) #remove comment if you need display in terminal
        update_board_buttons()
        if check_winner(board, "X"):
            messagebox.showinfo("Game Over", "Congratulations! You win!")
            root.destroy()
        elif board_full(board):
            messagebox.showinfo("Game Over", "It's a tie!")
            root.destroy()
        else:
            ai_move()

# to update the GUI board buttons
def update_board_buttons():
    for i in range(3):
        for j in range(3):
            if board[i][j] == "_":
                buttons[i][j].config(text=" ", state="normal")
            else:
                buttons[i][j].config(text=board[i][j], state="disabled")

# to check if the board is full
def board_full(board):
    for row in board:
        for cell in row:
            if cell == "_":
                return False
    return True


# Minimax algorithm for AI move (Brute force)
def minimax(board, depth, maximizing_player):
    # Base cases for terminal states (win/lose/draw)

    if check_winner(board, "O"):
        return 1
    elif check_winner(board, "X"):
        return -1
    elif board_full(board):
        return 0

    if maximizing_player:
        max_eval = float('-inf')
        best_move = None
        for row in range(3):
            for col in range(3):
                if board[row][col] == "_":
                    board[row][col] = "O"
                    eval = minimax(board, depth + 1, False)
                    board[row][col] = "_"
                    if eval > max_eval:
                        max_eval = eval
                        if depth == 0:
                            best_move = (row, col)
        if depth == 0:
            return best_move
        return max_eval
    else:
        min_eval = float('inf')
        for row in range(3):
            for col in range(3):
                if board[row][col] == "_":
                    board[row][col] = "X"
                    eval = minimax(board, depth + 1, True)
                    board[row][col] = "_"
                    if eval < min_eval:
                        min_eval = eval
        return min_eval

# Function for easy mode AI move (Randomized algorithm)
def easy_ai_move(board):
    empty_cells = [(i, j) for i in range(len(board)) for j in range(len(board)) if board[i][j] == "_"]
    return random.choice(empty_cells) if empty_cells else None

# Function for medium mode AI move (Rule based straight forward algorithm evaluating all possibilities)
def straightforward_ai_move(board):
    # Check for winning moves
    for i in range(3):
        for j in range(3):
            if board[i][j] == "_":
                board[i][j] = "O"
                if check_winner(board, "O"):
                    return i, j
                board[i][j] = "_"
    
    # Check for opponent's winning moves and block
    for i in range(3):
        for j in range(3):
            if board[i][j] == "_":
                board[i][j] = "X"
                if check_winner(board, "X"):
                    return i, j
                board[i][j] = "_"
    
    # Select center if available
    if board[1][1] == "_":
        return 1, 1
    
    # Select a corner
    corners = [(0, 0), (0, 2), (2, 0), (2, 2)]
    random.shuffle(corners)
    for corner in corners:
        if board[corner[0]][corner[1]] == "_":
            return corner
    
    # Select any available side position
    sides = [(0, 1), (1, 0), (1, 2), (2, 1)]
    random.shuffle(sides)
    for side in sides:
        if board[side[0]][side[1]] == "_":
            return side

    return None

# Function for medium mode AI move (Heuristic algorithm considering the best moves and eliminating the need to evaluate ALL the possible moves)
def heuristic_ai_move(board):
    for i in range(3):
        # Check for winning moves
        for j in range(3):
            if board[i][j] == "_":
                board[i][j] = "O"
                if check_winner(board, "O"):
                    return i, j
                board[i][j] = "_"

        # Check for opponent's winning moves to block
        for j in range(3):
            if board[i][j] == "_":
                board[i][j] = "X"
                if check_winner(board, "X"):
                    return i, j
                board[i][j] = "_"

    # Prefer center
    if board[1][1] == "_":
        return 1, 1

    # Prefer corners
    corners = [(0, 0), (0, 2), (2, 0), (2, 2)]
    random.shuffle(corners)
    for corner in corners:
        if board[corner[0]][corner[1]] == "_":
            return corner

    # If no heuristic move found, make a random move
    empty_cells = [(i, j) for i in range(3) for j in range(3) if board[i][j] == "_"]
    return random.choice(empty_cells) if empty_cells else None


# Function for AI move in the UI
def ai_move():
    # Choose AI move based on difficulty
    difficulty = difficulty_var.get()
    if difficulty == "Easy (Random)":
        ai_row, ai_col = easy_ai_move(board)
    elif difficulty == "Medium (Rule Based)":
        ai_row, ai_col = straightforward_ai_move(board)
    elif difficulty == "Hard (Mini-Max Brute Force)":
        ai_row, ai_col = minimax(board, 0, True)
    elif difficulty == "Medium (Heuristic)":
        ai_row, ai_col = heuristic_ai_move(board)
    else:
        messagebox.showerror("Error", "Invalid difficulty level!")
        return

    board[ai_row][ai_col] = "O"
    # display_board(board) #remove comment if you need display in terminal
    update_board_buttons()
    if check_winner(board, "O"):
        messagebox.showinfo("Game Over", "AI wins! Better luck next time.")
        root.destroy()
    elif board_full(board):
        messagebox.showinfo("Game Over", "It's a tie!")
        root.destroy()

# UI setup using tkinter library using tkinter's documentation
root = tk.Tk()
root.title("Tic Tac Toe")

board = [["_"] * 3 for _ in range(3)]
buttons = []

for i in range(3):
    row_buttons = []
    for j in range(3):
        button = tk.Button(root, text=" ", font=("Arial", 30), width=8, height=2, command=lambda row=i, col=j: player_move(row, col))
        button.grid(row=i, column=j)
        row_buttons.append(button)
    buttons.append(row_buttons)

difficulty_var = tk.StringVar(root)
difficulty_var.set("Easy (Random)")
difficulty_menu = tk.OptionMenu(root, difficulty_var, "Easy (Random)", "Medium (Rule Based)", "Medium (Heuristic)", "Hard (Mini-Max Brute Force)")
difficulty_menu.grid(row=3, column=1, pady=10)

root.mainloop()

