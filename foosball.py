import os
import json
import random
from itertools import combinations

# File path for storing player data permanently
DATA_FILE = "players.json"

def load_players():
    """
    Load player data (names and championship records) from the persistent file.
    If the file doesn't exist, prompt for an initial list of player names and create the file.
    """
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        data = {"names": [], "championships": {}}
        print("Player data file not found. Please enter the names of players (one per line, leave empty to finish):")
        while True:
            name = input("Player name: ").strip()
            if name == "":
                break
            data["names"].append(name)
            data["championships"][name] = 0
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    return data

def save_players(data):
    """
    Save player data to the persistent file.
    """
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def select_today_players(all_names):
    """
    For each player in the persistent list, ask if they are present today.
    Returns a list of names for players playing today.
    """
    today_names = []
    print("\nFor each player below, indicate if they are playing today.")
    for name in all_names:
        response = input(f"Is '{name}' playing today? (y/n): ").strip().lower()
        if response.startswith('y'):
            today_names.append(name)
    return today_names

def create_teams(names):
    """
    Shuffle the names randomly and create teams.
    Teams are pairs if possible; if one player remains, they form a one-player team.
    """
    random.shuffle(names)
    teams = []
    i = 0
    while i < len(names):
        if i + 1 < len(names):
            team = (names[i], names[i+1])
            i += 2
        else:
            team = (names[i],)
            i += 1
        teams.append(team)
    return teams

def schedule_matches(teams):
    """
    Create a round-robin schedule where each team plays against every other team once,
    then randomly shuffle the match order.
    Returns a list of match tuples (indices of team 1 and team 2).
    """
    matches = list(combinations(range(len(teams)), 2))
    random.shuffle(matches)
    return matches

def input_match_result(team1, team2):
    """
    Prompt the user to enter the result of the match between two teams.
    1: Team 1 wins (3 - 0)
    2: Team 2 wins (0 - 3)
    d: Draw (1 - 1)
    """
    team1_display = " & ".join(team1)
    team2_display = " & ".join(team2)
    print(f"\nMatch: {team1_display} vs. {team2_display}")
    print("Enter the match result:")
    print("1: Team 1 wins (3 - 0)")
    print("2: Team 2 wins (0 - 3)")
    print("d: Draw (1 - 1)")
    while True:
        result = input("Result (1/2/d): ").strip().lower()
        if result in ["1", "2", "d"]:
            return result
        else:
            print("Invalid input. Please try again.")

def main():
    # Load persistent player data
    data = load_players()
    
    # Ask which players are playing today (from the persistent names)
    if data["names"]:
        today_names = select_today_players(data["names"])
    else:
        today_names = []
    
    # If none of the persistent players are available, prompt for names
    if not today_names:
        print("No persistent players selected. Please enter today's players (one per line, leave empty to finish):")
        while True:
            name = input("Player name: ").strip()
            if name == "":
                break
            today_names.append(name)
            # Also add new players to persistent data
            if name not in data["names"]:
                data["names"].append(name)
                data["championships"][name] = 0

    if not today_names:
        print("No players entered for today.")
        return

    # Form teams with today's players
    teams = create_teams(today_names)
    print("\nTeams created:")
    for idx, team in enumerate(teams):
        print(f"Team {idx+1}: {' & '.join(team)}")

    # Create random round-robin schedule for matches
    matches = schedule_matches(teams)
    team_scores = {i: 0 for i in range(len(teams))}
    
    print("\nScheduled matches:")
    for match in matches:
        t1, t2 = match
        print(f"Match between Team {t1+1} and Team {t2+1}")

    # Process each match and update scores, displaying score after each match
    for match in matches:
        t1, t2 = match
        result = input_match_result(teams[t1], teams[t2])
        if result == "1":
            team_scores[t1] += 3
        elif result == "2":
            team_scores[t2] += 3
        elif result == "d":
            team_scores[t1] += 1
            team_scores[t2] += 1

        # Display the current scoreboard after each match
        print("\nCurrent Scoreboard:")
        for i, score in team_scores.items():
            team_display = " & ".join(teams[i])
            print(f"Team {i+1} ({team_display}): {score} point(s)")

    # Final scoreboard display
    print("\nFinal scores:")
    for i, score in team_scores.items():
        team_display = " & ".join(teams[i])
        print(f"Team {i+1} ({team_display}): {score} point(s)")

    # Determine the winning team(s)
    max_score = max(team_scores.values())
    winners = [i for i, score in team_scores.items() if score == max_score]

    if len(winners) == 1:
        winning_team = teams[winners[0]]
        print(f"\nWinning Team: Team {winners[0]+1} ({' & '.join(winning_team)}) with {max_score} points")
        # Update championship counts for each player on the winning team
        for player in winning_team:
            data["championships"][player] += 1
    else:
        print("\nThere is a tie between the following teams:")
        for i in winners:
            team_display = " & ".join(teams[i])
            print(f"Team {i+1}: {team_display}")
        # In case of a tie, championship counts are not updated

    # Save updated player data
    save_players(data)

    print("\nChampionship count for players:")
    for name, count in data["championships"].items():
        print(f"{name}: {count} championship(s)")

if __name__ == "__main__":
    main()
