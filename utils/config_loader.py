import json

def load_data(archieve: str):
    try:
        with open(archieve, 'r') as file:
            data = json.load(file)
            return data
    except json.JSONDecodeError as e:
        print(f"Error al parsear el JSON: {e}")
    except FileNotFoundError:
        print("El archivo no se encuentra.")
    except Exception as e:
        print(f"Ocurrió un error: {e}")
    return None
