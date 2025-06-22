#Función de separar poemas del archivo
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
def separar_crear_indice():

    #Inputs para generar las funciones anteriores
    archivo_original = input("Escriba la ruta del archivo que desea separar en páginas: ")

    #Verifica que el archivo ingresado sea compatible con el programa
    while archivo_original[-4:] != ".txt":
        print("No se ha detectado un archivo compatible. Por favor, ingrese un archivo válido.\n")
        archivo_original = input("Escriba la ruta del archivo que desea separar en páginas: ")

    ruta_destino = input("Escriba la ruta donde desea que se creen los archivos: ")

    while ruta_destino[-1] not in "\\/":
         print("No se ha escrito bien la ruta destinada. Por favor, ingrese una ruta válida.\n")
         ruta_destino = input("Escriba la ruta donde desea que se creen los archivos: ")


    #Creación del Indice
    nombre_indice = input("Ingresa el nombre que te gustaría para el índice: ")

    indice = crear_archivos_lista(separar_paginas_archivo(archivo_original) , ruta_destino, nombre_indice)

    while indice == "":
        #Inputs para generar las funciones anteriores
        archivo_original = input("Escriba la ruta del archivo que desea separar en páginas: ")

        #Verifica que el archivo ingresado sea compatible con el programa
        while archivo_original[-4:] != ".txt":
            print("No se ha detectado un archivo compatible. Por favor, ingrese un archivo válido.\n")
            archivo_original = input("Escriba la ruta del archivo que desea separar en páginas: ")

        ruta_destino = input("Escriba la ruta donde desea que se creen los archivos: ")
        
        while ruta_destino[-1] not in "\\/":
            print("No se ha escrito bien la ruta destinada. Por favor, ingrese una ruta válida.\n")
            ruta_destino = input("Escriba la ruta donde desea que se creen los archivos: ")


        #Creación del Indice
        nombre_indice = input("Ingresa el nombre que te gustaría para el índice: ")

        indice = crear_archivos_lista(separar_paginas_archivo(archivo_original) , ruta_destino, nombre_indice)

    print(f"{nombre_indice}:\n")

    pagina_indice = ""
    i=0

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



separar_crear_indice()

