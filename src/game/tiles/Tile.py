import pygame


class Tile(pygame.sprite.Sprite):
    def __init__(self, row, col):
        super().__init__()
        self.row = row
        self.col = col
        self.image = None
        self.rect = None
        self.tile_type = ""
        self.is_walkable = False
        self.tile_size = 50
        self.game_object = None

    def add_game_object(self, game_object):
        self.game_object = game_object
        #self.game_object.row = self.row
        #self.game_object.col = self.col
        self.game_object.update_position(self.row, self.col)

    def remove_game_object(self):
        self.game_object = None

    def is_empty(self):
        return self.game_object is None

    def update(self):
        pass
