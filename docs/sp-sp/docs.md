# Sisyph — Documentación

**Sisyph** es un lenguaje de programación imperativo y orientado a líneas. Un programa es una secuencia de líneas de comandos que ejecuta línea a línea un intérprete escrito en Python (`main.py`).

La característica clave: Sisyph no inventa su propia aritmética ni lógica — cada expresión y cada valor de variable es una expresión de Python. El lenguaje se encarga de la estructura del programa (etiquetas, saltos, subrutinas), mientras que todo el cálculo se delega al intérprete de Python.

## Índice

1. [Sobre el lenguaje](#1-sobre-el-lenguaje)
2. [Ejecución de programas](#2-ejecución-de-programas)
3. [Sintaxis](#3-sintaxis)
4. [Comandos de control](#4-comandos-de-control)
5. [La biblioteca stdlib](#5-la-biblioteca-stdlib)
6. [La biblioteca v](#6-la-biblioteca-v)
7. [La biblioteca file](#7-la-biblioteca-file)
8. [La biblioteca pylib](#8-la-biblioteca-pylib)
9. [Programas de ejemplo](#9-programas-de-ejemplo)
10. [Limitaciones y particularidades](#10-limitaciones-y-particularidades)
11. [Mensajes de error](#11-mensajes-de-error)
12. [Ecosistema](#12-ecosistema)
13. [BSYHC — El compilador](#13-bsyhc--el-compilador)
14. [Bibliotecas del lenguaje](#14-bibliotecas-del-lenguaje)

## 1. Sobre el lenguaje

| Propiedad | Valor |
|---|---|
| Nombre | Sisyph |
| Extensión de archivo | `.syh` |
| Paradigma | imperativo, orientado a líneas |
| Intérprete | `main.py` (Python 3) |
| Expresiones | Python (`eval` / `exec`) |
| Tipado | dinámico (tipos de Python) |
| Ámbito | global (un único espacio de nombres de Python) |

## 2. Ejecución de programas

Un programa se ejecuta con el comando:

```
python3 main.py programa.syh
```

Ejemplo:

```
python3 main.py a.syh
```

Si el archivo no existe, el intérprete imprime un mensaje de error y termina.

Un programa también se puede ejecutar a través del compilador BSYHC en modo de interpretación (véase [la sección 13](#13-bsyhc--el-compilador)):

```
python3 bsyhc.py -i programa.syh
```

## 3. Sintaxis

Un programa consta de líneas. Cada línea contiene un solo comando. Las líneas vacías se ignoran.

### Separador de comandos

Varios comandos pueden escribirse en una misma línea separados por punto y coma:

```
goto check; goto back
```

### Etiquetas

Una etiqueta es el nombre de una línea a la que se puede saltar. Una etiqueta empieza con el carácter `@` y ocupa su propia línea:

```
@main
stdlib.stdout "¡Hola!"
```

Las líneas que contienen etiquetas se omiten durante la ejecución.

### Comentarios

El lenguaje no tiene sintaxis propia de comentarios. Como las expresiones las procesa Python, dentro de las expresiones se puede usar el carácter de comentario `#` de Python.

### Sensibilidad a mayúsculas

Los comandos distinguen mayúsculas de minúsculas: `goto` es un comando, `GOTO` no lo es.

### Variables

Las variables se crean implícitamente con los comandos `v.*`, `stdlib.stdin`, `file.*` y `pylib.*`. No se necesita declaración explícita. Los nombres de variable son nombres ordinarios de Python.

## 4. Comandos de control

### include

Carga un archivo de biblioteca o una biblioteca incorporada:

```
include nombre
```

Si el archivo `nombre.syh` existe, sus líneas se añaden al final del programa actual y las etiquetas del archivo quedan disponibles con el prefijo `nombre.etiqueta`:

```
include lib
goto lib.start
```

Si el archivo no existe, `nombre` se considera una biblioteca incorporada. Bibliotecas incorporadas: `stdlib`, `v`, `file`, `pylib`.

### goto

Salto incondicional a una etiqueta:

```
goto etiqueta
```

La posición del salto se guarda en la pila de llamadas, por lo que se puede volver a ella más tarde.

### goto back

Retorno de una subrutina:

```
goto back
```

Saca de la pila de llamadas la posición del último salto y reanuda la ejecución desde allí. Si la pila está vacía, se imprime un mensaje de error.

Ejemplo de subrutina:

```
@main
goto work
exit 0

@work
stdlib.stdout "trabajando..."
goto back
```

### exit

Termina el programa:

```
exit
exit 0
exit 5
```

- `exit` / `exit 0` — terminación exitosa, imprime `The program has completed successfully.`
- `exit <código>` — terminación con un código, imprime `The program terminated with code "<código>".`

### if

Ejecución condicional en una sola línea:

```
if <expresión> then <comando>
```

Si la expresión es verdadera (se convierte a `bool` en Python), se ejecuta el comando después de `then`. No existe `else`.

Ejemplo:

```
if x > 10 then goto big
if x <= 10 then goto small
```

## 5. La biblioteca stdlib

Añada `include stdlib` para usarla.

### stdlib.stdout

Imprime el valor de una expresión:

```
stdlib.stdout <expresión>
```

La expresión la evalúa Python; se admiten f-strings:

```
stdlib.stdout f"Valor: {x}"
```

### stdlib.stdin

Lee una cadena del teclado:

```
stdlib.stdin <variable> <indicador>
```

El resultado se guarda en la variable. El indicador puede ser una cadena o una expresión:

```
stdlib.stdin name "¿Cómo te llamas? "
```

Lectura sin guardar:

```
stdlib.stdin <indicador>
```

## 6. La biblioteca v

Añada `include v` para usarla.

La biblioteca convierte el valor de una expresión al tipo indicado y lo guarda en una variable:

| Comando | Tipo |
|---|---|
| `v.int` | entero (`int`) |
| `v.str` | cadena (`str`) |
| `v.float` | número de coma flotante (`float`) |
| `v.bool` | valor booleano (`bool`) |
| `v.list` | lista (`list`) |

Sintaxis:

```
v.int x "42"
v.list l [1, 2, 3]
v.str s l[0]
```

## 7. La biblioteca file

Añada `include file` para usarla.

| Comando | Función |
|---|---|
| `file.read <variable> <ruta>` | lee el archivo completo en una variable |
| `file.write <ruta> <expresión>` | escribe la expresión en un archivo (sobrescribe) |
| `file.append <ruta> <expresión>` | añade la expresión al final de un archivo |
| `file.delete <ruta>` | elimina un archivo |
| `file.exists <variable> <ruta>` | guarda `True`/`False` sobre si el archivo existe |
| `file.lines <variable> <ruta>` | guarda la lista de líneas del archivo |

Ejemplo:

```
file.write "data.txt" f"línea: {x}\n"
file.read content "data.txt"
file.exists ok "data.txt"
```

Si un archivo no se puede leer ni eliminar, se imprime `Sisyph File Error` con el texto de la excepción y la variable recibe un valor por defecto (`""` o `[]`).

## 8. La biblioteca pylib

Añada `include pylib` para usarla.

La biblioteca da acceso directo a Python.

| Comando | Función |
|---|---|
| `pylib.exec <código>` | ejecuta código Python arbitrario |
| `pylib.eval <variable> <expresión>` | evalúa una expresión y guarda el resultado |
| `pylib.import <módulo>` | importa un módulo de Python |
| `pylib.importas <módulo> <alias>` | importa un módulo con un alias |
| `pylib.from <código>` | ejecuta `from <código>` |
| `pylib.get <variable> <variable de Python>` | copia el valor de una variable de Python |
| `pylib.set <variable de Python> <expresión>` | asigna un valor a una variable de Python |
| `pylib.print <expresión>` | evalúa una expresión e imprime el resultado |

Ejemplo:

```
pylib.importas math m
pylib.set x m.sqrt(16)
pylib.print x
```

## 9. Programas de ejemplo

### Ejemplo 1. Listas y conversión de tipos (`a.syh`)

```
include v
include stdlib

v.list l ["po", 14, 17.3, True, ["object"]]
v.str q l[0]
v.str w l[1]
v.str e l[2]
v.str r l[3]
v.str t l[4]
v.str u l[4][0]
stdlib.stdout f"{q}\n{w}\n{e}\n{r}\n{t}\n{u}\n"
exit 0
```

Salida:

```
po
14
17.3
True
["object"]
object
```

### Ejemplo 2. Entrada, saltos y subrutinas (`b.syh`)

```
include v
include stdlib

v.str false_o "Ты не угадал("
v.str true_o "Ты угадал!"

@main
stdlib.stdin sa "Введите строку: "
v.str object "НИЧЕГО"
goto check
exit 0

@check
if sa == object then goto true
if sa != object then goto false
goto back

@true
stdlib.stdout true_o
goto back

@false
stdlib.stdout false_o, "\n"
goto main
```

El programa pide una cadena, la compara con la palabra «НИЧЕГО» e imprime el resultado. Las subrutinas `@true` y `@false` regresan mediante `goto back`.

## 10. Limitaciones y particularidades

- **Sin bucles.** La repetición se organiza únicamente con `goto`.
- **Sin funciones.** Las etiquetas con `goto` / `goto back` actúan como subrutinas.
- **Sin variables locales.** Todo vive en el espacio de nombres global de Python.
- **Sin `else`.** La ramificación solo es posible con `if ... then`.
- **`if` de una sola línea.** El comando después de `then` es uno solo, aunque puede contener `;`.
- **Análisis por espacios y puntos.** Los argumentos que contienen espacios (por ejemplo, rutas de archivos) se analizan de forma insegura: `file.write "my file.txt" x` no funcionará.
- **Pila de llamadas compartida.** Los saltos recursivos están permitidos, pero no limitados.
- **Las expresiones son Python.** Cualquier error en una expresión es un error de Python, no de Sisyph.
- **`include` inserta código.** El archivo incluido se añade al programa actual y se ejecuta al alcanzarse.

## 11. Mensajes de error

| Mensaje | Situación |
|---|---|
| `Sisyph Error: File '<nombre>' not found.` | no se encontró el archivo del programa |
| `Sisyph Error: Unknown label '<etiqueta>'` | salto a una etiqueta inexistente |
| `Sisyph Error: Call stack is empty, nowhere to return` | `goto back` con la pila vacía |
| `Sisyph File Error: <excepción>` | error en una operación con archivos |
| `Sisyph PyLib Error: <tipo>: <mensaje>` | error de Python en la biblioteca pylib |
| `The program has completed successfully.` | terminación exitosa (`exit 0`) |
| `The program terminated with code "<código>"` | terminación con un código |

## 12. Ecosistema

- **Archivos `.syh`** — programas y bibliotecas.
- **`include`** — el mecanismo de reutilización: las etiquetas de otros archivos se llaman con el prefijo del nombre del archivo (`nombre.etiqueta`).
- **Bibliotecas incorporadas** — `stdlib` (entrada/salida), `v` (tipos), `file` (archivos), `pylib` (Python).
- **`pylib`** — el punto de extensión: cualquier código de Python es alcanzable desde Sisyph sin modificar el intérprete.
- **BSYHC** — el compilador: `bsyhc.py` empaqueta `.syh` en un `.py` autónomo, permite descompilar y la compilación de varios archivos (véase [la sección 13](#13-bsyhc--el-compilador)).
- **Bibliotecas del lenguaje** — `mathlib`, `strlib`, `listlib`, `randlib`, `timelib`: subrutinas para matemáticas, cadenas, listas, aleatoriedad y tiempo (véase [la sección 14](#14-bibliotecas-del-lenguaje)).

## 13. BSYHC — El compilador

**BSYHC** (Base SisYpH Compiler, `bsyhc.py`) es el compilador del lenguaje Sisyph. Empaqueta un archivo `.syh` en un array en el que cada nueva línea es un nuevo elemento del array, incrusta una copia del intérprete en el archivo de salida y ejecuta el programa directamente desde el array. El archivo `.py` compilado es autónomo y no requiere `main.py` junto a él.

### Modos de trabajo

| Modo | Comando |
|---|---|
| Compilar | `python3 bsyhc.py -i b.syh -c -o bsyhc-test-b.py` |
| Descompilar | `python3 bsyhc.py -i bsyhc-test-b.py -d -o b-de.syh` |
| Interpretar | `python3 bsyhc.py -i b.syh` |

Si solo se indica un archivo de entrada (sin `-c` ni `-d`), BSYHC simplemente interpreta el programa, igual que `main.py`.

### Banderas

| Bandera | Función |
|---|---|
| `-i, --input <archivo>` | archivo de entrada; puede repetirse para compilar varios archivos en una sola salida |
| `-o, --output <archivo>` | archivo de salida (por defecto: `<entrada>.py` / `<entrada>.syh`) |
| `-c, --compile` | compilar `.syh` en un `.py` autónomo |
| `-d, --decompile` | descompilar un `.py` compilado de vuelta a `.syh` |
| `--merge concat \| include` | forma de fusionar archivos al compilar (por defecto `concat`) |
| `--split` | al descompilar, restaurar cada archivo fuente por separado (en el directorio de `-o`) |

### Compilar varios archivos

`-i` puede repetirse: todos los archivos se reúnen en una única salida:

```
python3 bsyhc.py -i main.syh -i lib.syh -c -o program.py
```

- `--merge concat` — las líneas de los archivos simplemente se unen en orden.
- `--merge include` — el primer archivo es el punto de entrada; los demás se añaden como con `include`: sus etiquetas reciben el prefijo `archivo.etiqueta` (por ejemplo, `goto lib.start`).

### Descompilación

El archivo compilado es fácil de descompilar: el programa se restaura a partir del array:

```
python3 bsyhc.py -i bsyhc-test-b.py -d -o b-de.syh
```

Por defecto se produce un único `.syh` fusionado. Con la bandera `--split`, cada archivo fuente se restaura por separado en el directorio indicado con `-o`.

## 14. Bibliotecas del lenguaje

El lenguaje incluye bibliotecas de subrutinas — archivos `.syh` ordinarios que se cargan con `include` y se invocan mediante `goto <biblioteca>.<subrutina>`. Los archivos se encuentran en el directorio `lib/` y se incluyen sin ruta.

### Convenciones

- Un archivo se carga con `include <nombre>`, una subrutina se invoca con `goto <nombre>.<subrutina>` y regresa con `goto back`.
- Una subrutina lee sus variables de entrada (cada biblioteca tiene su propio prefijo) y escribe el resultado en la variable `<prefijo>_result`.
- Los datos se pasan mediante variables globales, por lo que deben restablecerse antes de cada llamada.
- No hay bucles dentro de las subrutinas: cada `goto` coloca una posición en la pila de llamadas, así que un bucle dentro de una subrutina ensuciaría la pila. La repetición se organiza en el código del programa principal.
- El compilador BSYHC puede incrustar bibliotecas directamente en el archivo compilado — véase la sección 13, la bandera `--merge include`.

### Ejemplo

```
include v
include stdlib
include mathlib

v.int ml_x 5
goto mathlib.factorial
stdlib.stdout f"5! = {ml_result}\n"
exit 0
```

### lib/mathlib.syh — matemáticas (prefijo `ml_`)

| Subrutina | Entrada | Salida | Descripción |
|---|---|---|---|
| `mathlib.abs` | `ml_x` | `ml_result` | valor absoluto |
| `mathlib.sign` | `ml_x` | `ml_result` | signo del número: −1, 0 o 1 |
| `mathlib.min2` | `ml_a`, `ml_b` | `ml_result` | el menor de dos números |
| `mathlib.max2` | `ml_a`, `ml_b` | `ml_result` | el mayor de dos números |
| `mathlib.clamp` | `ml_x`, `ml_lo`, `ml_hi` | `ml_result` | valor restringido a los límites |
| `mathlib.pow` | `ml_a`, `ml_b` | `ml_result` | `a` elevado a `b` |
| `mathlib.is_even` | `ml_x` | `ml_result` | si el número es par |
| `mathlib.is_odd` | `ml_x` | `ml_result` | si el número es impar |
| `mathlib.factorial` | `ml_x` | `ml_result` | factorial del número |
| `mathlib.gcd` | `ml_a`, `ml_b` | `ml_result` | máximo común divisor |

### lib/strlib.syh — cadenas (prefijo `sl_`)

| Subrutina | Entrada | Salida | Descripción |
|---|---|---|---|
| `strlib.upper` | `sl_text` | `sl_result` | cadena en mayúsculas |
| `strlib.lower` | `sl_text` | `sl_result` | cadena en minúsculas |
| `strlib.capitalize` | `sl_text` | `sl_result` | cadena con la primera letra en mayúscula |
| `strlib.length` | `sl_text` | `sl_result` | longitud de la cadena |
| `strlib.strip` | `sl_text` | `sl_result` | sin espacios en los extremos |
| `strlib.reverse` | `sl_text` | `sl_result` | cadena invertida |
| `strlib.contains` | `sl_sub`, `sl_text` | `sl_result` | si la subcadena está presente |
| `strlib.replace` | `sl_text`, `sl_old`, `sl_new` | `sl_result` | reemplazo de subcadena |
| `strlib.split` | `sl_text`, `sl_sep` | `sl_result` | dividir la cadena en una lista |
| `strlib.join` | `sl_list`, `sl_sep` | `sl_result` | unir una lista en una cadena |
| `strlib.is_digit` | `sl_text` | `sl_result` | si consta solo de dígitos |

### lib/listlib.syh — listas (prefijo `ll_`)

| Subrutina | Entrada | Salida | Descripción |
|---|---|---|---|
| `listlib.length` | `ll_list` | `ll_result` | número de elementos |
| `listlib.sum` | `ll_list` | `ll_result` | suma de elementos |
| `listlib.min` | `ll_list` | `ll_result` | elemento mínimo |
| `listlib.max` | `ll_list` | `ll_result` | elemento máximo |
| `listlib.sort` | `ll_list` | `ll_result` | ordenación ascendente |
| `listlib.reverse` | `ll_list` | `ll_result` | lista en orden inverso |
| `listlib.unique` | `ll_list` | `ll_result` | lista sin duplicados |
| `listlib.contains` | `ll_item`, `ll_list` | `ll_result` | si la lista contiene el elemento |
| `listlib.append` | `ll_list`, `ll_item` | `ll_result` | lista con el elemento añadido |
| `listlib.range_n` | `ll_n` | `ll_result` | números de 0 a `n-1` |

### lib/randlib.syh — aleatoriedad (prefijo `rl_`)

| Subrutina | Entrada | Salida | Descripción |
|---|---|---|---|
| `randlib.randint` | `rl_a`, `rl_b` | `rl_result` | entero aleatorio dentro de los límites (inclusive) |
| `randlib.uniform` | `rl_a`, `rl_b` | `rl_result` | número aleatorio de coma flotante |
| `randlib.choice` | `rl_list` | `rl_result` | elemento aleatorio de la lista (como cadena) |
| `randlib.shuffle` | `rl_list` | `rl_result` | copia mezclada de la lista |

### lib/timelib.syh — tiempo (prefijo `tl_`)

| Subrutina | Entrada | Salida | Descripción |
|---|---|---|---|
| `timelib.now` | — | `tl_result` | marca de tiempo actual (segundos desde la época) |
| `timelib.strftime` | `tl_fmt` | `tl_result` | hora actual según el formato (p. ej. `"%Y-%m-%d %H:%M:%S"`) |
| `timelib.sleep` | `tl_sec` | — | pausar la ejecución durante el número de segundos indicado |

---

© Sisyph Language. La documentación corresponde al intérprete `main.py` y al compilador `bsyhc.py`.