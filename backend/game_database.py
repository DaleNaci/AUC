class GameDatabase:
    def __init__(self):
        # key = game id, value = player ids
        self.games = {}

        # key = player id, value = game id
        self.players = {}

        # Game ID, counts upwards
        self.game_number = 0

        # key = message id, value = game id
        self.pending = {}

        # key = game id, value = [(impostor ids), win/loss for imp]
        self.imps = {}


    # Add game to database
    def add_game(self, ids):
        # Add ids to "games" dictionary
        self.games[self.game_number] = ids

        # Add ids to "players" dictionary
        for id in ids:
            self.players[id] = self.game_number

        self.game_number += 1


    # Remove game from database
    # id is a player in the game
    def remove_game(self, id):
        # Get ids of players and game
        game_id = self.players[id]
        ids = self.games[game_id]

        # Delete game and delete players from database
        del self.games[game_id]

        for id in ids:
            # Only delete if the player's current game is listed
            if self.players[id] == game_id:
                del self.players[id]


    # Get list of players ids in a game
    # id is a player in the game
    def get_game(self, id):
        # Get game from id
        game_id = self.players[id]
        return self.games[game_id]


    # Get game id
    # id is a player in the game
    def get_game_id(self, id):
        return self.players[id]


    # Add game id to list of pending games
    def add_pending_game(self, msg_id, game_id, imp_ids, didCrewWin):
        self.pending[msg_id] = game_id
        self.imps[game_id] = (imp_ids, not didCrewWin)


    # Remove game from list of pending games using game ID
    def remove_pending_game(self, game_id):
        del self.games[game_id]

        for k, v in self.pending.items():
            if v == game_id:
                del self.pending[k]
                break

    # Changes a pending game back to "in progress"
    def reverse_pending(self, game_id):
        for k, v in self.pending.items():
            if v == game_id:
                del self.pending[k]
                break


    def is_game_pending(self, game_id):
        return game_id in self.pending.values()
