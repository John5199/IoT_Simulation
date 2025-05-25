import random

class PLC:
    def __init__(self, id: int, sensors: dict, gateway_id: int):
        self.data = {"id": id, "sensors": sensors}
        self.gateway_id = gateway_id

    def readSensorData(self):
        for key in self.data['sensors']:
            self.data['sensors'][key] = random.randint(1, 100)

    def getIdSender(self):
        return self.gateway_id
    
    def sendInfo(self):
        return self.data
