#!/usr/bin/python3

import sys
import time
import numpy as np
import tkinter as Mazegame
from termcolor import colored
from PIL import ImageTk, Image
from tkinter import ttk, Canvas, Label

#Mazegame.NoDefaultRoot()
def input_postion(n):
    try:
        src = int(input("Enter the position of Rat: "))
    except:
        src = 0

    if src not in range(0, n*n):
        print("Enter a valid Source Position")
        sys.exit()

    try:
        dest = int(input("Enter the position of Cheese: "))
    except:
        dest = n*n-1

    if dest not in range(0, n*n):
        print("Enter a valid Destination Position")
        sys.exit()

    return src, dest

def rando(n):
    limit = np.random.randint(n*n/4,n*n/2)
    check = list()

    for i in range(limit):
        hold = np.random.randint(n*n-1)
        chk = 0
        for j in range(len(check)):
            if check[j] == hold or hold == 0:
                chk = 1
        if chk == 0:
            check.append(hold)
    return check

def prepare_maze(n, check, src, dest):
    maze = [[0 for i in range(n)] for j in range(n)]
    for i in range(len(check)):
        maze[check[i]//n][check[i]%n] = 1

    maze[src//n][src%n] = 0
    maze[dest//n][dest%n] = 0

    return maze

def display_maze(n, maze, pos):
    print("")
    for i in range(n):
        for j in range(n):
            if pos == i*n+j:
                print(colored("[8]", "blue"), end="")
            elif maze[i][j] == 0:
                print(colored("[0]", "green"), end="")
            elif maze[i][j] == 1:
                print(colored("[1]", "red"), end="")
            elif maze[i][j] == -1:
                print(colored("[3]", "yellow"), end="")
            elif maze[i][j] == 2:
                print(colored("[3]", "cyan"), end="")
        print("")

def make_screen(n):
    if n in range(2,9):
       size = 300
    elif n in range(9,43):
       size = 640
    elif n in range(43, 75):
       size = 750
    else:
        print("Invalid Maze size")
        sys.exit()

    cellw = int(size/n)
    cellh = int(size/n)

    screen = Mazegame.Tk()
    screen.title("Can rat find the cheese?")
    grid = Canvas(screen, width=cellw*n, height=cellh*n, highlightthickness=0)
    grid.pack(side="top", fill="both", expand="true")

    rect = {}
    for col in range(n):
        for row in range(n):
            x1 = col * cellw
            y1 = row * cellh
            x2 = x1 + cellw
            y2 = y1 + cellh
            rect[row, col] = grid.create_rectangle(x1,y1,x2,y2, fill="red", tags="rect")
    return grid, rect, screen, cellw

def load_img(size, path, dest):
    xcod = dest//n
    ycod = dest%n
    load = Image.open(path)
    load = load.resize((size, size), Image.ANTIALIAS)
    render = ImageTk.PhotoImage(load)
    img = Label(image=render)
    img.image = render
    img.place(x = ycod*size, y = xcod*size)
    return img

def redraw_maze(grid, rect, screen, n, maze, pos, delay, size, dest):
    grid.itemconfig("rect", fill="green")
    path1 = "./go.png"
    path2 = "./cheese.jpg"
    for i in range(n):
        for j in range(n):
            item_id = rect[i,j]
            if pos == i*n+j:
                grid.itemconfig(item_id, fill="blue")
            elif maze[i][j] == 0:
                grid.itemconfig(item_id, fill="salmon3")
            elif maze[i][j] == 1:
                grid.itemconfig(item_id, fill="black")
            elif maze[i][j] == -1:
                grid.itemconfig(item_id, fill="DeepSkyBlue2")
            elif maze[i][j] == 2:
                grid.itemconfig(item_id, fill="SpringGreen2")

    load_img(size, path2, dest)
    screen.update_idletasks()
    screen.update()
    time.sleep(delay)
    return

def button(text, win, window):
    b = ttk.Button(window, text=text, command = win.destroy)
    b.pack()

def popup_win(msg, title, path, screen):
    popup = Mazegame.Tk()
    popup.wm_title(title)
    label = ttk.Label(popup, text=msg, font=("Times", 20))
    label.pack(side="top", fill="x", pady=50, padx=50)
    button("Close Maze", screen, popup)
    button("Close popup", popup, popup)
    popup.mainloop()

def path(n, maze, src, dest):
    pos = src
    stack = list()
    delay = 0.1
    path1 = "./fail.png"
    path2 = "./pass.png"
    grid, rect, screen, wid = make_screen(n)

    while pos != dest:
        r = pos//n
        c = pos%n
        if r in range(n) and c+1 in range(n) and maze[r][c+1] != 1 and maze[r][c+1] != -1 and maze[r][c+1] != 2:
            stack.append(r*n+c)
            maze[r][c] = -1
            pos = pos + 1
        elif r+1 in range(n) and c in range(n) and maze[r+1][c] != 1 and maze[r+1][c] != -1 and maze[r+1][c] != 2:
            stack.append(r*n+c)
            maze[r][c] = -1
            pos = pos + n
        elif r in range(n) and c-1 in range(n) and maze[r][c-1] != 1 and maze[r][c-1] != -1 and maze[r][c-1] != 2:
            stack.append(r*n+c)
            maze[r][c] = -1
            pos = pos - 1
        elif r-1 in range(n) and c in range(n) and maze[r-1][c] != 1 and maze[r-1][c] != -1 and maze[r-1][c] != 2:
            stack.append(r*n+c)
            maze[r][c] = -1
            pos = pos - n
        else:
            maze[pos//n][pos%n] = -1
            if len(stack) == 0:
                msg = "Rat can't find the cheese struck in maze."
                popup_win(msg, "Better luck next time", path1, screen)
                print("Rat can't find the cheese struck in maze.")
                sys.exit()
            else:
                maze[pos//n][pos%n] = 2
                pos = stack.pop()
                while check_pos(pos//n, pos%n, n, maze) != 1:
                    maze[pos//n][pos%n] = 2
                    if len(stack) == 0:
                        display_maze(n, maze, pos)
                        redraw_maze(grid, rect, screen, n, maze, pos, delay, wid, dest)
                        msg = "Rat can't find the cheese struck in maze."
                        popup_win(msg, "Better luck next time", path1, screen)
                        print("Rat can't find the cheese struck in maze.")
                        sys.exit()
                    pos = stack.pop()
                    display_maze(n, maze, pos)
                    redraw_maze(grid, rect, screen, n, maze, pos, delay, wid, dest)
                maze[pos//n][pos%n] = 2
        display_maze(n, maze, pos)
        redraw_maze(grid, rect, screen, n, maze, pos, delay, wid, dest)
    print("Rat Found The Cheese")
    msg = "Rat Found The Cheese"
    popup_win(msg, "Congrats", path2, screen)

def check_pos(r, c, n, maze):
    if r in range(n) and c+1 in range(n) and maze[r][c+1] == 0:
        return 1
    elif r+1 in range(n) and c in range(n) and maze[r+1][c] == 0:
        return 1
    elif r in range(n) and c-1 in range(n) and maze[r][c-1] == 0:
        return 1
    elif r-1 in range(n) and c in range(n) and maze[r-1][c] == 0:
        return 1
    return 0

if __name__ == "__main__":
    n = int(input("Enter the dimension of the maze: "))
    src, dest = input_postion(n)
    randno = rando(n)
    maze = prepare_maze(n, randno, src, dest)
    path(n, maze, src, dest)
