# Sisyph — Dokumentation

**Sisyph** ist eine imperative, zeilenorientierte Programmiersprache. Ein Programm ist eine Folge von Befehlszeilen, die von einem in Python geschriebenen Interpreter (`main.py`) Zeile für Zeile ausgeführt werden.

Das wesentliche Merkmal: Sisyph erfindet keine eigene Arithmetik oder Logik — jeder Ausdruck und jeder Variablenwert ist ein Python-Ausdruck. Die Sprache übernimmt die Struktur des Programms (Marken, Sprünge, Unterprogramme), während alle Berechnungen an den Python-Interpreter delegiert werden.

## Inhaltsverzeichnis

1. [Über die Sprache](#1-über-die-sprache)
2. [Programme ausführen](#2-programme-ausführen)
3. [Syntax](#3-syntax)
4. [Steuerbefehle](#4-steuerbefehle)
5. [Die Bibliothek stdlib](#5-die-bibliothek-stdlib)
6. [Die Bibliothek v](#6-die-bibliothek-v)
7. [Die Bibliothek file](#7-die-bibliothek-file)
8. [Die Bibliothek pylib](#8-die-bibliothek-pylib)
9. [Beispielprogramme](#9-beispielprogramme)
10. [Einschränkungen und Besonderheiten](#10-einschränkungen-und-besonderheiten)
11. [Fehlermeldungen](#11-fehlermeldungen)
12. [Ökosystem](#12-ökosystem)
13. [BSYHC — Der Compiler](#13-bsyhc--der-compiler)
14. [Sprachbibliotheken](#14-sprachbibliotheken)

## 1. Über die Sprache

| Eigenschaft | Wert |
|---|---|
| Name | Sisyph |
| Dateiendung | `.syh` |
| Paradigma | imperativ, zeilenorientiert |
| Interpreter | `main.py` (Python 3) |
| Ausdrücke | Python (`eval` / `exec`) |
| Typsystem | dynamisch (Python-Typen) |
| Gültigkeitsbereich | global (ein einziger Python-Namensraum) |

## 2. Programme ausführen

Ein Programm wird mit folgendem Befehl ausgeführt:

```
python3 main.py programm.syh
```

Beispiel:

```
python3 main.py a.syh
```

Wenn die Datei nicht gefunden wird, gibt der Interpreter eine Fehlermeldung aus und beendet sich.

Ein Programm kann auch über den BSYHC-Compiler im Interpretationsmodus gestartet werden (siehe [Abschnitt 13](#13-bsyhc--der-compiler)):

```
python3 bsyhc.py -i programm.syh
```

## 3. Syntax

Ein Programm besteht aus Zeilen. Jede Zeile enthält genau einen Befehl. Leere Zeilen werden ignoriert.

### Befehlstrenner

Mehrere Befehle können in einer Zeile durch Semikolons getrennt werden:

```
goto check; goto back
```

### Marken

Eine Marke ist der Name einer Zeile, zu der man springen kann. Eine Marke beginnt mit dem Zeichen `@` und belegt eine eigene Zeile:

```
@main
stdlib.stdout "Hallo!"
```

Zeilen mit Marken werden bei der Ausführung übersprungen.

### Kommentare

Die Sprache hat keine eigene Kommentarsyntax. Da Ausdrücke von Python verarbeitet werden, kann innerhalb von Ausdrücken das Python-Kommentarzeichen `#` verwendet werden.

### Groß-/Kleinschreibung

Befehle unterscheiden Groß- und Kleinschreibung: `goto` ist ein Befehl, `GOTO` nicht.

### Variablen

Variablen werden implizit durch die Befehle `v.*`, `stdlib.stdin`, `file.*` und `pylib.*` erzeugt. Eine explizite Deklaration ist nicht nötig. Variablennamen sind gewöhnliche Python-Namen.

## 4. Steuerbefehle

### include

Lädt eine Bibliotheksdatei oder eine eingebaute Bibliothek:

```
include name
```

Wenn die Datei `name.syh` existiert, werden ihre Zeilen an das Ende des aktuellen Programms angehängt und die Marken der Datei sind mit dem Präfix `name.markierung` verfügbar:

```
include lib
goto lib.start
```

Wenn die Datei nicht existiert, gilt `name` als eingebaute Bibliothek. Eingebaute Bibliotheken: `stdlib`, `v`, `file`, `pylib`.

### goto

Unbedingter Sprung zu einer Marke:

```
goto markierung
```

Die Sprungposition wird auf dem Aufrufstapel gespeichert, sodass man später zurückkehren kann.

### goto back

Rückkehr aus einem Unterprogramm:

```
goto back
```

Holt die Position des letzten Sprungs vom Aufrufstapel und setzt die Ausführung dort fort. Ist der Stapel leer, wird eine Fehlermeldung ausgegeben.

Beispiel für ein Unterprogramm:

```
@main
goto work
exit 0

@work
stdlib.stdout "arbeite..."
goto back
```

### exit

Beendet das Programm:

```
exit
exit 0
exit 5
```

- `exit` / `exit 0` — erfolgreiche Beendigung, gibt `The program has completed successfully.` aus
- `exit <code>` — Beendigung mit einem Code, gibt `The program terminated with code "<code>".` aus

### if

Bedingte Ausführung in einer Zeile:

```
if <ausdruck> then <befehl>
```

Wenn der Ausdruck wahr ist (wird in Python zu `bool` konvertiert), wird der Befehl nach `then` ausgeführt. Ein `else` gibt es nicht.

Beispiel:

```
if x > 10 then goto big
if x <= 10 then goto small
```

## 5. Die Bibliothek stdlib

Für die Verwendung: `include stdlib` hinzufügen.

### stdlib.stdout

Gibt den Wert eines Ausdrucks aus:

```
stdlib.stdout <ausdruck>
```

Der Ausdruck wird von Python ausgewertet; f-Strings werden unterstützt:

```
stdlib.stdout f"Wert: {x}"
```

### stdlib.stdin

Liest eine Zeichenkette von der Tastatur:

```
stdlib.stdin <variable> <aufforderung>
```

Das Ergebnis wird in der Variable gespeichert. Die Aufforderung kann eine Zeichenkette oder ein Ausdruck sein:

```
stdlib.stdin name "Wie heißt du? "
```

Lesen ohne Speichern:

```
stdlib.stdin <aufforderung>
```

## 6. Die Bibliothek v

Für die Verwendung: `include v` hinzufügen.

Die Bibliothek konvertiert den Wert eines Ausdrucks in den angegebenen Typ und speichert ihn in einer Variable:

| Befehl | Typ |
|---|---|
| `v.int` | Ganzzahl (`int`) |
| `v.str` | Zeichenkette (`str`) |
| `v.float` | Gleitkommazahl (`float`) |
| `v.bool` | Wahrheitswert (`bool`) |
| `v.list` | Liste (`list`) |

Syntax:

```
v.int x "42"
v.list l [1, 2, 3]
v.str s l[0]
```

## 7. Die Bibliothek file

Für die Verwendung: `include file` hinzufügen.

| Befehl | Zweck |
|---|---|
| `file.read <variable> <pfad>` | liest die gesamte Datei in eine Variable |
| `file.write <pfad> <ausdruck>` | schreibt den Ausdruck in eine Datei (überschreibt) |
| `file.append <pfad> <ausdruck>` | hängt den Ausdruck an das Ende einer Datei an |
| `file.delete <pfad>` | löscht eine Datei |
| `file.exists <variable> <pfad>` | speichert `True`/`False` darüber, ob die Datei existiert |
| `file.lines <variable> <pfad>` | speichert die Liste der Zeilen der Datei |

Beispiel:

```
file.write "data.txt" f"Zeile: {x}\n"
file.read content "data.txt"
file.exists ok "data.txt"
```

Wenn eine Datei nicht gelesen oder gelöscht werden kann, wird `Sisyph File Error` mit dem Text der Ausnahme ausgegeben und die Variable erhält einen Standardwert (`""` oder `[]`).

## 8. Die Bibliothek pylib

Für die Verwendung: `include pylib` hinzufügen.

Die Bibliothek gewährt direkten Zugriff auf Python.

| Befehl | Zweck |
|---|---|
| `pylib.exec <code>` | führt beliebigen Python-Code aus |
| `pylib.eval <variable> <ausdruck>` | wertet einen Ausdruck aus und speichert das Ergebnis |
| `pylib.import <modul>` | importiert ein Python-Modul |
| `pylib.importas <modul> <alias>` | importiert ein Modul mit einem Alias |
| `pylib.from <code>` | führt `from <code>` aus |
| `pylib.get <variable> <python-variable>` | kopiert den Wert einer Python-Variable |
| `pylib.set <python-variable> <ausdruck>` | weist einer Python-Variable einen Wert zu |
| `pylib.print <ausdruck>` | wertet einen Ausdruck aus und gibt das Ergebnis aus |

Beispiel:

```
pylib.importas math m
pylib.set x m.sqrt(16)
pylib.print x
```

## 9. Beispielprogramme

### Beispiel 1. Listen und Typkonvertierung (`a.syh`)

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

Ausgabe:

```
po
14
17.3
True
["object"]
object
```

### Beispiel 2. Eingabe, Sprünge und Unterprogramme (`b.syh`)

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

Das Programm fragt eine Zeichenkette ab, vergleicht sie mit dem Wort «НИЧЕГО» und gibt das Ergebnis aus. Die Unterprogramme `@true` und `@false` kehren über `goto back` zurück.

## 10. Einschränkungen und Besonderheiten

- **Keine Schleifen.** Wiederholungen werden ausschließlich über `goto` organisiert.
- **Keine Funktionen.** Marken mit `goto` / `goto back` dienen als Unterprogramme.
- **Keine lokalen Variablen.** Alles lebt im globalen Python-Namensraum.
- **Kein `else`.** Verzweigungen sind nur mit `if ... then` möglich.
- **`if` in einer Zeile.** Der Befehl nach `then` ist ein einzelner, kann aber `;` enthalten.
- **Parsen nach Leerzeichen und Punkten.** Argumente mit Leerzeichen (zum Beispiel Dateipfade) werden unsicher geparst: `file.write "my file.txt" x` funktioniert nicht.
- **Gemeinsamer Aufrufstapel.** Rekursive Sprünge sind erlaubt, aber nicht begrenzt.
- **Ausdrücke sind Python.** Jeder Fehler in einem Ausdruck ist ein Python-Fehler, kein Sisyph-Fehler.
- **`include` fügt Code ein.** Die eingebundene Datei wird an das aktuelle Programm angehängt und beim Erreichen ausgeführt.

## 11. Fehlermeldungen

| Meldung | Situation |
|---|---|
| `Sisyph Error: File '<name>' not found.` | die Programmdatei wurde nicht gefunden |
| `Sisyph Error: Unknown label '<markierung>'` | Sprung zu einer nicht existierenden Marke |
| `Sisyph Error: Call stack is empty, nowhere to return` | `goto back` bei leerem Stapel |
| `Sisyph File Error: <ausnahme>` | Fehler bei Dateioperationen |
| `Sisyph PyLib Error: <typ>: <meldung>` | Python-Fehler in der Bibliothek pylib |
| `The program has completed successfully.` | erfolgreiche Beendigung (`exit 0`) |
| `The program terminated with code "<code>"` | Beendigung mit einem Code |

## 12. Ökosystem

- **`.syh`-Dateien** — Programme und Bibliotheken.
- **`include`** — der Wiederverwendungsmechanismus: Marken fremder Dateien werden mit dem Präfix des Dateinamens aufgerufen (`name.markierung`).
- **Eingebaute Bibliotheken** — `stdlib` (Ein-/Ausgabe), `v` (Typen), `file` (Dateien), `pylib` (Python).
- **`pylib`** — der Erweiterungspunkt: beliebiger Python-Code ist aus Sisyph erreichbar, ohne den Interpreter zu ändern.
- **BSYHC** — der Compiler: `bsyhc.py` verpackt `.syh` in eine eigenständige `.py`, kann Dekompilieren und Mehrfachdatei-Builds (siehe [Abschnitt 13](#13-bsyhc--der-compiler)).
- **Sprachbibliotheken** — `mathlib`, `strlib`, `listlib`, `randlib`, `timelib`: Unterprogramme für Mathematik, Zeichenketten, Listen, Zufall und Zeit (siehe [Abschnitt 14](#14-sprachbibliotheken)).

## 13. BSYHC — Der Compiler

**BSYHC** (Base SisYpH Compiler, `bsyhc.py`) ist der Compiler der Sprache Sisyph. Er verpackt eine `.syh`-Datei in ein Array, in dem jede neue Zeile ein neues Element des Arrays ist, bettet eine Kopie des Interpreters in die Ausgabedatei ein und führt das Programm direkt aus dem Array aus. Die kompilierte `.py`-Datei ist eigenständig und benötigt kein `main.py` daneben.

### Arbeitsmodi

| Modus | Befehl |
|---|---|
| Kompilieren | `python3 bsyhc.py -i b.syh -c -o bsyhc-test-b.py` |
| In ELF kompilieren | `python3 bsyhc.py -i b.syh -c -elf -o b_bin` |
| In EXE kompilieren | `python3 bsyhc.py -i b.syh -c -exe -o b.exe` |
| Dekompilieren | `python3 bsyhc.py -i bsyhc-test-b.py -d -o b-de.syh` |
| Binärdatei dekompilieren | `python3 bsyhc.py -i b_bin -d -o b-de.syh` |
| Interpretieren | `python3 bsyhc.py -i b.syh` |

Wenn nur eine Eingabedatei angegeben wird (ohne `-c` und `-d`), interpretiert BSYHC das Programm einfach, genau wie `main.py`.

### Flags

| Flag | Zweck |
|---|---|
| `-i, --input <datei>` | Eingabedatei; kann wiederholt werden, um mehrere Dateien in eine Ausgabe zu kompilieren |
| `-o, --output <datei>` | Ausgabedatei (Standard: `<eingabe>.py` / `<eingabe>.syh`) |
| `-c, --compile` | `.syh` in eine eigenständige `.py` kompilieren |
| `-elf` | `.syh` über PyInstaller in eine ELF-Binärdatei kompilieren (Linux) |
| `-exe` | `.syh` über PyInstaller in eine EXE-Binärdatei kompilieren (Windows) |
| `-d, --decompile` | eine kompilierte `.py` (oder BSYHC-Binärdatei) zurück in `.syh` dekompilieren |
| `--merge concat \| include` | Art der Dateizusammenführung beim Kompilieren (Standard `concat`) |
| `--split` | beim Dekompilieren jede Quelldatei einzeln wiederherstellen (in das `-o`-Verzeichnis) |

### Mehrere Dateien kompilieren

`-i` kann wiederholt werden — alle Dateien werden in einer einzigen Ausgabe gesammelt:

```
python3 bsyhc.py -i main.syh -i lib.syh -c -o program.py
```

- `--merge concat` — die Zeilen der Dateien werden einfach der Reihe nach zusammengefügt.
- `--merge include` — die erste Datei ist der Einstiegspunkt, die übrigen werden wie bei `include` angehängt: ihre Marken erhalten das Präfix `datei.markierung` (zum Beispiel `goto lib.start`).

### In eine Binärdatei kompilieren (ELF / EXE)

BSYHC kann das Programm auch über PyInstaller (`--onefile`) in eine Binärdatei bauen:

```
python3 bsyhc.py -i b.syh -c -elf -o b_bin
python3 bsyhc.py -i b.syh -c -exe -o b.exe
```

- `-elf` — eine ELF-Binärdatei (Build unter Linux).
- `-exe` — eine EXE-Binärdatei (Build unter Windows).
- PyInstaller muss installiert sein (`pip install pyinstaller`); das Projekt kann seine eigene `env/`-Umgebung verwenden.
- Der Build läuft in einem temporären Verzeichnis: `build/`, `dist/`, `*.spec` und die Zwischen-`.py` werden automatisch entfernt — es bleibt nur die fertige Binärdatei übrig.
- PyInstaller kann nicht cross-kompilieren: unter Linux erzeugt `-exe` eine native Binärdatei mit dem Namen `*.exe`; eine echte Windows-EXE kann nur unter Windows gebaut werden.
- Eine von BSYHC gebaute Binärdatei kann zurück in `.syh` dekompiliert werden (siehe unten).

### Dekompilieren

Die kompilierte Datei lässt sich leicht dekompilieren — das Programm wird aus dem Array wiederhergestellt:

```
python3 bsyhc.py -i bsyhc-test-b.py -d -o b-de.syh
```

Standardmäßig entsteht eine einzige zusammengeführte `.syh`. Mit dem Flag `--split` wird jede Quelldatei einzeln in das über `-o` angegebene Verzeichnis wiederhergestellt.

Nicht nur `.py`-Dateien, sondern auch gebaute Binärdateien lassen sich dekompilieren — BSYHC stellt das Quell-Array aus dem in der Binärdatei eingebetteten Code wieder her:

```
python3 bsyhc.py -i b_bin -d -o b-de.syh
```

## 14. Sprachbibliotheken

Die Sprache wird mit Unterprogramm-Bibliotheken ausgeliefert — gewöhnliche `.syh`-Dateien, die mit `include` geladen und über `goto <bibliothek>.<unterprogramm>` aufgerufen werden. Die Dateien liegen im Verzeichnis `lib/` und werden ohne Pfad eingebunden.

### Konventionen

- Eine Datei wird mit `include <name>` geladen, ein Unterprogramm wird mit `goto <name>.<unterprogramm>` aufgerufen und kehrt mit `goto back` zurück.
- Ein Unterprogramm liest seine Eingabevariablen (jede Bibliothek hat ihr eigenes Präfix) und schreibt das Ergebnis in die Variable `<präfix>_result`.
- Daten werden über globale Variablen übergeben, daher müssen sie vor jedem Aufruf neu gesetzt werden.
- In Unterprogrammen gibt es keine Schleifen: jedes `goto` legt eine Position auf den Aufrufstapel, eine Schleife im Unterprogramm würde den Stapel also verschmutzen. Wiederholungen werden im Hauptprogramm organisiert.
- Der BSYHC-Compiler kann Bibliotheken direkt in die kompilierte Datei einbetten — siehe Abschnitt 13, Flag `--merge include`.

### Beispiel

```
include v
include stdlib
include mathlib

v.int ml_x 5
goto mathlib.factorial
stdlib.stdout f"5! = {ml_result}\n"
exit 0
```

### lib/mathlib.syh — Mathematik (Präfix `ml_`)

| Unterprogramm | Eingabe | Ausgabe | Beschreibung |
|---|---|---|---|
| `mathlib.abs` | `ml_x` | `ml_result` | Betrag |
| `mathlib.sign` | `ml_x` | `ml_result` | Vorzeichen: −1, 0 oder 1 |
| `mathlib.min2` | `ml_a`, `ml_b` | `ml_result` | die kleinere von zwei Zahlen |
| `mathlib.max2` | `ml_a`, `ml_b` | `ml_result` | die größere von zwei Zahlen |
| `mathlib.clamp` | `ml_x`, `ml_lo`, `ml_hi` | `ml_result` | Wert auf Grenzen begrenzt |
| `mathlib.pow` | `ml_a`, `ml_b` | `ml_result` | `a` hoch `b` |
| `mathlib.is_even` | `ml_x` | `ml_result` | ob die Zahl gerade ist |
| `mathlib.is_odd` | `ml_x` | `ml_result` | ob die Zahl ungerade ist |
| `mathlib.factorial` | `ml_x` | `ml_result` | Fakultät der Zahl |
| `mathlib.gcd` | `ml_a`, `ml_b` | `ml_result` | größter gemeinsamer Teiler |

### lib/strlib.syh — Zeichenketten (Präfix `sl_`)

| Unterprogramm | Eingabe | Ausgabe | Beschreibung |
|---|---|---|---|
| `strlib.upper` | `sl_text` | `sl_result` | Zeichenkette in Großbuchstaben |
| `strlib.lower` | `sl_text` | `sl_result` | Zeichenkette in Kleinbuchstaben |
| `strlib.capitalize` | `sl_text` | `sl_result` | Zeichenkette mit großem Anfangsbuchstaben |
| `strlib.length` | `sl_text` | `sl_result` | Länge der Zeichenkette |
| `strlib.strip` | `sl_text` | `sl_result` | ohne Randleerzeichen |
| `strlib.reverse` | `sl_text` | `sl_result` | umgekehrte Zeichenkette |
| `strlib.contains` | `sl_sub`, `sl_text` | `sl_result` | ob die Teilzeichenkette enthalten ist |
| `strlib.replace` | `sl_text`, `sl_old`, `sl_new` | `sl_result` | Teilzeichenkette ersetzen |
| `strlib.split` | `sl_text`, `sl_sep` | `sl_result` | in eine Liste zerlegen |
| `strlib.join` | `sl_list`, `sl_sep` | `sl_result` | Liste zu einer Zeichenkette verbinden |
| `strlib.is_digit` | `sl_text` | `sl_result` | nur aus Ziffern? |

### lib/listlib.syh — Listen (Präfix `ll_`)

| Unterprogramm | Eingabe | Ausgabe | Beschreibung |
|---|---|---|---|
| `listlib.length` | `ll_list` | `ll_result` | Anzahl der Elemente |
| `listlib.sum` | `ll_list` | `ll_result` | Summe der Elemente |
| `listlib.min` | `ll_list` | `ll_result` | kleinstes Element |
| `listlib.max` | `ll_list` | `ll_result` | größtes Element |
| `listlib.sort` | `ll_list` | `ll_result` | aufsteigend sortieren |
| `listlib.reverse` | `ll_list` | `ll_result` | Liste in umgekehrter Reihenfolge |
| `listlib.unique` | `ll_list` | `ll_result` | Liste ohne Duplikate |
| `listlib.contains` | `ll_item`, `ll_list` | `ll_result` | ob das Element enthalten ist |
| `listlib.append` | `ll_list`, `ll_item` | `ll_result` | Liste mit angehängtem Element |
| `listlib.range_n` | `ll_n` | `ll_result` | Zahlen von 0 bis `n-1` |

### lib/randlib.syh — Zufall (Präfix `rl_`)

| Unterprogramm | Eingabe | Ausgabe | Beschreibung |
|---|---|---|---|
| `randlib.randint` | `rl_a`, `rl_b` | `rl_result` | zufällige Ganzzahl in den Grenzen (inklusive) |
| `randlib.uniform` | `rl_a`, `rl_b` | `rl_result` | zufällige Gleitkommazahl |
| `randlib.choice` | `rl_list` | `rl_result` | zufälliges Element der Liste (als Zeichenkette) |
| `randlib.shuffle` | `rl_list` | `rl_result` | gemischte Kopie der Liste |

### lib/timelib.syh — Zeit (Präfix `tl_`)

| Unterprogramm | Eingabe | Ausgabe | Beschreibung |
|---|---|---|---|
| `timelib.now` | — | `tl_result` | aktueller Timestamp (Sekunden seit der Epoche) |
| `timelib.strftime` | `tl_fmt` | `tl_result` | aktuelle Zeit nach Format (z. B. `"%Y-%m-%d %H:%M:%S"`) |
| `timelib.sleep` | `tl_sec` | — | Ausführung für die angegebene Anzahl Sekunden pausieren |

---

© Sisyph Language. Die Dokumentation entspricht dem Interpreter `main.py` und dem Compiler `bsyhc.py`.