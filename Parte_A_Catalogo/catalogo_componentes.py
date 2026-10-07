"""Módulo de gestión del catálogo de componentes eléctricos (Parte A).

El catálogo se almacena en un diccionario de ámbito de módulo en el que
cada clave es el identificador (cadena de caracteres única) del componente
y su valor asociado es otro diccionario con su tipo y su valor nominal:

    _componentes = {
        "R1": {"tipo": "resistencia", "valor": 5},
        "C1": {"tipo": "condensador", "valor": 20e-6},
        "L1": {"tipo": "inductancia", "valor": 4e-3},
    }

Las funciones de consulta devuelven siempre COPIAS de los datos, de forma
que la estructura interna del módulo no pueda modificarse desde fuera.
"""

# Tipos de componentes admitidos en el catálogo
_tipos_validos = {"resistencia", "condensador", "inductancia"}

# Diccionario interno del catálogo (privado por convención de nombre)
_componentes = {}


def _validar_tipo(tipo):
    """Comprueba que el tipo indicado es uno de los admitidos.

    Genera ValueError si el tipo no es válido.
    """
    if tipo not in _tipos_validos:
        raise ValueError(
            f"Tipo de componente no admitido: {tipo!r}. "
            f"Tipos válidos: {sorted(_tipos_validos)}"
        )


def _validar_valor(valor):
    """Comprueba que el valor es numérico y estrictamente mayor que cero.

    Genera TypeError si el valor no es numérico y ValueError si es <= 0.
    """
    # bool es subclase de int, por lo que se descarta explícitamente
    if isinstance(valor, bool) or not isinstance(valor, (int, float)):
        raise TypeError(
            f"El valor debe ser numérico, se ha recibido {type(valor).__name__}"
        )
    if valor <= 0:
        raise ValueError(
            f"El valor del componente debe ser mayor que cero (recibido: {valor})"
        )


def add_nuevo_componente(identificador, tipo, valor):
    """Registra un nuevo componente en el catálogo.

    Genera una excepción si:
    - el identificador no es una cadena de caracteres o está vacío,
    - ya existe un componente con ese identificador,
    - el tipo no es uno de los admitidos,
    - el valor no es numérico,
    - el valor es igual o menor que cero.
    """
    if not isinstance(identificador, str) or not identificador:
        raise ValueError("El identificador debe ser una cadena de caracteres no vacía")
    if identificador in _componentes:
        raise ValueError(
            f"Ya existe un componente con el identificador {identificador!r}"
        )
    _validar_tipo(tipo)
    _validar_valor(valor)
    _componentes[identificador] = {"tipo": tipo, "valor": valor}


def obtener_componente(identificador):
    """Devuelve la información del componente indicado.

    Genera KeyError si el identificador no está registrado.
    Se devuelve una copia del diccionario del componente, no una referencia
    que permita modificar la estructura interna del módulo.
    """
    if identificador not in _componentes:
        raise KeyError(
            f"El componente {identificador!r} no está registrado en el catálogo"
        )
    return dict(_componentes[identificador])


def acceder_componentes():
    """Devuelve la información de todos los componentes como diccionario.

    Se devuelve una nueva estructura con los mismos valores, de forma que el
    diccionario interno no puede modificarse desde fuera del módulo.
    """
    return {ident: dict(datos) for ident, datos in _componentes.items()}


def componentes_tipo(tipo):
    """Devuelve una lista con los identificadores de los componentes del tipo indicado.

    Genera ValueError si el tipo no es uno de los admitidos.
    """
    _validar_tipo(tipo)
    return [ident for ident, datos in _componentes.items() if datos["tipo"] == tipo]


def resumen_componentes():
    """Devuelve un diccionario con el número de componentes de cada tipo."""
    resumen = {tipo: 0 for tipo in _tipos_validos}
    for datos in _componentes.values():
        resumen[datos["tipo"]] += 1
    return resumen
