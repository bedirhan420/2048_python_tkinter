import tkinter as tk
import random
import numpy as np

class Game2048:
    def __init__(self, master):
        self.master = master
        self.master.title("2048 Oyunu")
        
        self.size = 4
        self.colors = {
            0: "#cdc1b4", 2: "#eee4da", 4: "#ede0c8", 8: "#f2b179",
            16: "#f59563", 32: "#f67c5f", 64: "#f65e3b", 128: "#edcf72",
            256: "#edcc61", 512: "#edc850", 1024: "#edc53f", 2048: "#edc22e"
        }
        self.grid = np.zeros((self.size, self.size), dtype=int)
        self.add_2()
        self.add_2()

        self.frame = tk.Frame(self.master)
        self.frame.grid()
        self.cells = [[tk.Label(self.frame, text="", width=4, height=2, font=("Arial", 24), bg="#cdc1b4", fg="#776e65", borderwidth=2, relief="solid")
                       for _ in range(self.size)] for _ in range(self.size)]
        for i in range(self.size):
            for j in range(self.size):
                self.cells[i][j].grid(row=i, column=j, padx=5, pady=5)

        self.update_grid()
        self.master.bind("<Key>", self.key_handler)

    def add_2(self):
        empty_cells = [(i, j) for i in range(self.size) for j in range(self.size) if self.grid[i][j] == 0]
        if empty_cells:
            i, j = random.choice(empty_cells)
            self.grid[i][j] = 2

    def compress(self, mat):
        new_mat = np.zeros_like(mat)
        for i in range(len(mat)):
            pos = 0
            for j in range(len(mat[0])):
                if mat[i][j] != 0:
                    new_mat[i][pos] = mat[i][j]
                    pos += 1
        return new_mat

    def merge(self, mat):
        for i in range(len(mat)):
            for j in range(len(mat[0]) - 1):
                if mat[i][j] == mat[i][j + 1] and mat[i][j] != 0:
                    mat[i][j] = mat[i][j] * 2
                    mat[i][j + 1] = 0
        return mat

    def reverse(self, mat):
        return np.flip(mat, axis=1)

    def transpose(self, mat):
        return np.transpose(mat)

    def move_left(self):
        self.grid = self.compress(self.grid)
        self.grid = self.merge(self.grid)
        self.grid = self.compress(self.grid)

    def move_right(self):
        self.grid = self.reverse(self.grid)
        self.move_left()
        self.grid = self.reverse(self.grid)

    def move_up(self):
        self.grid = self.transpose(self.grid)
        self.move_left()
        self.grid = self.transpose(self.grid)

    def move_down(self):
        self.grid = self.transpose(self.grid)
        self.move_right()
        self.grid = self.transpose(self.grid)

    def update_grid(self):
        for i in range(self.size):
            for j in range(self.size):
                value = self.grid[i][j]
                self.cells[i][j].config(text=str(value) if value != 0 else "",
                                        bg=self.colors[value])
        self.frame.update_idletasks()

    def key_handler(self, event):
        if event.keysym == 'Up':
            self.move_up()
        elif event.keysym == 'Down':
            self.move_down()
        elif event.keysym == 'Left':
            self.move_left()
        elif event.keysym == 'Right':
            self.move_right()
        else:
            return

        self.add_2()
        self.update_grid()

        if self.is_game_over():
            self.show_game_over()

    def is_game_over(self):
        if any(0 in row for row in self.grid):
            return False
        for i in range(self.size):
            for j in range(self.size - 1):
                if self.grid[i][j] == self.grid[i][j + 1]:
                    return False
        for i in range(self.size - 1):
            for j in range(self.size):
                if self.grid[i][j] == self.grid[i + 1][j]:
                    return False
        return True
    
    def reset_game(self):
        self.grid = np.zeros((self.size, self.size), dtype=int)
        self.add_2()
        self.add_2()
        self.update_grid()
   
    def reset_and_destroy(self, frame):
        frame.destroy()
        self.reset_game()
   
    def show_game_over(self):
        game_over_frame = tk.Frame(self.master, bg="#ffffff")
        game_over_frame.place(relx=0.5, rely=0.5, anchor="center")
        tk.Label(game_over_frame, text="Oyun Bitti!", font=("Arial", 24), fg="red", bg="#ffffff").pack(pady=10)
        tk.Button(game_over_frame, text="Tekrar Oyna", font=("Arial", 24), fg="red", bg="#ffffff",cursor="hand2", command=lambda: self.reset_and_destroy(game_over_frame)).pack(pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    game = Game2048(root)
    root.mainloop()
