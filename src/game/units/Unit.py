from game.objects.GameObject import GameObject

class Unit(GameObject):
    def __init__(self, name, health, damage, position):
        super().__init__(position)
        self.name = name
        self.health = health
        self.damage = damage
    
    def attack(self, target):
        target.health -= self.damage

    def move(self, direction):
        pass

    def is_alive(self):
        return self.health > 0

    def __str__(self):
        return f'{self.name} has {self.health} health and {self.damage} damage'