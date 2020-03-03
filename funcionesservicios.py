# -*- coding: utf-8 -*-

'''
Gestiona todos lo que tiene que ver con los servicios
'''
import sqlite3
import conexion,variables



def listarser():
    '''
    Se encarga de recoger los servicios registrados en la base de datos

    @param nada :
    @return: listado de servicios
    '''
    try:
        conexion.cur.execute('select * from servicios ')
        listado = conexion.cur.fetchall()
        conexion.conex.commit()
        return listado
    except sqlite3.OperationalError as e:
        print(e)
        conexion.conex.rollback()

def listadoser(list):

    '''
    Se encarga de listar todos los servicios recogidos en variables.listado

    @param list: lista de servicios
    '''
    try:
        variables.listado = listarser()
        list.clear()
        for registro in variables.listado:
            list.append(registro)
    except:
        print("error en cargar treeview de servicios")

def listaserviciosprecios():

    '''
    Se encarga de cargar los precios de los servicios basicos
    en las entradas de datos de precios de esos servicios

    '''
    try:
        conexion.cur.execute('select precio from servicios where codigo = ?', (1,))
        preciodesayuno = conexion.cur.fetchone()
        conexion.cur.execute('select precio from servicios where codigo = ?', (2,))
        preciocomida = conexion.cur.fetchone()
        conexion.cur.execute('select precio from servicios where codigo = ?', (3,))
        precioparking = conexion.cur.fetchone()

        variables.entradaPrecioServicios[0].set_text(preciodesayuno[0])
        variables.entradaPrecioServicios[1].set_text(preciocomida[0])
        variables.entradaPrecioServicios[2].set_text(precioparking[0])

        conexion.conex.commit()

    except sqlite3.OperationalError as e:
        print(e)
        conexion.conex.rollback()

def modifprecioservicio():
    '''
    Se encarga de actualizar el precio a los servicios basicos

    '''

    try:
        preciodesayuno = variables.entradaPrecioServicios[0].get_text()
        preciocomida = variables.entradaPrecioServicios[1].get_text()
        precioparking = variables.entradaPrecioServicios[2].get_text()

        conexion.cur.execute('update servicios set precio = ? where codigo = ?', (preciodesayuno, 1))
        conexion.cur.execute('update servicios set precio = ? where codigo = ?', (preciocomida, 2))
        conexion.cur.execute('update servicios set precio = ? where codigo = ?', (precioparking, 3))

        conexion.conex.commit()

    except sqlite3.OperationalError as e:
        print(e)
        conexion.conex.rollback()

def altaservicioadicional():
    '''
    Se encarga de dar de alta servicios adicionales
    @param nada :
    @return: nada
    '''
    try:
        conexion.cur.execute('insert into servicios(nombre,precio) values(?,?)', (variables.entradaServiciosAdicionales[0].get_text(),variables.entradaServiciosAdicionales[1].get_text(),))
        variables.entradaServiciosAdicionales[0].set_text('')
        variables.entradaServiciosAdicionales[1].set_text('')

        conexion.conex.commit()

    except sqlite3.OperationalError as e:
        print(e)
        conexion.conex.rollback()

def altanuevoservicio():
    '''
    Se encarga de dar de alta un nuevo servicio recogiendo los datos desde los entries
    de nuevos servicios

    @param nada :
    @return: nada
    '''
    try:

        conexion.cur.execute('insert into servicios(nombre,precio) values(?,?)', (variables.entradaNuevosServicios[0].get_text(),variables.entradaNuevosServicios[1].get_text(),))
        variables.entradaNuevosServicios[0].set_text('')
        variables.entradaNuevosServicios[1].set_text('')

        conexion.conex.commit()

    except sqlite3.OperationalError as e:
        print(e)
        conexion.conex.rollback()
def altaservicio(fila):
    '''
    Se encarga de dar de alta un nuevo servicio recogiendo los datos desde los entries
    de nuevos servicios

    @param nada :
    @return: nada
    '''
    try:
        conexion.cur.execute('insert into serviciosreservas(servicio,reserva) values(?,?)', fila)
        conexion.conex.commit(


            
        )
    except sqlite3.OperationalError as e:
        print(e)
        conexion.conex.rollback()


def bajaservicio(fila):
    '''
    Se encarga de dar de baja un servicio a traves de pasarle la fila de datos que contiene
    el codigo del servicio y de la reserva

    @param fila : con servicio y reserva
    @return: nada
    '''
    try:
        conexion.cur.execute('delete from serviciosreservas where servicio = ? and reserva = ?', fila)
        conexion.conex.commit()
    except sqlite3.OperationalError as e:
        print(e)
        conexion.conex.rollback()

def buscarprecioservicio(cod):
    '''
    Se encarga de buscar el precio del servicio recibido a traves de su codigo

    @param servicio : codigo
    @return: precio servicio
    '''
    try:
        conexion.cur.execute('select precio from servicios where codigo = ?', (cod,))
        precio = conexion.cur.fetchone()
        conexion.conex.commit()
        return precio
    except sqlite3.OperationalError as e:
        print(e)
        conexion.conex.rollback()

def buscarservicio(servicio):
    '''
    Se encarga de buscar el codigo del servicio recibido a traves de su nombre

    @param  servicio: nombre del servicio
    @return: codigo servicio
    '''
    try:
        conexion.cur.execute('select codigo from servicios where nombre = ?', (servicio,))
        codigo = conexion.cur.fetchone()
        conexion.conex.commit()
        return codigo
    except sqlite3.OperationalError as e:
        print(e)
        conexion.conex.rollback()

def buscarserviciosreservas(reserva):
    '''
    Se encarga de buscar los servicios asociados a la reserva que se le pasa al metodo

    @param  reserva: codigo de reserva
    @return: conjunto de servicios de serviciosreservas
    '''
    try:
        conexion.cur.execute('select servicio from serviciosreservas where reserva = ?', (reserva,))
        fila = conexion.cur.fetchall()
        conexion.conex.commit()
        return fila
    except sqlite3.OperationalError as e:
        print(e)
        conexion.conex.rollback()

def buscarservicioadicional(servicio):

    '''
    Se encarga de buscar si existe el servicio recibido como parametro

    @param  servicio: nombre del servicio:
    @return: boolean: True si existe, False si no existe
    '''
    try:
        conexion.cur.execute('select codigo from servicios where nombre = ?', (servicio,))
        cod = conexion.cur.fetchone()
        conexion.conex.commit()
        if cod != None:
            return True
        else:
            return False

    except sqlite3.OperationalError as e:
        print(e)
        conexion.conex.rollback()

def buscarservicioporcodigo(servicio):
    ''' Se encarga de buscar el nombre y el precio del servicio, recibiendo su codigo como parametro

    @param  servicio: codigo servicio
    @return: conjunto de servicios de serviciosreservas
    '''
    try:
        conexion.cur.execute('select nombre, precio from servicios where codigo = ?', (servicio,))
        nombre = conexion.cur.fetchone()
        conexion.conex.commit()
        return nombre
    except sqlite3.OperationalError as e:
        print(e)
        conexion.conex.rollback()

def limpiarlbls():
    ''' Se encarga de vaciar las labels del grid de facturas

    @param  nada:
    @return: nada
    '''
    for i in range(0, 36):
        variables.gridfactura[i].set_text('')







