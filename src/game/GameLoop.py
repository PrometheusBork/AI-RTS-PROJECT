class GameLoop:
    def __init__(self, game):
        self.game = game
        self.running = True

    def start(self):
        while self.running:
            self.game.draw()

    def stop(self):
        self.running = False
