import networkx as nx
import tkinter as tk
import math
import random

# Define the size of the game board (9x9)
BOARD_SIZE = 9
color = random.choice(['R', 'B'])
current_player = color

def get_row_col_new_old(event, cell_frames):
    for (r, c), frame in cell_frames.items():
            if frame.winfo_children()[0] == event.widget:
                row = r; col = c
                break
    for r, c in G.nodes:
        if G.nodes[(r, c)]['value'] == color:
            old_row = r; old_col = c
            break
    return row, col, old_row, old_col

def change_color(color):
    if color == "B":
        return "R"
    return "B"

# def check_movement_pawn(G, row, col, old_row, old_col, color):
#     print(color, current_player)
#     if color == current_player:
#         return True
#     return False

# Function to handle a cell (pawn) click event
def cell_click_pawn(event, cell_frames, G, label):
    global color
    row, col, old_row, old_col = get_row_col_new_old(event, cell_frames)

    if True:
        # Put the game pieces at the (row, col) position
        G.nodes[(row, col)]["value"] = color
        G.nodes[(old_row, old_col)]["value"] = "X"

        # Update colour -> row, col = colour; instead old_row, old_col -> again gray
        cell_frames[(old_row, old_col)].winfo_children()[0].configure(bg="gray")
        if color == "B":
            cell_frames[(row, col)].winfo_children()[0].config(bg="blue")
        if color == "R":
            cell_frames[(row, col)].winfo_children()[0].config(bg="red")
        color = change_color(color)
        text = "It's " + color + "'s turn!"
        label.config(text=text)
# Function to handle a cell (wall) click event
def cell_click_wall(event, b):
    row, col = event.widget.grid_info()["row"], event.widget.grid_info()["column"]
    b.configure(bg='yellow')

def draw_board(window, G, label):
    cell_frames = {}
    # Through the nodes (cells) of the game board
    for row, col in G.nodes:
        # Create a frame for the current cell
        cell_frame = tk.Frame(window, width=40, height=40, relief="solid")
        # Determine the background color for the cell based on the cell value
        if G.nodes[(row, col)]['value'] == "B":
            cell_bg = 'blue'  # Blue for Player B
        elif G.nodes[(row, col)]['value'] == "R":
            cell_bg = 'red'   # Red for Player R
        else:
            cell_bg = 'gray'  # Gray for empty cells

        # Create an inner frame for the cell with the determined background color
        cell_inner_frame = tk.Frame(cell_frame, width=40, height=40, bg=cell_bg)
        cell_inner_frame.grid(row=0, column=0)

        # Check if this cell is not in the last column
        if col != (BOARD_SIZE - 1):
            adjacent_bg = '#2c2c2c'  # Background color for the adjacent cell
            # Create a frame to represent the border between adjacent cells (horizontally)
            under_frame = tk.Frame(cell_frame, width=10, height=40, bg=adjacent_bg)
            under_frame.grid(row=0, column=1)

        # Check if this cell is not in the last row
        if row != (BOARD_SIZE - 1):
            adjacent_bg = '#2c2c2c'  # Background color for the adjacent cell
            # Create a frame to represent the border between adjacent cells (vertically)
            lateral_frame = tk.Frame(cell_frame, width=40, height=10, bg=adjacent_bg)
            lateral_frame.grid(row=1, column=0)

        # Place the main cell frame within the game board grid
        cell_frame.grid(row=row, column=col)
        cell_frames[(row, col)] = cell_frame
        
        # Bind the click event to the inner cell frame
        cell_inner_frame.bind("<Button-1>", lambda event, cell_frames=cell_frames, 
                              G=G, label=label: cell_click_pawn(event, cell_frames, G, label))
        # Bind the click event to the horizontal border frame (under_frame)
        under_frame.bind("<Button-1>", lambda event, cell_frame=under_frame: cell_click_wall(event, cell_frame))
        # Bind the click event to the vertical border frame (lateral_frame)
        lateral_frame.bind("<Button-1>", lambda event, cell_frame=lateral_frame: cell_click_wall(event, cell_frame))

# Create a grid graph
G = nx.grid_2d_graph(BOARD_SIZE, BOARD_SIZE)
# Assign the empty value for each cell of the grid
node_values = {(x, y): "X" for x in range(BOARD_SIZE) for y in range(BOARD_SIZE)}
# Put the game pieces at the starting position
node_values[(0, math.floor(BOARD_SIZE / 2))] = "R"
node_values[(BOARD_SIZE - 1, math.floor(BOARD_SIZE / 2))] = "B"
# Set the value for each vertex
nx.set_node_attributes(G, values=node_values, name="value")

# Create a Tkinter window
window = tk.Tk()
window.title("Quoridor Game")
# Add a label below the board
text = "Welcome! " + color + " starts!"
label = tk.Label(window, text=text, font=("Helvetica", 14))
label.grid(row=BOARD_SIZE, columnspan=BOARD_SIZE)

draw_board(window, G, label)

# Start the Tkinter main loop
window.mainloop()