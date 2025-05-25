import json

def load_data(archieve: str, mode):
    try:
        with open(archieve, mode) as file:
            if mode == 'r':
                data = json.load(file)
                return data
            else:
                pass
                ##Escriure algo al logger
    except json.JSONDecodeError as e:
        print(f"Error al parsear el JSON: {e}")
    except FileNotFoundError:
        print("El archivo no se encuentra.")
    except Exception as e:
        print(f"Ocurrió un error: {e}")
    return None
##log perque sha obert be el arxiu info
##logs pels errors aquestos
##la ubicacio recalcarho