# -*- coding: utf-8 -*-

from time import strftime
from datetime import datetime
import datetime
from datetime import datetime, timedelta

import conexion,funcionescli,variables, xlrd, xlwt

'''
Gestiona el importar e exportar de/a un fichero
'''

def importar(destino):
    '''
    Se encarga de importar clientes a nuestra base de datos e imprimirlas en el treeView de clientes a traves de un fichero .xlsx
    @return:
    '''


    document = xlrd.open_workbook(str(destino))  #Abrimos el fichero Excel
    clientes = document.sheet_by_index(0)

    # Leemos el numero de filas y columnas de Clientes.

    filas_clientes = clientes.nrows
    columnas_clientes = clientes.ncols
    print("Clientes tiene " + str(filas_clientes) + " filas y " + str(columnas_clientes) + " columnas")

    for i in range(1,filas_clientes):

        dni = clientes.cell_value(i,0)
        apelidos = clientes.cell_value(i, 1)
        nome = clientes.cell_value(i, 2)

        data = float(clientes.cell_value(i, 3))

        year, mont, d, h, m, s = xlrd.xldate_as_tuple(data, 0)
        dia = str(d)
        mes = str(mont)
        ano = str(year)
        fecha = dia.zfill(2) + '/' + mes.zfill(2) + '/' + ano

        print(dni,apelidos,nome,fecha)

        datos_a_introducir = (dni,apelidos,nome,fecha)


        conexion.cur.execute('insert into  clientes(dni, apel, nome, data) values(?,?,?,?)', datos_a_introducir)
        conexion.conex.commit()

        funcionescli.listadocli(variables.listclientes)



def exportar():
    '''
    Se encarga de exportar los datos de los clientes de nuestra base de datos e imprimirlas en el fichero export.xls
    @return:
    '''
    try:
        style0 = xlwt.easyxf('font: name Times New Roman, colour red, bold on')
        style1 = xlwt.easyxf()

        wb = xlwt.Workbook()

        ws = wb.add_sheet('NuevosClientes',  True)
        ws.write(0, 0, 'DNI', style0)
        ws.write(0, 1, 'APELIDOS', style0)
        ws.write(0, 2, 'NOMBRE', style0)
        ws.write(0, 3, 'FECHA ALTA', style0)

        listado = funcionescli.listar()
        j = 1
        for registro in listado:
            for i in range(len(registro)-1):
                ws.write(j,i,registro[i+1],style1)
            j = j + 1


        wb.save('export.xls')
        print("Export realizado")

    except Exception as e:
        print("Error exportando", e)

