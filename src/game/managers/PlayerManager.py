class PlayerManager:
    def __init__(self):
        self.players = set()

    def add_player(self, player):
        self.players.add(player)

    def remove_player(self, player):
        self.players.discard(player)

    def get_player_by_base(self, base):
        return next((player for player in self.players if player.base == base), None)

    def get_player_by_unit(self, unit):
        return next((player for player in self.players if unit in player.units), None)
