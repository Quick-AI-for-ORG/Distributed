class Player:
    count = 0
    def __init__(self, name, health=3):
        Player.count += 1
        self.id = Player.count
        self.name = name
        self.health = health

