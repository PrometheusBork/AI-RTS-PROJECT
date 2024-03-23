class PlayerManager:
    def __init__(self):
        self.players = []

    def add_player(self, player):
        self.players.append(player)

    def remove_player(self, player):
        self.players.remove(player)

    def get_player(self, base):
        for player in self.players:
            if player.base == base:
                return player
        return None

    def get_players(self):
        return self.players