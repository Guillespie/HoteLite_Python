# -*- coding: utf-8 -*-
"""
Aqui vendran todas las funciones que afectan a la gestion de las habitaciones

"""

import conexion, sqlite3, variables

def insertarhab(fila):
    ''' Se encarga de registrar una habitacion en la base de datos
    @param  fila: datos de la habitacion
    @return: nada
    '''
    try:
        conexion.cur.execute('insert into habitacion(numero,tipo,prezo,libre) values(?,?,?,?)', fila)
        conexion.conex.commit()
    except sqlite3.OperationalError as e:
        print(e)
        conexion.conex.rollback()

def listarhab():
    ''' Se encarga de listar todas las habitaciones a traves de una consultas almacenandolas en listado
    @param  nada:
    @return: listado de habitaciones
    '''
    try:
        conexion.cur.execute('select * from habitacion')
        listado = conexion.cur.fetchall()
        conexion.conex.commit()
        return listado
    except sqlite3.OperationalError as e:
        print(e)
        conexion.conex.rollback()

def limpiarentry(fila):
    ''' Se encarga de limpiar la entrada de datos de las habitaciones

    @param  fila:
    @return: nada
    '''
    for i in range(len(fila)):
        fila[i].set_text('')

def listadohab(listhab):
    ''' Se encarga de listar las habitaciones en el treeView de habitaciones
    @param  listhab: listado de habitaciones
    @return: nada
    '''
    try:
        variables.listado = listarhab()
        variables.listhab.clear()
        for registro in variables.listado:
            listhab.append(registro)
    except:
        print("error en cargar treeview de hab")


def bajahab(numhab):
    ''' Se encarga de dar de baja una habitacion
    @param numhab: numero de la habitacion
    @return: nada
    '''
    try:
        conexion.cur.execute('delete from habitacion where numero = ?', (numhab,))
        conexion.conex.commit()
    except sqlite3.OperationalError as e:
        print(e)
        conexion.conex.rollback()


def modifhab(registro, numhab):
    ''' Se encarga de modificar una habitacion existente
    @param registro:
    @param numhab:
    @return: nada
    '''
    try:
        conexion.cur.execute('update habitacion set tipo = ?, prezo = ?, libre = ? where numero = ?',
                             (registro[1], registro[0], registro[2], numhab))
        conexion.conex.commit()
    except sqlite3.OperationalError as e:
        print(e)
        conexion.conex.rollback()

def listadonumhab(self):
    ''' Se encarga de listar los codigos de todas las habitaciones
    @param nada :
    @return: nada
    '''

    try:
        conexion.cur.execute('select numero from habitacion')
        listado = conexion.cur.fetchall()
        variables.listcmbhab.clear()
        for row in listado:
            variables.listcmbhab.append(row)
        conexion.conex.commit()

    except sqlite3.OperationalError as e:
        print(e)
        conexion.conex.rollback()


def listadonumhabres():
    ''' Se encarga de listar los numeros de las habitaciones que hay registradas en el hotel
    @param nada :
    @return: numero de todas las habitaciones en lista
    '''

    try:
        conexion.cur.execute('select numero from habitacion')
        lista = conexion.cur.fetchall()
        return lista
        conexion.conex.commit()
    except sqlite3.OperationalError as e:
        print(e)
        conexion.conex.rollback()


def cambiaestadohab(libre, numhabres):
    ''' Se encarga de cambiar el estado de la habitacion
    @param libre:
    @param numhabres:
    @return: nada
    '''

    try:
        print(libre)
        conexion.cur.execute('update habitacion set libre = ? where numero = ?',
                             (libre[0], numhabres))
        conexion.conex.commit()
    except sqlite3.OperationalError as e:
       print(e)
       conexion.conex.rollback()