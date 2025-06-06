
#Función de separar poemas del archivo
def separarPaginasArchivo (ruta_archivo):

    listaArchivos = []
    pagina = []

    #Abre el archivo y lo asigna a una variable
    with open(ruta_archivo, "r" , encoding='utf-8') as archivo:
        archivoPaginas = archivo.readlines()

    #Itera entre la lista generada con las líneas
    for linea in archivoPaginas:

        linea = linea.replace("\ufeff", "")

        #Si hay un salto de página o es la ultima linea, hacer otro archivo
        if "________________" in linea or linea == archivoPaginas[-1]:
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

def crearArchivosLista (lista, ruta):

    titulos = []

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
        with open(f"{ruta}/{pagina_titulo}.md", "w", encoding="utf-8") as nuevoArchivo:
            nuevoArchivo.write(archivo)

    return titulos

#Separa las paginas para conectarlas a un indice nuevo en Obsidian
def separarCrearIndice():

    #Inputs para generar las funciones anteriores
    archivoOriginal = input("Escriba la ruta del archivo que desea separar en páginas: ")
    rutaDestino = input("Escriba la ruta donde desea que se creen los archivos: ")

    #Creación del Indice
    nombreIndice = input("Ingresa el nombre que te gustaría para el índice: ")
    indice = crearArchivosLista(separarPaginasArchivo(archivoOriginal) , rutaDestino)

    print(f"{nombreIndice}:\n")

    paginaIndice = ""
    i=0
    for pagina in indice:
        if i%2 == 0:
            paginaIndice += f"\n\n- [[{pagina}]]"
        else:
            paginaIndice += f" [[{pagina}]]"


    print(paginaIndice + "\n")

    with open(f"{rutaDestino}/{nombreIndice}.md", "w", encoding="utf-8") as nuevoArchivo:
            nuevoArchivo.write(paginaIndice)

    print("Se creo el indice con Éxito\n\n")

    return



separarCrearIndice()

