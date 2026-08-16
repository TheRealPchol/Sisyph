import os
import sys
labels: dict = {}
debug: bool = False
libs: dict = {}
call_stack: list = []


def execute_line(line: str, lines: list, pc: list):
    if debug: print(f"DEBUG exec: '{line.strip()}'")
    line = line.strip()
    if not line:
        return

    if ';' in line:
        for sub in line.split(';'):
            execute_line(sub, lines, pc)
        return {'; parsed successfully.': True}

    args_sp: list = line.split(' ')
    args_dot: list = line.split('.')

    # --- INCLUDE ---
    if args_sp[0] == "include":
        filepath = f"{args_sp[1]}.syh"
        if not os.path.isfile(filepath):
            filepath = os.path.join("lib", filepath)
        if os.path.isfile(filepath):
            with open(filepath, 'r', encoding='utf-8') as ffi:
                ffi_lines = ffi.readlines()
            
            offset = len(lines)
            new_labels = collect_labels(ffi_lines)
            
            # Сохраняем с префиксом имени библиотеки
            lib_name = os.path.basename(args_sp[1])
            for name, pos in new_labels.items():
                labels[f"{lib_name}.{name}"] = pos + offset
            
            lines.extend(ffi_lines)
            return
        else:
            libs[os.path.basename(args_sp[1])] = True
            exec(f"{os.path.basename(args_sp[1])} = True", globals())
            return
    # --- GOTO ---
    if args_sp[0] == "goto":
        if len(args_sp) >= 2:
            target = args_sp[1]
            if target == "back":
                if call_stack:
                    pc[0] = call_stack.pop()
                    if debug: print(f"DEBUG goto back: pc_after={pc[0]}")
                else:
                    print("Sisyph Error: Call stack is empty, nowhere to return")
            elif target in labels:
                call_stack.append(pc[0])  # сохраняем куда вернёмся
                pc[0] = labels[target]
                if debug: print(f"DEBUG goto: pc_after={pc[0]}, stack_depth={len(call_stack)}")
            else:
                print(f"Sisyph Error: Unknown label '{target}'")
        return
    # --- EXIT ---
    if args_sp[0] == "exit":
        exit_code: str = line.split('exit ', 1)[1].strip() if 'exit ' in line else ''
        if exit_code in ('0', 'True', ''):
            print('The program has completed successfully.')
        else:
            print(f'The program terminated with code "{exit_code}"')
        pc[0] = len(lines)
        return
    # --- STDLIB ---
    if libs.get("stdlib"):
        if args_dot[0] == "stdlib":
            method = args_dot[1].split()[0]  # берём только имя метода без аргументов
            
            if method == "stdout":
                arg = line.split("stdlib.stdout ", 1)[1]
                exec(f"print({arg})", globals())
                
            elif method == "stdin":
                if len(args_sp) >= 3:
                    var_name = args_sp[1]
                    prompt_raw = line.split(f"stdlib.stdin {var_name} ", 1)[1].strip()
                    try:
                        prompt_val = eval(prompt_raw, globals())
                    except Exception:
                        prompt_val = prompt_raw
                    globals()[var_name] = input(prompt_val)
                else:
                    prompt_raw = line.split("stdlib.stdin ", 1)[1].strip()
                    try:
                        prompt_val = eval(prompt_raw, globals())
                    except Exception:
                        prompt_val = prompt_raw
                    input(prompt_val)
            return
    # --- V ---
    if libs.get("v") and args_dot[0] == "v":
        if debug: print(f"DEBUG v: libs={libs}, args_dot={args_dot}")  # ← временно
        method = args_dot[1].split()[0] if len(args_dot) > 1 else ""

        match method:
            case 'int':
                var_name = args_sp[1]
                value_expr = line.split(f"v.int {var_name} ", 1)[1]
                exec(f"{var_name} = int({value_expr})", globals())
            
            case 'str':
                var_name = args_sp[1]
                value_expr = line.split(f"v.str {var_name} ", 1)[1]
                exec(f"{var_name} = str({value_expr})", globals())
            
            case 'float':
                var_name = args_sp[1]
                value_expr = line.split(f"v.float {var_name} ", 1)[1]
                exec(f"{var_name} = float({value_expr})", globals())

            case 'bool':
                var_name = args_sp[1]
                value_expr = line.split(f"v.bool {var_name} ", 1)[1]
                exec(f"{var_name} = bool({value_expr})", globals())
            case 'list':
                var_name = args_sp[1]
                value_expr = line.split(f"v.list {var_name} ", 1)[1]
                exec(f"{var_name} = list({value_expr})", globals())
                if debug: print(f"DEBUG list: {var_name} = {globals()[var_name]}")  # ← временно
        return
    # --- IF ---
    if args_sp[0] == 'if':
        condition_raw = line.split("if ", 1)[1].split(" then ", 1)[0]
        then_cmd = line.split(" then ", 1)[1]
        
        exec(f"_sisyph_temp = bool({condition_raw})", globals())
        if globals()["_sisyph_temp"]:
            execute_line(then_cmd, lines, pc)
        return
    # --- FILE ---
    if libs.get("file") and args_dot[0] == "file":
        method = args_dot[1].split()[0] if len(args_dot) > 1 else ""
        
        match method:
            case 'read':
                var_name = args_sp[1]
                filepath = line.split(f"file.read {var_name} ", 1)[1].strip()
                try:
                    with open(filepath.strip('"').strip("'"), 'r', encoding='utf-8') as f:
                        globals()[var_name] = f.read()
                except Exception as e:
                    print(f"Sisyph File Error: {e}")
                    globals()[var_name] = ""
            
            case 'write':
                filepath = args_sp[1].strip('"').strip("'")
                content_expr = line.split(f"file.write {args_sp[1]} ", 1)[1]
                try:
                    content = eval(content_expr, globals())
                except Exception:
                    content = content_expr
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(str(content))
            
            case 'append':
                filepath = args_sp[1].strip('"').strip("'")
                content_expr = line.split(f"file.append {args_sp[1]} ", 1)[1]
                try:
                    content = eval(content_expr, globals())
                except Exception:
                    content = content_expr
                with open(filepath, 'a', encoding='utf-8') as f:
                    f.write(str(content))
            
            case 'delete':
                filepath = args_sp[1].strip('"').strip("'")
                try:
                    os.remove(filepath)
                except Exception as e:
                    print(f"Sisyph File Error: {e}")
            
            case 'exists':
                var_name = args_sp[1]
                filepath = args_sp[2].strip('"').strip("'")
                globals()[var_name] = os.path.isfile(filepath)
            
            case 'lines':
                var_name = args_sp[1]
                filepath = line.split(f"file.lines {var_name} ", 1)[1].strip()
                try:
                    with open(filepath.strip('"').strip("'"), 'r', encoding='utf-8') as f:
                        globals()[var_name] = f.readlines()
                except Exception as e:
                    print(f"Sisyph File Error: {e}")
                    globals()[var_name] = []
        return
    # --- PYLIB ---
    if libs.get("pylib") and args_dot[0] == "pylib":
        method = args_dot[1].split()[0] if len(args_dot) > 1 else ""
        
        match method:
            case 'exec':
                code = line.split("pylib.exec ", 1)[1]
                try:
                    exec(code, globals())
                except Exception as e:
                    print(f"Sisyph PyLib Error: {type(e).__name__}: {e}")
            
            case 'eval':
                var_name = args_sp[1]
                code = line.split(f"pylib.eval {var_name} ", 1)[1]
                try:
                    globals()[var_name] = eval(code, globals())
                except Exception as e:
                    print(f"Sisyph PyLib Error: {type(e).__name__}: {e}")
                    globals()[var_name] = None
            
            case 'import':
                module_name = args_sp[1]
                try:
                    exec(f"import {module_name}", globals())
                except Exception as e:
                    print(f"Sisyph PyLib Error: {type(e).__name__}: {e}")
            
            case 'importas':
                module_name = args_sp[1]
                alias = args_sp[2]
                try:
                    exec(f"import {module_name} as {alias}", globals())
                except Exception as e:
                    print(f"Sisyph PyLib Error: {type(e).__name__}: {e}")
            
            case 'from':
                code = line.split("pylib.from ", 1)[1]
                try:
                    exec(f"from {code}", globals())
                except Exception as e:
                    print(f"Sisyph PyLib Error: {type(e).__name__}: {e}")
            
            case 'get':
                var_name = args_sp[1]
                py_var = args_sp[2]
                try:
                    globals()[var_name] = globals()[py_var]
                except KeyError:
                    print(f"Sisyph PyLib Error: Variable '{py_var}' not found")
                    globals()[var_name] = None
            
            case 'set':
                py_var = args_sp[1]
                value_expr = line.split(f"pylib.set {py_var} ", 1)[1]
                try:
                    globals()[py_var] = eval(value_expr, globals())
                except Exception:
                    globals()[py_var] = value_expr
            
            case 'print':
                code = line.split("pylib.print ", 1)[1]
                try:
                    result = eval(code, globals())
                    print(result)
                except Exception as e:
                    print(f"Sisyph PyLib Error: {type(e).__name__}: {e}")
        return
def execute_lines(lines: list):
    # Проход 1: сбор всех меток
    labels.clear()
    call_stack.clear()
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith('@'):
            label_name = stripped.lstrip('@').strip().split()[0]
            labels[label_name] = i

    # Проход 2: выполнение с управляемым PC
    pc = [0]  # список чтобы менять из execute_line
    while pc[0] < len(lines):
        line = lines[pc[0]]
        pc[0] += 1  # сначала увеличиваем, потом выполняем

        if line.strip().startswith('@'):
            continue  # пропускаем строки-метки

        execute_line(line, lines, pc)
def execute_file(filename: str):
    if not os.path.isfile(filename):
        print(f"Sisyph Error: File '{filename}' not found.")
        return

    with open(filename, "r", encoding="utf-8") as fl:
        lines = fl.readlines()

    execute_lines(lines)
def collect_labels(lines: list) -> dict:
    labels = {}
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith('@'):
            label_name = stripped.lstrip('@').strip().split()[0]
            
            labels[label_name] = i
    return labels
if __name__ == "__main__":
    import traceback
    try:
        execute_file(sys.argv[1])
    except Exception as e:
        traceback.print_exc()