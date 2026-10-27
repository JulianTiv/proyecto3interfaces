import math
from flask import Flask, render_template, request, redirect, url_for, session, flash, abort

import usuarios
from calculos import OPCIONES

app = Flask(__name__)
app.secret_key = "clave-del-proyecto-interfaces-1"

usuarios.crear_archivo_si_no_existe()


@app.route("/")
def inicio():
    if "usuario" in session:
        return redirect(url_for("menu"))
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        nombre = request.form.get("usuario", "").strip()
        clave = request.form.get("password", "")

        usuario = usuarios.buscar_usuario(nombre)
        if usuario is not None and usuarios.clave_correcta(usuario, clave):
            session["usuario"] = usuario["usuario"]
            session["perfil"] = usuario["perfil"]
            return redirect(url_for("menu"))

        flash("Usuario o contraseña incorrectos.", "error")
        return render_template("login.html", usuario=nombre)

    return render_template("login.html", usuario="")


@app.route("/registro", methods=["GET", "POST"])
def registro():
    if request.method == "POST":
        nombre = request.form.get("usuario", "").strip()
        clave = request.form.get("password", "")
        confirmar = request.form.get("confirmar", "")
        perfil = request.form.get("perfil", "Operario")

        error = None
        if nombre == "":
            error = "Escribe un usuario."
        elif usuarios.buscar_usuario(nombre) is not None:
            error = "Ese usuario ya existe. Elige otro."
        elif len(clave) < 8:
            error = "La contraseña debe tener mínimo 8 caracteres."
        elif clave != confirmar:
            error = "Las contraseñas no coinciden."
        elif perfil not in usuarios.PERFILES:
            error = "Elige un perfil válido."

        if error:
            flash(error, "error")
            return render_template("registro.html", usuario=nombre, perfil=perfil,
                                   perfiles=usuarios.PERFILES)

        usuarios.registrar_usuario(nombre, clave, perfil)
        flash("Cuenta creada. Ya puedes iniciar sesión.", "ok")
        return redirect(url_for("login"))

    return render_template("registro.html", usuario="", perfil="Operario",
                           perfiles=usuarios.PERFILES)


@app.route("/menu")
def menu():
    if "usuario" not in session:
        return redirect(url_for("login"))
    return render_template("menu.html", usuario=session["usuario"], opciones=OPCIONES)


def leer_numero(texto):
    try:
        numero = float(texto.strip().replace(",", "."))
    except ValueError:
        return None
    if not math.isfinite(numero) or numero <= 0:
        return None
    return numero


@app.route("/calculo/<int:numero>", methods=["GET", "POST"])
def calculo(numero):
    if "usuario" not in session:
        return redirect(url_for("login"))
    if numero not in OPCIONES:
        abort(404)

    opcion = OPCIONES[numero]
    valores = {}
    resultado = None

    for campo in opcion["campos"]:
        if campo["tipo"] == "opciones":
            valores[campo["id"]] = campo["defecto"]

    if request.method == "POST":
        datos = {}
        error = None
        for campo in opcion["campos"]:
            texto = request.form.get(campo["id"], "")
            valores[campo["id"]] = texto
            if campo["tipo"] == "opciones":
                if texto not in [v for v, _ in campo["opciones"]]:
                    error = "Elige un " + campo["etiqueta"].lower() + "."
                datos[campo["id"]] = texto
            else:
                numero_leido = leer_numero(texto)
                if numero_leido is None:
                    error = "Escribe un número mayor que 0 en «" + campo["etiqueta"] + "»."
                datos[campo["id"]] = numero_leido

        if error:
            flash(error, "error")
        else:
            resultado = opcion["calcular"](datos)

    return render_template("calculo.html", numero=numero, opcion=opcion,
                           valores=valores, resultado=resultado)


@app.route("/salir")
def salir():
    session.clear()
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
