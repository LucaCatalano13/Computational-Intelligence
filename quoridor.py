import networkx as nx
import tkinter as tk
import math
# Define the size of the game board (9x9)
BOARD_SIZE = 9

# Function to handle a cell click event
# TODO: controllo R, B nelle posizioni giuste. Spostare R, B se condizioni ok
def cell_click(event, b):
    row, col = event.widget.grid_info()["row"], event.widget.grid_info()["column"]
    print(f"Clicked on cell ({row}, {col})")
    print(b)
    b.configure(bg='yellow')  # Change to your desired color

# Function to draw the game board
def draw_board(window, G):
    for row, col in G.nodes:
        if G.nodes[(row, col)]['value'] == "B":
            cell_label.configure(bg='blue')
        if G.nodes[(row, col)]['value'] == "R":
            cell_label.configure(bg='red')
        cell_label = tk.Label(window, width=4, height=2, relief="solid")
        cell_label.grid(row=row, column=col, padx=2, pady=2)  # Add padx and pady for spacing
        cell_label.bind("<Button-1>", lambda event, cell_label=cell_label: cell_click(event, cell_label))


# Function to place a horizontal wall
def place_horizontal_wall():
    print("Placing a horizontal wall")

# Function to place a vertical wall
def place_vertical_wall():
    print("Placing a vertical wall")

# Create a grid graph
G = nx.grid_2d_graph(BOARD_SIZE, BOARD_SIZE)
# Assign the empty value for each cell of the grid
node_values = {(x, y): "X" for x in range(BOARD_SIZE) for y in range(BOARD_SIZE)}
# Put the game pieces at the starting position
node_values[(0, math.ceil(BOARD_SIZE / 2))] = "R"
node_values[(BOARD_SIZE - 1, math.ceil(BOARD_SIZE / 2))] = "B"
# Set the value for each vertices
nx.set_node_attributes(G, values=node_values, name="value")

# Create a Tkinter window
window = tk.Tk()
window.title("Quoridor Game")
draw_board(window, G)

# Start the Tkinter main loop
window.mainloop()