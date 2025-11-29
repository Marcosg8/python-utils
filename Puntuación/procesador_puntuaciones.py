import os  # para trabajar con rutas y listar archivos
import sys  # para leer los argumentos pasados al script
import re  # para detectar tiempo+genero pegados

# Esto es muy simple, como si fuera un niñ@ de 2º grado.
# Función que convierte una cadena de tiempo a segundos (float).
def convertir_tiempo(t):
    t = t.strip()  # quitar espacios al principio y final
    if not t:
        # si la cadena está vacía devolvemos 0.0 segundos
        return 0.0
    if ":" in t:
        # si contiene ":" la interpretamos como mm:ss o hh:mm:ss
        partes = t.split(":")
        partes = [float(x) for x in partes]  # convertir cada parte a float
        partes = list(reversed(partes))  # invertir para multiplicar por 1,60,3600...
        segundos = 0.0
        mul = 1.0
        for p in partes:
            segundos += p * mul  # sumar parte * multiplicador
            mul *= 60.0  # siguiente parte vale 60 veces más
        return segundos
    try:
        # si no tiene ":", intentamos convertir directamente a float (segundos)
        return float(t)
    except:
        # si falla devolvemos 0.0 (evitamos que se rompa el programa)
        return 0.0

# Función que lee el archivo de puntuaciones y devuelve una lista de registros.
def leer_puntuaciones(ruta):
    if not os.path.isfile(ruta):
        # si no existe el archivo lanzamos FileNotFoundError para que lo maneje el llamador
        raise FileNotFoundError(ruta)
    lista = []
    # abrimos el archivo en modo lectura con codificación utf-8
    with open(ruta, "r", encoding="utf-8") as f:
        lineas = f.readlines()  # leemos todas las líneas

    # recorremos línea por línea con su número (útil para mensajes)
    for i, linea in enumerate(lineas, start=1):
        linea = linea.strip()  # quitar espacios y salto de línea
        if not linea:
            continue  # saltar líneas vacías
        if linea.startswith("#") or linea.startswith("//"):
            continue  # saltar líneas comentario
        # suponemos formato: nombre,puntos,tiempo,genero
        partes = [p.strip() for p in linea.split(",")]

        # Si hay 3 campos y el tercero mezcla tiempo+genero (ej "02:02F"), separarlo
        if len(partes) == 3:
            m = re.match(r'^([0-9:.]+)\s*([A-Za-z])$', partes[2])
            if m:
                tiempo_s = m.group(1)
                genero = m.group(2)
                partes = [partes[0], partes[1], tiempo_s, genero]

        if len(partes) < 4:
            # si hay menos de 4 campos mostramos aviso y saltamos esa línea
            print(f"Línea {i} mal (menos de 4). Se salta.")
            continue
        nombre = partes[0]
        try:
            puntos = int(partes[1])  # intentamos convertir puntos a entero
        except:
            print(f"Línea {i} puntos no válidos. Se salta.")
            continue
        tiempo = convertir_tiempo(partes[2])  # convertir tiempo a segundos
        genero = partes[3]
        # añadimos un diccionario con los datos procesados a la lista
        lista.append({"nombre": nombre, "puntos": puntos, "tiempo": tiempo, "genero": genero})
    return lista  # devolvemos la lista de registros válidos

# Función que escribe la clasificación ordenada en un archivo.
def escribir_clasificacion(lista, ruta):
    # ordenar por puntos descendente y, si empatan, por tiempo ascendente
    orden = sorted(lista, key=lambda x: (-x["puntos"], x["tiempo"]))
    # abrimos el archivo de salida y escribimos cabecera y filas
    with open(ruta, "w", encoding="utf-8") as f:
        f.write("nombre,puntos,tiempo_s\n")
        for x in orden:
            f.write(f"{x['nombre']},{x['puntos']},{x['tiempo']:.2f}\n")

# Función que escribe estadísticas (total partidas, jugadores distintos, media puntos)
def escribir_estadisticas(lista, ruta):
    total = len(lista)  # total de partidas procesadas
    distintos = len(set(x["nombre"] for x in lista))  # jugadores distintos por nombre
    media = sum(x["puntos"] for x in lista) / total if total else 0.0  # media segura
    with open(ruta, "w", encoding="utf-8") as f:
        f.write(f"Total partidas: {total}\n")
        f.write(f"Total jugadores distintos: {distintos}\n")
        f.write(f"Media global de puntos: {media:.2f}\n")

# Función principal que decide qué archivo leer y llama a las funciones anteriores.
def main():
    carpeta = os.path.dirname(os.path.abspath(__file__))  # carpeta donde está el script

    # Si se pasó ruta por argumento la usamos primero
    if len(sys.argv) >= 2 and os.path.isfile(sys.argv[1]):
        ruta = sys.argv[1]
    else:
        # Preferencia por nombre en español "datos_jugadores.txt"
        preferido = os.path.join(carpeta, "datos_jugadores.txt")
        if os.path.isfile(preferido):
            ruta = preferido
        else:
            # Buscar cualquier archivo .txt válido en la carpeta (excluir salidas)
            txts = [f for f in sorted(os.listdir(carpeta)) if f.lower().endswith(".txt")]
            excluidos = {"clasificacion.txt", "estadisticas.txt", "datos_jugadores.txt"}
            script_name = os.path.basename(__file__).lower()
            candidato = None
            for t in txts:
                tl = t.lower()
                if tl in excluidos:
                    continue  # no queremos elegir los archivos que escribimos
                if tl == script_name:
                    continue  # evitar el propio script si tiene .txt por algún motivo
                candidato = os.path.join(carpeta, t)
                break
            if candidato:
                ruta = candidato
                print(f"Usando archivo .txt encontrado: {os.path.basename(ruta)} (se trata como datos_jugadores.txt)")
            else:
                # Fallbacks históricos si no se encontró nada
                archivo_es = os.path.join(carpeta, "datos_juego.txt")
                archivo_old = os.path.join(carpeta, "game_data.txt")
                if os.path.isfile(archivo_es):
                    ruta = archivo_es
                elif os.path.isfile(archivo_old):
                    ruta = archivo_old
                    print("Usando game_data.txt (renómbralo a datos_jugadores.txt si quieres).")
                else:
                    # si no hay ningún archivo, avisamos y salimos
                    print("No encuentro ningún archivo .txt válido en la carpeta.")
                    return

    try:
        lista = leer_puntuaciones(ruta)  # leer y procesar el archivo elegido
    except FileNotFoundError:
        print("Archivo no encontrado:", ruta)
        return

    if not lista:
        # si no hay registros válidos informamos y salimos
        print("No hay partidas válidas.")
        return

    # rutas de salida para clasificación y estadísticas
    ruta_clas = os.path.join(carpeta, "clasificacion.txt")
    ruta_est = os.path.join(carpeta, "estadisticas.txt")

    try:
        escribir_clasificacion(lista, ruta_clas)  # crear archivo de ranking
        escribir_estadisticas(lista, ruta_est)  # crear archivo de estadísticas
    except Exception as e:
        # si ocurre un error al escribir archivos lo mostramos
        print("Error escribiendo archivos:", e)
        return

    # mensajes finales para que el usuario sepa dónde están los archivos
    print("Hecho. Archivos creados:")
    print(" -", ruta_clas)
    print(" -", ruta_est)
    print("Lista procesada (orden original):")
    for x in lista:
        # mostramos la lista tal como se procesó (no ordenada)
        print(f" {x['nombre']} - {x['puntos']} pts - {x['tiempo']:.2f}s - {x['genero']}")

if __name__ == "__main__":
    main()  # arrancar la función principal cuando se ejecuta el script directamente