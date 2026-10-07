"""Programa principal de prueba del módulo catalogo_componentes (Parte A).

Registra los componentes del circuito a partir de una lista de tuplas,
muestra el catálogo y las consultas disponibles, y comprueba todos los
casos de error previstos en el enunciado.
"""

from Parte_A_Catalogo import catalogo_componentes as cc
from Parte_A_Catalogo.catalogo_componentes import (
    add_nuevo_componente,
    obtener_componente,
    acceder_componentes,
    componentes_tipo,
    resumen_componentes,
)

datosComponentes = [
    ("R1", "resistencia", 5),
    ("R2", "resistencia", 10),
    ("R3", "resistencia", 30),
    ("C1", "condensador", 20e-6),
    ("C2", "condensador", 200e-6),
    ("L1", "inductancia", 4e-3),
]

# Cargar el catálogo recorriendo la lista
for identificador, tipo, valor in datosComponentes:
    add_nuevo_componente(identificador, tipo, valor)

# 1. Mostrar el catálogo completo de forma legible
print("=" * 55)
print("CATÁLOGO DE COMPONENTES")
print("=" * 55)
for identificador, datos in acceder_componentes().items():
    print(f"  {identificador:<6}{datos['tipo']:<15}{datos['valor']}")

# 2. Consulta de un componente
print()
print("CONSULTA DE R1")
print(obtener_componente("R1"))

# 3. Mostrar por separado los identificadores de:
#    resistencias, condensadores e inductancias
print()
print("Resistencias:  ", componentes_tipo("resistencia"))
print("Condensadores: ", componentes_tipo("condensador"))
print("Inductancias:  ", componentes_tipo("inductancia"))

# 4. Mostrar el resumen del número de componentes de cada tipo
print()
print("Resumen:", resumen_componentes())

# 5. Comprobar que las estructuras devueltas son copias seguras:
#    modificarlas no debe alterar el catálogo interno del módulo
catalogo = acceder_componentes()
catalogo["R1"]["valor"] = 999
componente_r1 = obtener_componente("R1")
componente_r1["valor"] = 123
print()
print("Tras modificar las copias, R1 sigue siendo:", obtener_componente("R1"))


def probar_excepcion(descripcion, excepcion_esperada, func, *args):
    """Ejecuta func(*args) comprobando que lance la excepción esperada.

    Imprime el motivo de la excepción o avisa si no se lanza ninguna.
    """
    try:
        func(*args)
    except excepcion_esperada as e:
        print(f"{descripcion}: {e}")
    else:
        print(f"{descripcion}: ERROR, no se lanzó {excepcion_esperada.__name__}")


# 6-8. Pruebas de los casos de error
print()
print("=" * 55)
print("PRUEBAS DE ERRORES")
print("=" * 55)

# Identificador repetido
probar_excepcion(
    "Identificador repetido",
    ValueError,
    add_nuevo_componente,
    "R1", "resistencia", 7,
)

# Identificador vacío
probar_excepcion(
    "Identificador vacío",
    ValueError,
    cc.add_nuevo_componente,
    "", "resistencia", 7,
)

# Tipo de componente no admitido
probar_excepcion(
    "Tipo no admitido",
    ValueError,
    add_nuevo_componente,
    "R9", "capacitor", 10,
)

# Valor no numérico
probar_excepcion(
    "Valor no numérico",
    TypeError,
    add_nuevo_componente,
    "R9", "resistencia", "cinco ohmios",
)

# Valor igual a cero
probar_excepcion(
    "Valor igual a cero",
    ValueError,
    add_nuevo_componente,
    "R9", "resistencia", 0,
)

# Valor menor que cero
probar_excepcion(
    "Valor menor que cero",
    ValueError,
    add_nuevo_componente,
    "R9", "resistencia", -5,
)

# Consulta de un componente inexistente
probar_excepcion(
    "Componente inexistente",
    KeyError,
    obtener_componente,
    "R9",
)

# El catálogo debe seguir intacto tras las pruebas de error
print()
print("Resumen final:", resumen_componentes())
