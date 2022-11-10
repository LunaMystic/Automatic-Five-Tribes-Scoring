class ScoreSheet:
    def __init__(self, color):
        self.color = color
        self.merManager = MerchandiseManager()

class MerchandiseManager:
    def __init__(self, color):
        self.inventory = {}
