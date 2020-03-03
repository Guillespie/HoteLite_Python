# -*- coding: utf-8 -*-
'''
Gestiona abrir y cerrar la base de datos
'''
import os, sqlite3

class Conexion:

    def abrirbbdd(self):
        '''
        Se encarga de abrir la conexion con la base de datos
        @return:
        '''
        try:
            global bbdd, conex, cur
            bbdd = 'empresa.sqlite'         #variable que almacena la base de datos
            conex = sqlite3.connect(bbdd)   #la abrimos
            cur = conex.cursor()            #la variable cursor que hara las operaciones
            print("Conexion realizada correctamente")
        except sqlite3.OperationalError as e:
            print("Error al abrir: ", e)

    def cerrarbbdd(self):
        '''
        Se encarga de cerrar la conexion con la base de datos
        @return:
        '''
        try:
            cur.close()
            conex.close()
            print("Base de datos cerrada correctamente ")
        except sqlite3.OperationalError as e:
            print("Error al cerrar: ", e)




