class PlayerManager:
    def __init__(self):
        self.players = list()

    def add_player(self, player):
        self.players.append(player)

    def remove_player(self, player):
        self.players.remove(player)

    def get_player_by_base(self, base):
        for player in self.players:
            if player.base == base:
                return player

    def get_player_by_unit(self, unit):
        for player in self.players:
            if unit in player.units:
                return player
