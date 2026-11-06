# ============================================================
#  ACTIVIDAD 3.4 - MODULO DE NOMINA
#  Transportes del Gran Caribe Colombiano S.C.A. - TransCaribeCol
# ============================================================

from pathlib import Path

# ------------- REGLAS DE NEGOCIO (Guía) -------------
# Administrativo
VALOR_HORA_ADMIN       = 20000
VALOR_HORA_EXTRA_ADMIN = 25000
ARL_ADMIN              = 0.00522  # Riesgo I (0,522 %)

# SUPUESTO: La guía no indica salud/pensión para admin. Asumimos 0.
# Consultar con la instructora. Si ella dice otro valor, se cambia aquí.
SALUD_ADMIN   = 0.0
PENSION_ADMIN = 0.0

# Operativo
VALOR_HORA_OPERATIVO = 40000
IBC_OPERATIVO        = 0.40    # 40% del salario
TASA_SALUD           = 0.125   # 12,5%
TASA_PENSION         = 0.16    # 16%

# Cargos operativos: horas mensuales fijas y ARL según nivel de riesgo
CARGOS_OPERATIVOS = {
    "Conductor":         {"horas": 160, "arl": 0.01044},  # Riesgo II
    "Oficios Generales": {"horas": 100, "arl": 0.00522},  # Riesgo I
    "Vigilancia":        {"horas": 336, "arl": 0.04350},  # Riesgo IV
}

TIPO_ADMIN     = "ADMINISTRATIVO"
TIPO_OPERATIVO = "OPERATIVO"

# Archivo TXT junto al programa
ARCHIVO_TXT = Path(__file__).resolve().parent / "03_Registros_Nomina.txt"

# Posición de cada dato dentro de la MATRIZ
NOMBRE, TIPO, CARGO, HT, SALARIO, HE, TPHE, SALUD, PENSION, ARL, TOTAL = range(11)
ENCABEZADOS = ["Nombre", "Tipo", "Cargo", "HT", "Salario", "HE", "TPHE", "Salud", "Pension", "ARL", "Total a pagar"]
ANCHOS = [20, 15, 18, 5, 12, 5, 10, 10, 10, 8, 12]

# Estructura de datos: Matriz (lista de listas)
registros = []


# ------------------------------ UTILIDADES ------------------------------
def leer_texto(mensaje):
    """Pide un texto y repite hasta que no esté vacío."""
    while True:
        valor = input(mensaje).strip()
        if valor:
            return valor.replace("|", "/")  # Evita romper el formato del TXT
        print("   >> Error: Este campo no puede estar vacío.")


def leer_entero(mensaje, minimo=0, maximo=None):
    """Pide un entero dentro de un rango."""
    while True:
        texto = input(mensaje).strip()
        try:
            numero = int(texto)
        except ValueError:
            print("   >> Error: Escriba un número entero (sin letras).")
            continue
        if numero < minimo or (maximo is not None and numero > maximo):
            limite = f"entre {minimo} y {maximo}" if maximo is not None else f">= {minimo}"
            print(f"   >> Error: El valor debe estar {limite}.")
            continue
        return numero


def formatear_pesos(valor):
    return f"${valor:,.0f}".replace(",", ".")


def porcentaje(tasa):
    return f"{tasa * 100:g}".replace(".", ",")


def formatear_fila(celdas):
    """Alinea una fila en columnas separadas por '|' (consola y TXT)."""
    return " | ".join(str(c).ljust(a) for c, a in zip(celdas, ANCHOS)).rstrip()


# ------------------------------ CALCULOS ------------------------------
def calcular_administrativo(nombre, cargo, horas, horas_extra):
    salario   = horas * VALOR_HORA_ADMIN
    tp_he     = horas_extra * VALOR_HORA_EXTRA_ADMIN
    base      = salario + tp_he

    salud   = round(base * SALUD_ADMIN)
    pension = round(base * PENSION_ADMIN)
    arl     = round(base * ARL_ADMIN)
    total   = base - salud - pension - arl

    return [nombre, TIPO_ADMIN, cargo, horas, salario, horas_extra, tp_he, salud, pension, arl, total]


def calcular_operativo(nombre, cargo):
    horas   = CARGOS_OPERATIVOS[cargo]["horas"]
    salario = horas * VALOR_HORA_OPERATIVO
    ibc     = round(salario * IBC_OPERATIVO)

    salud   = round(ibc * TASA_SALUD)
    pension = round(ibc * TASA_PENSION)
    arl     = round(ibc * CARGOS_OPERATIVOS[cargo]["arl"])
    total   = salario - salud - pension - arl

    return [nombre, TIPO_OPERATIVO, cargo, horas, salario, 0, 0, salud, pension, arl, total]


# ------------------------------ PANTALLA ------------------------------
def mostrar_volante(r):
    es_admin = r[TIPO] == TIPO_ADMIN
    p_salud   = SALUD_ADMIN if es_admin else TASA_SALUD
    p_pension = PENSION_ADMIN if es_admin else TASA_PENSION
    p_arl     = ARL_ADMIN if es_admin else CARGOS_OPERATIVOS[r[CARGO]]["arl"]

    linea = "*" * 60
    print("\n" + linea)
    print(" VOLANTE DE PAGO ".center(60, "*"))
    print(linea)
    print(f" Nombre : {r[NOMBRE]}")
    print(f" Cargo  : {r[CARGO]}")
    print(f" Horas T: {r[HT]}")
    print(f" Salario: {formatear_pesos(r[SALARIO])}")
    
    if es_admin:
        print(f" H. Extra: {r[HE]} (Pago: {formatear_pesos(r[TPHE])})")
    else:
        ibc = round(r[SALARIO] * IBC_OPERATIVO)
        print(f" IBC(40%): {formatear_pesos(ibc)}")
        
    print("-" * 60)
    print(" DESCUENTOS DE LEY ".center(60, "-"))
    print(f" Salud({porcentaje(p_salud)}%)   : {formatear_pesos(r[SALUD])}")
    print(f" Pensión({porcentaje(p_pension)}%): {formatear_pesos(r[PENSION])}")
    print(f" ARL({porcentaje(p_arl)}%)       : {formatear_pesos(r[ARL])}")
    print(f" Total Deducciones: {formatear_pesos(r[SALUD] + r[PENSION] + r[ARL])}")
    print("-" * 60)
    print(f" TOTAL A PAGAR    : {formatear_pesos(r[TOTAL])}")
    print(linea + "\n")


def mostrar_tabla():
    if not registros:
        print("\n   >> No hay registros en memoria.")
        return
    encabezado = formatear_fila(ENCABEZADOS)
    print("\n" + encabezado)
    print("-" * len(encabezado))
    for i, fila in enumerate(registros, start=1):
        print(f"{i:>2}. " + formatear_fila(fila))


# ------------------------------ ARCHIVO TXT ------------------------------
def guardar_txt():
    """Sobrescribe el TXT con todos los registros actuales de la matriz."""
    with open(ARCHIVO_TXT, "w", encoding="utf-8") as archivo:
        archivo.write("REGISTROS DE NOMINA - TransCaribeCol\n")
        archivo.write(formatear_fila(ENCABEZADOS) + "\n")
        archivo.write("-" * 110 + "\n")
        for fila in registros:
            archivo.write(formatear_fila(fila) + "\n")
    print(f"   >> Archivo '{ARCHIVO_TXT.name}' actualizado.")


def cargar_txt():
    """Lee el TXT al iniciar el programa para no perder los datos."""
    if not ARCHIVO_TXT.exists():
        return []
    lista_recuperada = []
    with open(ARCHIVO_TXT, "r", encoding="utf-8") as archivo:
        lineas = archivo.read().splitlines()
    
    # Saltamos las 3 primeras líneas (título, encabezados y guiones)
    for linea in lineas[3:]:
        if not linea.strip(): continue
        celdas = [c.strip() for c in linea.split("|")]
        try:
            if len(celdas) == 11:
                # Los primeros 3 son texto, el resto enteros
                fila = celdas[:3] + [int(c) for c in celdas[3:]]
                lista_recuperada.append(fila)
        except ValueError:
            continue
    return lista_recuperada


def ver_txt():
    print(f"\n--- CONTENIDO DE {ARCHIVO_TXT.name} ---")
    if not ARCHIVO_TXT.exists():
        print("   >> El archivo aún no se ha creado.")
        return
    with open(ARCHIVO_TXT, "r", encoding="utf-8") as archivo:
        print(archivo.read())


# ------------------------------ MENU PRINCIPAL ------------------------------
def main():
    global registros
    registros = cargar_txt()
    if registros:
        print(f"\n   >> Se recuperaron {len(registros)} registro(s) del archivo TXT.")

    while True:
        print("\n=========== MENU PRINCIPAL ===========")
        print("1. Registrar trabajador ADMINISTRATIVO")
        print("2. Registrar trabajador OPERATIVO")
        print("3. Ver tabla de registros")
        print("4. Ver volante de pago (por número)")
        print("5. Leer archivo TXT")
        print("0. Salir")
        print("======================================")
        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            print("\n--- REGISTRO ADMINISTRATIVO ---")
            nombre = leer_texto("Nombre completo: ")
            cargo = leer_texto("Cargo (Ej. Auxiliar): ")
            horas = leer_entero("Horas trabajadas: ", 1, 744)
            extra = leer_entero("Horas extra (0 si no aplica): ", 0)
            
            fila = calcular_administrativo(nombre, cargo, horas, extra)
            registros.append(fila)
            guardar_txt()
            mostrar_volante(fila)

        elif opcion == "2":
            print("\n--- REGISTRO OPERATIVO ---")
            nombre = leer_texto("Nombre completo: ")
            print("Cargos disponibles:")
            for i, c in enumerate(CARGOS_OPERATIVOS, start=1):
                print(f"  {i}. {c} ({CARGOS_OPERATIVOS[c]['horas']} h)")
            
            op = leer_entero("Seleccione cargo: ", 1, 3)
            cargo = list(CARGOS_OPERATIVOS)[op - 1]
            
            fila = calcular_operativo(nombre, cargo)
            registros.append(fila)
            guardar_txt()
            mostrar_volante(fila)

        elif opcion == "3":
            mostrar_tabla()

        elif opcion == "4":
            if not registros:
                print("\n   >> No hay registros.")
                continue
            mostrar_tabla()
            num = leer_entero("\nNúmero de trabajador para ver volante: ", 1, len(registros))
            mostrar_volante(registros[num - 1])

        elif opcion == "5":
            ver_txt()

        elif opcion == "0":
            print("\n   >> Saliendo del programa...")
            break
        else:
            print("   >> Opción inválida.")


if __name__ == "__main__":
    main()