def formato(numero, decimales):
    return f"{numero:,.{decimales}f}"


def formato_corto(numero):
    texto = f"{numero:,.2f}"
    if "." in texto:
        texto = texto.rstrip("0").rstrip(".")
    return texto


def calcular_superficie(ancho, largo):
    return ancho * largo


def calcular_volumen(espesor, ancho, largo):
    return espesor * ancho * largo


def calcular_muro(datos):
    tabla = {
        "30": {"cemento": 15.2, "arena": 0.115, "ladrillos": 120},
        "20": {"cemento": 10.9, "arena": 0.09, "ladrillos": 90},
    }
    por_m2 = tabla[datos["espesor"]]
    superficie = calcular_superficie(datos["largo"], datos["alto"])
    return {
        "principal": formato_corto(superficie),
        "unidad": "m² de superficie",
        "titulo": "Materiales necesarios",
        "lista": [
            ("Cemento", formato(superficie * por_m2["cemento"], 1), "kg"),
            ("Arena", formato(superficie * por_m2["arena"], 2), "m³"),
            ("Ladrillos", formato(superficie * por_m2["ladrillos"], 0), "un"),
        ],
    }


def calcular_viga(datos):
    largo = datos["largo"]
    return {
        "principal": formato_corto(largo),
        "unidad": "m de largo",
        "titulo": "Materiales necesarios",
        "lista": [
            ("Cemento", formato(largo * 9, 1), "kg"),
            ("Arena", formato(largo * 0.02, 2), "m³"),
            ("Piedra", formato(largo * 0.02, 2), "m³"),
            ("Hierro del 8", formato(largo * 4, 1), "m"),
            ("Hierro del 4", formato(largo * 3, 1), "m"),
        ],
    }


def calcular_columnas(datos):
    largo = datos["largo"]
    return {
        "principal": formato_corto(largo),
        "unidad": "m de largo",
        "titulo": "Materiales necesarios",
        "lista": [
            ("Cemento", formato(largo * 7.5, 1), "kg"),
            ("Arena", formato(largo * 0.016, 2), "m³"),
            ("Piedra", formato(largo * 0.016, 2), "m³"),
            ("Hierro del 10", formato(largo * 6, 1), "m"),
            ("Hierro del 4", formato(largo * 3, 1), "m"),
        ],
    }


def calcular_contrapiso(datos):
    espesor_m = datos["espesor"] / 100
    volumen = calcular_volumen(espesor_m, datos["ancho"], datos["largo"])
    return {
        "principal": formato_corto(volumen),
        "unidad": "m³ de volumen",
        "titulo": "Materiales necesarios",
        "lista": [
            ("Cemento", formato(volumen * 105, 1), "kg"),
            ("Arena", formato(volumen * 0.45, 2), "m³"),
            ("Piedra", formato(volumen * 0.9, 2), "m³"),
        ],
    }


def calcular_techo(datos):
    superficie = calcular_superficie(datos["ancho"], datos["largo"])
    return {
        "principal": formato_corto(superficie),
        "unidad": "m² de superficie",
        "titulo": "Materiales necesarios",
        "lista": [
            ("Cemento", formato(superficie * 33, 1), "kg"),
            ("Arena", formato(superficie * 0.072, 2), "m³"),
            ("Piedra", formato(superficie * 0.072, 2), "m³"),
            ("Hierro del 8", formato(superficie * 7, 1), "m"),
            ("Hierro del 6", formato(superficie * 4, 1), "m"),
        ],
    }


def calcular_pisos(datos):
    superficie = calcular_superficie(datos["ancho"], datos["largo"])
    extra = superficie * 0.10
    return {
        "principal": formato_corto(superficie + extra),
        "unidad": "m² a comprar (con 10% extra)",
        "titulo": "Detalle",
        "lista": [
            ("Superficie", formato_corto(superficie), "m²"),
            ("Extra por recortes", formato_corto(extra), "m²"),
        ],
    }


def calcular_pintura(datos):
    superficie = datos["superficie"]
    litros = superficie / 6
    return {
        "principal": formato_corto(superficie),
        "unidad": "m² de superficie",
        "titulo": "Materiales necesarios",
        "lista": [
            ("Pintura", formato(litros, 1), "L"),
        ],
    }


OPCIONES = {
    1: {"nombre": "Muro de ladrillo", "calcular": calcular_muro, "campos": [
        {"id": "espesor", "etiqueta": "Espesor", "tipo": "opciones",
         "opciones": [("20", "20 cm"), ("30", "30 cm")], "defecto": "30"},
        {"id": "largo", "etiqueta": "Largo (m)", "tipo": "numero"},
        {"id": "alto", "etiqueta": "Alto (m)", "tipo": "numero"},
    ]},
    2: {"nombre": "Viga de hormigón", "calcular": calcular_viga, "campos": [
        {"id": "largo", "etiqueta": "Largo (m)", "tipo": "numero"},
    ]},
    3: {"nombre": "Columnas de hormigón", "calcular": calcular_columnas, "campos": [
        {"id": "largo", "etiqueta": "Largo (m)", "tipo": "numero"},
    ]},
    4: {"nombre": "Contrapisos", "calcular": calcular_contrapiso, "campos": [
        {"id": "espesor", "etiqueta": "Espesor (cm)", "tipo": "numero"},
        {"id": "ancho", "etiqueta": "Ancho (m)", "tipo": "numero"},
        {"id": "largo", "etiqueta": "Largo (m)", "tipo": "numero"},
    ]},
    5: {"nombre": "Techo", "calcular": calcular_techo, "campos": [
        {"id": "espesor", "etiqueta": "Espesor (cm)", "tipo": "numero"},
        {"id": "ancho", "etiqueta": "Ancho (m)", "tipo": "numero"},
        {"id": "largo", "etiqueta": "Largo (m)", "tipo": "numero"},
    ]},
    6: {"nombre": "Pisos", "calcular": calcular_pisos, "campos": [
        {"id": "ancho", "etiqueta": "Ancho (m)", "tipo": "numero"},
        {"id": "largo", "etiqueta": "Largo (m)", "tipo": "numero"},
    ]},
    7: {"nombre": "Pintura", "calcular": calcular_pintura, "campos": [
        {"id": "superficie", "etiqueta": "Superficie del muro (m²)", "tipo": "numero"},
    ]},
}
