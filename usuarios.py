import json
import os
from werkzeug.security import generate_password_hash, check_password_hash

CARPETA = os.path.dirname(os.path.abspath(__file__))
ARCHIVO = os.path.join(CARPETA, "usuarios.json")

PERFILES = ["Operario", "Supervisor"]


def crear_archivo_si_no_existe():
    if not os.path.exists(ARCHIVO):
        guardar_usuarios([])


def leer_usuarios():
    crear_archivo_si_no_existe()
    with open(ARCHIVO, "r", encoding="utf-8") as f:
        return json.load(f)


def guardar_usuarios(lista):
    with open(ARCHIVO, "w", encoding="utf-8") as f:
        json.dump(lista, f, indent=2, ensure_ascii=False)


def buscar_usuario(nombre):
    for u in leer_usuarios():
        if u["usuario"].lower() == nombre.lower():
            return u
    return None


def registrar_usuario(nombre, clave, perfil):
    lista = leer_usuarios()
    lista.append({
        "usuario": nombre,
        "password": generate_password_hash(clave, method="pbkdf2:sha256"),
        "perfil": perfil,
    })
    guardar_usuarios(lista)


def clave_correcta(usuario, clave):
    return check_password_hash(usuario["password"], clave)
