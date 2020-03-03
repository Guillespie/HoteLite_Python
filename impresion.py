# -*- coding: utf-8 -*-

'''
Gestiona la impresion de la factura
'''
from sqlite3 import OperationalError

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import os,funcionescli,facturacion,variables,funcionesservicios


def basico():
    '''
    Se encarga de imprimir la factura en pdf. Este metodo carga en la factura los datos basicos
    de la misma: la imagen del logo del hotel, el nombre, el cif y sus datos de contacto
    @return:
    '''
    try:
        global bill
        bill = canvas.Canvas('prueba.pdf', pagesize=A4)
        bill.drawImage('./img/logohotel.png', 475 ,680 , width = 64, height = 64)
        bill.setFont('Helvetica-Bold', size = 16)
        bill.drawString(250, 780, 'HOTEL LITE')
        bill.setFont('Times-Italic', size=10)
        bill.drawString(180, 765, 'Esperemos que la estancia en el hotel haya sido de su agrado')
        bill.drawString(260, 755, 'CIF: 000000000A')
        bill.line(50, 660, 540, 660)
        bill.setFont('Times-Italic', size=8)
        bill.drawString(170, 20, 'Hotel Lite, tlf = 986123456 e-mail = info@hotelite.com')
        bill.line(50, 30, 540, 30)

    except Exception as e:
        print(e)

def factura(datosfactura):

    ''' Se encarga de completar de imprimir la factura, aqui se imprimiran los datos de la factura de la reserva seleccionada, calculando el iva y el precio final.

    @param  datosfactura:
    @return:
    '''
    try:
        basico()
        bill.setTitle('FACTURA')

        bill.setFont('Helvetica-Bold', size = 8)
        bill.drawString(50,735,'Nº FACTURA: ')

        bill.setFont('Helvetica', size=8)
        bill.drawString(140, 735, str(datosfactura[0]))

        bill.setFont('Helvetica-Bold', size = 8)
        bill.drawString(300,735,'FECHA FACTURA: ')

        bill.setFont('Helvetica-Bold', size=8)
        bill.drawString(380, 735, str(datosfactura[4]))

        bill.setFont('Helvetica-Bold', size=8)
        bill.drawString(50, 710, 'DNI CLIENTE: ')

        bill.setFont('Helvetica', size=8)
        bill.drawString(120, 710, str(datosfactura[2]))

        bill.setFont('Helvetica-Bold', size=8)
        bill.drawString(300, 710, 'Nº HABITACIoN: ')

        bill.setFont('Helvetica', size=8)
        bill.drawString(380, 710, str(datosfactura[3]))

        apelnome = funcionescli.apelnomfac(str(datosfactura[2]))
        print(apelnome)


        bill.setFont('Helvetica-Bold', size=8)
        bill.drawString(50, 680, 'APELLIDOS:')

        bill.setFont('Helvetica', size=9)
        bill.drawString(110, 680, str(camelcase(apelnome[0].lower())))

        bill.setFont('Helvetica-Bold', size=8)
        bill.drawString(300, 680, 'NOMBRE:')

        bill.setFont('Helvetica', size=9)
        bill.drawString(350, 680, str(camelcase(apelnome[1].lower())))

        contadorY = 0
        preciototalservicios = 0

        fila = funcionesservicios.buscarserviciosreservas(datosfactura[0])


        #
        # bill.setFont('Helvetica-Bold', size=8)
        # bill.drawString(50, 620, 'SERVICIOS')
        #
        # bill.setFont('Helvetica-Bold', size=8)
        # bill.drawString(150, 620, 'PRECIO')

        # PRECIO

        precio = facturacion.precioNoche(str(datosfactura[3]))
        total = "{0:.2f}".format(float(precio[0]) * float(datosfactura[1]))
        precioSinIva = "{0:.2f}".format(float(total) + float(preciototalservicios))
        totalConIva = "{0:.2f}".format(float(precioSinIva) + float(variables.iva))



        bill.setFont('Helvetica', size=10)
        bill.drawString(80, 600, 'Noches')
        bill.drawString(230, 600, str(datosfactura[1]))
        bill.drawRightString(375, 600, str("{0:.2f}".format(float(precio[0]))) + '€')
        bill.drawRightString(500, 600, str("{0:.2f}".format(float(total))) + '€')

        bill.setFont('Helvetica-Bold', size=12)
        bill.drawString(70, 640, 'CONCEPTO')
        bill.drawString(200, 640, 'UNIDADES')
        bill.drawString(330, 640, 'PRECIO')
        bill.drawString(460, 640, 'TOTAL')
        bill.line(50, 630, 540, 630)

        for i in range(len(fila)):
            datos = funcionesservicios.buscarservicioporcodigo(str(fila[i][0]))
            preciototalservicios = preciototalservicios + float(datos[1]) * float(datosfactura[1])

            bill.setFont('Helvetica', size=10)
            bill.drawString(80, 580 - contadorY, str(datos[0]).capitalize())
            bill.drawString(230, 580 - contadorY, str(datosfactura[1]))
            bill.drawRightString(375, 580 - contadorY, str("{0:.2f}".format(float(datos[1])) + '€'))
            bill.drawRightString(500, 580 - contadorY, str("{0:.2f}".format(float(datos[1]) * float(datosfactura[1]))) + '€')


            contadorY = contadorY + 20

        bill.line(50, 120, 540, 120)
        bill.setFont('Helvetica-Bold', size=10)
        bill.drawString(390, 95, 'SUBTOTAL:')
        bill.drawRightString(500, 95, str("{0:.2f}".format(float(precioSinIva))) + '€')
        bill.drawString(390, 75, 'IVA:')
        bill.drawRightString(500, 75, str("{0:.2f}".format(float(variables.iva))) + '€')
        bill.drawString(390, 55, 'TOTAL:')
        bill.drawRightString(500, 55, str("{0:.2f}".format(float(totalConIva))) + '€')

        # bill.setFont('Helvetica-Bold', size=8)
        # bill.drawString(300, 620 , 'Nº DE NOCHES')
        #
        # bill.setFont('Helvetica-Bold', size=8)
        # bill.drawString(300, 590, 'PRECIO POR NOCHE')
        #
        # bill.setFont('Helvetica-Bold', size=8)
        # bill.drawString(300, 560, 'PRECIO TOTAL NOCHES')
        #
        # bill.setFont('Helvetica-Bold', size=8)
        # bill.drawString(300, 530, 'PRECIO SERVICIOS POR DiA')
        #
        # bill.setFont('Helvetica-Bold', size=8)
        # bill.drawString(300, 500, 'PRECIO SERVICIOS')
        #
        # bill.setFont('Helvetica-Bold', size=8)
        # bill.drawString(300, 470, 'PRECIO TOTAL SIN IVA')
        #
        # bill.setFont('Helvetica-Bold', size=8)
        # bill.drawString(300, 400, 'IVA')
        #
        # bill.setFont('Helvetica-Bold', size=10)
        # bill.drawString(300, 425, 'TOTAL A PAGAR')




        # bill.setFont('Helvetica', size=9)
        # bill.drawString(430, 620, str(datosfactura[1]))
        #
        # bill.setFont('Helvetica', size=9)
        # bill.drawString(430, 590, str("{0:.2f}".format(float(precio[0]))) + '€')
        #
        # bill.setFont('Helvetica', size=9)
        # bill.drawString(430, 560, str("{0:.2f}".format(float(total))) + '€')
        #
        # bill.setFont('Helvetica', size=9)
        # bill.drawString(430, 530, str("{0:.2f}".format(float(preciototalservicios)/float(datosfactura[1]))) + '€')
        #
        # bill.setFont('Helvetica', size=9)
        # bill.drawString(430, 500, str("{0:.2f}".format(float(preciototalservicios))) + '€')
        #
        # bill.setFont('Helvetica', size=9)
        # bill.drawString(430, 470, str("{0:.2f}".format(float(precioSinIva))) + '€')
        #
        # bill.setFont('Helvetica-Bold', size=10)
        # bill.drawString(430, 425, str("{0:.2f}".format(float(totalConIva))) + '€')
        #
        # bill.setFont('Helvetica', size=9)
        # bill.drawString(430, 400, str("{0:.2f}".format(float(variables.iva))) + '€')


        bill.showPage()
        bill.save()
        dir = os.getcwd()
        os.system('/usr/bin/xdg-open ' + dir + '/prueba.pdf')
    except Exception as e:
        print(e)

def camelcase(s):
    ''' Se encarga de convertir la primera letra de las palabras recibidas en mayuscula

    @param  string: s
    @return: string con cada primera letra de una palabra en mayuscula
    '''

    if(len(s) == 0):
        return
    s1 = ''
    s1 += s[0].upper()
    for i in range(1, len(s)):
        if (s[i] == ' '):
            s1 += ' ' + s[i + 1].upper()
            i += 1
        elif(s[i - 1] != ' '):
            s1 += s[i]
    return s1