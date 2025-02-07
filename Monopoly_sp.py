import random
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk, colorchooser

class MonopolyGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Monopoly Game")
        self.root.geometry("1200x800")
        self.root.minsize(1000, 700)
        self.root.configure(bg="#2E2E2E")
        
        # Game State
        self.players = []
        self.game_started = False
        self.current_player = 0
        self.visited = set()
        self.selected_tile = None
        
        # Initialize Board
        self.tiles = self.create_initial_tiles()
        
        # Start Screen
        self.create_start_screen()

    def create_initial_tiles(self):
        tiles = []
        for i in range(24):
            tiles.append({
                'color': "#%06x" % random.randint(0, 0xFFFFFF),
                'value': random.randint(10, 200) if i not in {0, 6, 12, 18} else 0,
                'text': f"Tile {i+1}",
                'hyperlink': f"https://tile{i+1}.com",
                'position': i
            })
        return tiles

    def create_start_screen(self):
        self.start_frame = tk.Frame(self.root, bg="#3E3E3E")
        self.start_frame.pack(expand=True, fill=tk.BOTH)
        
        title = tk.Label(self.start_frame, text="MONOPOLY", font=("Arial", 32, "bold"), 
                        bg="#3E3E3E", fg="white")
        title.pack(pady=40)
        
        btn_style = {"font": ("Arial", 16), "width": 15, "height": 2}
        
        self.start_btn = tk.Button(self.start_frame, text="Start Game", command=self.start_game,
                                  bg="#4CAF50", fg="white", **btn_style)
        self.start_btn.pack(pady=10)
        
        self.add_player_btn = tk.Button(self.start_frame, text="Add Player", command=self.add_player,
                                       bg="#2196F3", fg="white", **btn_style)
        self.add_player_btn.pack(pady=10)
        
        self.quit_btn = tk.Button(self.start_frame, text="Quit Game", command=self.root.destroy,
                                 bg="#F44336", fg="white", **btn_style)
        self.quit_btn.pack(pady=10)

    def create_game_ui(self):
        self.start_frame.destroy()
        
        # Main Game Container
        self.main_frame = tk.Frame(self.root, bg="#2E2E2E")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Board Canvas
        self.canvas = tk.Canvas(self.main_frame, bg="white", highlightthickness=0)
        self.canvas.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        
        # Control Panel
        control_frame = tk.Frame(self.main_frame, bg="#3E3E3E")
        control_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        
        # Tile Edit Panel
        self.create_tile_edit_panel(control_frame)
        
        # Configure grid weights
        self.main_frame.grid_columnconfigure(0, weight=4)
        self.main_frame.grid_columnconfigure(1, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=1)
        
        # Game Controls
        self.create_game_controls(control_frame)
        
        # Bind events
        self.canvas.bind("<Configure>", self.on_resize)
        self.canvas.bind("<Button-1>", self.select_tile)

    def create_tile_edit_panel(self, parent):
        edit_frame = tk.LabelFrame(parent, text="Tile Properties", font=("Arial", 12, "bold"),
                                  bg="#3E3E3E", fg="white")
        edit_frame.pack(pady=10, fill=tk.X)
        
        self.color_btn = tk.Button(edit_frame, text="Choose Color", command=self.choose_color,
                                  bg="#757575", fg="white")
        self.color_btn.pack(pady=5, fill=tk.X)
        
        self.value_entry = tk.Entry(edit_frame, font=("Arial", 12))
        self.value_entry.pack(pady=5, fill=tk.X)
        
        self.text_entry = tk.Entry(edit_frame, font=("Arial", 12))
        self.text_entry.pack(pady=5, fill=tk.X)
        
        self.link_entry = tk.Entry(edit_frame, font=("Arial", 12))
        self.link_entry.pack(pady=5, fill=tk.X)
        
        save_btn = tk.Button(edit_frame, text="Save Changes", command=self.save_tile_properties,
                            bg="#4CAF50", fg="white")
        save_btn.pack(pady=10, fill=tk.X)

    def create_game_controls(self, parent):
        self.dice_label = tk.Label(parent, text="Dice: ", font=("Arial", 16), 
                                  bg="#3E3E3E", fg="white")
        self.dice_label.pack(pady=10)
        
        self.score_label = tk.Label(parent, text="Scores:\n", font=("Arial", 14), 
                                   bg="#3E3E3E", fg="white")
        self.score_label.pack(pady=10)
        
        self.roll_btn = tk.Button(parent, text="Roll Dice", command=self.roll_dice_turn,
                                 font=("Arial", 14), bg="#2196F3", fg="white")
        self.roll_btn.pack(pady=20)
        
        quit_btn = tk.Button(parent, text="Quit Game", command=self.root.destroy,
                            font=("Arial", 12), bg="#F44336", fg="white")
        quit_btn.pack(side=tk.BOTTOM, pady=20)

    def on_resize(self, event):
        self.draw_board()

    def start_game(self):
        if len(self.players) < 1:
            messagebox.showwarning("Players Needed", "Add at least 1 player to start!")
            return
        self.game_started = True
        self.create_game_ui()

    def add_player(self):
        if len(self.players) >= 4:
            messagebox.showinfo("Max Players", "Maximum 4 players allowed!")
            return
            
        name = simpledialog.askstring("Add Player", "Enter player name:")
        if name:
            initial_score = simpledialog.askinteger("Initial Score", 
                                                   f"Enter initial score for {name}:",
                                                   minvalue=0, maxvalue=1000)
            color = simpledialog.askstring("Player Color", "Choose color (red, blue, green, yellow):")
            
            self.players.append({
                'name': name,
                'score': initial_score or 0,
                'color': color or "white",
                'position': 0,
                'started': False
            })

    def draw_board(self):
        self.canvas.delete("all")
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        tile_size = min(w//8, h//8)
        
        positions = []
        for row in range(6, -1, -1): positions.append((row, 6))
        for col in range(5, -1, -1): positions.append((0, col))
        for row in range(1, 7): positions.append((row, 0))
        for col in range(1, 6): positions.append((6, col))
        
        for idx, (row, col) in enumerate(positions):
            tile = self.tiles[idx]
            x = col * tile_size + tile_size//2
            y = row * tile_size + tile_size//2
            
            # Draw tile
            self.canvas.create_rectangle(x-tile_size//2, y-tile_size//2,
                                        x+tile_size//2, y+tile_size//2,
                                        fill=tile['color'], outline="black")
            
            # Tile text
            self.canvas.create_text(x, y-15, text=tile['text'],
                                   font=("Arial", 10), fill="black")
            
            # Hyperlink
            self.canvas.create_text(x, y+5, text=tile['hyperlink'], 
                                   font=("Arial", 8), fill="blue")
            
            # Value
            self.canvas.create_text(x, y+20, text=f"Value: {tile['value']}",
                                   font=("Arial", 8), fill="black")
            
        # Draw players
        for player in self.players:
            if player['started']:
                pos = player['position']
                row, col = positions[pos]
                x = col * tile_size + tile_size//2
                y = row * tile_size + tile_size//2
                self.canvas.create_oval(x-10, y-10, x+10, y+10,
                                       fill=player['color'], outline="black")

    def select_tile(self, event):
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        tile_size = min(w//8, h//8)
        
        col = (event.x) // tile_size
        row = (event.y) // tile_size
        
        # Convert to perimeter position
        positions = []
        for r in range(6, -1, -1): positions.append((r, 6))
        for c in range(5, -1, -1): positions.append((0, c))
        for r in range(1, 7): positions.append((r, 0))
        for c in range(1, 6): positions.append((6, c))
        
        for idx, (r, c) in enumerate(positions):
            if r == row and c == col:
                self.selected_tile = idx
                self.update_edit_form()
                break

    def update_edit_form(self):
        if self.selected_tile is None:
            return
            
        tile = self.tiles[self.selected_tile]
        self.value_entry.delete(0, tk.END)
        self.value_entry.insert(0, str(tile['value']))
        self.text_entry.delete(0, tk.END)
        self.text_entry.insert(0, tile['text'])
        self.link_entry.delete(0, tk.END)
        self.link_entry.insert(0, tile['hyperlink'])

    def choose_color(self):
        color = colorchooser.askcolor()[1]
        if color:
            self.color_btn.configure(bg=color)

    def save_tile_properties(self):
        if self.selected_tile is None:
            return
            
        try:
            self.tiles[self.selected_tile]['value'] = int(self.value_entry.get())
            self.tiles[self.selected_tile]['text'] = self.text_entry.get()
            self.tiles[self.selected_tile]['hyperlink'] = self.link_entry.get()
            self.tiles[self.selected_tile]['color'] = self.color_btn.cget("bg")
            self.draw_board()
        except ValueError:
            messagebox.showerror("Invalid Input", "Value must be a number!")

    def roll_dice_turn(self):
        if not self.game_started: return
        
        player = self.players[self.current_player]
        roll = random.randint(1, 6)
        self.dice_label.config(text=f"Dice: {roll}")
        
        if not player['started']:
            if roll == 1:
                player['started'] = True
                self.visited.update([0, 1])
                player['position'] = 1
                messagebox.showinfo("Started!", f"{player['name']} has started!")
            else:
                messagebox.showinfo("Roll Again", "Need 1 to start!")
        else:
            new_pos = (player['position'] + roll) % 24
            player['position'] = new_pos
            self.visited.add(new_pos)
            player['score'] += self.tiles[new_pos]['value']
            
            messagebox.showinfo("Moved", 
                f"{player['name']} moved to {self.tiles[new_pos]['text']}\n" +
                f"Score: +{self.tiles[new_pos]['value']}")
            
        self.update_scores()
        self.draw_board()
        
        if len(self.visited) >= 24:
            self.declare_winner()
            return
            
        self.current_player = (self.current_player + 1) % len(self.players)
        
    def update_scores(self):
        scores = "\n".join([f"{p['name']}: {p['score']}" for p in self.players])
        self.score_label.config(text=f"Scores:\n{scores}")
        
    def declare_winner(self):
        max_score = max(p['score'] for p in self.players)
        winners = [p for p in self.players if p['score'] == max_score]
        
        if len(winners) == 1:
            msg = f"Winner: {winners[0]['name']} with {max_score} points!"
        else:
            names = ", ".join([w['name'] for w in winners])
            msg = f"Tie between {names} with {max_score} points!"
            
        messagebox.showinfo("Game Over", msg)
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    game = MonopolyGame(root)
    root.mainloop()