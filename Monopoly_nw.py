import random
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk

class MonopolyGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Monopoly Game")
        self.root.geometry("1000x700")
        self.root.minsize(800, 600)
        self.root.configure(bg="#2E2E2E")
        
        # Game State
        self.players = []
        self.game_started = False
        self.current_player = 0
        self.visited = set()
        
        # Start Screen
        self.create_start_screen()
        
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
        
        # Initialize Board
        self.board, self.tile_values, self.tile_texts = self.create_board()
        self.draw_board()
        
        # Bind resize event
        self.canvas.bind("<Configure>", self.on_resize)
        
    def on_resize(self, event):
        self.draw_board()
        
    def create_board(self):
        perimeter = []
        for row in range(6, -1, -1): perimeter.append((row, 6))
        for col in range(5, -1, -1): perimeter.append((0, col))
        for row in range(1, 7): perimeter.append((row, 0))
        for col in range(1, 6): perimeter.append((6, col))
        
        tile_values = []
        tile_texts = []
        corners = {0, 6, 12, 18}
        for i in range(24):
            tile_values.append(0 if i in corners else random.randint(10, 200))
            tile_texts.append(f"Tile {i+1}" if i not in corners else "Corner")
        return perimeter, tile_values, tile_texts
        
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
        
        for idx, (row, col) in enumerate(self.board):
            x = col * tile_size + tile_size//2
            y = row * tile_size + tile_size//2
            
            # Draw tile
            self.canvas.create_rectangle(x-tile_size//2, y-tile_size//2,
                                        x+tile_size//2, y+tile_size//2,
                                        fill="#E0E0E0", outline="black")
            
            # Tile text
            self.canvas.create_text(x, y-10, text=self.tile_texts[idx],
                                   font=("Arial", 10), fill="black")
            
            # Dummy hyperlink
            self.canvas.create_text(x, y+10, text="[Edit Link]", 
                                   font=("Arial", 8), fill="blue")
            
        # Draw players
        for player in self.players:
            if player['started']:
                row, col = self.board[player['position']]
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
            player['score'] += self.tile_values[new_pos]
            
            messagebox.showinfo("Moved", 
                f"{player['name']} moved to Tile {new_pos+1}\nScore: +{self.tile_values[new_pos]}")
            
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