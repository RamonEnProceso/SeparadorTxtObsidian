
#Función de separar poemas del archivo
def separarPaginasArchivo (ruta_archivo, separador = "________________"):

    listaArchivos = []
    pagina = []

    #Abre el archivo y lo asigna a una variable
    with open(ruta_archivo, "r" , encoding='utf-8') as archivo:
        archivoPaginas = archivo.readlines()

    #Itera entre la lista generada con las líneas
    for linea in archivoPaginas:

        linea = linea.replace("\ufeff", "")

        #Si hay un salto de página o es la ultima linea, hacer otro archivo
        if separador in linea or linea == archivoPaginas[-1]:
            listaArchivos.append(pagina)
            hayTitulo = False
            pagina = []

        else:
            
            #Si la línea no contiene nada, no escribirla
            if linea == "\n" and not hayTitulo:
                continue

            #Si es la primera linea, converir en título
            if pagina == []:
                linea = "# " + linea + "\n"
                hayTitulo = True

            #Insertar linea en archivo
            linea = linea.replace("\ufeff", "")
            pagina.append(linea)

    return listaArchivos

def crearArchivosLista (lista, ruta, tag):

    titulos = []

    #Crea un header con un hashtag que lo conecta al dataview del índice
    tag= tag.replace(" ", "_")
    paginaTag = f'---\ntags:\n  - "{tag}"\n---\n'

    for paginas in lista:

        archivo = "".join(paginas)

        #Separa el titulo para nombrar al archivo
        pagina_titulo = paginas[0]

        #Convierte el titulo a un H1 para Obsidian
        pagina_titulo = pagina_titulo.replace("# ", "")

        #Elimina espacios innecesarios al final
        pagina_titulo = pagina_titulo.replace("\n", "")

        #Coloca los tags a la página
        archivo = paginaTag + archivo

        while pagina_titulo[-1] == " ":
            pagina_titulo = pagina_titulo[:-1]

        titulos.append(pagina_titulo)        
        print("Se generó el archivo: " + pagina_titulo + ".md")

        #Crea el archivo
        with open(f"{ruta}/{pagina_titulo}.md", "w", encoding="utf-8") as nuevoArchivo:
            nuevoArchivo.write(archivo)

    return titulos

#Separa las paginas para conectarlas a un indice nuevo en Obsidian
def separarCrearIndice():

    #Inputs para generar las funciones anteriores
    

    #Creación del Indice
    nombreIndice = input("Ingresa el nombre que te gustaría para el índice: ")
    archivoOriginal = input("Escriba la ruta del archivo que desea separar en páginas: ")
    rutaDestino = input("Escriba la ruta donde desea que se creen los archivos: ")

    indice = crearArchivosLista(separarPaginasArchivo(archivoOriginal) , rutaDestino, nombreIndice)

    print(f"{nombreIndice}:\n")

    paginaIndice = ""
    i=0

    #Crea un Dataview para identificar los archivos del indice
    tag= nombreIndice
    tag= tag.replace(" ", "_")
    paginaDataview = f'```dataview\ntable year\nfrom #{tag}\nsort rating desc\n```\n'
    
    #Crea la lista con los indices
    for pagina in indice:
            paginaIndice += f"\n- [[{pagina}]]\n"

    #Crea un Dataview al Inicio
    paginaIndice = paginaDataview + paginaIndice

    print(paginaIndice + "\n")

    with open(f"{rutaDestino}/{nombreIndice}.md", "w", encoding="utf-8") as nuevoArchivo:
            nuevoArchivo.write(paginaIndice)

    print("Se creo el indice con Éxito\n\n")

    return



separarCrearIndice()

