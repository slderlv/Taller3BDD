# -*- coding: utf-8 -*-
from itertools import cycle
from psycopg2 import connect, Error
"""
Created on Mon Oct 24 20:24:04 2022
"""
pw = 'anashe123'
def connection():
    try:
        connection = connect(host = 'localhost', database = 'T3',user='postgres',password=pw,port='5432')
        return connection
    except (Exception, Error) as error:
        connection.rollback()
        print("Error: ",error)
 
 
def register_query(rut,contraseña):
    try:
        con = connection()
        cursor = con.cursor()
        cursor.execute("INSERT INTO cliente (rut,password,saldo) values(%s,%s,0)",(rut,contraseña))
        con.commit()
    except(Exception, Error) as error:
        print("Error: %s" % error)

def register():
    rut = format_rut(input("Ingrese su rut: "))
    if validar_rut(rut)==False:    
        while True:
            rut = input("Rut invalido, ingrese uno valido (Si no desea continuar ingrese 'No'): ")
            if rut.lower() == 'no':
                return
            rut = format_rut(rut)
            if validar_rut(rut):
                break
    
    contraseña = input("Ingrese su contraseña: ")
    validar_contraseña = input("Ingrese su contraseña nuevamente: ")
    
    if contraseña == validar_contraseña:
        register_query(rut,contraseña)
        print("Registro terminado con exito")
    else:
        print("Las contraseñas no coinciden")        
        
def login_query(rut,password):
    try:
        con = connection()
        cursor = con.cursor()
        cursor.execute("SELECT * FROM cliente WHERE rut = %s AND password = %s",(rut,password))
        return cursor.fetchall()
    except(Exception, Error) as error:
        print(error)
    
def digito_verificador(rut):
    reversed_digits = map(int, reversed(str(rut)))
    factors = cycle(range(2, 8))
    s = sum(d * f for d, f in zip(reversed_digits, factors))
    #print(-s % 11)
    return (-s) % 11
    
 
def format_rut(rut):
    rut = rut.replace(".","").replace("-","")
    if (rut[len(rut)-1:len(rut)] == 'k' or rut[len(rut)-1:len(rut)] == 'K' ):
        rut = rut[0:len(rut)-1] + "-K" 
    else:
        rut = rut[0:len(rut)-1] + "-" + rut[len(rut)-1:len(rut)]
    return rut

def validar_rut(rut):
    partes = rut.split("-")
    digito = digito_verificador(partes[0])
    if digito == 10 and partes[1] == "K":
        return True
    if digito == int(partes[1]):
        return True
    return False
    
def login():
    rut = format_rut(input("Ingrese su rut: "))
    contraseña = input("Ingrese su contraseña: ")
    if rut == "ADMIN" and contraseña =="NegocioJuanita":
        print("ADMIN")
    else:
        results = login_query(rut,contraseña)
        try:
            if results[0][0] == rut and results[0][1] == contraseña:
                print("Login valido")
                menu_usuario(rut,contraseña)
        except:
            print("RUT o contraseña invalidas")
            validacion = input("Desea registrarse? (si - no): ")
            if(validacion.lower() == "si"):
                register()        
 
def cambiar_pass_query(rut,password):
    try:
        con = connection()
        cursor = con.cursor()
        cursor.execute("UPDATE cliente SET password = %s WHERE rut = %s;",(password, rut))
        con.commit()    
    except(Exception, Error) as error:
        print(error)   
  
def cambiar_password(rut,password):
    pass_vef = input("Ingrese su anterior contraseña: ")
    if pass_vef == password:
        new_pass = input("Ingrese la nueva contraseña: ")
        if new_pass == password:
            print("La contraseña es igual a la anterior")
            return
        new_vef = input("Ingrese nuevamente la contraseña: ")
        if new_pass == new_vef:
            cambiar_pass_query(rut,new_pass)
            print("Contraseña cambiada con exito")
        else:
            print("La contraseña no coincide")
    else:
        print("La contraseña no coincide")
   
def mostrar_productos_query():
    try:
        con = connection()
        cursor = con.cursor()
        cursor.execute("SELECT * FROM producto")
        return cursor.fetchall()
    except(Exception, Error) as error:
        print(error)

def obtener_datos_producto(producto):
    try:
        con = connection()
        cursor = con.cursor()
        cursor.execute("SELECT * FROM producto WHERE nombre = %s",(producto,))
        return cursor.fetchall()
    except(Exception, Error) as error:
        print(error)

def update_stock(producto, cantidad):
    try:
        con = connection()
        cursor = con.cursor()
        cursor.execute("UPDATE producto SET stock = %s WHERE nombre = %s;",(cantidad, producto))
        con.commit()    
    except(Exception, Error) as error:
        print(error)  

def compras_usuario(rut):
    try:
        con = connection()
        cursor = con.cursor()
        cursor.execute("SELECT * FROM compra WHERE rut_user = %s",(rut,))
        return cursor.fetchall()
    except(Exception, Error) as error:
        print(error)
        
def agregar_compra(rut):
    try:
        con = connection()
        cursor = con.cursor()
        cursor.execute("INSERT INTO compra(id,rut_user,estado) VALUES (default, %s, 'CARRITO')",(rut,))
        con.commit()    
    except(Exception, Error) as error:
        print(error) 
     
def agregar_compra_producto(id_compra,id_producto,cantidad):
    try:
        con = connection()
        cursor = con.cursor()
        cursor.execute("INSERT INTO compra_producto(id,id_compra,id_producto,cantidad) VALUES (default, %s,%s,%s )",(id_compra,id_producto,cantidad))
        con.commit()    
    except(Exception, Error) as error:
        print(error) 

def obtener_compras(rut):
    try:
        con = connection()
        cursor = con.cursor()
        cursor.execute("SELECT * FROM compra WHERE rut_user = %s",(rut,))
        return cursor.fetchall()
    except(Exception, Error) as error:
        print(error)
    
def edit_compra_producto(id_compra,id_prod,cantidad):
    try:
        con = connection()
        cursor = con.cursor()
        cursor.execute("UPDATE compra_producto SET cantidad = %s WHERE id_compra = %s AND id_producto = %s",(cantidad,id_compra,id_prod))
        con.commit()    
    except(Exception, Error) as error:
        print(error) 


def elegir_producto(rut):
    while True:
        products = mostrar_productos_query()
        for product in products:
            print("{}) {} -> {}$ (STOCK DISPONIBLE: {})".format(product[0],product[1],product[3],product[2]))
        producto = input("Ingrese que producto quiere agregar al carrito: ('salir' para salir) ")
        if producto.lower() == "salir":
            return
        datos = obtener_datos_producto(producto)
        try:
            cantidad = int(input("Que cantidad desea agregar de {} (STOCK: {}): ".format(datos[0][1],datos[0][2])))
            compras = compras_usuario(rut)
            if len(compras) == 0:
                if cantidad <= datos[0][2]:
                    agregar_compra(rut)
                    update_stock(producto, datos[0][2]-cantidad)
                    compras_nuevo = compras_usuario(rut)
                    id_compra = compras_nuevo[0][0]
                    compra_producto = obtener_compra_producto(id_compra)
                    if (len (compra_producto)==0):
                        agregar_compra_producto(id_compra,datos[0][0],cantidad)
                    else:
                        flag = False
                        for i in range(len(compra_producto)):
                            if compra_producto[i][2] == datos[0][0]:
                                edit_compra_producto(id_compra,datos[0][0],cantidad+compra_producto[i][3])
                                flag = True
                            if not flag:
                                agregar_compra_producto(id_compra,datos[0][0],cantidad)
                            
            else:
                #Ya ha comprado
                compras = obtener_compras(rut)
                if compras[len(compras)-1][2] == "CARRITO":
                    if cantidad <= datos[0][2]:
                        update_stock(producto, datos[0][2]-cantidad)
                        id_compra = compras[len(compras)-1][0]
                        compra_producto = obtener_compra_producto(id_compra)
                        if (len (compra_producto)==0):
                            agregar_compra_producto(id_compra,datos[0][0],cantidad)
                        else:
                            flag = False
                            for i in range(len(compra_producto)):
                                if compra_producto[i][2] == datos[0][0]:
                                    edit_compra_producto(id_compra,datos[0][0],cantidad+compra_producto[i][3])
                                    flag = True
                            if not flag:
                                agregar_compra_producto(id_compra,datos[0][0],cantidad)
                    else:
                        print("Por favor ingrese una cantidad valida")
                else:
                    if cantidad <= datos[0][2]:
                        agregar_compra(rut)
                        update_stock(producto, datos[0][2]-cantidad)
                        id_compra = compras[len(compras)-1][0]
                        compra_producto = obtener_compra_producto(id_compra)
                        if (len (compra_producto)==0):
                            agregar_compra_producto(id_compra,datos[0][0],cantidad)
                        else:
                            flag = False
                            for i in range(len(compra_producto)):
                                if compra_producto[i][2] == datos[0][0]:
                                    edit_compra_producto(id_compra,datos[0][0],cantidad+compra_producto[i][3])
                                    flag = True
                            if not flag:
                                agregar_compra_producto(id_compra,datos[0][0],cantidad)
                    else:
                        print("Por favor ingrese una cantidad valida")
        except:
            print("Por favor ingrese un valor numerico")
       

def obtener_saldo_query(rut):
    try:
        con = connection()
        cursor = con.cursor()
        cursor.execute("SELECT * FROM cliente WHERE rut = %s",(rut,))
        #Poner * queda con mejor formato
        return cursor.fetchall()
    except(Exception, Error) as error:
        print(error)

def ver_saldo(rut):
    data = obtener_saldo_query(rut)
    print("Tu saldo es:",data[0][2])

def agregar_saldo_query(rut,saldo):
    try:
        con = connection()
        cursor = con.cursor()
        cursor.execute("UPDATE cliente SET saldo = %s WHERE rut = %s;",(saldo, rut))
        con.commit()
    except(Exception, Error) as error:
        print(error) 


def recargar_saldo(rut):
    try:
        nuevo_saldo = int(input("Ingrese el saldo a agregar: "))
        saldo = int(obtener_saldo_query(rut)[0][2]) + nuevo_saldo
        agregar_saldo_query(rut,saldo)
        print("Saldo agregado con exito")
    except:
        print("Ocurrio un error, por favor ingrese numeros validos")

def obtener_compra_producto(id_compra):
    try:
        con = connection()
        cursor = con.cursor()
        cursor.execute("SELECT * FROM compra_producto WHERE id_compra = %s",(id_compra,))
        return cursor.fetchall()
    except(Exception, Error) as error:
        print(error)

def obtener_producto_id(id_producto):
    try:
        con = connection()
        cursor = con.cursor()
        cursor.execute("SELECT * FROM producto WHERE id = %s",(id_producto,))
        return cursor.fetchall()
    except(Exception, Error) as error:
        print(error)

def ver_carrito(rut):
    compras = compras_usuario(rut)
    ultima_compra = compras[len(compras)-1][0]
    compras_productos = obtener_compra_producto(ultima_compra)

    print("\nCARRITO ")
    if compras[len(compras)-1][2] == "CARRITO":
        contador = 1
        for compra in compras_productos:
            producto = obtener_producto_id(compra[2])
            if(compra[3]) != 0:
                print("{}) {} , cantidad: {} -> precio final {}$".format(contador,producto[0][1],compra[3],producto[0][3]*compra[3]))
                contador+=1
    else:
        print("CARRITO VACIO")

def quitar_carrito(rut):
    compras = compras_usuario(rut)
    ultima_compra = compras[len(compras)-1][0]
    ver_carrito(rut)
    producto = input("Que producto desea quitar: ")
    producto_real = obtener_datos_producto(producto)
    
    if len(producto_real) == 0:
        print("No existe el producto")
        return 
    else:
        try:
            cantidad = int(input("Ingrese la cantidad a quitar: "))
            carrito = obtener_compra_producto(ultima_compra)
            if cantidad > 0:
                for producto in carrito:
                    if producto[2] == producto_real[0][0] and producto[3] >= cantidad:
                        edit_compra_producto(ultima_compra,producto[2],producto[3] - cantidad)
                        update_stock(producto_real[0][1],producto_real[0][2] + cantidad)
                        print("Eliminado con exito")
            else:
                print("ingrese un numero valido")
                    
        except:
            print("Ingrese un numero valido")
                

def pagar_carrito(rut,contraseña):
    pass

def menu_usuario(rut,contraseña):
    while True:
        print ("Bienvenido, que desea hacer ?")
        print ("1) Cambiar contraseña")
        print ("2) Elegir un producto")
        print ("3) Ver saldo")
        print ("4) Recargar saldo")
        print ("5) Ver carrito")
        print ("6) Quitar del carrito")
        print ("7) Pagar carrito")
        try:
            opcion = int(input("Eliga opcion (8 para salir): "))
            if opcion == 8:
                break
            
            if opcion == 1:
                cambiar_password(rut,contraseña)
            elif opcion == 2:
                elegir_producto(rut)
            elif opcion == 3:
                ver_saldo(rut)
            elif opcion == 4:
                recargar_saldo(rut)
            elif opcion == 5:
                ver_carrito(rut)
            elif opcion == 6:
                quitar_carrito(rut)
            elif opcion == 7:
                pagar_carrito(rut,contraseña)
            else:
                print("Opcion invalida")
        except:
            print("Por favor ingrese un numero")
    return
   
while True:
    login()
    terminar = input("Desea finalizar el programa (si-no):  ")
    if terminar.lower() == 'si':
        break
