from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from datetime import datetime
import json
import os

app = FastAPI(title="API Lâmpada ESP32")

ARQUIVO = "dados.json"

# Garante que o arquivo existe
if not os.path.exists(ARQUIVO):
    with open(ARQUIVO, "w") as f:
        json.dump([], f)

class Registro(BaseModel):
    tempoLigado: int          # em segundos

def carregar_registros():
    if not os.path.exists(ARQUIVO):
        return []

    with open(ARQUIVO, "r") as f:
        content = f.read().strip()
        if not content:  # arquivo está vazio
            return []
        return json.loads(content)


def salvar_registros(registros):
    with open(ARQUIVO, "w") as f:
        json.dump(registros, f, indent=4)

@app.post("/registrar")
def registrar_evento(evento: Registro):
    registros = carregar_registros()

    novo = {
        "tempoLigado": evento.tempoLigado,
        "data": datetime.now().isoformat()
    }

    registros.append(novo)
    salvar_registros(registros)

    return {"status": "ok", "salvo": novo}

@app.get("/registros")
def listar():
    return carregar_registros()
