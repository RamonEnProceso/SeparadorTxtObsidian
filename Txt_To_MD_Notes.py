import os
import json



#Función de separar paginas del archivo
def separar_paginas_archivo (ruta_archivo, separador = "________________"):

    lista_archivos = []
    pagina = []
    hay_titulo = False

    try:
        #Abre el archivo y lo asigna a una variable
        with open(ruta_archivo, "r" , encoding='utf-8') as archivo:
            archivo_paginas = archivo.readlines()

        #Itera entre la lista generada con las líneas
        for linea in archivo_paginas:

            linea = linea.replace("\ufeff", "")

            #Si hay un salto de página o es la ultima linea, hacer otro archivo
            if separador in linea or linea == archivo_paginas[-1]:
                lista_archivos.append(pagina)
                hay_titulo = False
                pagina = []

            else:
                
                #Si la línea no contiene nada, no escribirla
                if linea == "\n" and not hay_titulo:
                    continue

                #Si es la primera linea, converir en título
                if pagina == []:
                    linea = "# " + linea + "\n"
                    hay_titulo = True

                #Insertar linea en archivo
                linea = linea.replace("\ufeff", "")
                pagina.append(linea)

        return lista_archivos
    except FileNotFoundError:
        print("La ruta del archivo a separar es incorrecta.\n")
        return "error"



#Función para crear las notas
def crear_archivos_lista (lista, ruta, tag):

    titulos = []

    #Crea un header con un hashtag que lo conecta al dataview del índice
    tag= tag.replace(" ", "_")
    pagina_tag = f'---\ntags:\n  - "{tag}"\n---\n'

    if lista == "error":
        return ""

    for paginas in lista:

        archivo = "".join(paginas)

        #Separa el titulo para nombrar al archivo
        pagina_titulo = paginas[0]

        #Convierte el titulo a un H1 para Obsidian
        pagina_titulo = pagina_titulo.replace("# ", "")

        #Elimina espacios innecesarios al final
        pagina_titulo = pagina_titulo.replace("\n", "")

        while pagina_titulo[-1] == " ":
            pagina_titulo = pagina_titulo[:-1]

        titulos.append(pagina_titulo)        
        print("Se generó el archivo: " + pagina_titulo + ".md")

        #Crea el archivo
        with open(f"{ruta}/{pagina_titulo}.md", "w", encoding="utf-8") as nuevo_archivo:
            nuevo_archivo.write(pagina_tag + "\n" + archivo)

    return titulos



#Separa las paginas para conectarlas a un indice nuevo en Obsidian
def separar_indice(diccionario):
    nombre_indice = diccionario["nombre"]
    archivo_origen = diccionario["origen"]
    ruta_destino = diccionario["destino"]
    indice = crear_archivos_lista(separar_paginas_archivo(archivo_origen) , ruta_destino, nombre_indice)

    print(f"{diccionario["nombre"]}:\n")

    pagina_indice = ""

    #Crea un Dataview para identificar los archivos del indice
    tag= nombre_indice
    tag= tag.replace(" ", "_")
    pagina_dataview = f'```dataview\ntable year\nfrom #{tag}\nsort rating desc\n```\n'
    
    #Crea la lista con los indices
    for pagina in indice:
            pagina_indice += f"\n- [[{pagina}]]\n"

    #Crea un Dataview al Inicio
    pagina_indice = pagina_dataview + pagina_indice

    print(pagina_indice + "\n")

    with open(f"{ruta_destino}/{nombre_indice}.md", "w", encoding="utf-8") as nuevo_archivo:
            nuevo_archivo.write(pagina_indice)

    print("Se creo el indice con Éxito\n\n")

    return






#Verifica si los inputs son correctos

def input_archivo_origen(): 
    condicion = False 
    while not condicion: #Mientras que no se cumplan las condiciones, repetir
        valor = input("Escriba la ruta del archivo que desea separar en páginas: ")
        if not os.path.exists(valor):
            print("No se ha detectado un archivo existente. Por favor, ingrese un archivo.\n")
        elif valor[-4:] != ".txt":
            print("No se ha detectado un archivo compatible. Por favor, ingrese un archivo válido.\n")
        else:
            condicion = True
    return valor

def input_ruta_destino():
    condicion = False
    while not condicion:
        ruta = input("Escriba la ruta donde desea que se creen los archivos: ")
        if not os.path.exists(ruta):
             print("No se ha escrito una ruta existente. Por favor, ingrese una ruta válida\n")
        elif ruta [-1] not in "\\/":
            print("No se ha escrito bien la ruta destinada. Por favor, ingrese una ruta válida.\n")
        else:
            condicion = True
    return ruta

def input_indice_nombre():
    nombre = input("Ingresa el nombre que te gustaría para el índice: ")
    return nombre

def input_respuesta():
    respuesta = input('Ingrese "y" para sí, o "n" para no: ').lower()
    while respuesta not in "yn":
        print("Por favor ingrese un valor correcto")
        respuesta = input('Ingrese "y" para sí, o "n" para no: ')
    if respuesta == "y":
        return True
    else:
        return False

def input_indice_elegir(cantidad):
    condicion = False
    while not condicion:
        try:
            indice_elegido = int(input("Ingrese el número del índice que desea elegir: "))
            if indice_elegido < 0 or indice_elegido > cantidad:
                print("El número se encuentra fuera de rango. Por favor ingrese un número valido")
            else:
                condicion = True
        except ValueError:
            print("El valor escrito no es válido. Por favor ingrese un número valido")
    return indice_elegido




#Verifica o carga antiguos indices

def cargar_indices_guardados_inicio():
    try:
        with open("historial.json","r",encoding="utf-8") as archivo:
            historial = json.load(archivo)

        contador = 0

        print("Se han econtrado historiales pasados. ¿Desea separar nuevamente un índice?")
        respuesta_1 = input_respuesta()

        if respuesta_1:
            for indices in historial:
                print(f"{contador}. {indices["nombre"]}")
                contador += 1
            indice_elegido = input_indice_elegir(contador)
            separar_indice(historial[indice_elegido])
            print("\n¿Desea crear un nuevo indice?. \n")
            respuesta_2 = input_respuesta()
            return respuesta_2
        else:
            return True

    except FileNotFoundError:
        return True
    
    except json.JSONDecodeError:
        print("El historial de indices encontrado está dañado. ¿Desea crear uno nuevo de cero?\n")
        respuesta_3 = input_respuesta()
        if respuesta_3:
            with open("historial.json","w",encoding="utf-8") as archivo:
                json.dump("[]", archivo, indent=2)
            return True
        else:
            return True



#Crear indice nuevo
def crear_indice():

    print("\nSe procedera a crear un nuevo índice. \n")

    indice = ""
    nombre_indice = input_indice_nombre()

    while indice == "":
        archivo_origen = input_archivo_origen()
        ruta_destino = input_ruta_destino()
        indice = crear_archivos_lista(separar_paginas_archivo(archivo_origen) , ruta_destino, nombre_indice)

    diccionario_indice = {"nombre":nombre_indice,"origen":archivo_origen,"destino":ruta_destino}
        
    separar_indice(diccionario_indice)

    json_guardar(diccionario_indice)

    return



#Guarda los datos en el json
def json_guardar(diccionario):
    print("¿Desea guardar los datos para próximos usos? (y/n)")
    respuesta = input_respuesta()
    if respuesta:
        
        try:
            with open("historial.json","r",encoding="utf-8") as archivo:
                historial = json.load(archivo)
                if isinstance(historial, str):
                    historial = []
        except FileNotFoundError:
            print("No se ha encontrado un archivo de guardado. Generandolo...")
            historial = []

        historial.append(diccionario)

        with open("historial.json","w",encoding="utf-8") as archivo:
            json.dump(historial, archivo, indent=2)


#Función maestra 
def main():

    continuar = cargar_indices_guardados_inicio()

    respuesta = True
    if continuar:
        while respuesta:
            crear_indice()
            print("¿Desea crear otro indice?")
            respuesta = input_respuesta()
        print("¡Gracias por usar mi programa! ¡Suerte con tu documentación!!")
        return
    else:
        print("¡Gracias por usar mi programa! ¡Suerte con tu documentación!!")
        return

main()

