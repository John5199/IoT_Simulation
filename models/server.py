from datetime import datetime
import csv

class Server:
    def __init__(self, ip: str):
        self.ip = ip
        ##log requisits que ha de tenir
    def receiveInfo(self, data: dict):
        self.data = data    
    
    def storeData(self):
        archivo = "data/iot_data.csv"
        fecha = datetime.now().strftime("%Y-%m-%d")
        hora = datetime.now().strftime("%H:%M:%S")

        plc_id = self.data['id']
        sensors = self.data['sensors']

        with open(archivo, mode='a', newline='') as file:
            fieldnames = ['fecha', 'hora', 'plc_id', 'sensor', 'valor']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader() if file.tell() == 0 else None
            for sensor_type, value in sensors.items():
                row = {
                    'fecha': fecha, 
                    'hora': hora, 
                    'plc_id': plc_id, 
                    'sensor': sensor_type, 
                    'valor': value}
                writer.writerow(row)

##Falta crear encapCalat de la taula csv
##Anotar lo de les direccions