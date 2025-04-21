import os
import json
import random
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from itertools import combinations

DATA_FILE = "players.json"

class TournamentApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Foosball Tournament Manager")
        self.root.geometry("450x350")
        
        self.data = self.load_data()
        self.current_players = []
        self.teams = []
        self.matches = []
        self.postponed = []
        self.scores = {}
        self.current_match_index = 0
        
        # NEW: Configure button styles with colors
        self.configure_button_styles()
        
        self.create_main_frame()

    def configure_button_styles(self):
        # NEW: Define custom styles for buttons with different colors
        style = ttk.Style()
        
        # Style for "Add Player" button (Green)
        style.configure("Add.TButton", background="#4CAF50", foreground="white", font=('Arial', 10))
        style.map("Add.TButton", background=[('active', '#45a049')])
        
        # Style for "Start Tournament" button (Blue)
        style.configure("Start.TButton", background="#2196F3", foreground="white", font=('Arial', 10))
        style.map("Start.TButton", background=[('active', '#1e88e5')])
        
        # Style for "View Champions" button (Purple)
        style.configure("Champions.TButton", background="#9C27B0", foreground="white", font=('Arial', 10))
        style.map("Champions.TButton", background=[('active', '#8e24aa')])
        
        # Style for "Team 1 Wins" button (Dark Green)
        style.configure("Team1.TButton", background="#2E7D32", foreground="white", font=('Arial', 10))
        style.map("Team1.TButton", background=[('active', '#27632a')])
        
        # Style for "Team 2 Wins" button (Red)
        style.configure("Team2.TButton", background="#D32F2F", foreground="white", font=('Arial', 10))
        style.map("Team2.TButton", background=[('active', '#b71c1c')])
        
        # Style for "Draw" button (Gray)
        style.configure("Draw.TButton", background="#757575", foreground="white", font=('Arial', 10))
        style.map("Draw.TButton", background=[('active', '#616161')])
        
        # Style for "Postpone" button (Orange)
        style.configure("Postpone.TButton", background="#F57C00", foreground="white", font=('Arial', 10))
        style.map("Postpone.TButton", background=[('active', '#e65100')])
        
        # Style for "View Scores" button (Teal)
        style.configure("Scores.TButton", background="#009688", foreground="white", font=('Arial', 10))
        style.map("Scores.TButton", background=[('active', '#00796b')])

    def load_data(self):
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r") as f:
                return json.load(f)
        return {"names": [], "championships": {}}

    def save_data(self):
        with open(DATA_FILE, "w") as f:
            json.dump(self.data, f, indent=4)

    def create_main_frame(self):
        self.clear_window()
        
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        ttk.Label(self.main_frame, text="Select Players", font=('Arial', 16)).pack(pady=10)
        
        self.player_listbox = tk.Listbox(self.main_frame, selectmode=tk.MULTIPLE, height=10)
        for player in self.data["names"]:
            self.player_listbox.insert(tk.END, player)
        self.player_listbox.pack(pady=10)
        
        btn_frame = ttk.Frame(self.main_frame)
        btn_frame.pack(pady=10)
        
        # MODIFIED: Apply custom styles to buttons
        ttk.Button(btn_frame, text="Add Player", command=self.add_player, style="Add.TButton").pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Start Tournament", command=self.start_tournament, style="Start.TButton").pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="View Champions", command=self.show_champions, style="Champions.TButton").pack(side=tk.LEFT, padx=5)

    def add_player(self):
        name = simpledialog.askstring("Add Player", "Enter player name:")
        if name and name not in self.data["names"]:
            self.data["names"].append(name)
            self.data["championships"][name] = 0
            self.player_listbox.insert(tk.END, name)
            self.save_data()

    def start_tournament(self):
        selected = self.player_listbox.curselection()
        if not selected:
            messagebox.showerror("Error", "Please select at least one player!")
            return
        
        self.current_players = [self.data["names"][i] for i in selected]
        self.create_teams()
        self.create_matches()
        self.show_match()

    def create_teams(self):
        random.shuffle(self.current_players)
        self.teams = []
        for i in range(0, len(self.current_players), 2):
            team = self.current_players[i:i+2]
            self.teams.append(tuple(team))
        self.scores = {i: 0 for i in range(len(self.teams))}

    def create_matches(self):
        self.matches = list(combinations(range(len(self.teams)), 2))
        random.shuffle(self.matches)
        self.current_match_index = 0

    def show_match(self):
        self.clear_window()
        
        if self.current_match_index >= len(self.matches):
            self.finalize_tournament()
            return
            
        t1, t2 = self.matches[self.current_match_index]
        team1 = self.teams[t1]
        team2 = self.teams[t2]
        
        match_frame = ttk.Frame(self.root)
        match_frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        ttk.Label(match_frame, text="Current Match", font=('Arial', 14)).pack(pady=10)
        
        vs_frame = ttk.Frame(match_frame)
        vs_frame.pack(pady=20)
        
        ttk.Label(vs_frame, text=" vs ".join(team1), font=('Arial', 12)).pack(side=tk.LEFT)
        ttk.Label(vs_frame, text=" VS ", font=('Arial', 14, 'bold')).pack(side=tk.LEFT, padx=20)
        ttk.Label(vs_frame, text=" vs ".join(team2), font=('Arial', 12)).pack(side=tk.LEFT)
        
        btn_frame = ttk.Frame(match_frame)
        btn_frame.pack(pady=20)
        
        # MODIFIED: Apply custom styles to match buttons
        ttk.Button(btn_frame, text="Team 1 Wins", command=lambda: self.record_result(t1, t2, '1'), style="Team1.TButton").pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Team 2 Wins", command=lambda: self.record_result(t1, t2, '2'), style="Team2.TButton").pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Draw", command=lambda: self.record_result(t1, t2, 'd'), style="Draw.TButton").pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Postpone", command=self.postpone_match, style="Postpone.TButton").pack(side=tk.LEFT, padx=5)
        
        # MODIFIED: Apply custom style to View Scores button
        ttk.Button(match_frame, text="View Scores", command=self.show_scores, style="Scores.TButton").pack(pady=10)

    def record_result(self, t1, t2, result):
        if result == '1':
            self.scores[t1] += 3
        elif result == '2':
            self.scores[t2] += 3
        elif result == 'd':
            self.scores[t1] += 1
            self.scores[t2] += 1
        
        self.current_match_index += 1
        self.show_match()

    def postpone_match(self):
        self.postponed.append(self.matches[self.current_match_index])
        self.current_match_index += 1
        self.show_match()

    def show_scores(self):
        score_window = tk.Toplevel(self.root)
        score_window.title("Current Scores")
        
        # Set window size and center it on the screen
        window_width = 300
        window_height = 200
        screen_width = score_window.winfo_screenwidth()
        screen_height = score_window.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        score_window.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        # Increase font size for the title
        ttk.Label(score_window, text="Team Scores", font=('Arial', 14)).pack(pady=10)
        
        for idx, score in self.scores.items():
            team = " & ".join(self.teams[idx])
            ttk.Label(score_window, text=f"{team}: {score} points", font=('Arial', 12)).pack(pady=5)

    def finalize_tournament(self):
        if self.postponed:
            self.matches = self.postponed
            self.postponed = []
            self.current_match_index = 0
            self.show_match()
            return
            
        max_score = max(self.scores.values())
        winners = [i for i, s in self.scores.items() if s == max_score]
        
        if len(winners) == 1:
            self.declare_champion(winners[0])
        else:
            self.handle_tie(winners)

    def declare_champion(self, winner_idx):
        winner = self.teams[winner_idx]
        for player in winner:
            self.data["championships"][player] += 1
        self.save_data()
        
        messagebox.showinfo("Champion!", f"Champions: {' & '.join(winner)}!")
        self.create_main_frame()

    def handle_tie(self, winners):
        if len(winners) == 2:
            self.tiebreaker(winners[0], winners[1])
        else:
            messagebox.showinfo("No Champion", "Multiple tie - No champion declared!")
            self.create_main_frame()

    def tiebreaker(self, t1, t2):
        self.clear_window()
        
        tie_frame = ttk.Frame(self.root)
        tie_frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        ttk.Label(tie_frame, text="Tiebreaker Match!", font=('Arial', 14)).pack(pady=10)
        
        team1 = self.teams[t1]
        team2 = self.teams[t2]
        
        vs_frame = ttk.Frame(tie_frame)
        vs_frame.pack(pady=20)
        
        ttk.Label(vs_frame, text=" vs ".join(team1), font=('Arial', 12)).pack(side=tk.LEFT)
        ttk.Label(vs_frame, text=" VS ", font=('Arial', 14, 'bold')).pack(side=tk.LEFT, padx=20)
        ttk.Label(vs_frame, text=" vs ".join(team2), font=('Arial', 12)).pack(side=tk.LEFT)
        
        btn_frame = ttk.Frame(tie_frame)
        btn_frame.pack(pady=20)
        
        # MODIFIED: Apply custom styles to tiebreaker buttons
        ttk.Button(btn_frame, text="Team 1 Wins", command=lambda: self.declare_champion(t1), style="Team1.TButton").pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Team 2 Wins", command=lambda: self.declare_champion(t2), style="Team2.TButton").pack(side=tk.LEFT, padx=5)

    def show_champions(self):
        champ_window = tk.Toplevel(self.root)
        champ_window.title("Championship Records")
        
        ttk.Label(champ_window, text="Championship Counts", font=('Arial', 12)).pack(pady=10)
        
        for player, count in self.data["championships"].items():
            ttk.Label(champ_window, text=f"{player}: {count}").pack()

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = TournamentApp(root)
    root.mainloop()