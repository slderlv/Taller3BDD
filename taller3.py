# -*- coding: utf-8 -*-
"""
Created on Mon Oct 24 20:24:04 2022
"""

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