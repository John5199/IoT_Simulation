from utils.config_loader import load_data
from models.plc import PLC
from models.gateway import Gateway
from models.server import Server
from models.telegramBot import MiBotTelegram, TOKEN, GROUP_ID
import asyncio


async def main():
    data = load_data('config.json')
    mibot = MiBotTelegram(TOKEN, GROUP_ID)
    
    await mibot.app.initialize()
    await mibot.app.start()            
    await mibot.app.updater.start_polling()

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

            await asyncio.sleep(3)  # Usa sleep no bloqueante

if __name__ == "__main__":
    asyncio.run(main())