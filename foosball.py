import os
import json
import random
import tkinter as tk
from tkinter import ttk, messagebox
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
        self.current_match_index = 0

        # NEW: stats for each team: points, goals for, goals against
        self.team_stats = {}

        self.configure_button_styles()
        self.create_main_frame()

    def configure_button_styles(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Add.TButton", background="#2196F3", foreground="black", font=('Arial', 10))
        style.configure("Start.TButton", background="#4CAF50", foreground="black", font=('Arial', 10))
        style.configure("Champions.TButton", background="#d47cf7", foreground="black", font=('Arial', 10))
        style.configure("Team1.TButton", background="#2E7D32", foreground="white", font=('Arial', 10))
        style.configure("Team2.TButton", background="#D32F2F", foreground="white", font=('Arial', 10))
        style.configure("Draw.TButton", background="#757575", foreground="white", font=('Arial', 10))
        style.configure("Postpone.TButton", background="#F57C00", foreground="white", font=('Arial', 10))
        style.configure("Scores.TButton", background="#009688", foreground="white", font=('Arial', 10))
        style.configure("Seed.TButton", background="#f59f69", foreground="black", font=('Arial', 10))
        style.configure("DialogGreen.TButton", background="#4CAF50", foreground="white")
        style.map("DialogGreen.TButton",
            background=[('active', '#43a047')],
            foreground=[('active', 'white')]
        )

        style.configure("DialogRed.TButton", background="#D32F2F", foreground="white")
        style.map("DialogRed.TButton",
            background=[('active', '#b71c1c')],
            foreground=[('active', 'white')]
        )

    def load_data(self):
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r") as f:
                data = json.load(f)
                if "players" not in data:
                    data["players"] = [{"name": name, "seed": 1} for name in data.get("names", [])]
                    data.pop("names", None)
                if "scores" not in data:
                    data["scores"] = {player["name"]: 0 for player in data["players"]}
                return data
        return {"players": [], "championships": {}, "scores": {}}

    def save_data(self):
        with open(DATA_FILE, "w") as f:
            json.dump(self.data, f, indent=4)

    def create_main_frame(self):
        self.clear_window()
        self.root.configure(bg="#eaf0fb")
        self.root.geometry("750x500")

        card = tk.Frame(self.root, bg="#f8f6ff", bd=3, relief="ridge")
        card.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.92, relheight=0.92)

        tk.Label(
            card, text="Foosball Tournament Manager", font=('Arial', 18, 'bold'),
            bg="#f8f6ff", fg="#5433a3"
        ).pack(pady=(18, 4))

        tk.Label(
            card, text="Select Players", font=('Arial', 13, 'bold'),
            bg="#f8f6ff", fg="#333"
        ).pack(pady=(0, 12))

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

        btn_frame = tk.Frame(card, bg="#f8f6ff")
        btn_frame.pack(pady=18)

        style = ttk.Style()
        style.configure("TButton", font=('Arial', 11, 'bold'), padding=8)
        style.map("TButton",
                foreground=[('active', '#fff')],
                background=[('active', '#7a83fa')])

        ttk.Button(btn_frame, text="Add/Remove Player", command=self.manage_players, style="Add.TButton").pack(side=tk.LEFT, padx=8, ipadx=10)
        ttk.Button(btn_frame, text="Start Tournament", command=self.start_tournament, style="Start.TButton").pack(side=tk.LEFT, padx=8, ipadx=10)
        ttk.Button(btn_frame, text="View Champions", command=self.show_champions, style="Champions.TButton").pack(side=tk.LEFT, padx=8, ipadx=10)
        ttk.Button(btn_frame, text="Manage Seeds", command=self.manage_seeds, style="Seed.TButton").pack(side=tk.LEFT, padx=8, ipadx=10)

        tk.Label(
            card, text="Tip: Hold Ctrl (Cmd on Mac) to select multiple players",
            font=('Arial', 9), bg="#f8f6ff", fg="#888"
        ).pack(side=tk.BOTTOM, pady=(6, 10))

    def manage_players(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Add/Remove Player")
        dialog.geometry("510x390")
        dialog.configure(bg="#eaf0fb")
        dialog.grab_set()
        dialog.resizable(False, False)
        dialog.transient(self.root)

        card = tk.Frame(dialog, bg="#f8f6ff", bd=3, relief="ridge")
        card.pack(expand=True, fill=tk.BOTH, padx=18, pady=18)

        tk.Label(
            card, text="Add / Remove Players", font=('Arial', 16, 'bold'),
            bg="#f8f6ff", fg="#5433a3"
        ).pack(pady=(12, 8))

        listbox_frame = tk.Frame(card, bg="#cfd8ff", bd=2, relief="groove")
        listbox_frame.pack(pady=(0, 12), padx=18, fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(listbox_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        player_listbox = tk.Listbox(
            listbox_frame, selectmode=tk.MULTIPLE, height=7, font=('Segoe UI', 12),
            bg="#f8f6ff", fg="#222",
            selectbackground="#a4b0ff", activestyle='none', relief='flat',
            yscrollcommand=scrollbar.set
        )
        player_listbox.pack(padx=6, pady=6, fill=tk.BOTH, expand=True)
        scrollbar.config(command=player_listbox.yview)

        def refresh_players():
            player_listbox.delete(0, tk.END)
            for player in self.data["players"]:
                player_listbox.insert(tk.END, f"{player['name']} (Seed {player['seed']})")
        refresh_players()

        entry_frame = tk.Frame(card, bg="#f8f6ff")
        entry_frame.pack(pady=(6, 10))

        tk.Label(entry_frame, text="New Player Name:", font=('Arial', 11), bg="#f8f6ff").pack(side=tk.LEFT, padx=(0, 8))
        name_var = tk.StringVar()
        name_entry = tk.Entry(entry_frame, textvariable=name_var, font=('Arial', 11), width=16)
        name_entry.pack(side=tk.LEFT, padx=(0, 12))
        name_entry.focus_set()

        tk.Label(entry_frame, text="Seed:", font=('Arial', 11), bg="#f8f6ff").pack(side=tk.LEFT, padx=(0, 5))
        seed_var = tk.IntVar(value=1)
        seeds = [
            {"text": "1", "bg": "#e2f3fa", "fg": "#0c457d", "selectcolor": "#b0e3ff"},
            {"text": "2", "bg": "#fae2fa", "fg": "#7d0c69", "selectcolor": "#edc6f8"},
            {"text": "3", "bg": "#fef4e3", "fg": "#b86b00", "selectcolor": "#ffe5b0"},
        ]
        for s in seeds:
            tk.Radiobutton(
                entry_frame, text=s["text"], variable=seed_var, value=int(s["text"]),
                font=('Arial', 11, 'bold'), bg=s["bg"], fg=s["fg"],
                selectcolor=s["selectcolor"], indicatoron=0, width=3, pady=4, bd=2, relief="groove"
            ).pack(side=tk.LEFT, padx=2)

        btn_frame = tk.Frame(card, bg="#f8f6ff")
        btn_frame.pack(pady=10)

        style = ttk.Style()
        style.configure("DialogGreen.TButton", font=('Arial', 11, 'bold'), padding=8)
        style.configure("DialogRed.TButton", font=('Arial', 11, 'bold'), padding=8)
        style.configure("DialogGray.TButton", font=('Arial', 11, 'bold'), padding=8)

        def add_player_action():
            name = name_var.get().strip()
            if not name:
                messagebox.showwarning("Input Error", "Player name cannot be empty.", parent=dialog)
                return
            if any(p["name"] == name for p in self.data["players"]):
                messagebox.showwarning("Duplicate Name", f"Player '{name}' already exists!", parent=dialog)
                return
            seed = seed_var.get()
            self.data["players"].append({"name": name, "seed": seed})
            self.data["championships"][name] = 0
            self.data["scores"][name] = 0
            refresh_players()
            name_var.set("")
            self.save_data()
            if hasattr(self, "player_listbox"):
                self.player_listbox.delete(0, tk.END)
                for player in self.data["players"]:
                    self.player_listbox.insert(tk.END, player["name"])

        def remove_player_action():
            selection = player_listbox.curselection()
            if not selection:
                messagebox.showwarning("No Selection", "Please select player(s) to remove.", parent=dialog)
                return
            to_remove = [player_listbox.get(i).split(" (Seed")[0] for i in selection]
            if not messagebox.askyesno("Remove Player", f"Are you sure you want to remove the selected player(s)?", parent=dialog):
                return
            self.data["players"] = [p for p in self.data["players"] if p["name"] not in to_remove]
            for name in to_remove:
                self.data["championships"].pop(name, None)
                self.data["scores"].pop(name, None)
            refresh_players()
            self.save_data()
            if hasattr(self, "player_listbox"):
                self.player_listbox.delete(0, tk.END)
                for player in self.data["players"]:
                    self.player_listbox.insert(tk.END, player["name"])

        ttk.Button(btn_frame, text="Remove Selected Player(s)", command=remove_player_action, style="DialogRed.TButton").pack(side=tk.LEFT, padx=12, ipadx=10)
        ttk.Button(btn_frame, text="Add Player", command=add_player_action, style="DialogGreen.TButton").pack(side=tk.LEFT, padx=12, ipadx=10)

    def manage_seeds(self):
        seed_window = tk.Toplevel(self.root)
        seed_window.title("Manage Player Seeds")
        seed_window.geometry("480x440")
        seed_window.configure(bg="#eaf0fb")
        seed_window.resizable(False, False)

        card = tk.Frame(seed_window, bg="#f8f6ff", bd=3, relief="ridge")
        card.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.93, relheight=0.97)

        tk.Label(
            card, text="Players and Seeds", font=('Arial', 16, 'bold'),
            bg="#f8f6ff", fg="#5433a3"
        ).pack(pady=(18, 8))

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

        style = ttk.Style()
        style.configure("SeedChange.TButton", font=('Arial', 11, 'bold'), padding=8)

        def change_seed():
            selection = listbox.curselection()
            if not selection:
                messagebox.showwarning("No Selection", "Please select a player to change seed.")
                return

            index = selection[0]
            player = self.data["players"][index]
            new_seed = self.ask_seed(seed_window, player["name"], player["seed"])
            if new_seed in (1, 2, 3):
                self.data["players"][index]["seed"] = new_seed
                self.save_data()
                refresh_list()

        button_frame = tk.Frame(card, bg="#f8f6ff")
        button_frame.pack(pady=(10, 10))
        ttk.Button(
            button_frame,
            text="Change Selected Player's Seed",
            command=change_seed,
            style="SeedChange.TButton"
        ).pack(ipadx=8)

        tk.Label(
            card, text="Tip: 1 = stronger, 2 = strong, 3 = beginner",
            font=('Arial', 9), bg="#f8f6ff", fg="#888"
        ).pack(side=tk.BOTTOM, pady=(4, 12))

    def ask_seed(self, parent, player_name, current_seed):
        dialog = tk.Toplevel(parent)
        dialog.title("Change Seed")
        dialog.geometry("340x310")
        dialog.configure(bg="#eaf0fb")
        dialog.grab_set()
        dialog.resizable(False, False)
        dialog.transient(parent)

        card = tk.Frame(dialog, bg="#f8f6ff", bd=3, relief="ridge")
        card.pack(expand=True, fill=tk.BOTH, padx=14, pady=14)

        tk.Label(
            card, text=f"Seed for {player_name}", font=('Arial', 14, 'bold'),
            bg="#f8f6ff", fg="#5433a3"
        ).pack(pady=(18, 7))

        var = tk.IntVar(value=current_seed)
        radio_frame = tk.Frame(card, bg="#f8f6ff")
        radio_frame.pack(pady=10)

        options = [
            {"text": "1 (Stronger)", "value": 1, "bg": "#e2f3fa", "fg": "#0c457d", "selectcolor": "#b0e3ff"},
            {"text": "2 (Strong)", "value": 2, "bg": "#fae2fa", "fg": "#7d0c69", "selectcolor": "#edc6f8"},
            {"text": "3 (Beginner)", "value": 3, "bg": "#fef4e3", "fg": "#b86b00", "selectcolor": "#ffe5b0"},
        ]
        for opt in options:
            tk.Radiobutton(
                radio_frame, text=opt["text"], variable=var, value=opt["value"],
                font=('Arial', 12, 'bold'), bg=opt["bg"], fg=opt["fg"],
                selectcolor=opt["selectcolor"], indicatoron=0, width=16, pady=7, bd=2, relief="groove", anchor="w"
            ).pack(pady=6)

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

    # ---- START TOURNAMENT MODIFIED ----
    def start_tournament(self):
        selected = self.player_listbox.curselection()
        if not selected:
            messagebox.showerror("Error", "Please select at least one player!")
            return

        selected_names = [self.player_listbox.get(i) for i in selected]
        self.current_players = [p for p in self.data["players"] if p["name"] in selected_names]

        # Ask for team creation method
        team_mode = self.ask_team_mode()
        if team_mode is None:
            return  # Cancelled

        if team_mode == "seed":
            self.create_teams(use_seed=True)
            self.create_matches()
            self.show_match()
        elif team_mode == "random":
            self.create_teams(use_seed=False)
            self.create_matches()
            self.show_match()
        elif team_mode == "custom":
            if not self.custom_team_builder():
                return  # cancelled
            self.create_matches()
            self.show_match()

    # ---- TEAM MODE CHOICE DIALOG ----
    def ask_team_mode(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Team Formation Mode")
        dialog.geometry("500x500")
        dialog.configure(bg="#eaf0fb")
        dialog.grab_set()
        dialog.transient(self.root)
        dialog.resizable(False, False)

        card = tk.Frame(dialog, bg="#f8f6ff", bd=3, relief="ridge")
        card.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

        tk.Label(card, text="How would you like to form teams?", font=('Arial', 14, 'bold'), bg="#f8f6ff", fg="#5433a3").pack(pady=(12, 14))

        choice = tk.StringVar(value="random")

        opt1 = ttk.Radiobutton(card, text="Random Teams", variable=choice, value="random", style="Start.TButton")
        opt1.pack(anchor="w", padx=22, pady=8)
        opt2 = ttk.Radiobutton(card, text="Seeded Teams", variable=choice, value="seed", style="Seed.TButton")
        opt2.pack(anchor="w", padx=22, pady=8)
        opt3 = ttk.Radiobutton(card, text="Custom Teams (Manual Selection)", variable=choice, value="custom", style="Champions.TButton")
        opt3.pack(anchor="w", padx=22, pady=8)

        btn_frame = tk.Frame(card, bg="#f8f6ff")
        btn_frame.pack(pady=18)

        result = {"mode": None}

        def done():
            result["mode"] = choice.get()
            dialog.destroy()
        def cancel():
            dialog.destroy()

        ttk.Button(btn_frame, text="Cancel", command=cancel, style="Draw.TButton").pack(side=tk.LEFT, padx=18, ipadx=12)
        ttk.Button(btn_frame, text="Continue", command=done, style="Start.TButton").pack(side=tk.LEFT, padx=18, ipadx=12)

        dialog.wait_window()
        return result["mode"]

    # ---- CUSTOM TEAM BUILDER ----
    def custom_team_builder(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Create Custom Teams")
        dialog.geometry("700x600")
        dialog.configure(bg="#eaf0fb")
        dialog.grab_set()
        dialog.transient(self.root)
        dialog.resizable(False, False)

        card = tk.Frame(dialog, bg="#f8f6ff", bd=3, relief="ridge")
        card.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

        tk.Label(card, text="Build Teams (2 Players per Team)", font=('Arial', 15, 'bold'), bg="#f8f6ff", fg="#5433a3").pack(pady=(10, 8))

        remaining_players = [p["name"] for p in self.current_players]
        teams = []

        frame = tk.Frame(card, bg="#f8f6ff")
        frame.pack(pady=10, fill=tk.BOTH, expand=True)

        left = tk.Frame(frame, bg="#f8f6ff")
        left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(14,7))
        right = tk.Frame(frame, bg="#f8f6ff")
        right.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(7,14))

        tk.Label(left, text="Available Players", font=('Arial', 12, 'bold'), bg="#f8f6ff", fg="#6a1b9a").pack(pady=(0,3))
        avail_lb = tk.Listbox(left, selectmode=tk.MULTIPLE, height=18, font=('Segoe UI', 12), bg="#f8f6ff", fg="#222", selectbackground="#b0e3ff")
        avail_lb.pack(fill=tk.BOTH, expand=True)
        for p in remaining_players:
            avail_lb.insert(tk.END, p)

        tk.Label(right, text="Teams", font=('Arial', 12, 'bold'), bg="#f8f6ff", fg="#6a1b9a").pack(pady=(0,3))
        teams_lb = tk.Listbox(right, height=18, font=('Segoe UI', 12), bg="#f8f6ff", fg="#222", selectbackground="#b0e3ff")
        teams_lb.pack(fill=tk.BOTH, expand=True)

        def refresh():
            avail_lb.delete(0, tk.END)
            for p in remaining_players:
                avail_lb.insert(tk.END, p)
            teams_lb.delete(0, tk.END)
            for t in teams:
                teams_lb.insert(tk.END, " & ".join(t))

        def add_team():
            sel = avail_lb.curselection()
            if len(sel) != 2:
                messagebox.showwarning("Need 2 Players", "Select exactly 2 players for a team.", parent=dialog)
                return
            team = [avail_lb.get(i) for i in sel]
            for p in team:
                remaining_players.remove(p)
            teams.append(tuple(team))
            refresh()

        def remove_team():
            sel = teams_lb.curselection()
            if not sel:
                return
            t = teams[sel[0]]
            for p in t:
                remaining_players.append(p)
            teams.pop(sel[0])
            refresh()

        action_frame = tk.Frame(card, bg="#f8f6ff")
        action_frame.pack(pady=(8, 5))
        ttk.Button(action_frame, text="Add Team", command=add_team, style="Start.TButton").pack(side=tk.LEFT, padx=12, ipadx=10)
        ttk.Button(action_frame, text="Remove Team", command=remove_team, style="Draw.TButton").pack(side=tk.LEFT, padx=12, ipadx=10)

        result = {"ok": False}

        def done():
            if len(remaining_players) == 1:
                teams.append((remaining_players[0],))
            elif remaining_players:
                messagebox.showwarning("Incomplete Teams", "All players must be assigned to a team (or one solo).", parent=dialog)
                return
            if len(teams) < 2:
                messagebox.showwarning("Not Enough Teams", "You must create at least 2 teams.", parent=dialog)
                return
            self.teams = teams.copy()
            self.team_stats = {i: {'points': 0, 'gf': 0, 'ga': 0} for i in range(len(self.teams))}
            result["ok"] = True
            dialog.destroy()

        def cancel():
            dialog.destroy()

        btn_frame = tk.Frame(card, bg="#f8f6ff")
        btn_frame.pack(pady=(12, 7))
        ttk.Button(btn_frame, text="Cancel", command=cancel, style="Draw.TButton").pack(side=tk.LEFT, padx=18, ipadx=12)
        ttk.Button(btn_frame, text="Done", command=done, style="Start.TButton").pack(side=tk.LEFT, padx=18, ipadx=12)

        dialog.wait_window()
        return result["ok"]

    def create_teams(self, use_seed=False):
        self.teams = []
        if use_seed:
            seed1 = [p["name"] for p in self.current_players if p["seed"] == 1]
            seed2 = [p["name"] for p in self.current_players if p["seed"] == 2]
            seed3 = [p["name"] for p in self.current_players if p["seed"] == 3]
            random.shuffle(seed1)
            random.shuffle(seed2)
            random.shuffle(seed3)
            min13 = min(len(seed1), len(seed3))
            for i in range(min13):
                self.teams.append((seed1[i], seed3[i]))
            leftover_1 = seed1[min13:]
            leftover_3 = seed3[min13:]
            pairs_2 = len(seed2) // 2
            for i in range(pairs_2):
                self.teams.append((seed2[2*i], seed2[2*i+1]))
            leftover_2 = seed2[2*pairs_2:]
            leftovers = list(leftover_1) + list(leftover_2) + list(leftover_3)
            random.shuffle(leftovers)
            i = 0
            while i < len(leftovers) - 1:
                self.teams.append((leftovers[i], leftovers[i+1]))
                i += 2
            if i < len(leftovers):
                self.teams.append((leftovers[i],))
        else:
            players = [p["name"] for p in self.current_players]
            random.shuffle(players)
            i = 0
            while i < len(players) - 1:
                self.teams.append((players[i], players[i+1]))
                i += 2
            if i < len(players):
                self.teams.append((players[i],))

        # NEW: team stats structure
        self.team_stats = {i: {'points': 0, 'gf': 0, 'ga': 0} for i in range(len(self.teams))}

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

        self.root.configure(bg="#eaf0fb")
        match_frame = tk.Frame(self.root, bg="#eaf0fb")
        match_frame.pack(expand=True, fill='both')

        # --- Main Card ---
        card = tk.Frame(match_frame, bg="#f8f6ff", bd=5, relief="ridge", highlightbackground="#bca8f7", highlightthickness=2)
        card.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.88, relheight=0.82)

        # --- Match Number Badge ---
        badge = tk.Label(
            card,
            text=f"Match {match_num}/{total_matches}",
            font=('Arial', 12, 'bold'),
            bg="#6d47c3", fg="white",
            bd=0, padx=16, pady=4
        )
        badge.place(relx=0.5, y=19, anchor="n")

        # --- Teams Display ---
        vs_frame = tk.Frame(card, bg="#f8f6ff")
        vs_frame.place(relx=0.5, rely=0.20, anchor="n")

        def format_team(team):
            return " & ".join(team)

        team1_label = tk.Label(
            vs_frame, text=format_team(team1),
            font=('Arial', 14, 'bold'),
            bg="#e5eaff", fg="#5433a3",
            padx=22, pady=10, bd=2, relief="groove", width=15
        )
        team1_label.pack(side=tk.LEFT, padx=(0, 18))

        vs_label = tk.Label(
            vs_frame, text="VS",
            font=('Arial Black', 22, 'bold'),
            bg="#f8f6ff", fg="#9265df", padx=16
        )
        vs_label.pack(side=tk.LEFT)

        team2_label = tk.Label(
            vs_frame, text=format_team(team2),
            font=('Arial', 14, 'bold'),
            bg="#f5e6ff", fg="#5433a3",
            padx=22, pady=10, bd=2, relief="groove", width=15
        )
        team2_label.pack(side=tk.LEFT, padx=(18, 0))

        # --- Score Entry Section ---
        score_frame = tk.Frame(card, bg="#f8f6ff")
        score_frame.place(relx=0.5, rely=0.50, anchor="center")

        # Beautiful Score Inputs (with + and - buttons)
        def make_score_box(label_text, color_bg, color_fg, var):
            box = tk.Frame(score_frame, bg="#f8f6ff")
            tk.Label(box, text=label_text, font=('Arial', 13, 'bold'), bg="#f8f6ff", fg="#757575").pack()
            inner = tk.Frame(box, bg="#f8f6ff")
            inner.pack()
            def dec():
                var.set(max(0, var.get() - 1))
            def inc():
                var.set(var.get() + 1)
            dec_btn = tk.Button(inner, text="−", font=("Arial", 14, "bold"), width=2, command=dec, bg="#eee", fg="#444", bd=0, relief="flat")
            dec_btn.pack(side=tk.LEFT, padx=(0,3))
            entry = tk.Entry(inner, textvariable=var, font=('Arial', 19, 'bold'), width=3, justify="center", bg=color_bg, fg=color_fg, bd=2, relief="groove")
            entry.pack(side=tk.LEFT)
            inc_btn = tk.Button(inner, text="+", font=("Arial", 14, "bold"), width=2, command=inc, bg="#eee", fg="#444", bd=0, relief="flat")
            inc_btn.pack(side=tk.LEFT, padx=(3,0))
            return box

        g1_var = tk.IntVar(value=0)
        g2_var = tk.IntVar(value=0)
        team1_box = make_score_box("Goals Team 1", "#d7eaff", "#1a237e", g1_var)
        team2_box = make_score_box("Goals Team 2", "#f3e2fa", "#6a1b9a", g2_var)
        team1_box.pack(side=tk.LEFT, padx=(0, 35))
        team2_box.pack(side=tk.LEFT, padx=(35, 0))

        # --- Action Buttons ---
        def submit_result():
            try:
                g1 = int(g1_var.get())
                g2 = int(g2_var.get())
                if g1 < 0 or g2 < 0:
                    messagebox.showwarning("Error", "Goals cannot be negative.", parent=self.root)
                    return
            except:
                messagebox.showwarning("Error", "Enter a valid integer for goals.", parent=self.root)
                return
            self.record_goal_result(t1, t2, g1, g2)

        btns_frame = tk.Frame(card, bg="#f8f6ff")
        btns_frame.place(relx=0.5, rely=0.72, anchor="center")
        style = ttk.Style()
        # Ensure button styles are set ONCE per season to avoid warning
        if not hasattr(self, '_btn_styles_set'):
            style.configure("Result.TButton", font=('Arial', 13, 'bold'), background="#4CAF50", foreground="white", padding=8)
            style.map("Result.TButton", background=[('active', '#388e3c')])
            style.configure("Postpone.TButton", font=('Arial', 13, 'bold'), background="#F57C00", foreground="white", padding=8)
            style.map("Postpone.TButton", background=[('active', '#bb4d00')])
            self._btn_styles_set = True

        ttk.Button(btns_frame, text="✔ Submit Result", command=submit_result, style="Result.TButton").pack(side=tk.LEFT, padx=28, ipadx=12, ipady=7)
        ttk.Button(btns_frame, text="⏸ Postpone", command=self.postpone_match, style="Postpone.TButton").pack(side=tk.LEFT, padx=28, ipadx=12, ipady=7)

        # --- View Scores Button ---
        ttk.Button(card, text="View Scores", command=self.show_scores, style="Scores.TButton").place(relx=0.5, rely=0.89, anchor="center")

        # --- Footer Hint ---
        tk.Label(
            card,
            text="Tip: Use + / − or type to adjust goals, then press ✔",
            font=('Arial', 10, 'italic'),
            bg="#f8f6ff", fg="#999"
        ).place(relx=0.5, rely=0.97, anchor="center")
    
    def record_goal_result(self, t1, t2, g1, g2):
        # Update goals for and against
        self.team_stats[t1]['gf'] += g1
        self.team_stats[t1]['ga'] += g2
        self.team_stats[t2]['gf'] += g2
        self.team_stats[t2]['ga'] += g1

        # Update points
        if g1 > g2:
            self.team_stats[t1]['points'] += 3
            # Add goal difference to winning team's players
            goal_diff = g1 - g2
            for player in self.teams[t1]:
                self.data["scores"][player] += goal_diff
        elif g2 > g1:
            self.team_stats[t2]['points'] += 3
            # Add goal difference to winning team's players
            goal_diff = g2 - g1
            for player in self.teams[t2]:
                self.data["scores"][player] += goal_diff
        else:
            self.team_stats[t1]['points'] += 1
            self.team_stats[t2]['points'] += 1

        self.save_data()
        self.current_match_index += 1
        self.show_match()

    def postpone_match(self):
        self.postponed.append(self.matches[self.current_match_index])
        self.current_match_index += 1
        self.show_match()

    def show_scores(self):
        score_window = tk.Toplevel(self.root)
        score_window.title("Current Scores")
        score_window.geometry("780x500")
        score_window.configure(bg="#ede7f6")

        card = tk.Frame(score_window, bg="#f8f6ff", bd=3, relief="ridge")
        card.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.93, relheight=0.93)

        header = tk.Label(
            card,
            text="Team Scores",
            font=('Arial', 19, 'bold'),
            bg="#9265df",
            fg="white",
            pady=18,
            bd=2,
            relief="groove"
        )
        header.pack(fill=tk.X, padx=0, pady=(0, 10))

        font_row = ('DejaVu Sans Mono', 13, 'bold')
        font_header = ('DejaVu Sans Mono', 12, 'bold')

        table_frame = tk.Frame(card, bg="#f8f6ff")
        table_frame.pack(fill=tk.BOTH, expand=True, padx=12, pady=(0, 12))
        header_row = tk.Frame(table_frame, bg="#ede7f6")
        header_row.pack(fill=tk.X)

        # The widths here are tuned for the formatting below!
        tk.Label(header_row, text="Rk",   font=font_header, bg="#ede7f6", fg="#6a1b9a", width=4, anchor="e").pack(side=tk.LEFT)
        tk.Label(header_row, text="Team", font=font_header, bg="#ede7f6", fg="#6a1b9a", width=31, anchor="w").pack(side=tk.LEFT)
        tk.Label(header_row, text="Pts",  font=font_header, bg="#ede7f6", fg="#6a1b9a", width=6, anchor="e").pack(side=tk.LEFT)
        tk.Label(header_row, text="GF",   font=font_header, bg="#ede7f6", fg="#6a1b9a", width=6, anchor="e").pack(side=tk.LEFT)
        tk.Label(header_row, text="GA",   font=font_header, bg="#ede7f6", fg="#6a1b9a", width=6, anchor="e").pack(side=tk.LEFT)
        tk.Label(header_row, text="GD",   font=font_header, bg="#ede7f6", fg="#6a1b9a", width=6, anchor="e").pack(side=tk.LEFT)

        lb_frame = tk.Frame(table_frame, bg="#f8f6ff")
        lb_frame.pack(fill=tk.BOTH, expand=True, pady=(0,8))

        listbox = tk.Listbox(
            lb_frame,
            font=font_row,
            bg="#f8f6ff",
            fg="#111",
            width=80,
            height=14,
            bd=0,
            selectbackground="#d1c4e9",
            activestyle='none',
            highlightthickness=0,
        )
        listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        team_scores = []
        for idx, stats in self.team_stats.items():
            team = " & ".join(self.teams[idx])
            points = stats['points']
            gf = stats['gf']
            ga = stats['ga']
            gd = gf - ga
            team_scores.append((team, points, gf, ga, gd))

        sorted_teams = sorted(team_scores, key=lambda x: (-x[1], -x[4], x[0]))

        row_colors = [
            ("#ffe082", "#111"),
            ("#e0e0e0", "#111"),
            ("#ffccbc", "#111")
        ]

        for idx, (team, points, gf, ga, gd) in enumerate(sorted_teams, start=1):
            line = f"{idx:>3}  {team:<31}  {points:>4}   {gf:>4}   {ga:>4}   {gd:>4}"
            listbox.insert(tk.END, line)
            if idx <= 3:
                bg, fg = row_colors[idx-1]
                listbox.itemconfig(tk.END, bg=bg, fg=fg)

        tk.Label(
            card,
            font=('Arial', 9),
            bg="#f8f6ff",
            fg="#7b58d3"
        ).pack(pady=(0, 9))

        ttk.Button(
            card,
            text="Close",
            command=score_window.destroy,
            style="Draw.TButton"
        ).pack(pady=(0, 8))

    def finalize_tournament(self):
        if self.postponed:
            self.matches = self.postponed
            self.postponed = []
            self.current_match_index = 0
            self.show_match()
            return

        max_point = max(stat['points'] for stat in self.team_stats.values())
        winners = [i for i, stat in self.team_stats.items() if stat['points'] == max_point]

        if len(winners) == 1:
            self.declare_champion(winners[0])
        elif len(winners) == 2:
            self.handle_tie(winners)
        else:
            # Check for best goal difference
            teams_gd = [(i, self.team_stats[i]['gf'] - self.team_stats[i]['ga']) for i in winners]
            max_gd = max(gd for _, gd in teams_gd)
            best = [i for i, gd in teams_gd if gd == max_gd]
            if len(best) == 1:
                self.declare_champion(best[0])
            else:
                messagebox.showinfo("No Champion", "Same Teams With Same Point Ans Same Goals!")
                self.create_main_frame()

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

        # Main background frame
        tie_frame = tk.Frame(self.root, bg="#eaf0fb")
        tie_frame.pack(expand=True, fill='both', padx=24, pady=24)

        # Card-like frame
        card = tk.Frame(tie_frame, bg="#f8f6ff", bd=5, relief="ridge", highlightbackground="#bca8f7", highlightthickness=2)
        card.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.88, relheight=0.82)

        # Badge for Tiebreaker
        badge = tk.Label(
            card,
            text="⚡ Final Tiebreaker!",
            font=('Arial', 13, 'bold'),
            bg="#e04e6a", fg="white",
            bd=0, padx=18, pady=5
        )
        badge.place(relx=0.5, y=19, anchor="n")

        # VS Teams Display
        vs_frame = tk.Frame(card, bg="#f8f6ff")
        vs_frame.place(relx=0.5, rely=0.20, anchor="n")

        team1 = self.teams[t1]
        team2 = self.teams[t2]

        def format_team(team):
            return " & ".join(team)

        team1_label = tk.Label(
            vs_frame, text=format_team(team1),
            font=('Arial', 19, 'bold'),
            bg="#e5eaff", fg="#5433a3",
            padx=22, pady=10, bd=2, relief="groove", width=15
        )
        team1_label.pack(side=tk.LEFT, padx=(0, 18))

        vs_label = tk.Label(
            vs_frame, text="VS",
            font=('Arial Black', 22, 'bold'),
            bg="#f8f6ff", fg="#e04e6a", padx=16
        )
        vs_label.pack(side=tk.LEFT)

        team2_label = tk.Label(
            vs_frame, text=format_team(team2),
            font=('Arial', 19, 'bold'),
            bg="#f5e6ff", fg="#5433a3",
            padx=22, pady=10, bd=2, relief="groove", width=15
        )
        team2_label.pack(side=tk.LEFT, padx=(18, 0))

        # Beautiful Score Entry
        score_frame = tk.Frame(card, bg="#f8f6ff")
        score_frame.place(relx=0.5, rely=0.50, anchor="center")

        def make_score_box(label_text, color_bg, color_fg, var):
            box = tk.Frame(score_frame, bg="#f8f6ff")
            tk.Label(box, text=label_text, font=('Arial', 13, 'bold'), bg="#f8f6ff", fg="#757575").pack()
            inner = tk.Frame(box, bg="#f8f6ff")
            inner.pack()
            def dec():
                var.set(max(0, var.get() - 1))
            def inc():
                var.set(var.get() + 1)
            dec_btn = tk.Button(inner, text="−", font=("Arial", 14, "bold"), width=2, command=dec, bg="#eee", fg="#444", bd=0, relief="flat")
            dec_btn.pack(side=tk.LEFT, padx=(0,3))
            entry = tk.Entry(inner, textvariable=var, font=('Arial', 19, 'bold'), width=3, justify="center", bg=color_bg, fg=color_fg, bd=2, relief="groove")
            entry.pack(side=tk.LEFT)
            inc_btn = tk.Button(inner, text="+", font=("Arial", 14, "bold"), width=2, command=inc, bg="#eee", fg="#444", bd=0, relief="flat")
            inc_btn.pack(side=tk.LEFT, padx=(3,0))
            return box

        t1_goal = tk.IntVar(value=0)
        t2_goal = tk.IntVar(value=0)
        team1_box = make_score_box("Goals Team 1", "#d7eaff", "#1a237e", t1_goal)
        team2_box = make_score_box("Goals Team 2", "#f3e2fa", "#6a1b9a", t2_goal)
        team1_box.pack(side=tk.LEFT, padx=(0, 35))
        team2_box.pack(side=tk.LEFT, padx=(35, 0))

        # Action Button
        def submit_tiebreaker():
            try:
                g1 = int(t1_goal.get())
                g2 = int(t2_goal.get())
                if g1 < 0 or g2 < 0:
                    messagebox.showwarning("Error", "Wrong number!", parent=self.root)
                    return
            except:
                messagebox.showwarning("Error", "Wrong number!", parent=self.root)
                return
            if g1 == g2:
                messagebox.showwarning("Draw", "Finals must have a winner!", parent=self.root)
                return
            winner = t1 if g1 > g2 else t2
            # Add goal difference to winning team's players
            goal_diff = abs(g1 - g2)
            for player in self.teams[winner]:
                self.data["scores"][player] += goal_diff
            self.save_data()
            self.declare_champion(winner)

        btns_frame = tk.Frame(card, bg="#f8f6ff")
        btns_frame.place(relx=0.5, rely=0.72, anchor="center")
        style = ttk.Style()
        if not hasattr(self, '_tiebreak_btn_styles_set'):
            style.configure("Result.TButton", font=('Arial', 13, 'bold'), background="#4CAF50", foreground="white", padding=8)
            style.map("Result.TButton", background=[('active', '#388e3c')])
            self._tiebreak_btn_styles_set = True

        ttk.Button(btns_frame, text="🏆 Declare Winner", command=submit_tiebreaker, style="Result.TButton").pack(ipadx=18, ipady=7)

        tk.Label(
            card,
            text="Tip: Use + / − or type to adjust goals. Draws are not allowed in the final.",
            font=('Arial', 10, 'italic'),
            bg="#f8f6ff", fg="#e04e6a"
        ).place(relx=0.5, rely=0.97, anchor="center")

    def show_champions(self):
        champ_window = tk.Toplevel(self.root)
        champ_window.title("Championship Records")
        champ_window.geometry("420x480")
        champ_window.configure(bg="#ede7f6")

        card = tk.Frame(champ_window, bg="#f8f6ff", bd=3, relief="ridge")
        card.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.93, relheight=0.93)

        header = tk.Label(
            card,
            text="Championship Leaderboard",
            font=('Arial', 19, 'bold'),
            bg="#9265df",
            fg="white",
            pady=18,
            bd=2,
            relief="groove"
        )
        header.pack(fill=tk.X, padx=0, pady=(0, 10))

        table_frame = tk.Frame(card, bg="#f8f6ff")
        table_frame.pack(fill=tk.BOTH, expand=True, padx=12, pady=(0, 12))
        header_row = tk.Frame(table_frame, bg="#ede7f6")
        header_row.pack(fill=tk.X)
        tk.Label(header_row, text="Rank", font=('DejaVu Sans Mono', 12, 'bold'), bg="#ede7f6", fg="#6a1b9a", width=6, anchor="w").pack(side=tk.LEFT, padx=(2,0))
        tk.Label(header_row, text="Player", font=('Arial', 12, 'bold'), bg="#ede7f6", fg="#6a1b9a", width=16, anchor="w").pack(side=tk.LEFT, padx=(10,0))
        tk.Label(header_row, text="Scores", font=('Arial', 12, 'bold'), bg="#ede7f6", fg="#6a1b9a", width=8, anchor="e").pack(side=tk.LEFT, padx=(8,0))
        tk.Label(header_row, text="Wins", font=('Arial', 12, 'bold'), bg="#ede7f6", fg="#6a1b9a", width=7, anchor="e").pack(side=tk.LEFT, padx=(8,0))

        lb_frame = tk.Frame(table_frame, bg="#f8f6ff")
        lb_frame.pack(fill=tk.BOTH, expand=True, pady=(0,8))

        listbox = tk.Listbox(
            lb_frame,
            font=('DejaVu Sans Mono', 13, 'bold'),
            bg="#f8f6ff",
            fg="#111",
            width=50,
            height=13,
            bd=0,
            selectbackground="#d1c4e9",
            activestyle='none',
            highlightthickness=0,
        )

        listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        row_colors = [
            ("#ffe082", "#111"),
            ("#e0e0e0", "#111"),
            ("#ffccbc", "#111")
        ]

        sorted_champs = sorted(
            [(player, self.data["scores"].get(player, 0), wins) for player, wins in self.data["championships"].items()],
            key=lambda x: (-x[1], -x[2], x[0])
        )
        for idx, (player, score, wins) in enumerate(sorted_champs, start=1):
            line = f"{str(idx):>2}   {player:<15} {str(score).rjust(6)} {str(wins).rjust(6)}"
            listbox.insert(tk.END, line)
            if idx <= 3:
                bg, fg = row_colors[idx-1]
                listbox.itemconfig(tk.END, bg=bg, fg=fg)

        tk.Label(
            card,
            font=('Arial', 9),
            bg="#f8f6ff",
            fg="#7b58d3"
        ).pack(pady=(0, 9))

        ttk.Button(
            card,
            text="Close",
            command=champ_window.destroy,
            style="Draw.TButton"
        ).pack(pady=(0, 8))

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = TournamentApp(root)
    root.mainloop()