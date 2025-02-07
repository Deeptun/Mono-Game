import random
import tkinter as tk
import webbrowser
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
        
        # Initialize Board with hardcoded properties
        self.tiles = self.create_initial_tiles()
        
        # Start Screen
        self.create_start_screen()

    def create_initial_tiles(self):
        # Hardcoded tile properties
        return [
            {'text': "Go",        'value': 0,   'hyperlink': "https://en.wikipedia.org/wiki/Go_(Monopoly)", 'color': "#FFFFFF"},
            {'text': "Mediterranean Avenue", 'value': 60,  'hyperlink': "https://en.wikipedia.org/wiki/Go_(Monopoly)", 'color': "#8B4513"},
            {'text': "Community Chest", 'value': 0,   'hyperlink': "https://en.wikipedia.org/wiki/Go_(Monopoly)", 'color': "#F0E68C"},
            {'text': "Baltic Avenue",  'value': 60,  'hyperlink': "https://en.wikipedia.org/wiki/Go_(Monopoly)", 'color': "#8B4513"},
            {'text': "Income Tax",     'value': 200, 'hyperlink': "https://en.wikipedia.org/wiki/Go_(Monopoly)", 'color': "#FFD700"},
            {'text': "Reading Railroad", 'value': 200, 'hyperlink': "https://en.wikipedia.org/wiki/Go_(Monopoly)", 'color': "#000000"},
            {'text': "Oriental Avenue", 'value': 100, 'hyperlink': "https://en.wikipedia.org/wiki/Go_(Monopoly)", 'color': "#87CEEB"},
            {'text': "Chance",         'value': 0,   'hyperlink': "https://en.wikipedia.org/wiki/Go_(Monopoly)", 'color': "#FFA500"},
            {'text': "Vermont Avenue", 'value': 100, 'hyperlink': "https://en.wikipedia.org/wiki/Go_(Monopoly)", 'color': "#87CEEB"},
            {'text': "Connecticut Avenue", 'value': 120, 'hyperlink': "https://en.wikipedia.org/wiki/Go_(Monopoly)", 'color': "#87CEEB"},
            {'text': "Jail",           'value': 0,   'hyperlink': "https://en.wikipedia.org/wiki/Go_(Monopoly)", 'color': "#808080"},
            {'text': "St. Charles Place", 'value': 140, 'hyperlink': "https://en.wikipedia.org/wiki/Go_(Monopoly)", 'color': "#FF69B4"},
            {'text': "Electric Company", 'value': 150, 'hyperlink': "https://en.wikipedia.org/wiki/Go_(Monopoly)", 'color': "#FFFF00"},
            {'text': "States Avenue",  'value': 140, 'hyperlink': "https://en.wikipedia.org/wiki/Go_(Monopoly)", 'color': "#FF69B4"},
            {'text': "Virginia Avenue", 'value': 160, 'hyperlink': "https://en.wikipedia.org/wiki/Go_(Monopoly)", 'color': "#FF69B4"},
            {'text': "Pennsylvania Railroad", 'value': 200, 'hyperlink': "https://en.wikipedia.org/wiki/Go_(Monopoly)", 'color': "#000000"},
            {'text': "St. James Place", 'value': 180, 'hyperlink': "https://en.wikipedia.org/wiki/Go_(Monopoly)", 'color': "#FF0000"},
            {'text': "Community Chest", 'value': 0,   'hyperlink': "https://en.wikipedia.org/wiki/Go_(Monopoly)", 'color': "#F0E68C"},
            {'text': "Tennessee Avenue", 'value': 180, 'hyperlink': "https://en.wikipedia.org/wiki/Go_(Monopoly)", 'color': "#FF0000"},
            {'text': "New York Avenue", 'value': 200, 'hyperlink': "https://en.wikipedia.org/wiki/Go_(Monopoly)", 'color': "#FF0000"},
            {'text': "Free Parking",   'value': 0,   'hyperlink': "https://en.wikipedia.org/wiki/Go_(Monopoly)", 'color': "#00FF00"},
            {'text': "Kentucky Avenue", 'value': 220, 'hyperlink': "https://en.wikipedia.org/wiki/Go_(Monopoly)", 'color': "#FFA500"},
            {'text': "Chance",         'value': 0,   'hyperlink': "https://en.wikipedia.org/wiki/Go_(Monopoly)", 'color': "#FFA500"},
            {'text': "Indiana Avenue", 'value': 220, 'hyperlink': "https://en.wikipedia.org/wiki/Go_(Monopoly)", 'color': "#FFA500"},
            {'text': "Illinois Avenue", 'value': 240, 'hyperlink': "https://en.wikipedia.org/wiki/Go_(Monopoly)", 'color': "#FFA500"},
        ]

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
        
        # Configure grid weights
        self.main_frame.grid_columnconfigure(0, weight=4)
        self.main_frame.grid_columnconfigure(1, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=1)
        
        # Game Controls
        self.dice_label = tk.Label(control_frame, text="Dice: ", font=("Arial", 16), 
                                  bg="#3E3E3E", fg="white")
        self.dice_label.pack(pady=10)
        
        self.score_label = tk.Label(control_frame, text="Scores:\n", font=("Arial", 14), 
                                   bg="#3E3E3E", fg="white")
        self.score_label.pack(pady=10)
        
        self.roll_btn = tk.Button(control_frame, text="Roll Dice", command=self.roll_dice_turn,
                                 font=("Arial", 14), bg="#2196F3", fg="white")
        self.roll_btn.pack(pady=20)
        
        quit_btn = tk.Button(control_frame, text="Quit Game", command=self.root.destroy,
                            font=("Arial", 12), bg="#F44336", fg="white")
        quit_btn.pack(side=tk.BOTTOM, pady=20)
        
        # Bind events
        self.canvas.bind("<Configure>", self.on_resize)
        self.draw_board()
        
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
            
            self.players.append({
                'name': name,
                'score': initial_score or 0,
                'color': random.choice(["red", "blue", "green", "yellow"]),
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
            
            # Create clickable tile name
            text_id = self.canvas.create_text(x, y, text=tile['text'], 
                                            font=("Arial", 9), fill="black",
                                            width=tile_size-10)
            
            # Make text clickable with hand cursor
            self.canvas.tag_bind(text_id, "<Enter>", lambda e: self.root.config(cursor="hand2"))
            self.canvas.tag_bind(text_id, "<Leave>", lambda e: self.root.config(cursor=""))
            self.canvas.tag_bind(text_id, "<Button-1>", 
                               lambda e, url=tile['hyperlink']: webbrowser.open(url))
            
        # Draw players
        for player in self.players:
            if player['started']:
                pos = player['position']
                row, col = positions[pos]
                x = col * tile_size + tile_size//2
                y = row * tile_size + tile_size//2
                self.canvas.create_oval(x-10, y-10, x+10, y+10,
                                       fill=player['color'], outline="black")
                
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
                f"{player['name']} landed on {self.tiles[new_pos]['text']}\n" +
                f"Value added: {self.tiles[new_pos]['value']}")
            
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