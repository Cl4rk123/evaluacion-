from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
from datetime import datetime

app = FastAPI()

# Datos guardados en memoria (se borran si apagas el servidor)
eventos = []
inscripciones = []

# --- Modelos de datos ---
class Evento(BaseModel):
    titulo: str
    fecha_inicio: datetime
    fecha_fin: datetime
    cupo: int

class Registro(BaseModel):
    email: EmailStr


# --- Endpoints ---

@app.get("/events")
def listar_eventos():
    return {"status": "ok", "data": eventos}


@app.post("/events")
def crear_evento(evento: Evento):
    # Validaciones básicas
    if evento.fecha_fin < evento.fecha_inicio:
        raise HTTPException(status_code=400, detail="La fecha de fin no puede ser menor que la de inicio.")
    if evento.cupo < 0:
        raise HTTPException(status_code=400, detail="El cupo no puede ser negativo.")

    nuevo_evento = {
        "id": len(eventos) + 1,
        "titulo": evento.titulo,
        "fecha_inicio": evento.fecha_inicio.isoformat(),
        "fecha_fin": evento.fecha_fin.isoformat(),
        "cupo": evento.cupo,
        "inscritos_count": 0
    }
    eventos.append(nuevo_evento)
    return {"status": "ok", "message": "Evento creado", "data": nuevo_evento}


@app.post("/events/{id}/register")
def registrar_usuario(id: int, registro: Registro):
    # Buscar evento
    evento = next((e for e in eventos if e["id"] == id), None)
    if not evento:
        raise HTTPException(status_code=404, detail="Evento no encontrado")

    # Verificar cupo
    if evento["inscritos_count"] >= evento["cupo"]:
        raise HTTPException(status_code=409, detail="El cupo está lleno")

    # Verificar duplicado
    for ins in inscripciones:
        if ins["evento_id"] == id and ins["usuario_email"] == registro.email:
            raise HTTPException(status_code=409, detail="Ya estás inscrito en este evento")

    inscripciones.append({"evento_id": id, "usuario_email": registro.email})
    evento["inscritos_count"] += 1

    return {"status": "ok", "message": f"{registro.email} inscrito correctamente al evento '{evento['titulo']}'"}
