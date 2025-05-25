from utils.config_loader import load_data
from models.plc import PLC
from models.gateway import Gateway
from models.server import Server
import time

##Carreguem les dades
data = load_data('config.json', 'r')

####Creem objectes plc, gateway, server
if data:

    PLCS_arr = {
        f"PLC_{plc['id']}": PLC(
            plc["id"],
            {sensor["type"]: None for sensor in plc["sensors"]},
            plc["gateway_id"]
        )
        for plc in data["plcs"]
    }

    gateways_arr = {
        f"Gateway_{gw['id']}": Gateway(gw["id"], gw["protocol"], gw["server_ip"])
        for gw in data["gateways"]
    }

    servers_arr = {
        f"Server_{srv['ip']}": Server(srv["ip"])
        for srv in data["servers"]
    }

##Establir relacions
    while True:
        for plc in PLCS_arr.values():
            plc.readSensorData()
            dt = plc.sendInfo()

            gate = gateways_arr[f"Gateway_{plc.getIdSender()}"]
            gate.receiveInfo(dt)
            ds = gate.sendInfo()

            server = servers_arr[f"Server_{gate.getIdSender()}"]
            server.receiveInfo(ds)
            server.storeData()

        time.sleep(3)

