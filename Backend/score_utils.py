SALES_RATE = [0,1,3,7,13,21,30,40,50,60]
class ScoreSheet:
    def __init__(self, color):
        self.color = color
        self.merManager = MerchandiseManager()

class MerchandiseManager:
    def __init__(self):
        self.inventory = {}

    def calculateScore(self, detailFlag=True):
        temp_inventory, score = self.inventory.copy(), 0
        while len(temp_inventory):
            if detailFlag:
                print("Set Contains ", len(temp_inventory), " merchandises, Score: ",SALES_RATE[len(temp_inventory)])
            score += len(temp_inventory)
            temp_inventory = {key: value-1 for key, value in temp_inventory.items() if value-1}
        return score