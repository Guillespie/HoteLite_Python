
# -*- coding: utf-8 -*-
'''
Gestiona todos lo que tiene que ver con la facturacion
'''
import variables,conexion,sqlite3,funcionesservicios

def cargargridfactura(datosfactura):

    ''' Se encarga de cargar el grid de factura con los servicios que esta usando el cliente,
        a su vez se va calculando el iva segun el tipo de servicio que seleccione la reserva

        @param  datosfactura:
        @return: nada
    '''
    try:
        global facturadatos
        variables.iva = 0
        funcionesservicios.limpiarlbls()

        # CONCEPTO
        variables.gridfactura[0].set_text('Noches')

        # UNIDADES
        variables.gridfactura[1].set_text(str(datosfactura[1]))

        # PRECIO
        precio = precioNoche(str(datosfactura[3]))
        variables.gridfactura[2].set_text(str(precio[0]))

        # PRECIO TOTAL

        total = float(precio[0]) * float(datosfactura[1])
        variables.gridfactura[3].set_text(str(total))
        precioTotal = total
        variables.iva = float(variables.iva) + float(total) * 0.1
        print(variables.iva)

        # CARGA GRID DE FACTURA

        fila = funcionesservicios.buscarserviciosreservas(datosfactura[0])
        for i in range(len(fila)):
            datos = funcionesservicios.buscarservicioporcodigo(str(fila[i][0]))
            totalPrecioNoches = "{0:.2f}".format(float(datosfactura[1]) * float(datos[1]))
            datosaimprimir = (str(datos[0]).capitalize(), datosfactura[1], datos[1], str(totalPrecioNoches))
            facturadatos = datosaimprimir
            precioTotal = precioTotal + float(totalPrecioNoches)

            if(datos[0] in variables.serviciosbasicos):
                variables.iva = float(variables.iva) + float(totalPrecioNoches) * 0.1
                print(variables.iva)
            else:
                variables.iva = float(variables.iva) + float(totalPrecioNoches) * 0.21
                print(variables.iva)


            for j in range(4):
                variables.gridfactura[(i + 1) * 4 + j].set_text(datosaimprimir[j])
                # print(datosaimprimir[0], (i + 1) * 4 + j)

        # MODIFICAR LABEL TOTAL FACTURA CON SU TOTAL EN EUROS

        variables.entradaServicios[7].set_text('Subtotal: ' + str("{0:.2f}".format(precioTotal)) + '€')
        variables.entradaServicios[6].set_text('Total IVA: ' + str("{0:.2f}".format(variables.iva)) + '€')
        variables.entradaServicios[5].set_text('Total: ' + str("{0:.2f}".format(precioTotal+variables.iva)) + '€')


    except Exception as e:
        print(e)

def precioNoche(hab):

    ''' Se encarga de buscar el precio unitario por noche que tiene la habitacion recibida como parametro

        @param hab: numero de habitacion
        @return: Precio de la habitacion
    '''

    try:
        conexion.cur.execute('select prezo from habitacion where numero = ?', (hab,))
        precio = conexion.cur.fetchone()
        conexion.conex.commit()
        return precio
    except sqlite3.OperationalError as e:
        print(e)
        conexion.conex.rollback()