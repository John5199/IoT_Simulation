from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import csv
import json
import asyncio

TOKEN = '7875769921:AAH-if0PY4clmKENv1desXUIkTAIrMPa9t8'
GROUP_ID = -1002557923218

class MiBotTelegram:
    def __init__(self, token: str, group_id: int):
        self.token = token
        self.group_id = group_id
        self.app = Application.builder().token(self.token).build()
        self._add_comands()

        self.subscriptions = {}
        self.alerts = {}
        self.user_tasks = {}

    def _openCSVFile(self):
        with open('data/iot_data.csv', newline='', encoding='utf-8') as archivo:
            lector = list(csv.reader(archivo))
            return lector[1:]

    def getNewData(self, archivo, subs):
        resultado = {}
        for plc_id, sensores in subs.items():
            valores = {}
            for row in reversed(archivo):
                if row[2] == str(plc_id) and row[3] in sensores:
                    if row[3] not in valores:
                        valores[row[3]] = {
                            "valor": row[4],
                            "fecha": row[0],
                            "hora": row[1]
                        }
                if len(valores) == len(sensores):
                    break
            if valores:
                resultado[plc_id] = valores
        return resultado

    def _add_comands(self):
        self.app.add_handler(CommandHandler("subscribe", self.subscribe))
        self.app.add_handler(CommandHandler("get_data", self.get_data))
        self.app.add_handler(CommandHandler("create_alert", self.create_alert))


    async def _sendDataPeriodically(self, user_id, data_subs):
        while True:
            try:
                archivo = self._openCSVFile()
                resultado = self.getNewData(archivo, data_subs)
            
                if resultado:
                    await self.app.bot.send_message(chat_id=user_id, text=json.dumps(resultado, indent=2))
            
                if user_id in self.alerts:
                    alertas_usuario = self.alerts[user_id]
                    datos_alerta = self.getNewData(archivo, alertas_usuario)
                
                    for plc_id, sensores in datos_alerta.items():
                        for sensor, info in sensores.items():
                            try:
                                valor = float(info['valor'])
                                umbral = alertas_usuario.get(plc_id, {}).get(sensor)
                                if umbral is not None and valor > umbral:
                                    await self.app.bot.send_message(
                                        chat_id=user_id,
                                        text=f"[ALERTA]\nPLC: {plc_id}\nSensor: {sensor}\nValor: {valor}\nFecha: {info['fecha']} {info['hora']}"
                            )
                            except ValueError:
                                continue
            except Exception as e:
                print(f"Error at sending {user_id}: {e}")
            await asyncio.sleep(2)


    async def subscribe(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.effective_chat.id != self.group_id:
            return
        try:
            user_id = update.effective_user.id
            data = json.loads(" ".join(context.args))
            self.subscriptions[user_id] = data
            await update.message.reply_text("Subscript.")

            if user_id not in self.user_tasks:
                self.user_tasks[user_id] = asyncio.create_task(self._sendDataPeriodically(user_id, data))

        except Exception as e:
            await update.message.reply_text(f"Error: {e}")

    async def get_data(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.effective_chat.id != self.group_id:
            return
        try:
            user_input = json.loads(" ".join(context.args))
            archivo = self._openCSVFile()
            resultado =  self.getNewData(archivo, user_input)
            await update.effective_message.reply_text(json.dumps(resultado, indent=2))
        except Exception as e:
            await update.effective_message.reply_text(f"Error al obtener datos: {e}")

    async def create_alert(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.effective_chat.id != self.group_id:
            return
        try:
            user_id = update.effective_user.id
            data = json.loads(" ".join(context.args))
            self.alerts[user_id] = data
            await update.message.reply_text("Alertas configuradas.")
        except Exception as e:
            await update.message.reply_text(f"Error al configurar alertas: {e}")

    def run(self):
        self.app.run_polling()

