import re

class CodeParser:
    def __init__(self, file_name):
        self.file_name = file_name

    def parse_file(self):
        try:
            with open(self.file_name, 'r') as file:
                lines = file.readlines()

            for line_num, line in enumerate(lines, start=1):
                line = line.strip()
                if not line or line.startswith('#'):  # Ignorar líneas vacías o comentarios
                    continue
                self.parse_line(line, line_num)
        except FileNotFoundError:
            print(f"Error: El archivo '{self.file_name}' no existe.")
        except Exception as e:
            print(f"Error inesperado: {e}")

    def parse_line(self, line, line_num):
        if line.startswith('global'):
            self.parse_global(line, line_num)
        elif line.startswith('procedure'):
            self.parse_procedure(line, line_num)
        elif line == 'begin':
            print(f"Línea {line_num}: Inicio de bloque.")
        elif line == 'end.' or line == 'end':
            print(f"Línea {line_num}: Fin de bloque.")
        elif ':=' in line:
            self.parse_assignment(line, line_num)
        elif line.startswith('while'):
            self.parse_loop(line, line_num)
        elif re.match(r'[a-zA-Z0-9_]+\(.+\)', line):
            self.parse_function_call(line, line_num)
        else:
            print(f"Advertencia: Línea desconocida en la línea {line_num}: {line}")

    def parse_global(self, line, line_num):
        match = re.match(r'global\s+([a-zA-Z0-9_,\s]+)\.', line)
        if not match:
            print(f"Error: Declaración 'global' inválida en la línea {line_num}: {line}")
        else:
            vars_declared = match.group(1).split(',')
            vars_declared = [var.strip() for var in vars_declared]
            print(f"Línea {line_num}: Variables globales declaradas: {vars_declared}")

    def parse_procedure(self, line, line_num):
        match = re.match(r'procedure\s+([a-zA-Z0-9_]+)\s*(\((.*?)\))?', line)
        if not match:
            print(f"Error: Declaración de procedimiento inválida en la línea {line_num}: {line}")
        else:
            proc_name = match.group(1)
            parameters = match.group(3)
            if parameters:
                param_list = [param.strip() for param in parameters.split(',')]
            else:
                param_list = []
            print(f"Línea {line_num}: Procedimiento '{proc_name}' definido con parámetros: {param_list}")

    def parse_assignment(self, line, line_num):
        match = re.match(r'([a-zA-Z0-9_]+)\s*:=\s*(.+)\.', line)
        if not match:
            print(f"Error: Asignación inválida en la línea {line_num}: {line}")
        else:
            var_name = match.group(1)
            value = match.group(2)
            print(f"Línea {line_num}: Asignación '{var_name} := {value}'")

    def parse_loop(self, line, line_num):
        match = re.match(r'while\s+(.+)\s+do', line)
        if not match:
            print(f"Error: Instrucción 'while' inválida en la línea {line_num}: {line}")
        else:
            condition = match.group(1)
            print(f"Línea {line_num}: Bucle 'while' con condición: {condition}")

    def parse_function_call(self, line, line_num):
        match = re.match(r'([a-zA-Z0-9_]+)\((.*?)\)', line)
        if not match:
            print(f"Error: Llamada a función inválida en la línea {line_num}: {line}")
        else:
            func_name = match.group(1)
            args = match.group(2).split(',')
            args = [arg.strip() for arg in args]
            print(f"Línea {line_num}: Llamada a función '{func_name}' con argumentos: {args}")


# Ejemplo de uso
if __name__ == "__main__":
    parser = CodeParser('entrada.txt')
    parser.parse_file()
