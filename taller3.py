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
    
def login():
    rut = input("Ingrese su rut: ")
    contraseña = input("Ingrese su contraseña: ")
    if rut == "ADMIN" and contraseña =="NegocioJuanita":
        print("ADMIN")
    else:
        results = login_query(rut,contraseña)
        try:
            if results[0][1] == rut and results[0][2] == contraseña:
                print("Login valido")
        except:
            print("Usuario o contraseña invalidas")
            print("Desea registrarse? ()")
        
    
def login_query(rut,password):
    try:
        con = connection()
        cursor = con.cursor()
        cursor.execute("SELECT * FROM cliente WHERE usuario = %s AND password = %s",(rut,password))
        return cursor.fetchall()
    except(Exception, Error) as error:
        print(error)

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