# -*- coding: utf-8 -*-
'''
Gestiona todos lo que tiene que ver con las reservas
'''
import conexion
import sqlite3
import variables
from datetime import datetime

def limpiarentry(fila):

    '''
    Se encarga de limpiar la entrada de datos de la reserva

    @param  fila:
    @return: nada
    '''
    for i in range(len(fila)):
        fila[i].set_text('')
    for i in range(len(variables.menslabel)):
        variables.menslabel[i].set_text('')
    variables.cmbhab.set_active(-1)

def calculardias():
    '''
    Se encarga calcular los dias de entrada y de salida, para comprobar que el check-out de todas las reservas deba ser posterior al check-in.
    Si esto no se cumple se escribe en el label correspondiente un mensaje de aviso

    @param  nada:
    @return: nada
    '''

    diain = variables.filareserva[2].get_text()
    date_in = datetime.strptime(diain, '%d/%m/%Y').date()
    diaout = variables.filareserva[3].get_text()
    date_out = datetime.strptime(diaout, '%d/%m/%Y').date()
    noches = (date_out-date_in).days
    if noches <= 0:
        variables.menslabel[2].set_text('Check-Out debe ser posterior')
        variables.reserva = 0
    else:
        variables.reserva = 1
        variables.menslabel[2].set_text(str(noches))

def insertares(fila):
    '''
    Se encarga de insertar una reserva

    @param  fila: datos de la reserva a insertar
    @return: nada
    '''
    try:
        conexion.cur.execute('insert into  reservas(dni, numhab, checkin, checkout, noches) values(?,?,?,?,?)', fila)
        conexion.conex.commit()

    except sqlite3.OperationalError as e:
        print(e)
        conexion.conex.rollback()

def listadores():
    '''
    Se encarga listar las reservas

    @param  nada:
    @return: nada
    '''
    try:
        variables.listado = listares()
        variables.listreservas.clear()
        for registro in variables.listado:
            variables.listreservas.append(registro)
    except sqlite3.OperationalError as e:
        print(e)
        conexion.conex.rollback()

def listares():
    '''
    Se encarga de buscar todas las reservas y seleccionar su codigo, dni, nHab, checkin, checkout y noches de cada una.

    @param  nada:
    @return: listado de reservas
    '''
    try:
        conexion.cur.execute('select codreser, dni, numhab, checkin, checkout, noches from reservas')
        listado = conexion.cur.fetchall()
        conexion.conex.commit()
        return listado
    except sqlite3.OperationalError as e:
        print(e)
        conexion.conex.rollback()

def buscarapelcli(dni):
    '''
    Se encarga de buscar el apellido de un cliente a traves de su dni

    @param  dni : del cliente
    @return: apellido cliente
    '''
    try:
        conexion.cur.execute('select apel from clientes where dni = ?', (dni,))
        apel = conexion.cur.fetchone()
        conexion.conex.commit()
        return apel
    except sqlite3.OperationalError as e:
        print(e)
        conexion.conex.rollback()

def buscarnome(dni):
    '''
    Se encarga de buscar el nombre de un cliente a traves de su dni

    @param dni : del cliente
    @return: nombre cliente
    '''
    try:
        conexion.cur.execute('select nome from clientes where dni = ?', (dni,))
        nome = conexion.cur.fetchone()
        conexion.conex.commit()
        return nome
    except sqlite3.OperationalError as e:
        print(e)
        conexion.conex.rollback()

def bajareserva(cod):
    '''
    Se encarga de dar de baja una reserva a traves de su codigo

    @param  cod: codigo de la reserva
    @return: nada
    '''
    try:
        print(cod)
        conexion.cur.execute('delete from reservas where codreser = ?', (cod,))
        conexion.conex.commit()
        if variables.switch.get_active():
            libre = 'SI'
        else:
            libre = 'NO'
    except sqlite3.OperationalError as e:
        print(e)
        conexion.conex.rollback()

def versilibre(numhab):
    '''
    Se encarga de comprobar si la habitacion recibida esta libre o no

    @param  numhab: numero de habitacion
    @return: boolean, False si esta ocupada, True si esta libre.
    '''
    try:
        conexion.cur.execute('select libre from habitacion where numero = ?', (numhab,))
        lista= conexion.cur.fetchone()
        conexion.conex.commit()
        if lista[0] == 'SI':
            return True
        else:
            return False
    except sqlite3.OperationalError as e:
        print(e)
        conexion.conex.rollback()