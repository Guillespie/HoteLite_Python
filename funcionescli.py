# -*- coding: utf-8 -*-
"""Modulo que gestiona los clientes, este modulo contiene las funciones siguientes:
"""

import conexion
import sqlite3
import variables

def limpiarentry(fila):
    '''
    Se encarga de limpiar los widgets de clientes

    @param fila: una tupla con los widgets del cliente
    @return: nada
    '''
    variables.menslabel[1].set_text('')
    for i in range(len(fila)):
        fila[i].set_text('')

def validoDNI(dni):
    '''
    Se encarga de validar el dni del cliente

    @param  dni cliente
    @return: boolean, True si es valido, False si no lo es.
    '''
    try:
        tabla = "TRWAGMYFPDXBNJZSQVHLCKE"   #letras del dni, es estandar
        dig_ext = "XYZ"
        #tabla letras extranjeroreemp_
        reemp_dig_ext = {'X':'0', 'Y':'1', 'Z':'2'}
        numeros = "1234567890"
        dni = dni.upper()
        if len(dni) == 9: #el dni debe tener 9 caracteres
            dig_control = dni[8]
            dni = dni[:8]                                          #el numero que son los 8 primeros
            if dni[0] in dig_ext:
                print(dni)
                dni = dni.replace(dni[0],reemp_dig_ext[dni[0]])
            return len(dni) == len([n for n in dni if n in numeros]) and tabla[int(dni)%23] == dig_control
        return False
    except:
        print("Error")
        return None

#inserta un registro

def insertarcli(fila):
    '''
    Se encarga de insertar un cliente

    @param  datos necesarios para la insercion de un cliente
    @return: nada
    '''
    try:
        conexion.cur.execute('insert into  clientes(dni,apel,nome, data) values(?,?,?,?)',fila)
        conexion.conex.commit()

    except sqlite3.OperationalError as e:
        print(e)
        conexion.conex.rollback()

def listar():
    '''
    Se encarga de listar todos los clientes registrados en la base de datos

    @param  nada
    @return: listado de clientes
    '''
    try:
        conexion.cur.execute('select * from clientes')
        listado = conexion.cur.fetchall()
        conexion.conex.commit()
        return listado
    except sqlite3.OperationalError as e:
        print(e)
        conexion.conex.rollback()

def bajacli(dni):
    '''
    Se encarga de dar de baja un cliente registrado en la base de datos

    @param  dni cliente
    @return: nada
    '''
    try:
        conexion.cur.execute('delete from clientes where dni = ?', (dni,))
        conexion.conex.commit()
    except sqlite3.OperationalError as e:
        print(e)
        conexion.conex.rollback()

# esta funcion modifica datos de clientes
def modifcli(registro, cod):
    '''
    Se encarga de modificar los datos de un cliente

    @param  datos del cliente a modificar , codigo cliente.
    @return: nada
    '''
    try:
        conexion.cur.execute('update clientes set dni = ?, apel= ?, nome = ?, data = ? where id = ?',
                             (registro[0], registro[1], registro[2], registro[3], cod))
        conexion.conex.commit()
    except sqlite3.OperationalError as e:
        print(e)
        conexion.conex.rollback()

#esta funcion carga el treeview con los datos de la tabla clientes

def listadocli(listclientes):

    '''
    Se encarga de listar todos los clientes en el treeView de clientes

    @param  listclientes: lista de clientes
    @return: nada
    '''
    try:
        variables.listado = listar()
        listclientes.clear()
        for registro in variables.listado:
            listclientes.append(registro[1:5])
    except:
        print("error en cargar treeview")


def selectcli(dni):
    '''
    Se encarga de seleccionar un cliente buscandolo a traves de su dni

    @param  dni : cliente
    @return: idcliente
    '''
    try:
        conexion.cur.execute('select id from clientes where dni = ?', (dni,))
        listado = conexion.cur.fetchone()
        conexion.conex.commit()
        return listado
    except sqlite3.OperationalError as e:
        print(e)
        conexion.conex.rollback()

def limpiarentry(fila):
    ''' Se encarga de limpiar la entrada de datos de los clientes

    @param  fila:
    @return: nada
    '''

    for i in range(len(fila)):
        fila[i].set_text('')


def apelnomfac(dni):
    '''
    Se encarga de buscar el apellido y nombres de un cliente a traves del dni recibido

    @param  dni: del cliente
    @return: apellidonombre
    '''
    try:
        conexion.cur.execute('select apel,nome from clientes where dni = ?',(dni,))
        apelnome = conexion.cur.fetchone()
        conexion.conex.commit()
        return apelnome
    except sqlite3.OperationalError as e:
        print(e)
        conexion.conex.rollback()
