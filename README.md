# Actividad 3.4 – Módulo de Nómina | TransCaribeCol

Aplicación de **consola en Python** para registrar y procesar la nómina del personal de *Transportes del Gran Caribe Colombiano S.C.A. – TransCaribeCol*. Calcula salarios, horas extra y descuentos de ley, muestra el volante de pago en pantalla y guarda los registros en un archivo de texto `.txt`.

**Equipo:** _[nombres de los integrantes]_
**Programa de formación:** Técnica en Programación de Software

---

## 1. Objetivo

Permitir que la empresa registre trabajadores **administrativos** y **operativos**, calcule automáticamente lo que corresponde a cada uno y conserve los registros en memoria secundaria (archivo plano), para que luego la gerencia los cargue en un módulo de confirmación y pago.

## 2. Requisitos

- Python 3.6 o superior.
- No requiere librerías externas (solo usa `pathlib`, incluida en Python).

## 3. Archivos del proyecto

| Archivo | Descripción |
| --- | --- |
| `programa_nomina.py` | Código fuente completo de la aplicación. |
| `03_Registros_Nomina.txt` | Archivo generado y actualizado por el programa con los registros procesados. |
| `Analisis_y_diseño.pdf` | Descripción del problema, entradas/procesos/salidas, reglas, supuestos, algoritmo, variables y estructura de datos. |
| `Pruebas_y_evidencias.pdf` | Capturas de pantalla de las pruebas realizadas. |
| `README.md` | Este documento. |

## 4. Cómo ejecutar

1. Guarde `programa_nomina.py` en una carpeta.
2. Abra una terminal en esa carpeta.
3. Ejecute:

```bash
python programa_nomina.py
```

El archivo `03_Registros_Nomina.txt` se crea automáticamente en la misma carpeta del programa al registrar el primer trabajador. Si ya existe, el programa lo carga al iniciar para no perder los datos anteriores.

## 5. Uso del menú

```
=========== MENU PRINCIPAL ===========
1. Registrar trabajador ADMINISTRATIVO
2. Registrar trabajador OPERATIVO
3. Ver tabla de registros
4. Ver volante de pago (por número)
5. Leer archivo TXT
0. Salir
======================================
```

| Opción | Qué hace |
| --- | --- |
| **1** | Pide nombre, cargo, horas trabajadas (1–744) y horas extra (≥ 0). Calcula, guarda en el TXT y muestra el volante. |
| **2** | Pide nombre y permite elegir el cargo (Conductor, Oficios Generales o Vigilancia). Las horas son fijas según el cargo. Calcula, guarda y muestra el volante. |
| **3** | Muestra en tabla todos los registros que están en memoria. |
| **4** | Muestra la tabla y, según el número elegido, imprime el volante de ese trabajador. |
| **5** | Lee y muestra el contenido del archivo TXT. |
| **0** | Sale del programa. |

Las entradas se validan: no se aceptan campos vacíos, letras en lugar de números ni valores fuera de rango.

## 6. Reglas de negocio aplicadas

### Personal administrativo

| Concepto | Valor |
| --- | --- |
| Asignación por hora | $20.000 |
| Hora extra | $25.000 |
| ARL | Riesgo I – 0,522 % |
| Salud / Pensión | 0 % (**supuesto**, ver sección 7) |

### Personal operativo (contrato de prestación de servicios, sin horas extra)

Valor por hora: **$40.000**. Las horas mensuales y la ARL dependen del cargo:

| Cargo | Horas mensuales | Nivel de riesgo | ARL |
| --- | --- | --- | --- |
| Conductor | 160 | II | 1,044 % |
| Oficios Generales | 100 | I | 0,522 % |
| Vigilancia | 336 | IV | 4,350 % |

Los aportes se calculan sobre el **IBC (Índice de Base de Cotización) = 40 % del salario**:

- Salud: 12,5 % del IBC
- Pensión: 16 % del IBC
- ARL: según el cargo, sobre el IBC

### Fórmulas

**Administrativo**

```
Salario        = horas trabajadas × 20.000
TPHE           = horas extra × 25.000
Base           = Salario + TPHE
Salud, Pensión = Base × tasa (0 % por supuesto)
ARL            = Base × 0,522 %
Total a pagar  = Base − Salud − Pensión − ARL
```

**Operativo**

```
Salario        = horas del cargo × 40.000
IBC            = Salario × 40 %
Salud          = IBC × 12,5 %
Pensión        = IBC × 16 %
ARL            = IBC × tasa del cargo
Total a pagar  = Salario − Salud − Pensión − ARL
```

Los valores se redondean a pesos enteros.

## 7. Supuestos y puntos por confirmar

La guía no especifica todos los valores, por lo que se dejaron documentados:

1. **Salud y pensión del administrativo:** se asumieron en **0 %** porque la guía no detalla esas tasas para este tipo de contrato. Se pueden cambiar en las constantes `SALUD_ADMIN` y `PENSION_ADMIN` al inicio del programa.
2. **Total a pagar:** se calcula como `(Salario + Horas extra) − Salud − Pensión − ARL`.
3. **Prestaciones de ley del administrativo:** la guía las menciona, pero no indica cómo calcularlas; no están incluidas en el cálculo.

> Estos puntos deben confirmarse con la instructora. Si cambian, solo hay que modificar las constantes del programa.

## 8. Estructura de datos

Los registros se guardan en una **matriz (lista de listas)**. Cada fila es un trabajador con 11 columnas:

| Nombre | Tipo | Cargo | HT | Salario | HE | TPHE | Salud | Pensión | ARL | Total a pagar |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

- **HT:** horas trabajadas · **HE:** horas extra · **TPHE:** total pago horas extra.
- En los operativos, HE y TPHE siempre son 0.

## 9. Formato del archivo TXT

Texto plano con columnas separadas por `|`: una línea de título, una de encabezados, una de guiones y luego una línea por trabajador. Ejemplo real generado por el programa:

```
REGISTROS DE NOMINA - TransCaribeCol
Nombre               | Tipo            | Cargo              | HT    | Salario      | HE    | TPHE       | Salud      | Pension    | ARL      | Total a pagar
--------------------------------------------------------------------------------------------------------------
Milton Escamilla     | ADMINISTRATIVO  | Gerente            | 60    | 1200000      | 0     | 0          | 0          | 0          | 6264     | 1193736
Daniel Perez         | OPERATIVO       | Conductor          | 160   | 6400000      | 0     | 0          | 320000     | 409600     | 26726    | 5643674
Juan Solano          | OPERATIVO       | Oficios Generales  | 100   | 4000000      | 0     | 0          | 200000     | 256000     | 8352     | 3535648
Luis Alvarez         | OPERATIVO       | Vigilancia         | 336   | 13440000     | 0     | 0          | 672000     | 860160     | 233856   | 11673984
```

El programa vuelve a leer este archivo al iniciar y reconstruye la matriz. Las líneas con formato inválido se omiten.

## 10. Pruebas realizadas

Las capturas están en `Pruebas_y_evidencias.pdf`.

| # | Escenario | Datos ingresados | Resultado obtenido (total a pagar) |
| --- | --- | --- | --- |
| 1 | Administrativo | Milton Escamilla, Gerente, 60 h, 0 h extra | $1.193.736 (salario $1.200.000 − ARL $6.264) |
| 2 | Operativo – Conductor | Daniel Perez | $5.643.674 (IBC $2.560.000; salud $320.000; pensión $409.600; ARL $26.726) |
| 3 | Operativo – Oficios Generales | Juan Solano | $3.535.648 (salud $200.000; pensión $256.000; ARL $8.352) |
| 4 | Operativo – Vigilancia | Luis Alvarez | $11.673.984 (salud $672.000; pensión $860.160; ARL $233.856) |
| 5 | Ver tabla de registros (opción 3) | – | Muestra los 4 registros |
| 6 | Ver volante por número (opción 4) | Registro 1 | Reimprime el volante de Milton Escamilla |
| 7 | Generación y lectura del TXT (opción 5) | – | Contenido del archivo coincide con la tabla |
| 8 | Salida del programa (opción 0) | – | Cierra correctamente |

## 11. Funcionamiento general (resumen del algoritmo)

```
Inicio
  Cargar registros previos desde el TXT
  Mientras la opción sea distinta de 0:
    Mostrar menú
    1 → pedir datos administrativo, calcular, guardar en matriz y TXT, mostrar volante
    2 → pedir nombre y cargo, calcular con IBC, guardar en matriz y TXT, mostrar volante
    3 → mostrar tabla de registros
    4 → mostrar volante de un registro
    5 → leer archivo TXT
Fin
```

## 12. Posibles mejoras

- Agregar prestaciones de ley al personal administrativo una vez la instructora indique cómo calcularlas.
- Permitir editar o eliminar registros.
- Exportar un volante individual a archivo.
