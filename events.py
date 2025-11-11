import argparse
import json
import os

# Archivo donde guardaremos los datos
DATA_FILE = "eventos.json"

# Si no existe, lo creamos vacío
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as f:
        json.dump({"events": [], "registrations": []}, f)

# Cargar datos
def load_data():
    with open(DATA_FILE, "r") as f:
        return json.load(f)

# Guardar datos
def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

# Crear evento
def create_event(titulo, inicio, fin, cupo):
    data = load_data()
    if fin < inicio:
        print("❌ La fecha de fin no puede ser menor que la de inicio.")
        return
    evento = {
        "id": len(data["events"]) + 1,
        "titulo": titulo,
        "fecha_inicio": inicio,
        "fecha_fin": fin,
        "cupo": cupo,
        "inscritos_count": 0
    }
    data["events"].append(evento)
    save_data(data)
    print(f"✅ Evento '{titulo}' creado con ID {evento['id']}")

# Listar eventos
def list_events():
    data = load_data()
    if not data["events"]:
        print("No hay eventos creados.")
        return
    for e in data["events"]:
        print(f"[{e['id']}] {e['titulo']} ({e['fecha_inicio']} → {e['fecha_fin']}) - Cupo: {e['inscritos_count']}/{e['cupo']}")

# Registrar usuario
def register(event_id, email):
    data = load_data()
    event = next((e for e in data["events"] if e["id"] == event_id), None)
    if not event:
        print("❌ Evento no encontrado.")
        return
    if event["inscritos_count"] >= event["cupo"]:
        print("❌ El cupo del evento está lleno.")
        return
    for r in data["registrations"]:
        if r["evento_id"] == event_id and r["usuario_email"] == email:
            print("❌ Ya estás inscrito en este evento.")
            return
    data["registrations"].append({"evento_id": event_id, "usuario_email": email})
    event["inscritos_count"] += 1
    save_data(data)
    print(f"✅ {email} inscrito al evento '{event['titulo']}'")

# --- Configuración de comandos ---
parser = argparse.ArgumentParser(description="Gestión de eventos (CLI)")
subparsers = parser.add_subparsers(dest="command")

# Crear evento
create_parser = subparsers.add_parser("create")
create_parser.add_argument("--titulo", required=True)
create_parser.add_argument("--inicio", required=True)
create_parser.add_argument("--fin", required=True)
create_parser.add_argument("--cupo", type=int, required=True)

# Listar eventos
list_parser = subparsers.add_parser("list")

# Registrar usuario
register_parser = subparsers.add_parser("register")
register_parser.add_argument("id", type=int)
register_parser.add_argument("--email", required=True)

args = parser.parse_args()

# Ejecutar según el comando
if args.command == "create":
    create_event(args.titulo, args.inicio, args.fin, args.cupo)
elif args.command == "list":
    list_events()
elif args.command == "register":
    register(args.id, args.email)
else:
    parser.print_help()
