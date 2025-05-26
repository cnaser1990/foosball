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
        self.root.geometry("500x400")

        self.data = self.load_data()
        self.current_players = []
        self.teams = []
        self.matches = []
        self.postponed = []
        self.scores = {}
        self.current_match_index = 0

        self.configure_button_styles()
        self.create_main_frame()

    def configure_button_styles(self):
        style = ttk.Style()
        style.configure("Add.TButton", background="#2196F3", foreground="black", font=('Arial', 10))
        style.configure("Start.TButton", background="#4CAF50", foreground="black", font=('Arial', 10))
        style.configure("Champions.TButton", background="#d47cf7", foreground="black", font=('Arial', 10))
        style.configure("Team1.TButton", background="#2E7D32", foreground="white", font=('Arial', 10))
        style.configure("Team2.TButton", background="#D32F2F", foreground="white", font=('Arial', 10))
        style.configure("Draw.TButton", background="#757575", foreground="white", font=('Arial', 10))
        style.configure("Postpone.TButton", background="#F57C00", foreground="white", font=('Arial', 10))
        style.configure("Scores.TButton", background="#009688", foreground="white", font=('Arial', 10))
        style.configure("Seed.TButton", background="#f59f69", foreground="black", font=('Arial', 10))

    def load_data(self):
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r") as f:
                data = json.load(f)
                if "players" not in data:  # Support old format
                    data["players"] = [{"name": name, "seed": 1} for name in data.get("names", [])]
                    data.pop("names", None)
                return data
        return {"players": [], "championships": {}}

    def save_data(self):
        with open(DATA_FILE, "w") as f:
            json.dump(self.data, f, indent=4)

    def create_main_frame(self):
        self.clear_window()

        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(expand=True, fill='both', padx=20, pady=20)

        ttk.Label(self.main_frame, text="Select Players", font=('Arial', 16)).pack(pady=10)

        self.player_listbox = tk.Listbox(self.main_frame, selectmode=tk.MULTIPLE, height=12)
        for player in self.data["players"]:
            self.player_listbox.insert(tk.END, player["name"])
        self.player_listbox.pack(pady=10)

        btn_frame = ttk.Frame(self.main_frame)
        btn_frame.pack(pady=10)

        ttk.Button(btn_frame, text="Add Player", command=self.add_player, style="Add.TButton").pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Start Tournament", command=self.start_tournament, style="Start.TButton").pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="View Champions", command=self.show_champions, style="Champions.TButton").pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Manage Seeds", command=self.manage_seeds, style="Seed.TButton").pack(side=tk.LEFT, padx=5)

    def add_player(self):
        name = simpledialog.askstring("Add Player", "Enter player name:")
        if name and not any(p["name"] == name for p in self.data["players"]):
            seed = simpledialog.askinteger("Player Seed", "Enter player seed (1 for stronger, 2 for strong):", minvalue=1, maxvalue=2)
            if seed in (1, 2):
                self.data["players"].append({"name": name, "seed": seed})
                self.data["championships"][name] = 0
                self.player_listbox.insert(tk.END, name)
                self.save_data()

    def manage_seeds(self):
        seed_window = tk.Toplevel(self.root)
        seed_window.title("Manage Player Seeds")
        seed_window.geometry("350x300")

        ttk.Label(seed_window, text="Players and Seeds", font=('Arial', 12)).pack(pady=10)

        listbox = tk.Listbox(seed_window, height=10)
        listbox.pack(pady=10, fill=tk.BOTH, expand=True)

        def refresh_list():
            listbox.delete(0, tk.END)
            for player in self.data["players"]:
                listbox.insert(tk.END, f"{player['name']} (Seed {player['seed']})")

        refresh_list()

        def change_seed():
            selection = listbox.curselection()
            if not selection:
                messagebox.showwarning("No Selection", "Please select a player to change seed.")
                return

            index = selection[0]
            player = self.data["players"][index]

            new_seed = simpledialog.askinteger("Change Seed", f"Enter new seed for {player['name']} (1 = stronger, 2 = strong):", minvalue=1, maxvalue=2)
            if new_seed in (1, 2):
                self.data["players"][index]["seed"] = new_seed
                self.save_data()
                refresh_list()

        ttk.Button(seed_window, text="Change Selected Player's Seed", command=change_seed, style="Start.TButton").pack(pady=5)

    def start_tournament(self):
        selected = self.player_listbox.curselection()
        if not selected:
            messagebox.showerror("Error", "Please select at least one player!")
            return

        selected_names = [self.player_listbox.get(i) for i in selected]
        self.current_players = [p for p in self.data["players"] if p["name"] in selected_names]

        use_seed = messagebox.askyesno("Use Seeding?", "Do you want to use seeding to create balanced teams?")
        self.create_teams(use_seed)
        self.create_matches()
        self.show_match()

    def create_teams(self, use_seed=False):
        self.teams = []
        self.scores = {}

        if use_seed:
            seed1 = [p["name"] for p in self.current_players if p["seed"] == 1]
            seed2 = [p["name"] for p in self.current_players if p["seed"] == 2]

            random.shuffle(seed1)
            random.shuffle(seed2)

            min_len = min(len(seed1), len(seed2))
            for i in range(min_len):
                self.teams.append((seed1[i], seed2[i]))

            leftovers = seed1[min_len:] + seed2[min_len:]
            random.shuffle(leftovers)
            i = 0
            while i < len(leftovers) - 1:
                self.teams.append((leftovers[i], leftovers[i+1]))
                i += 2
            if i < len(leftovers):
                self.teams.append((leftovers[i],))  # Solo team

        else:
            players = [p["name"] for p in self.current_players]
            random.shuffle(players)
            i = 0
            while i < len(players) - 1:
                self.teams.append((players[i], players[i+1]))
                i += 2
            if i < len(players):
                self.teams.append((players[i],))  # Solo team

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

        ttk.Button(btn_frame, text="Team 1 Wins", command=lambda: self.record_result(t1, t2, '1'), style="Team1.TButton").pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Team 2 Wins", command=lambda: self.record_result(t1, t2, '2'), style="Team2.TButton").pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Draw", command=lambda: self.record_result(t1, t2, 'd'), style="Draw.TButton").pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Postpone", command=self.postpone_match, style="Postpone.TButton").pack(side=tk.LEFT, padx=5)

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

        ttk.Button(btn_frame, text="Team 1 Wins", command=lambda: self.declare_champion(t1), style="Team1.TButton").pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Team 2 Wins", command=lambda: self.declare_champion(t2), style="Team2.TButton").pack(side=tk.LEFT, padx=5)

    def show_champions(self):
        champ_window = tk.Toplevel(self.root)
        champ_window.title("Championship Records")
        champ_window.geometry("350x400")
        ttk.Label(champ_window, text="🏆 Championship Leaderboard 🏆", font=('Arial', 16, 'bold')).pack(pady=15, padx=15)

        # Prepare sorted data (descending by championships, then by name)
        sorted_champs = sorted(
            self.data["championships"].items(),
            key=lambda x: (-x[1], x[0])
        )

        # Set up a Treeview for a nice table display
        columns = ("#1", "Player", "Titles")
        tree = ttk.Treeview(champ_window, columns=columns, show="headings", height=12)
        tree.heading("#1", text="Rank")
        tree.heading("Player", text="Player")
        tree.heading("Titles", text="Championships")

        # Set column widths
        tree.column("#1", width=50, anchor="center")
        tree.column("Player", width=150, anchor="center")
        tree.column("Titles", width=120, anchor="center")

        # Add data to the Treeview
        for idx, (player, count) in enumerate(sorted_champs, start=1):
            medal = ""
            if idx == 1:
                medal = "🥇 "
            elif idx == 2:
                medal = "🥈 "
            elif idx == 3:
                medal = "🥉 "
            tree.insert("", "end", values=(f"{idx}", f"{medal}{player}", count))

        tree.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)

        # Optional: Add a close button
        ttk.Button(champ_window, text="Close", command=champ_window.destroy, style="Draw.TButton").pack(pady=10)

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = TournamentApp(root)
    root.mainloop()