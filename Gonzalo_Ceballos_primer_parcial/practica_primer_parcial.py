import re
import json
import os

archivocsv = "C:\\Users\\gonza\\Documents\\tecnicatura\\1A\\programacion1\\ejemplo1\\Gonzalo_Ceballos_primer_parcial\\insumos.csv"

def mostrar_datos_ordenados(lista:list):
    for elementos in lista:
        print(f'{elementos["ID"]}, {elementos["NOMBRE"]}, {elementos["MARCA"]}, {elementos["PRECIO"]}, {elementos["CARACTERISTICAS"]},')

def cargar_datos(archivo:str):
    with open(archivo, "r", encoding='utf-8') as file:
        contenido = file.read()
    lista_contenido = contenido.split("\n")
    lista_listas = []
    lista_contenido = list(filter(lambda cadenas: cadenas != "", lista_contenido))
    for insumos in lista_contenido:
        elementos = insumos.split(",")
        lista_listas.append(elementos)   
    lista_insumos = []
    for i in range(len(lista_listas)):
        diccionario_insumos = {}
        if(i == 0):
            keys = lista_listas[i]
        else:
            diccionario_insumos[keys[0]] = lista_listas[i][0]
            diccionario_insumos[keys[1]] = lista_listas[i][1]
            diccionario_insumos[keys[2]] = lista_listas[i][2]
            diccionario_insumos[keys[3]] = lista_listas[i][3]
            diccionario_insumos[keys[4]] = lista_listas[i][4]
            lista_insumos.append(diccionario_insumos)
    return lista_insumos



def listar_cantidad_marcas(lista:list):
    lista_marcas = set()
    diccionario_cantidad_marcas = {}
    for insumos in lista:
        lista_marcas.add(insumos["MARCA"])
    for marcas in lista_marcas:
        diccionario_cantidad_marcas[marcas] = 0
    for i in range(len(lista)):
       for marcas in lista_marcas:
           if(lista[i]["MARCA"] == marcas):
               diccionario_cantidad_marcas[marcas] += 1
    for marcas in diccionario_cantidad_marcas:
        print(f"La marca {marcas} tiene {diccionario_cantidad_marcas[marcas]} insumos")



def listar_insumos_marca(lista:list):
    lista_marcas = set()
    lista_nombres_precios_marcas = []
    for insumos in lista:
        lista_marcas.add(insumos["MARCA"])
    for i in range(len(lista)):
       for marcas in lista_marcas:
           if(lista[i]["MARCA"] == marcas):
               lista_insumos = [lista[i]["NOMBRE"], lista[i]["MARCA"], lista[i]["PRECIO"]]
               lista_nombres_precios_marcas.append(lista_insumos)
    for insumos in lista_nombres_precios_marcas:
        print(f"el producto {insumos[0]} tiene la marca {insumos[1]}  y el precio es {insumos[2]}")



def insumos_por_caracteristicas(lista:list):
    caracteristica = input("¿Que caracteristica desea listar?")
    caracteristica = caracteristica.capitalize()
    lista_insumos_caracteristicas = list(filter(lambda insumo: re.search(caracteristica, insumo["CARACTERISTICAS"]), lista))
    if(len(lista_insumos_caracteristicas) == 0):
        print("Error esa carcteristica no exite")
    else:
        return lista_insumos_caracteristicas
    
    
    
def listar_insumos_ordenados(lista:list):
    tam = len(lista)
    for i in range(tam - 1):
        for j in range(i +1, tam):
            if (lista[i]["MARCA"] > lista[j]["MARCA"]) or ((lista[i]["MARCA"] == lista[j]["MARCA"]) and (lista[i]["PRECIO"] < lista[j]["PRECIO"])):
                aux = lista[i]
                lista[i] = lista[j]
                lista[j] = aux
    mostrar_datos_ordenados(lista)

def realizar_compras(lista:list):
    lista_compras = []
    while True:
        lista_elementos = []
        marca_usuario = input("¿Que marca desea comprar?")
        marca_usuario = marca_usuario.lower()
        lista_elementos = list(filter(lambda elementos: marca_usuario == elementos["MARCA"].lower(), lista))
        if(len(lista_elementos) == 0):
            print("Esa marca no existe") 
            break
        print("Estos son los productos de esa marca")
        for insumos in lista_elementos:
            print(f'{insumos["ID"]} ,{insumos["NOMBRE"]}, {insumos["MARCA"]} {insumos["PRECIO"]}, {insumos["CARACTERISTICAS"]}')
        producto_usuario = input("¿Que producto desea comprar?(escriba el numero del producto)")
        for insumos in lista_elementos:
            if(producto_usuario == insumos["ID"]):
                lista_compras.append(insumos)
                print("Agregado al carrito")
        if(len(lista_compras) == 0):
            print("Ese producto no esta en esa marca")
        eleccion_usuario = input("¿Desea seguir comprando s/n?")
        while(eleccion_usuario != "n" and eleccion_usuario != "s"):
            eleccion_usuario = input("la respuesta debe ser s(si) o n(no)")
            print(eleccion_usuario)
        if(eleccion_usuario == "n"):
            contador = 0
            total_compra = 0
            with open("texto.txt", "w", encoding="utf-8") as file:
                file.write("Compra de insumos: \n---------------------------\n")
                for insumos in lista_compras:
                    contador += 1
                    precio = insumos["PRECIO"].replace("$", "")
                    total_compra += float(precio) 
                    file.write(f'{insumos["NOMBRE"]}, {insumos["MARCA"]}, {insumos["CARACTERISTICAS"]},  PRECIO: {insumos["PRECIO"]}\n')
                file.write(f"Cantidad de productos: {contador}\nTotal: {total_compra:.2f}")
            print("compra realizada")
            break


def guardar_json(lista:list):
    lista_alimentos = []
    for insumos in lista:
        coincidencia = re.search(r"Alimento", insumos["NOMBRE"])
        if(coincidencia):
            lista_alimentos.append(insumos)
    with open("alimentos.json", "w", encoding="utf-8") as file:
        json.dump(lista_alimentos, file, ensure_ascii=False, indent=4)


def leer_json():
    with open("alimentos.json", "r") as file:
        contenido = file.read()
        lista_alimentos = json.loads(contenido)
    mostrar_datos_ordenados(lista_alimentos)

#esta funcion solo es para la funcion actuatizar_precios
def aumentar_precios(insumos):
        aumento = 8.4
        insumos["PRECIO"] = str(round(float(insumos["PRECIO"].replace("$", "")) + (float(insumos["PRECIO"].replace("$", "")) * (aumento/100)), 2))
        return insumos

def actualizar_precios(lista:list):
    lista_actualizada = list(map(aumentar_precios, lista))
    with open(archivocsv, "w", encoding="utf-8") as file:
        file.write("\nID,NOMBRE,MARCA,PRECIO,CARACTERISTICAS\n")
        for insumos in lista_actualizada:
            file.write(f'{insumos["ID"]},{insumos["NOMBRE"]},{insumos["MARCA"]},${insumos["PRECIO"]},{insumos["CARACTERISTICAS"]}\n')

#creamos la funcion agregar insumos marca que recibira una lista
def agregar_insumo_marca(lista:list):
    #declaramos las variables que usamos mas adelante en la funcion
    eleccion_correcta_marca = False
    caracteristicas = ""
    caracteristica_agregadas = 0
    #le pedimos al usuario que ingrese el nombre y precio del producto que va a agregar
    #y los guardamos en variables
    nombre_insumo_usuario = input("¿Cual es el nombre del producto que quiere agregar?")
    precio_insumo_usuario = input("¿Cual es el precio del producto?")
    #abrimos el archivo marcas.txt para lectura
    with open("Gonzalo_Ceballos_primer_parcial\\marcas.txt", "r") as file:
        #guardamos el contenido del archivo en contenido y lo mostramos para que el usuario vea las marcas
        contenido = file.read()
        print(f"Las marcas que puede elegir son:\n{contenido}")
        #convertimos el contenido en una lista dividida por saltos de linea y la guardamos en una variable
        lista_contenido_marcas = contenido.split("\n")
        #le quitamos las listas que quedaron con una cadena vacia para eliminar los espacios en blanco del archivo
        lista_contenido_marcas = list(filter(lambda cadenas: cadenas != "", lista_contenido_marcas))
    #le pedimos al usuario que elija una marca
    marca_eleccion_usuario = input("¿Que marca quiere que sea su producto?")
    #la validamos en la lista con las marcas que creamos
    for marcas in lista_contenido_marcas:
        if(marca_eleccion_usuario.lower() == marcas.lower()):
            #usamos una bandera para saber que hubo la marca que eligio el usuario fue correcta
            eleccion_correcta_marca = True
            marca_eleccion_usuario = marcas
     #mientras la bandera sea false, es decir que el usuario eligio una marca incorrecta
     # le volvera a preguntar cual es la marca hasta que ingrese una correcta       
    while(not eleccion_correcta_marca):
        marca_eleccion_usuario = input("Esa marca no existe por favor ingrese una marca existente: ")
        for marcas in lista_contenido_marcas:
            if(marca_eleccion_usuario.lower() == marcas.lower()):
                eleccion_correcta_marca = True
                marca_eleccion_usuario = marcas
    #caracteristicas agregadas es una variable que sirve para saber cuantas caracteristicas agrego y no se pase de 3
    while(caracteristica_agregadas >= 0 and caracteristica_agregadas <3):
        #le decimos al usuario que agregue una caracteristica
        caracteristicas_insumo_usuario = input("¿Que caracteristicas tiene el insumo?")
        #caracteristicas contiene un string con todas las caracteristicas
        caracteristicas += caracteristicas_insumo_usuario
        #validamos si el usuario quiere seguir agregando mas caracterisitcas
        eleccion_usuario = input("¿Desea agregar otra caracteristica s/n?")
        if(eleccion_usuario == "n"):
            caracteristica_agregadas = 4
        caracteristica_agregadas +=1
    #iteramos toda la lista hasta llegar al ultimo elemento para al id sumarle uno y ese sera el id del producto nuevo
    for insumos in lista:
        id_insumos = int(insumos["ID"]) + 1
    #creamos el diccionario del producto y lo agregamos a la lista para luego retornarla
    insumo_nuevo = {
        "ID": id_insumos,
        "NOMBRE": nombre_insumo_usuario,
        "MARCA": marca_eleccion_usuario,
        "PRECIO": "$" + str(float(precio_insumo_usuario)),
        "CARACTERISTICAS": caracteristicas 
    }
    lista.append(insumo_nuevo)
    return lista

#creamos la funcion guardar datos actualizados que recibira una lista
def guardar_datos_actualizados(lista:list):
    #le pedimos al usuario que ingrese el nombre del archivo en donde se va a guardar y la extension
    #luego pasamos ese archivo a minuscula
    archivo_usuario = input("¿Que nombre desea ponerle al archivo donde se guardara los datos?")
    opcion_usuario = input("¿En que tipo de archivo desea guardar los datos(CSV o JSON)?")
    opcion_usuario = opcion_usuario.lower()
    #dependiendo que extension eligio el usuario lo guardamos en diferentes archivos
    if(opcion_usuario == "csv"):
        #abrimos el archivo en escritura y le escribimos iterando la lista los insumos en el formato csv
        with open(archivo_usuario+".csv", "w", encoding="utf-8") as file:
            file.write("ID,NOMBRE,MARCA,PRECIO,CARACTERISTICAS\n")
            for insumos in lista:
                file.write(f'{insumos["ID"]},{insumos["NOMBRE"]},{insumos["MARCA"]},${insumos["PRECIO"]},{insumos["CARACTERISTICAS"]}\n')
    elif(opcion_usuario == "json"):
        #abrimos el archivo en escritura y utilizamos dump para agregar la lista al archivo json
        with open(archivo_usuario+".json", "w", encoding="utf-8") as file:
            json.dump(lista, file, ensure_ascii=False, indent=4)


def menu():
    flag_cargar_datos = False
    flag_JSON = False
    lista = cargar_datos(archivocsv)

    while True:
        os.system("cls")
        print("cerrar esto")
        print("""*** Menu de opciones ***
    --------------------------
    1-Cargar datos desde archivo
    2-Listar cantidad de insumos por marca
    3-Listar insumos por marca
    4-Buscar insumo por caracteristica
    5-Listar insumos ordenados
    6-Realizar compras
    7-Guardar en formaro JSON
    8-Leer desde formato JSON
    9-Actualizar precios
    10-Agregar insumo
    11-guardar datos actualizados en csv o json
    12-Salir del programa""")
        opcion = input("Ingrese una opcion: ")
        while(not opcion.isdigit() or (float(opcion) < 1 or float(opcion) > 12)):
            opcion = input("No es una opcion valida, por favor ingrese otra: ")

        match(opcion):
            case "1":
                flag_cargar_datos = True
                lista
            case "2":
                if(flag_cargar_datos):
                    listar_cantidad_marcas(lista)
                else:
                    print("Para realizar esto debes primero cargar los datos")
            case "3":
                if(flag_cargar_datos):
                    listar_insumos_marca(lista)
                else:
                    print("Para realizar esto debes primero cargar los datos")
            case "4":
                if(flag_cargar_datos):
                    insumos_por_caracteristicas(lista)
                else:
                    print("Para realizar esto debes primero cargar los datos")
            case "5":
                if(flag_cargar_datos):
                    listar_insumos_ordenados(lista)
                else:
                    print("Para realizar esto debes primero cargar los datos")
            case "6":
                if(flag_cargar_datos):
                    realizar_compras(lista)
                else:
                    print("Para realizar esto debes primero cargar los datos")
            case "7":
                flag_JSON = True
                if(flag_cargar_datos):
                    guardar_json(lista)
                else:
                    print("Para realizar esto debes primero cargar los datos")
            case "8":
                if(flag_JSON):
                    leer_json()
                else:
                    print("Para realizar esto debes primero guardar los datos en un archivo JSON")
            case "9":
                if(flag_cargar_datos):
                    actualizar_precios(lista)
                else:
                    print("Para realizar esto debes primero cargar los datos")
            case "10":
                #validamos con una bandera que la lista fue cargada
                if(flag_cargar_datos):
                    lista = agregar_insumo_marca(lista)
                else:
                    print("Para realizar esto debes primero cargar los datos")
            case "11":
                 #validamos con una bandera que la lista fue cargada
                if(flag_cargar_datos):
                    guardar_datos_actualizados(lista)
                else:
                    print("Para realizar esto debes primero cargar los datos")
            case "12":
                print("Saliste del programa")
                break

        os.system("pause")


menu()
