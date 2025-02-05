import os

def dibujar_circulo():
    circulo = [
        "   ***   ",
        " *     * ",
        "*       *",
        "*       *",
        " *     * ",
        "   ***   "
    ]
    for fila in circulo:
        print(fila)

def dibujar_cuadrado():
    cuadrado = [
        "*******",
        "*     *",
        "*     *",
        "*     *",
        "*******"
    ]
    for fila in cuadrado:
        print(fila)

def dibujar_triangulo():
    triangulo = [
        "    *    ",
        "   ***   ",
        "  *****  ",
        " ******* ",
        "*********"
    ]
    for fila in triangulo:
        print(fila)

def ejecutar_comando(archivo_ets):
    # Verificar si el archivo tiene la extensión .ets
    if not archivo_ets.endswith(".ets"):
        print("The filename does not include ETS extension")
        return
    
    # Verificar si el archivo existe
    if not os.path.exists(archivo_ets):
        print("The ETS file does not exist")
        return

    # Diccionario para almacenar variables
    variables = {}

    # Leer el archivo .ets
    with open(archivo_ets, 'r', encoding='utf-8') as archivo:
        lineas = archivo.readlines()

    # Procesar las líneas del archivo .ets
    for linea in lineas:
        linea = linea.strip()  # Eliminar espacios en blanco y saltos de línea

        if not linea:  # Ignorar líneas vacías
            continue

        # Detectar "ets info" para imprimir la información de ETS
        if "ets info" in linea:
            print("The meaning of ets is Easy Typing Script, Version: 1.0")

        # Procesar "info =" como un diccionario de variables
        elif "info =" in linea:
            info_line = linea.split("info =")[1].strip()
            # Dividir las palabras y asignarles valores
            palabras = info_line.split(";")
            for palabra in palabras:
                if ":" in palabra:
                    clave, valor = palabra.split(":")
                    clave = clave.strip()
                    valor = valor.strip()
                    variables[clave] = valor
                else:
                    clave = palabra.strip()
                    variables[clave] = None

        # Procesar "print =" para imprimir texto o variables con "v{}"
        elif "print =" in linea:
            texto = linea.split("print =")[1].strip()

            # Reemplazar las variables v{variable} por su valor
            for var in variables:
                texto = texto.replace(f"v{{{var}}}", str(variables[var]))

            # Reemplazar rutas r{ruta_archivo} por su valor real
            while 'r{' in texto and '}' in texto:
                inicio = texto.index('r{') + 2
                fin = texto.index('}', inicio)
                ruta = texto[inicio:fin]
                if os.path.exists(ruta):
                    texto = texto.replace(f"r{{{ruta}}}", ruta)
                else:
                    texto = texto.replace(f"r{{{ruta}}}", f"The file path {ruta} does not exist")
            
            print(texto)

        # Procesar operaciones matemáticas (ahora incluye resta)
        elif "operation(math)" in linea:
            operacion = linea.split("operation(math) =")[1].strip()
            try:
                resultado = eval(operacion)  # Evaluar la operación matemática
                print(f"The result of the operation {operacion} is: {resultado}")
            except Exception as e:
                print(f"Error in operation {operacion}: {e}")

        # Detectar operación de resta
        elif "operation(subtract)" in linea:
            operacion = linea.split("operation(subtract) =")[1].strip()
            try:
                resultado = eval(operacion)  # Evaluar la operación de resta
                print(f"The result of the subtraction {operacion} is: {resultado}")
            except Exception as e:
                print(f"Error in subtraction operation {operacion}: {e}")

        # Procesar el comando de dibujar un círculo
        elif "draw(shape)(circle)" in linea:
            print("Drawing circle:")
            dibujar_circulo()

        # Procesar el comando de dibujar un cuadrado
        elif "draw(shape)(square)" in linea:
            print("Drawing square:")
            dibujar_cuadrado()

        # Procesar el comando de dibujar un triángulo
        elif "draw(shape)(triangle)" in linea:
            print("Drawing triangle:")
            dibujar_triangulo()

        # Procesar asignaciones de variables
        elif "=" in linea and not "print =" in linea and not "operation(math)" in linea:
            variable, valor = linea.split("=")
            variable = variable.strip()
            valor = valor.strip()

            # Si el valor es un número, asignarlo
            if valor.isdigit():  # Si el valor es un número
                variables[variable] = int(valor)
            else:
                # Si no es un número, puede ser una operación matemática
                try:
                    variables[variable] = eval(valor)
                except Exception as e:
                    print(f"Error evaluating the assignment: {linea}. Error: {e}")

        # Procesar condicionales "if"
        elif "if" in linea:
            condicion = linea.split("if")[1].strip()
            # Evaluar la condición
            try:
                if eval(condicion):  # Si la condición es verdadera
                    print(f"The condition {condicion} is true")
                else:
                    print(f"The condition {condicion} is false")
            except Exception as e:
                print(f"Error evaluating condition {condicion}: {e}")

        # Procesar definiciones de funciones
        elif "function" in linea:
            funcion_definida = linea.split("function")[1].strip()
            nombre_funcion = funcion_definida.split("(")[0].strip()
            parametros = funcion_definida.split("(")[1].replace(")", "").strip()
            parametros = parametros.split(",") if parametros else []
            print(f"Function {nombre_funcion} defined with parameters {parametros}")

        # Procesar la ruta de archivo con "info = ruta"
        elif "info =" in linea and ":" not in linea:
            ruta_archivo = linea.split("info =")[1].strip()
            if os.path.exists(ruta_archivo):
                nombre_archivo = os.path.basename(ruta_archivo)
                print(f"The file at the specified path is: {nombre_archivo}")
            else:
                print(f"The file path {ruta_archivo} does not exist")

# Ejecución principal
if __name__ == "__main__":
    archivo_ets = input("Enter the .ets file name (with extension): ")
    ejecutar_comando(archivo_ets)
