import tkinter as tk
from tkinter import ttk, messagebox
import random
import webbrowser

# Global variables
BOARD_SIZE = 7
TILE_SIZE = 80
PLAYERS = []
current_player = 0
game_started = False

# Sample tile data (you can modify these)
tile_data = {
    'values': {},
    'links': {},
    'texts': {}
}

def initialize_board():
    """Initialize the board with random values, texts, and links"""
    positions = get_perimeter_positions()
    for pos in positions:
        if pos != (BOARD_SIZE-1, BOARD_SIZE-1) and not is_corner(pos):
            tile_data['values'][pos] = random.randint(10, 100)
            tile_data['links'][pos] = f"http://example.com/tile_{pos[0]}_{pos[1]}"
            tile_data['texts'][pos] = f"Tile {pos[0]},{pos[1]}"

def is_corner(pos):
    """Check if position is a corner tile"""
    corners = [(0,0), (0,BOARD_SIZE-1), (BOARD_SIZE-1,0), (BOARD_SIZE-1,BOARD_SIZE-1)]
    return pos in corners

def get_perimeter_positions():
    """Get all positions on the perimeter of the board"""
    positions = []
    for i in range(BOARD_SIZE):
        positions.append((0, i))  # Top row
        positions.append((BOARD_SIZE-1, i))  # Bottom row
        if i > 0 and i < BOARD_SIZE-1:  # Middle rows
            positions.append((i, 0))  # Left column
            positions.append((i, BOARD_SIZE-1))  # Right column
    return positions

def create_player(name):
    """Create a new player with initial position and score"""
    if len(PLAYERS) < 4:
        PLAYERS.append({
            'name': name,
            'position': (BOARD_SIZE-1, BOARD_SIZE-1),
            'score': 0,
            'visited': set([(BOARD_SIZE-1, BOARD_SIZE-1)])
        })
        update_players_list()
        update_game_status()

def roll_dice():
    """Roll the dice and move the current player"""
    global current_player, game_started
    
    if len(PLAYERS) == 0:
        messagebox.showwarning("Warning", "Add players first!")
        return
        
    if not game_started:
        value = random.randint(1, 6)
        if value == 1:
            game_started = True
            update_game_status(f"{PLAYERS[current_player]['name']} rolled 1! Game starts!")
        else:
            update_game_status(f"{PLAYERS[current_player]['name']} rolled {value}. Need 1 to start!")
            next_player()
        return
    
    value = random.randint(1, 6)
    move_player(value)
    update_board()
    update_game_status(f"{PLAYERS[current_player]['name']} rolled {value}")
    
    # Check if current player has visited all tiles
    if has_won():
        end_game()
    else:
        next_player()

def move_player(steps):
    """Move the current player by given number of steps"""
    positions = get_perimeter_positions()
    current_pos = PLAYERS[current_player]['position']
    current_idx = positions.index(current_pos)
    new_idx = (current_idx + steps) % len(positions)
    new_pos = positions[new_idx]
    
    PLAYERS[current_player]['position'] = new_pos
    PLAYERS[current_player]['visited'].add(new_pos)
    
    if new_pos in tile_data['values']:
        PLAYERS[current_player]['score'] += tile_data['values'][new_pos]

def next_player():
    """Move to the next player"""
    global current_player
    current_player = (current_player + 1) % len(PLAYERS)

def has_won():
    """Check if current player has visited all non-corner tiles"""
    valid_positions = set(pos for pos in get_perimeter_positions() if not is_corner(pos))
    return valid_positions.issubset(PLAYERS[current_player]['visited'])

def end_game():
    """End the game and declare winner"""
    winner = max(PLAYERS, key=lambda x: x['score'])
    messagebox.showinfo("Game Over", f"Game Over!\n{winner['name']} wins with score {winner['score']}!")

def open_link(pos):
    """Open hyperlink for the given position"""
    if pos in tile_data['links']:
        webbrowser.open(tile_data['links'][pos])

def create_gui():
    """Create the main GUI window"""
    root = tk.Tk()
    root.title("Monopoly-Style Board Game")
    root.configure(bg='#f0f0f0')
    
    # Create main frames
    board_frame = tk.Frame(root, bg='#f0f0f0')
    board_frame.pack(side=tk.LEFT, padx=20, pady=20)
    
    control_frame = tk.Frame(root, bg='#f0f0f0')
    control_frame.pack(side=tk.LEFT, padx=20, pady=20, fill=tk.BOTH)
    
    # Create board
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            pos = (i, j)
            if pos in get_perimeter_positions():
                if is_corner(pos):
                    if pos == (BOARD_SIZE-1, BOARD_SIZE-1):
                        text = "GO"
                    else:
                        text = ""
                else:
                    text = f"{tile_data['values'][pos]}\n{tile_data['texts'][pos]}"
                
                btn = tk.Button(board_frame, text=text, width=8, height=4,
                              command=lambda p=pos: open_link(p))
                btn.grid(row=i, column=j, padx=2, pady=2)
                
    # Control panel
    # Add player section
    tk.Label(control_frame, text="Add Player", bg='#f0f0f0', font=('Arial', 12, 'bold')).pack(pady=5)
    player_name = tk.Entry(control_frame)
    player_name.pack(pady=5)
    tk.Button(control_frame, text="Add Player", 
              command=lambda: create_player(player_name.get()),
              bg='#4CAF50', fg='white').pack(pady=5)
    
    # Players list
    tk.Label(control_frame, text="Players", bg='#f0f0f0', font=('Arial', 12, 'bold')).pack(pady=5)
    global players_listbox
    players_listbox = tk.Listbox(control_frame, height=6)
    players_listbox.pack(pady=5, fill=tk.X)
    
    # Dice roll
    tk.Button(control_frame, text="Roll Dice", 
              command=roll_dice,
              bg='#2196F3', fg='white', width=20, height=2).pack(pady=20)
    
    # Game status
    global status_label
    status_label = tk.Label(control_frame, text="Add players to start", 
                           bg='#f0f0f0', wraplength=200)
    status_label.pack(pady=5)
    
    return root

def update_players_list():
    """Update the players listbox"""
    players_listbox.delete(0, tk.END)
    for player in PLAYERS:
        players_listbox.insert(tk.END, 
                             f"{player['name']}: Score {player['score']}")

def update_game_status(message=""):
    """Update the game status label"""
    if message:
        status_label.config(text=message)
    else:
        if len(PLAYERS) == 0:
            status_label.config(text="Add players to start")
        else:
            status_label.config(text=f"Current player: {PLAYERS[current_player]['name']}")

def update_board():
    """Update the board display"""
    # This function would update the visual representation of players
    # on the board. For simplicity, we're not implementing it here
    pass

def main():
    """Main function to start the game"""
    initialize_board()
    root = create_gui()
    root.mainloop()

if __name__ == "__main__":
    main()
