from game.objects.GameObject import GameObject


class Unit(GameObject):
    def __init__(self, name, health, damage):
        super().__init__()
        self.name = name
        self.health = health
        self.damage = damage

    def update_position(self, row, col):
        self.row = row
        self.col = col
        self.rect.centerx = col * 50 + 50 // 2 + 50
        self.rect.centery = row * 50 + 50 // 2 + 50

    def attack(self, target):
        target.health -= self.damage

    def move(self, direction):
        pass

    def is_alive(self):
        return self.health > 0

    def __str__(self):
        return f'{self.name} has {self.health} health and {self.damage} damage'
