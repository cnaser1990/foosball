class TournamentApp {
    constructor() {
        this.currentPlayers = [];
        this.teams = [];
        this.matches = [];
        this.postponed = [];
        this.currentMatchIndex = 0;
        this.teamStats = {};
        this.isAdminLoggedIn = false;

        this.initializeApp();
    }

    async initializeApp() {
        this.data = await this.loadData();
        this.initializeEventListeners();
        this.refreshPlayerList();
    }

    // Data management
    async loadData() {
        try {
            const response = await fetch('/api/players');
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const data = await response.json();
            return data;
        } catch (error) {
            console.error('Error loading data from server:', error);
            // Return default data as fallback
            return {
                players: [
                    { name: "ghayem", seed: 1 },
                    { name: "elini", seed: 3 },
                    { name: "dinparvar", seed: 3 },
                    { name: "alivand", seed: 1 },
                    { name: "hoseinizade", seed: 3 },
                    { name: "hajali", seed: 3 },
                    { name: "dariushi", seed: 1 }
                ],
                championships: {
                    "ghayem": 6,
                    "elini": 2,
                    "dinparvar": 1,
                    "alivand": 1,
                    "hoseinizade": 3,
                    "hajali": 2,
                    "dariushi": 3
                },
                scores: {
                    "ghayem": 0,
                    "elini": 0,
                    "dinparvar": 0,
                    "alivand": 0,
                    "hoseinizade": 0,
                    "hajali": 0,
                    "dariushi": 0
                }
            };
        }
    }

    async saveData() {
        try {
            const response = await fetch('/api/players', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(this.data)
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const result = await response.json();
            if (!result.success) {
                throw new Error(result.message || 'Failed to save data');
            }
            
            console.log('Data saved successfully to players.json');
        } catch (error) {
            console.error('Error saving data to server:', error);
            this.showNotification('Failed to save data. Please try again.', 'error');
        }
    }

    // UI Management
    showScreen(screenId) {
        document.querySelectorAll('.screen').forEach(screen => {
            screen.classList.remove('active');
        });
        document.getElementById(screenId).classList.add('active');
    }

    showDialog(dialogId) {
        document.getElementById(dialogId).classList.add('active');
    }

    hideDialog(dialogId) {
        document.getElementById(dialogId).classList.remove('active');
    }

    hideAllDialogs() {
        document.querySelectorAll('.dialog').forEach(dialog => {
            dialog.classList.remove('active');
        });
    }

    // Notification system (optional enhancement)
    showNotification(message, type = 'info') {
        // You can implement a toast notification system here
        console.log(`[${type.toUpperCase()}] ${message}`);
    }

    // Event Listeners
    initializeEventListeners() {
        // Main screen buttons
        document.getElementById('manage-players-btn').addEventListener('click', () => this.showPlayerManagement());
        document.getElementById('start-tournament-btn').addEventListener('click', () => this.startTournament());
        document.getElementById('view-champions-btn').addEventListener('click', () => this.showChampions());
        document.getElementById('view-seasons-btn').addEventListener('click', () => this.showSeasons());
        document.getElementById('manage-seeds-btn').addEventListener('click', () => this.showSeedManagement());
        document.getElementById('finish-season-btn').addEventListener('click', () => this.showFinishSeasonDialog());

        // Player management dialog
        document.getElementById('add-player-btn').addEventListener('click', () => this.addPlayer());
        document.getElementById('remove-player-btn').addEventListener('click', () => this.removePlayer());
        document.getElementById('close-player-dialog-btn').addEventListener('click', () => this.hideDialog('player-management-dialog'));
        document.getElementById('new-player-name').addEventListener('keypress', (e) => {
            if (e.key === 'Enter') this.addPlayer();
        });

        // Seed management dialog
        document.getElementById('change-seed-btn').addEventListener('click', () => this.changeSeed());
        document.getElementById('close-seed-dialog-btn').addEventListener('click', () => this.hideDialog('seed-management-dialog'));

        // Team mode dialog
        document.getElementById('continue-team-mode-btn').addEventListener('click', () => this.continueWithTeamMode());
        document.getElementById('cancel-team-mode-btn').addEventListener('click', () => this.hideDialog('team-mode-dialog'));

        // Custom team dialog
        document.getElementById('add-team-btn').addEventListener('click', () => this.addCustomTeam());
        document.getElementById('remove-team-btn').addEventListener('click', () => this.removeCustomTeam());
        document.getElementById('done-custom-team-btn').addEventListener('click', () => this.finishCustomTeams());
        document.getElementById('cancel-custom-team-btn').addEventListener('click', () => this.hideDialog('custom-team-dialog'));

        // Match screen
        document.getElementById('team1-plus').addEventListener('click', () => this.adjustScore('team1-goals', 1));
        document.getElementById('team1-minus').addEventListener('click', () => this.adjustScore('team1-goals', -1));
        document.getElementById('team2-plus').addEventListener('click', () => this.adjustScore('team2-goals', 1));
        document.getElementById('team2-minus').addEventListener('click', () => this.adjustScore('team2-goals', -1));
        document.getElementById('submit-result-btn').addEventListener('click', () => this.submitResult());
        document.getElementById('postpone-match-btn').addEventListener('click', () => this.postponeMatch());
        document.getElementById('view-scores-btn').addEventListener('click', () => this.showScores());
        document.getElementById('back-to-menu-btn').addEventListener('click', () => this.showScreen('main-screen'));

        // Tiebreaker screen
        document.getElementById('tie-team1-plus').addEventListener('click', () => this.adjustScore('tie-team1-goals', 1));
        document.getElementById('tie-team1-minus').addEventListener('click', () => this.adjustScore('tie-team1-goals', -1));
        document.getElementById('tie-team2-plus').addEventListener('click', () => this.adjustScore('tie-team2-goals', 1));
        document.getElementById('tie-team2-minus').addEventListener('click', () => this.adjustScore('tie-team2-goals', -1));
        document.getElementById('declare-winner-btn').addEventListener('click', () => this.submitTiebreaker());

        // Dialog close buttons
        document.getElementById('close-scores-btn').addEventListener('click', () => this.hideDialog('scores-dialog'));
        document.getElementById('close-champions-btn').addEventListener('click', () => this.hideDialog('champions-dialog'));
        document.getElementById('close-seasons-btn').addEventListener('click', () => this.hideDialog('seasons-dialog'));
        document.getElementById('close-season-view-btn').addEventListener('click', () => this.hideDialog('season-view-dialog'));
        document.getElementById('view-season-btn').addEventListener('click', () => this.viewSeason());
        document.getElementById('ok-seed-change-btn').addEventListener('click', () => this.confirmSeedChange());
        document.getElementById('cancel-seed-change-btn').addEventListener('click', () => this.hideDialog('seed-change-dialog'));
        document.getElementById('confirm-finish-season-btn').addEventListener('click', () => this.finishSeason());
        document.getElementById('cancel-finish-season-btn').addEventListener('click', () => this.hideDialog('finish-season-dialog'));

        // Admin login and edit
        document.getElementById('admin-login-btn').addEventListener('click', () => this.showAdminLogin());
        document.getElementById('confirm-admin-login-btn').addEventListener('click', () => this.confirmAdminLogin());
        document.getElementById('cancel-admin-login-btn').addEventListener('click', () => this.hideDialog('admin-login-dialog'));
        document.getElementById('save-admin-edit-btn').addEventListener('click', () => this.saveAdminEdits());
        document.getElementById('cancel-admin-edit-btn').addEventListener('click', () => this.hideDialog('admin-edit-dialog'));

        // Admin password - Enter key
        document.getElementById('admin-password').addEventListener('keypress', (e) => {
            if (e.key === 'Enter') this.confirmAdminLogin();
        });

        // Season name - Enter key
        document.getElementById('season-name').addEventListener('keypress', (e) => {
            if (e.key === 'Enter') this.finishSeason();
        });

        // Close dialogs when clicking outside
        document.querySelectorAll('.dialog').forEach(dialog => {
            dialog.addEventListener('click', (e) => {
                if (e.target === dialog) {
                    dialog.classList.remove('active');
                }
            });
        });
    }

    // Player Management
    refreshPlayerList() {
        const listbox = document.getElementById('player-listbox');
        listbox.innerHTML = '';
        this.data.players.forEach(player => {
            const option = document.createElement('option');
            option.value = player.name;
            option.textContent = player.name;
            listbox.appendChild(option);
        });
    }

    showPlayerManagement() {
        this.refreshManagePlayerList();
        this.showDialog('player-management-dialog');
    }

    refreshManagePlayerList() {
        const listbox = document.getElementById('manage-player-listbox');
        listbox.innerHTML = '';
        this.data.players.forEach(player => {
            const option = document.createElement('option');
            option.value = player.name;
            const seedLabel = player.seed === 1 ? 'Pro' : player.seed === 2 ? 'Intermediate' : 'Beginner';
            option.textContent = `${player.name} (${seedLabel})`;
            listbox.appendChild(option);
        });
    }

    async addPlayer() {
        const nameInput = document.getElementById('new-player-name');
        const name = nameInput.value.trim();
        
        if (!name) {
            alert('Player name cannot be empty.');
            return;
        }

        if (this.data.players.some(p => p.name.toLowerCase() === name.toLowerCase())) {
            alert(`Player '${name}' already exists!`);
            return;
        }

        const seedValue = parseInt(document.querySelector('input[name="seed"]:checked').value);
        
        this.data.players.push({ name, seed: seedValue });
        this.data.championships[name] = 0;
        this.data.scores[name] = 0;

        await this.saveData();
        this.refreshPlayerList();
        this.refreshManagePlayerList();
        
        nameInput.value = '';
        document.getElementById('seed-1').checked = true;
        
        this.showNotification(`Player ${name} added successfully!`, 'success');
    }

    async removePlayer() {
        const listbox = document.getElementById('manage-player-listbox');
        const selected = Array.from(listbox.selectedOptions);
        
        if (selected.length === 0) {
            alert('Please select player(s) to remove.');
            return;
        }

        const playerNames = selected.map(option => option.value).join(', ');
        if (!confirm(`Are you sure you want to remove: ${playerNames}?`)) {
            return;
        }

        const toRemove = selected.map(option => option.value);
        this.data.players = this.data.players.filter(p => !toRemove.includes(p.name));
        
        toRemove.forEach(name => {
            delete this.data.championships[name];
            delete this.data.scores[name];
        });

        await this.saveData();
        this.refreshPlayerList();
        this.refreshManagePlayerList();
        
        this.showNotification(`${toRemove.length} player(s) removed successfully!`, 'success');
    }

    // Seed Management
    showSeedManagement() {
        this.refreshSeedPlayerList();
        this.showDialog('seed-management-dialog');
    }

    refreshSeedPlayerList() {
        const listbox = document.getElementById('seed-player-listbox');
        listbox.innerHTML = '';
        this.data.players.forEach(player => {
            const option = document.createElement('option');
            option.value = player.name;
            const seedLabel = player.seed === 1 ? 'Pro' : player.seed === 2 ? 'Intermediate' : 'Beginner';
            option.textContent = `${player.name} - ${seedLabel}`;
            listbox.appendChild(option);
        });
    }

    changeSeed() {
        const listbox = document.getElementById('seed-player-listbox');
        const selected = listbox.selectedOptions[0];
        
        if (!selected) {
            alert('Please select a player to change seed.');
            return;
        }

        const playerName = selected.value;
        const player = this.data.players.find(p => p.name === playerName);
        
        document.getElementById('seed-change-title').innerHTML = `<i class="fas fa-exchange-alt"></i> Change Seed for ${playerName}`;
        document.getElementById(`change-seed-${player.seed}`).checked = true;
        
        this.currentSeedChangePlayer = playerName;
        this.showDialog('seed-change-dialog');
    }

    async confirmSeedChange() {
        const newSeed = parseInt(document.querySelector('input[name="change-seed"]:checked').value);
        const player = this.data.players.find(p => p.name === this.currentSeedChangePlayer);
        
        if (player) {
            const oldSeed = player.seed;
            player.seed = newSeed;
            await this.saveData();
            this.refreshSeedPlayerList();
            
            const seedLabels = { 1: 'Pro', 2: 'Intermediate', 3: 'Beginner' };
            this.showNotification(
                `${player.name} changed from ${seedLabels[oldSeed]} to ${seedLabels[newSeed]}`, 
                'success'
            );
        }
        
        this.hideDialog('seed-change-dialog');
    }

    // Tournament Management
    startTournament() {
        const listbox = document.getElementById('player-listbox');
        const selected = Array.from(listbox.selectedOptions);
        
        if (selected.length === 0) {
            alert('Please select at least one player!');
            return;
        }

        if (selected.length < 2) {
            alert('Please select at least 2 players to start a tournament!');
            return;
        }

        const selectedNames = selected.map(option => option.value);
        this.currentPlayers = this.data.players.filter(p => selectedNames.includes(p.name));
        
        this.showDialog('team-mode-dialog');
    }

    async continueWithTeamMode() {
        const mode = document.querySelector('input[name="team-mode"]:checked').value;
        this.hideDialog('team-mode-dialog');
        
        if (mode === 'custom') {
            this.showCustomTeamBuilder();
        } else {
            this.createTeams(mode === 'seed');
            this.createMatches();
            await this.showMatch();
        }
    }

    // Team Creation
    createTeams(useSeeds = false) {
        this.teams = [];
        
        if (useSeeds) {
            const seed1 = this.currentPlayers.filter(p => p.seed === 1).map(p => p.name);
            const seed2 = this.currentPlayers.filter(p => p.seed === 2).map(p => p.name);
            const seed3 = this.currentPlayers.filter(p => p.seed === 3).map(p => p.name);
            
            this.shuffleArray(seed1);
            this.shuffleArray(seed2);
            this.shuffleArray(seed3);
            
            const min13 = Math.min(seed1.length, seed3.length);
            for (let i = 0; i < min13; i++) {
                this.teams.push([seed1[i], seed3[i]]);
            }
            
            const leftover1 = seed1.slice(min13);
            const leftover3 = seed3.slice(min13);
            const pairs2 = Math.floor(seed2.length / 2);
            
            for (let i = 0; i < pairs2; i++) {
                this.teams.push([seed2[2*i], seed2[2*i+1]]);
            }
            
            const leftover2 = seed2.slice(2*pairs2);
            const leftovers = [...leftover1, ...leftover2, ...leftover3];
            this.shuffleArray(leftovers);
            
            for (let i = 0; i < leftovers.length - 1; i += 2) {
                this.teams.push([leftovers[i], leftovers[i+1]]);
            }
            
            if (leftovers.length % 2 === 1) {
                this.teams.push([leftovers[leftovers.length - 1]]);
            }
        } else {
            const players = this.currentPlayers.map(p => p.name);
            this.shuffleArray(players);
            
            for (let i = 0; i < players.length - 1; i += 2) {
                this.teams.push([players[i], players[i+1]]);
            }
            
            if (players.length % 2 === 1) {
                this.teams.push([players[players.length - 1]]);
            }
        }
        
        this.teamStats = {};
        for (let i = 0; i < this.teams.length; i++) {
            this.teamStats[i] = { points: 0, gf: 0, ga: 0 };
        }
    }

    shuffleArray(array) {
        for (let i = array.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [array[i], array[j]] = [array[j], array[i]];
        }
    }

    // Custom Team Builder
    showCustomTeamBuilder() {
        this.availablePlayers = this.currentPlayers.map(p => p.name);
        this.customTeams = [];
        this.refreshCustomTeamBuilder();
        this.showDialog('custom-team-dialog');
    }

    refreshCustomTeamBuilder() {
        const availableListbox = document.getElementById('available-players-listbox');
        const teamsListbox = document.getElementById('teams-listbox');
        
        availableListbox.innerHTML = '';
        this.availablePlayers.forEach(player => {
            const option = document.createElement('option');
            option.value = player;
            option.textContent = player;
            availableListbox.appendChild(option);
        });
        
        teamsListbox.innerHTML = '';
        this.customTeams.forEach((team, index) => {
            const option = document.createElement('option');
            option.value = team.join(' & ');
            option.textContent = `Team ${index + 1}: ${team.join(' & ')}`;
            teamsListbox.appendChild(option);
        });
    }

    addCustomTeam() {
        const listbox = document.getElementById('available-players-listbox');
        const selected = Array.from(listbox.selectedOptions);
        
        if (selected.length !== 2) {
            alert('Select exactly 2 players for a team.');
            return;
        }
        
        const team = selected.map(option => option.value);
        team.forEach(player => {
            const index = this.availablePlayers.indexOf(player);
            if (index > -1) {
                this.availablePlayers.splice(index, 1);
            }
        });
        
        this.customTeams.push(team);
        this.refreshCustomTeamBuilder();
        
        this.showNotification(`Team created: ${team.join(' & ')}`, 'success');
    }

    removeCustomTeam() {
        const listbox = document.getElementById('teams-listbox');
        const selected = listbox.selectedOptions[0];
        
        if (!selected) {
            alert('Please select a team to remove.');
            return;
        }
        
        const teamIndex = listbox.selectedIndex;
        const team = this.customTeams[teamIndex];
        
        team.forEach(player => {
            this.availablePlayers.push(player);
        });
        
        this.customTeams.splice(teamIndex, 1);
        this.refreshCustomTeamBuilder();
        
        this.showNotification('Team removed successfully', 'info');
    }

    async finishCustomTeams() {
        if (this.availablePlayers.length === 1) {
            this.customTeams.push([this.availablePlayers[0]]);
            this.showNotification('Solo player added as team', 'info');
        } else if (this.availablePlayers.length > 1) {
            alert('All players must be assigned to a team (or one solo player remaining).');
            return;
        }
        
        if (this.customTeams.length < 2) {
            alert('You must create at least 2 teams.');
            return;
        }
        
        this.teams = this.customTeams.slice();
        this.teamStats = {};
        for (let i = 0; i < this.teams.length; i++) {
            this.teamStats[i] = { points: 0, gf: 0, ga: 0 };
        }
        
        this.hideDialog('custom-team-dialog');
        this.createMatches();
        await this.showMatch();
    }

    // Match Management
    createMatches() {
        this.matches = [];
        for (let i = 0; i < this.teams.length; i++) {
            for (let j = i + 1; j < this.teams.length; j++) {
                this.matches.push([i, j]);
            }
        }
        this.shuffleArray(this.matches);
        this.currentMatchIndex = 0;
        this.postponed = [];
    }

    async showMatch() {
        if (this.currentMatchIndex >= this.matches.length) {
            await this.finalizeTournament();
            return;
        }
        
        const [t1, t2] = this.matches[this.currentMatchIndex];
        const team1 = this.teams[t1];
        const team2 = this.teams[t2];
        
        document.getElementById('match-badge').textContent = 
            `Match ${this.currentMatchIndex + 1}/${this.matches.length}`;
        document.getElementById('team1-label').textContent = team1.join(' & ');
        document.getElementById('team2-label').textContent = team2.join(' & ');
        
        document.getElementById('team1-goals').value = 0;
        document.getElementById('team2-goals').value = 0;
        
        // Initialize score displays
        document.getElementById('team1-score-display').textContent = 0;
        document.getElementById('team2-score-display').textContent = 0;
        
        this.showScreen('match-screen');
    }

    adjustScore(inputId, delta) {
        const input = document.getElementById(inputId);
        const currentValue = parseInt(input.value) || 0;
        const newValue = Math.max(0, currentValue + delta);
        input.value = newValue;
        
        // Update the score display with animation
        const displayId = inputId.replace('-goals', '-score-display');
        const displayElement = document.getElementById(displayId);
        if (displayElement) {
            displayElement.textContent = newValue;
            displayElement.classList.add('score-change');
            setTimeout(() => {
                displayElement.classList.remove('score-change');
            }, 400);
        }
    }

    async submitResult() {
        const g1 = parseInt(document.getElementById('team1-goals').value) || 0;
        const g2 = parseInt(document.getElementById('team2-goals').value) || 0;
        
        if (g1 < 0 || g2 < 0) {
            alert('Goals cannot be negative.');
            return;
        }
        
        const [t1, t2] = this.matches[this.currentMatchIndex];
        await this.recordResult(t1, t2, g1, g2);
    }

    async recordResult(t1, t2, g1, g2) {
        // Update goals for and against
        this.teamStats[t1].gf += g1;
        this.teamStats[t1].ga += g2;
        this.teamStats[t2].gf += g2;
        this.teamStats[t2].ga += g1;
        
        // Update points
        if (g1 > g2) {
            this.teamStats[t1].points += 3;
            // Add goal difference to winning team's players
            const goalDiff = g1 - g2;
            this.teams[t1].forEach(player => {
                this.data.scores[player] = (this.data.scores[player] || 0) + goalDiff;
            });
        } else if (g2 > g1) {
            this.teamStats[t2].points += 3;
            // Add goal difference to winning team's players
            const goalDiff = g2 - g1;
            this.teams[t2].forEach(player => {
                this.data.scores[player] = (this.data.scores[player] || 0) + goalDiff;
            });
        } else {
            this.teamStats[t1].points += 1;
            this.teamStats[t2].points += 1;
        }
        
        this.currentMatchIndex++;
        await this.showMatch();
    }

    async postponeMatch() {
        this.postponed.push(this.matches[this.currentMatchIndex]);
        this.currentMatchIndex++;
        this.showNotification('Match postponed', 'info');
        await this.showMatch();
    }

    // Scores Display
    showScores() {
        const scoresList = document.getElementById('scores-list');
        scoresList.innerHTML = '';
        
        const teamScores = [];
        for (let idx in this.teamStats) {
            const team = this.teams[idx].join(' & ');
            const stats = this.teamStats[idx];
            const gd = stats.gf - stats.ga;
            teamScores.push({ team, points: stats.points, gf: stats.gf, ga: stats.ga, gd });
        }
        
        teamScores.sort((a, b) => {
            if (b.points !== a.points) return b.points - a.points;
            if (b.gd !== a.gd) return b.gd - a.gd;
            return a.team.localeCompare(b.team);
        });
        
        teamScores.forEach((teamScore, index) => {
            const row = document.createElement('div');
            row.className = 'table-row';
            row.innerHTML = `
                <div class="table-cell rank">${index + 1}</div>
                <div class="table-cell team">${teamScore.team}</div>
                <div class="table-cell stat">${teamScore.points}</div>
                <div class="table-cell stat">${teamScore.gf}</div>
                <div class="table-cell stat">${teamScore.ga}</div>
                <div class="table-cell stat">${teamScore.gd}</div>
            `;
            scoresList.appendChild(row);
        });
        
        this.showDialog('scores-dialog');
    }

    // Tournament Finalization
    async finalizeTournament() {
        if (this.postponed.length > 0) {
            this.matches = this.postponed;
            this.postponed = [];
            this.currentMatchIndex = 0;
            await this.showMatch();
            return;
        }
        
        const maxPoints = Math.max(...Object.values(this.teamStats).map(s => s.points));
        const winners = Object.keys(this.teamStats).filter(i => this.teamStats[i].points === maxPoints);
        
        if (winners.length === 1) {
            await this.declareChampion(parseInt(winners[0]));
        } else if (winners.length === 2) {
            this.handleTie(winners.map(w => parseInt(w)));
        } else {
            // Check goal difference
            const teamsGd = winners.map(i => ({
                index: parseInt(i),
                gd: this.teamStats[i].gf - this.teamStats[i].ga
            }));
            const maxGd = Math.max(...teamsGd.map(t => t.gd));
            const best = teamsGd.filter(t => t.gd === maxGd);
            
            if (best.length === 1) {
                await this.declareChampion(best[0].index);
            } else {
                alert('Multiple teams tied with same points and goal difference!');
                this.showScreen('main-screen');
            }
        }
    }

    handleTie(winners) {
        if (winners.length === 2) {
            this.showTiebreaker(winners[0], winners[1]);
        } else {
            alert('Multiple tie - No champion declared!');
            this.showScreen('main-screen');
        }
    }

    showTiebreaker(t1, t2) {
        const team1 = this.teams[t1];
        const team2 = this.teams[t2];
        
        document.getElementById('tie-team1-label').textContent = team1.join(' & ');
        document.getElementById('tie-team2-label').textContent = team2.join(' & ');
        
        document.getElementById('tie-team1-goals').value = 0;
        document.getElementById('tie-team2-goals').value = 0;
        
        // Initialize score displays
        document.getElementById('tie-team1-score-display').textContent = 0;
        document.getElementById('tie-team2-score-display').textContent = 0;
        
        this.tiebreakerTeams = [t1, t2];
        this.showScreen('tiebreaker-screen');
    }

    async submitTiebreaker() {
        const g1 = parseInt(document.getElementById('tie-team1-goals').value) || 0;
        const g2 = parseInt(document.getElementById('tie-team2-goals').value) || 0;
        
        if (g1 < 0 || g2 < 0) {
            alert('Goals cannot be negative!');
            return;
        }
        
        if (g1 === g2) {
            alert('Finals must have a winner! No draws allowed.');
            return;
        }
        
        const winner = g1 > g2 ? this.tiebreakerTeams[0] : this.tiebreakerTeams[1];
        // Add goal difference to winning team's players
        const goalDiff = Math.abs(g1 - g2);
        this.teams[winner].forEach(player => {
            this.data.scores[player] = (this.data.scores[player] || 0) + goalDiff;
        });
        await this.declareChampion(winner);
    }

    async declareChampion(winnerIndex) {
        const winner = this.teams[winnerIndex];
        winner.forEach(player => {
            this.data.championships[player] = (this.data.championships[player] || 0) + 1;
        });
        
        await this.saveData();
        
        // Show celebration alert
        const winnerNames = winner.join(' & ');
        alert(`🏆 CHAMPIONS: ${winnerNames}! 🏆`);
        
        this.showScreen('main-screen');
        this.showNotification(`${winnerNames} won the tournament!`, 'success');
    }

    // Champions Display
    showChampions() {
        const championsList = document.getElementById('champions-list');
        if (!championsList) {
            console.error('champions-list element not found');
            return;
        }

        championsList.innerHTML = '';

        const sortedChamps = Object.entries(this.data.championships)
            .map(([player, wins]) => [player, this.data.scores[player] || 0, wins])
            .sort(([nameA, scoreA, winsA], [nameB, scoreB, winsB]) => {
                if (winsB !== winsA) return winsB - winsA;
                if (scoreB !== scoreA) return scoreB - scoreA;
                return nameA.localeCompare(nameB);
            });

        sortedChamps.forEach(([player, score, wins], index) => {
            const row = document.createElement('div');
            row.className = 'table-row';
            row.innerHTML = `
                <div class="table-cell rank">${index + 1}</div>
                <div class="table-cell player">${player}</div>
                <div class="table-cell stat">${wins}</div>
                <div class="table-cell stat">${score}</div>
            `;
            championsList.appendChild(row);
        });

        this.showDialog('champions-dialog');
    }

    // Season History
    async showSeasons() {
        try {
            const response = await fetch('/api/seasons');
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const data = await response.json();
            const seasonsListbox = document.getElementById('seasons-listbox');
            seasonsListbox.innerHTML = '';
            
            if (data.seasons.length === 0) {
                const option = document.createElement('option');
                option.textContent = 'No archived seasons yet';
                option.disabled = true;
                seasonsListbox.appendChild(option);
            } else {
                data.seasons.forEach(season => {
                    const option = document.createElement('option');
                    option.value = season;
                    option.textContent = season.replace('_player_', '').replace('.json', '');
                    seasonsListbox.appendChild(option);
                });
            }
            this.showDialog('seasons-dialog');
        } catch (error) {
            console.error('Error loading seasons:', error);
            alert('Failed to load season history.');
        }
    }

    async viewSeason() {
        const seasonsListbox = document.getElementById('seasons-listbox');
        const selected = seasonsListbox.selectedOptions[0];

        if (!selected) {
            alert('Please select a season to view.');
            return;
        }

        const filename = selected.value;

        try {
            const response = await fetch(`/api/season/${filename}`);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const seasonData = await response.json();

            const championships = (seasonData && typeof seasonData.championships === 'object') ? seasonData.championships : {};
            const scores = (seasonData && typeof seasonData.scores === 'object') ? seasonData.scores : {};

            document.getElementById('season-view-title').innerHTML = 
                `<i class="fas fa-calendar-alt"></i> Season: ${filename.replace('_player_', '').replace('.json', '')}`;

            const seasonList = document.getElementById('season-view-list');
            seasonList.innerHTML = '';

            const sortedChamps = Object.entries(championships)
                .map(([player, wins]) => [player, (typeof scores[player] === 'number' ? scores[player] : 0), (typeof wins === 'number' ? wins : 0)])
                .sort(([nameA, scoreA, winsA], [nameB, scoreB, winsB]) => {
                    if (winsB !== winsA) return winsB - winsA;
                    if (scoreB !== scoreA) return scoreB - scoreA;
                    return nameA.localeCompare(nameB);
                });

            sortedChamps.forEach(([player, score, wins], index) => {
                const row = document.createElement('div');
                row.className = 'table-row';
                row.innerHTML = `
                    <div class="table-cell rank">${index + 1}</div>
                    <div class="table-cell player">${player}</div>
                    <div class="table-cell stat">${wins}</div>
                    <div class="table-cell stat">${score}</div>
                `;
                seasonList.appendChild(row);
            });

            this.hideDialog('seasons-dialog');
            this.showDialog('season-view-dialog');
        } catch (error) {
            console.error('Error loading season:', error);
            alert('Failed to load season data.');
        }
    }

    // Finish Season
    showFinishSeasonDialog() {
        document.getElementById('season-name').value = '';
        this.showDialog('finish-season-dialog');
    }

    async finishSeason() {
        const seasonName = document.getElementById('season-name').value.trim();

        if (!seasonName) {
            alert('Please enter a season name.');
            return;
        }

        if (!confirm('Are you sure you want to finish the season? This will archive current data and reset championships.')) {
            return;
        }

        try {
            const response = await fetch('/api/finish-season', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ seasonName })
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const result = await response.json();
            if (!result.success) {
                throw new Error(result.message || 'Failed to finish season');
            }

            alert('✅ Season finished successfully! A new season has begun.');
            this.hideDialog('finish-season-dialog');

            // Reload data to reflect the new season
            this.data = await this.loadData();
            this.refreshPlayerList();
            this.showNotification('New season started!', 'success');

        } catch (error) {
            console.error('Error finishing season:', error);
            alert('Failed to finish season. Please try again.');
        }
    }

    // Admin Login
    showAdminLogin() {
        document.getElementById('admin-password').value = '';
        this.showDialog('admin-login-dialog');
    }

    confirmAdminLogin() {
        const password = document.getElementById('admin-password').value;
        if (password === 'foosball') {
            this.isAdminLoggedIn = true;
            this.hideDialog('admin-login-dialog');
            this.showAdminEdit();
            this.showNotification('Admin access granted', 'success');
        } else {
            alert('❌ Incorrect password');
            document.getElementById('admin-password').value = '';
        }
    }

    // Admin Edit
    showAdminEdit() {
        const list = document.getElementById('admin-edit-list');
        list.innerHTML = '';
        // Sort players like championships: by wins desc, then scores desc, then name asc
        const sortedPlayers = this.data.players.slice().sort((a, b) => {
            const winsA = this.data.championships[a.name] || 0;
            const winsB = this.data.championships[b.name] || 0;
            const scoresA = this.data.scores[a.name] || 0;
            const scoresB = this.data.scores[b.name] || 0;
            if (winsB !== winsA) return winsB - winsA;
            if (scoresB !== scoresA) return scoresB - scoresA;
            return a.name.localeCompare(b.name);
        });
        sortedPlayers.forEach(player => {
            const row = document.createElement('div');
            row.className = 'table-row';
            row.innerHTML = `
                <div class="table-cell player">${player.name}</div>
                <div class="table-cell stat editable">
                    <input type="number" class="champ-input" data-player="${player.name}" value="${this.data.championships[player.name] || 0}" min="0">
                </div>
                <div class="table-cell stat editable">
                    <input type="number" class="score-input" data-player="${player.name}" value="${this.data.scores[player.name] || 0}">
                </div>
            `;
            list.appendChild(row);
        });
        this.showDialog('admin-edit-dialog');
    }

    async saveAdminEdits() {
        const champInputs = document.querySelectorAll('.champ-input');
        const scoreInputs = document.querySelectorAll('.score-input');
        
        champInputs.forEach(input => {
            const player = input.dataset.player;
            this.data.championships[player] = parseInt(input.value) || 0;
        });
        
        scoreInputs.forEach(input => {
            const player = input.dataset.player;
            this.data.scores[player] = parseInt(input.value) || 0;
        });
        
        await this.saveData();
        this.hideDialog('admin-edit-dialog');
        alert('✅ Changes saved successfully!');
        this.showNotification('Admin changes saved', 'success');
    }
}

// Initialize the app when the page loads
document.addEventListener('DOMContentLoaded', () => {
    new TournamentApp();
});