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
        self.root.configure(bg="#eaf0fb")
        self.root.geometry("750x500")  # Slightly taller for aesthetics

        # Card-like container for content
        card = tk.Frame(self.root, bg="#f8f6ff", bd=3, relief="ridge")
        card.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.92, relheight=0.92)

        # Large title
        tk.Label(
            card, text="Foosball Tournament Manager", font=('Arial', 18, 'bold'),
            bg="#f8f6ff", fg="#5433a3"
        ).pack(pady=(18, 4))

        # Subtitle
        tk.Label(
            card, text="Select Players", font=('Arial', 13, 'bold'),
            bg="#f8f6ff", fg="#333"
        ).pack(pady=(0, 12))

        # Stylish Listbox with a surrounding frame for border effect
        listbox_frame = tk.Frame(card, bg="#cfd8ff", bd=2, relief="groove")
        listbox_frame.pack(pady=(0, 14), padx=28, fill=tk.X)
        self.player_listbox = tk.Listbox(
            listbox_frame, selectmode=tk.MULTIPLE, height=11,
            font=('Segoe UI', 12), bg="#f8f6ff", fg="#222",
            selectbackground="#a4b0ff", activestyle='none', relief='flat'
        )
        for player in self.data["players"]:
            self.player_listbox.insert(tk.END, player["name"])
        self.player_listbox.pack(padx=6, pady=6, fill=tk.BOTH, expand=True)

        # Button frame
        btn_frame = tk.Frame(card, bg="#f8f6ff")
        btn_frame.pack(pady=18)

        # Button styles (make them bigger/bolder, add hover effect)
        style = ttk.Style()
        style.configure("TButton", font=('Arial', 11, 'bold'), padding=8)
        style.map("TButton",
                foreground=[('active', '#fff')],
                background=[('active', '#7a83fa')])

        ttk.Button(btn_frame, text="Add Player", command=self.add_player, style="Add.TButton").pack(side=tk.LEFT, padx=8, ipadx=10)
        ttk.Button(btn_frame, text="Start Tournament", command=self.start_tournament, style="Start.TButton").pack(side=tk.LEFT, padx=8, ipadx=10)
        ttk.Button(btn_frame, text="View Champions", command=self.show_champions, style="Champions.TButton").pack(side=tk.LEFT, padx=8, ipadx=10)
        ttk.Button(btn_frame, text="Manage Seeds", command=self.manage_seeds, style="Seed.TButton").pack(side=tk.LEFT, padx=8, ipadx=10)

        # Optional: Footer hint
        tk.Label(
            card, text="Tip: Hold Ctrl (Cmd on Mac) to select multiple players",
            font=('Arial', 9), bg="#f8f6ff", fg="#888"
        ).pack(side=tk.BOTTOM, pady=(6, 10))

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
        seed_window.geometry("480x440")
        seed_window.configure(bg="#eaf0fb")
        seed_window.resizable(False, False)

        # Card-like main frame (increase relheight)
        card = tk.Frame(seed_window, bg="#f8f6ff", bd=3, relief="ridge")
        card.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.93, relheight=0.97)

        # Title
        tk.Label(
            card, text="Players and Seeds", font=('Arial', 16, 'bold'),
            bg="#f8f6ff", fg="#5433a3"
        ).pack(pady=(18, 8))

        # Listbox with border for players (reduce height)
        listbox_frame = tk.Frame(card, bg="#cfd8ff", bd=2, relief="groove")
        listbox_frame.pack(pady=(0, 16), padx=28, fill=tk.BOTH, expand=True)

        listbox = tk.Listbox(
            listbox_frame, height=10, font=('Segoe UI', 12),
            bg="#f8f6ff", fg="#222",
            selectbackground="#a4b0ff", activestyle='none', relief='flat'
        )
        listbox.pack(padx=6, pady=6, fill=tk.BOTH, expand=True)

        def refresh_list():
            listbox.delete(0, tk.END)
            for player in self.data["players"]:
                listbox.insert(tk.END, f"{player['name']} (Seed {player['seed']})")
        refresh_list()

        # Nice button style
        style = ttk.Style()
        style.configure("SeedChange.TButton", font=('Arial', 11, 'bold'), padding=8)

        def change_seed():
            selection = listbox.curselection()
            if not selection:
                messagebox.showwarning("No Selection", "Please select a player to change seed.")
                return

            index = selection[0]
            player = self.data["players"][index]

            # Use the custom beautiful dialog
            new_seed = self.ask_seed(seed_window, player["name"], player["seed"])
            if new_seed in (1, 2):
                self.data["players"][index]["seed"] = new_seed
                self.save_data()
                refresh_list()

        # Place the button in its own frame to control placement
        button_frame = tk.Frame(card, bg="#f8f6ff")
        button_frame.pack(pady=(10, 10))
        ttk.Button(
            button_frame,
            text="Change Selected Player's Seed",
            command=change_seed,
            style="SeedChange.TButton"
        ).pack(ipadx=8)

        # Optional: Footer hint
        tk.Label(
            card, text="Tip: 1 = stronger, 2 = strong",
            font=('Arial', 9), bg="#f8f6ff", fg="#888"
        ).pack(side=tk.BOTTOM, pady=(4, 12))


    def ask_seed(self, parent, player_name, current_seed):
        dialog = tk.Toplevel(parent)
        dialog.title("Change Seed")
        dialog.geometry("340x270")  # Increased height
        dialog.configure(bg="#eaf0fb")
        dialog.grab_set()
        dialog.resizable(False, False)
        dialog.transient(parent)

        # Card frame - pack fills dialog
        card = tk.Frame(dialog, bg="#f8f6ff", bd=3, relief="ridge")
        card.pack(expand=True, fill=tk.BOTH, padx=14, pady=14)

        # Title
        tk.Label(
            card, text=f"Seed for {player_name}", font=('Arial', 14, 'bold'),
            bg="#f8f6ff", fg="#5433a3"
        ).pack(pady=(18, 7))

        # Radio buttons for seed selection
        var = tk.IntVar(value=current_seed)
        radio_frame = tk.Frame(card, bg="#f8f6ff")
        radio_frame.pack(pady=10)

        tk.Radiobutton(
            radio_frame, text="1 (Stronger)", variable=var, value=1,
            font=('Arial', 12, 'bold'), bg="#e2f3fa", fg="#0c457d",
            selectcolor="#b0e3ff", indicatoron=0, width=16, pady=7, bd=2, relief="groove", anchor="w"
        ).pack(pady=7)
        tk.Radiobutton(
            radio_frame, text="2 (Strong)", variable=var, value=2,
            font=('Arial', 12, 'bold'), bg="#fae2fa", fg="#7d0c69",
            selectcolor="#edc6f8", indicatoron=0, width=16, pady=7, bd=2, relief="groove", anchor="w"
        ).pack(pady=7)

        # Button frame
        btn_frame = tk.Frame(card, bg="#f8f6ff")
        btn_frame.pack(pady=18)

        result = {"seed": None}

        def confirm():
            result["seed"] = var.get()
            dialog.destroy()

        def cancel():
            dialog.destroy()

        ttk.Button(btn_frame, text="Cancel", command=cancel, style="Draw.TButton").pack(side=tk.LEFT, padx=18, ipadx=12)
        ttk.Button(btn_frame, text="OK", command=confirm, style="Start.TButton").pack(side=tk.LEFT, padx=18, ipadx=12)

        dialog.wait_window()
        return result["seed"]

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
        match_num = self.current_match_index + 1
        total_matches = len(self.matches)

        # Set root background for consistency
        self.root.configure(bg="#e9e9e9")
        
        # Main frame uses all available space
        match_frame = tk.Frame(self.root, bg="#e9e9e9")
        match_frame.pack(expand=True, fill='both')

        # Card-like frame, fills much of the window
        card = tk.Frame(match_frame, bg="#f7f5fa", bd=4, relief="ridge")
        card.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.88, relheight=0.78)

        # Match info
        tk.Label(card, text=f"Match {match_num} of {total_matches}", font=('Arial', 13, 'bold'), bg="#f7f5fa", fg="#555").pack(pady=(18, 8))

        # Team vs Team display (centered & bold)
        vs_frame = tk.Frame(card, bg="#f7f5fa")
        vs_frame.pack(pady=25)

        def format_team(team):
            return " & ".join(team)

        tk.Label(
            vs_frame, text=format_team(team1), font=('Arial', 18, 'bold'),
            bg="#d3eafd", fg="#183153", padx=18, pady=5, bd=2, relief="groove"
        ).pack(side=tk.LEFT, padx=(0, 18))
        tk.Label(
            vs_frame, text="VS", font=('Arial', 20, 'bold'),
            bg="#f7f5fa", fg="#9C27B0", padx=10
        ).pack(side=tk.LEFT)
        tk.Label(
            vs_frame, text=format_team(team2), font=('Arial', 18, 'bold'),
            bg="#ffd3d3", fg="#8B2323", padx=18, pady=5, bd=2, relief="groove"
        ).pack(side=tk.LEFT, padx=(18, 0))

        # Buttons with good spacing
        btn_frame = tk.Frame(card, bg="#f7f5fa")
        btn_frame.pack(pady=28)

        ttk.Button(btn_frame, text="Team 1 Wins", command=lambda: self.record_result(t1, t2, '1'), style="Team1.TButton").pack(side=tk.LEFT, padx=14, ipadx=12, ipady=7)
        ttk.Button(btn_frame, text="Team 2 Wins", command=lambda: self.record_result(t1, t2, '2'), style="Team2.TButton").pack(side=tk.LEFT, padx=14, ipadx=12, ipady=7)
        ttk.Button(btn_frame, text="Draw", command=lambda: self.record_result(t1, t2, 'd'), style="Draw.TButton").pack(side=tk.LEFT, padx=14, ipadx=12, ipady=7)
        ttk.Button(btn_frame, text="Postpone", command=self.postpone_match, style="Postpone.TButton").pack(side=tk.LEFT, padx=14, ipadx=12, ipady=7)

        # View scores button at the bottom
        ttk.Button(card, text="View Scores", command=self.show_scores, style="Scores.TButton").pack(pady=(18, 12))

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