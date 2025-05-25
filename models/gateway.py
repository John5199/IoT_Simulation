

class Gateway:
    def __init__(self, id: int, protocol: str, server_ip: str):
        self.id = id
        self.protocol = protocol
        ##logger mqtt o algun dels  que surten al document
        self.server_ip = server_ip
        ##el que esta creat al server

    def receiveInfo(self, data):
        self.data = data

    def getIdSender(self):
        return self.server_ip
    
    def sendInfo(self):
        return self.data
    