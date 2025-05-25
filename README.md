#IoT System Simulation
Aquest projecta simula de forma la transmisió d'informació d'uns sensors fins guardar-ho en una arxiu. Aquest sistema es configura alterant el codi del arxiu json.

#Funcionament
    En primer lloc es simulen unes dades, només pels dos primers projectes després ja seran reals, en el arxiu plc.py, que simula un plc, que passen cap un gateway que fa de intermediari entre el plc i el server el qual no´mes s'encarrega de la transimssió de la informació, que finalment arriven al server on s'emmagatzema en un arxiu csv.

    ##Objectes
        En els objectes creats trobem practicament els mateixos metodes que son:
            - __init__ : El qual s'encarrega d'inicialitzar el objecte.
            - receiveInfo : S'encarrega de rebre les dades.
            - sendInfo : S'encarrega d'enviar les dades
            - getIdSender : Ens dona el Id del objecte al qual s'envia la    informació
        També hi ha dues funcions uniques que son:
            - readsSensorData : Que simula les dadees, nomes pels dos primers projectes
            - storeData : S'encarrega de guardar la informació al iot_data.csv
        
    ##Main
        Aqui el que fem es llegir la informacio amb la funcio del config_loader que es troba al config.json i es creen els objectes corresponents, en el següent pas s'estableix les conexions entre els diferents objectes i passant la data.

    ##Aclaraments
        He trobat problemes al moment d'importar funcionsja que les ubicacions no s'ha usat el comado os 

##Codis vistos implementats de forma similar
    - bucle temporal
        https://www.freecodecamp.org/espanol/news/como-hacer-un-retraso-en-python-usando-la-funcion-sleep/

    - bucle final de sentencia 
        https://docs.python.org/es/3/tutorial/datastructures.html#list-comprehensions

    - comando f{""}
        https://docs.python.org/es/3/reference/lexical_analysis.html#f-strings