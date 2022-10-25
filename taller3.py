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
    
# def insert_query(query, data):
#     try:
#         con = connection()
            

class Usuario:
    def __init__(self,rut,contraseña):
        self.rut = rut
        self.contraseña = contraseña
        self.saldo = 0
    def getRut(self):
        return rut
    def getContraseña(self):
        return contraseña
    def __str__(self):
        return rut,contraseña
rut = input("Ingrese su rut: ")
contraseña = input("Ingrese su contraseña: ")
usuario = Usuario(rut,contraseña)
print(usuario.__str__())