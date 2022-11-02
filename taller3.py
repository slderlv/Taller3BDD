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
        cursor.execute("INSERT INTO cliente (rut,password) values(%s,%s)",(rut,contraseña))
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
  
  
def cambiar_password(rut,password):
    pass_vef = input("Ingrese su anterior contraseña: ")
    if pass_vef == password:
        new_pass = input("Ingrese la nueva contraseña: ")
        if new_pass == password:
            print("La contraseña es igual a la anterior")
            return
        new_vef = input("Ingrese nuevamente la contraseña: ")
        if new_pass == new_vef:
            con = connection()
            cursor = con.cursor()
            cursor.execute("UPDATE cliente SET password = %s WHERE rut = %s;",(new_pass, rut))
            con.commit()
            print("Contraseña cambiada con exito")
        else:
            print("La contraseña no coincide")
    else:
        print("La contraseña no coincide")
    
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
            if opcion > 8 or opcion < 0:
                print ("Opcion invalida")
                
            if opcion == 8:
                break
            
            if opcion == 1:
                cambiar_password(rut,contraseña)
        except:
            print("Por favor ingrese un numero")
    return
# class Usuario:
#     def __init__(self,rut,contraseña):
#         self.rut = rut
#         self.contraseña = contraseña
#        self.saldo = 0
#     def getRut(self):
#         return rut
#     def getContraseña(self):
#         return contraseña
#     def __str__(self):
#         return rut,contraseña
    
while True:
    login()
    terminar = input("Desea finalizar el programa (si-no):  ")
    if terminar.lower() == 'si':
        break



#usuario = Usuario(rut,contraseña)
#print(usuario.__str__())