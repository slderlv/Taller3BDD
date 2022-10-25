# -*- coding: utf-8 -*-
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
    rut = input("Ingrese su rut: ")
    contraseña = input("Ingrese su contraseña: ")
    validar_contraseña = input("Ingrese su contraseña nuevamente: ")
    
    if contraseña == validar_contraseña:
        register_query(rut,contraseña)
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
    
def login():
    rut = input("Ingrese su rut: ")
    contraseña = input("Ingrese su contraseña: ")
    if rut == "ADMIN" and contraseña =="NegocioJuanita":
        print("ADMIN")
    else:
        results = login_query(rut,contraseña)
        try:
            if results[0][0] == rut and results[0][1] == contraseña:
                print("Login valido")
        except:
            print("RUT o contraseña invalidas")
            validacion = input("Desea registrarse? (si - no): ")
            if(validacion.lower() == "si"):
                register()        
    

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
    
login()




#usuario = Usuario(rut,contraseña)
#print(usuario.__str__())