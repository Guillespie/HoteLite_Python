# -*- coding: utf-8 -*-
from datetime import date, datetime
from sqlite3 import OperationalError
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

import gi

import bigdata

gi.require_version('Gtk','3.0')
from gi.repository import Gtk
import funcioneshab, funcionesreser, funcionesvar,impresion,facturacion,funcionesservicios,conexion,funcionescli,variables, xlrd, xlwt
import os, shutil

class Eventos():

# eventos generales
    def on_acercade_activate(self, widget):
        '''
        Se encarga de ensenar la ventana de acerca de
        @param widget:
        @return:
        '''
        try:
            variables.venacercade.show()
        except:
            print('error abrira acerca de')

    def on_btnCerrarabout_clicked(self, widget):
        '''
        Se encarga de cerrar la ventana de acerca de
        @param widget:
        @return:
        '''
        try:
            variables.venacercade.connect('delete-event', lambda w, e: w.hide() or True)
            variables.venacercade.hide()
        except:
            print('error abrir calendario')

    def on_menuBarsalir_activate(self, widget):
        '''
        Se encarga de salir de la app desde el menubar
        @param widget:
        @return:
        '''
        try:
            self.salir()
        except:
            print('salir en menubar')

    def salir(self):
        '''
        Se encarga de cerrar la aplicacion y cerrar la base de datos
        @return:
        '''
        try:
            conexion.Conexion.cerrarbbdd(self)
            funcionesvar.cerrartimer()
            Gtk.main_quit()
        except:
            print('error funcion salir')

    def on_venPrincipal_destroy(self, widget):
        '''
        Se encarga de salir de la aplicacion
        @param widget:
        @return:
        '''
        self.salir()

    def on_btnSalirtool_clicked(self, widget):
        '''
        Se encarga de ensenar la ventana de salir de la aplicacion
        @param widget:
        @return:
        '''
        variables.vendialogsalir.show()

    def on_btnCancelarsalir_clicked(self, widget):
        '''
        Se encarga de cancelar el salir de la aplicacion y esconde la ventana de dialogo de salir
        @param widget:
        @return:
        '''
        variables.vendialogsalir.connect('delete-event', lambda w, e: w.hide() or True)
        variables.vendialogsalir.hide()

    def on_btnAceptarsalir_clicked(self, widget):
        '''
        Se encarga de aceptar salir de la aplicacion desde la ventana de dialogo y llama a la funcion salir
        @param widget:
        @return:
        '''
        self.salir()
    """
    Eventos Clientes
    """

    def on_btnAltacli_clicked(self, widget):
        '''
        Se encarga de recoger los datos de los clientes y meterlos en una lista, manda a validar el dni recogido e inserta el cliente.
        Despues llama a listado para actualizar la lista del treeview y vacia los datos de entrada para altas clientes
        @param widget:
        @return:
        '''
        try:
            dni = variables.filacli[0].get_text()
            apel = variables.filacli[1].get_text()
            nome = variables.filacli[2].get_text()
            data = variables.filacli[3].get_text()
            registro = (dni, apel, nome, data)
            if funcionescli.validoDNI(dni):
                funcionescli.insertarcli(registro)
                funcionescli.listadocli(variables.listclientes)
                funcionescli.limpiarentry(variables.filacli)
            else:
                variables.menslabel[0].set_text('ERROR DNI')
        except:
            print("Error alta cliente")

#boton baja cliente.

    def on_btnBajacli_clicked(self, widget):
        '''
        Se encarga de recoger el dni, mandar a buscarlo en la base de datos y eliminar al cliente que tenga ese dni.
        Despues llama a listado para actualizar la lista del treeview y vacia los datos de entrada para bajas clientes
        @param widget:
        @return:
        '''
        try:
            dni = variables.filacli[0].get_text()
            if dni != '' :
                funcionescli.bajacli(dni)
                funcionescli.listadocli(variables.listclientes)
                funcionescli.limpiarentry(variables.filacli)
            else:
                print('falta dni u otro error')
        except:
            print("error en boton baja cliente")

#  modificamos cliente
    def on_btnModifcli_clicked(self, widget):
        '''
        Se encarga de recoger los datos actualizados para modificar un cliente.
        Despues llama a listado para actualizar la lista del treeview y vacia los datos de entrada para modificar clientes
        @param widget:
        @return:
        '''
        try:
            cod = variables.menslabel[1].get_text()
            dni = variables.filacli[0].get_text()
            apel = variables.filacli[1].get_text()
            nome = variables.filacli[2].get_text()
            data = variables.filacli[3].get_text()
            registro = (dni, apel, nome, data)
            if dni != '':
                funcionescli.modifcli(registro, cod)
                funcionescli.listadocli(variables.listclientes)
                funcionescli.limpiarentry(variables.filacli)
            else:
                print('falta el dni')
        except:
            print('error en boton modificar')


# controla el valor del deni
    def on_entDni_focus_out_event(self, widget, dni):
        '''
        Se encarga de lanzar un mensaje de error si el dni escrito no es valido
        @param widget:
        @param dni:
        @return:
        '''
        try:
            dni = variables.filacli[0].get_text()
            if funcionescli.validoDNI(dni):
                variables.menslabel[0].set_text('')
                pass
            else:
                variables.menslabel[0].set_text('ERROR')
        except:
            print("Error alta cliente en out focus")


    def on_treeClientes_cursor_changed(self, widget):
        '''
        Se encarga de actualizar los datos segun el cliente que seleccionamos en el treeView.
        model es el modelo de la tabla de datos
        iter es el numero que identifica a la fila que marcamos
        @param widget:
        @return:
        '''
        try:
            model,iter = variables.treeclientes.get_selection().get_selected()

            variables.menslabel[0].set_text('')
            funcionescli.limpiarentry(variables.filacli)
            if iter != None:
                sdni = model.get_value(iter, 0)
                sapel = model.get_value(iter, 1)
                snome = model.get_value(iter, 2)
                sdata = model.get_value(iter, 3)
                if sdata == None:
                    sdata = ''
                cod = funcionescli.selectcli(sdni)
                variables.menslabel[1].set_text(str(cod[0]))
                variables.filacli[0].set_text(str(sdni))
                variables.filacli[1].set_text(str(sapel))
                variables.filacli[2].set_text(str(snome))
                variables.filacli[3].set_text(str(sdata))
                variables.menslabel[4].set_text(str(sdni))
                variables.menslabel[5].set_text(str(sapel))
        except:
            print ("error carga cliente")

    def on_btnCalendar_clicked(self, widget):
        '''
        Se encarga de ensenar el calendario de clientes cuando hacemos click en el
        @param widget:
        @return:
        '''
        try:
            variables.semaforo = 1
            variables.vencalendar.connect('delete-event', lambda w, e: w.hide() or True)
            variables.vencalendar.show()

        except:
            print('error abrir calendario')

    def on_btnCalendarResIn_clicked(self,widget):
        '''
        Se encarga de ensenar el calendario de reservas check in cuando hacemos click en el
        @param widget:
        @return:
        '''
        try:
            variables.semaforo = 2
            variables.vencalendar.connect('delete-event', lambda w, e: w.hide() or True)
            variables.vencalendar.show()
        except:
            print('error abrir calendario')

    def on_btnCalendarResOut_clicked(self, widget):
        '''
        Se encarga de ensenar el calendario de reservas- check out cuando hacemos click en el
        @param widget:
        @return:
        '''
        try:
            variables.semaforo  = 3
            variables.vencalendar.connect('delete-event', lambda w, e: w.hide() or True)
            variables.vencalendar.show()
        except:
            print('error abrir calendario')

    def on_Calendar_day_selected_double_click(self, widget):
        '''
        Se encarga de seleccionar una fecha cuando hacemos doble click en un dia del calendar
        @param widget:
        @return:
        '''
        try:
            agno, mes, dia = variables.calendar.get_date()
            fecha = "%s/" % dia + "%s/" % (mes + 1) + "%s" % agno
            if variables.semaforo == 1:
                variables.filacli[3].set_text(fecha)
            elif variables.semaforo == 2:
                variables.filareserva[2].set_text(fecha)
            elif variables.semaforo == 3:
                variables.filareserva[3].set_text(fecha)
                funcionesreser.calculardias()
            else:
                pass
            variables.vencalendar.hide()
        except:
            print('error al coger la fecha')

# Eventos de las habitaciones

    def on_btnAltahab_clicked(self, widget):
        '''
        Se encarga de recoger los datos de la habitacion para darla de alta
        @param widget:
        @return:
        '''
        try:
            numhab = variables.filahab[0].get_text()
            prezohab = variables.filahab[1].get_text()
            prezohab = prezohab.replace(',','.')
            prezohab = float(prezohab)
            prezohab = round(prezohab,2)
            if variables.filarbt[0].get_active():
                tipo = 'simple'
            elif variables.filarbt[1].get_active():
                tipo = 'doble'
            elif variables.filarbt[2].get_active():
                tipo = 'family'
            else:
                pass

            if variables.switch.get_active():
                libre = 'SI'
            else:
                libre = 'NO'
            registro = (numhab, tipo, prezohab, libre)
            if numhab != None:
               funcioneshab.insertarhab(registro)
               funcioneshab.listadohab(variables.listhab)
               funcioneshab.listadonumhab()
               funcioneshab.limpiarentry(variables.filahab)
            else:
                pass
        except:
            print("Error alta habitacion")

    def on_treeHab_cursor_changed(self, widget):
        '''
        Se encarga de actualizar los datos segun la habitacion que seleccionamos en el treeView.
        model es el modelo de la tabla de datos
        iter es el numero que identifica a la fila que marcamos
        @param widget:
        @return:
        '''
        try:
            model, iter = variables.treehab.get_selection().get_selected()
            funcioneshab.limpiarentry(variables.filahab)
            if iter != None:
                snumhab = model.get_value(iter, 0)
                stipo = model.get_value(iter, 1)
                sprezo = model.get_value(iter, 2)
                sprezo = round(sprezo,2)
                variables.filahab[0].set_text(str(snumhab))
                variables.filahab[1].set_text(str(sprezo))
                if stipo == str('simple'):
                    variables.filarbt[0].set_active(True)
                elif stipo == str('doble'):
                    variables.filarbt[1].set_active(True)
                elif stipo == str('family'):
                    variables.filarbt[2].set_active(True)
                slibre = model.get_value(iter,3)
                if slibre == str('SI'):
                    variables.switch.set_active(True)
                else:
                    variables.switch.set_active(False)
        except:
            print("error carga habitacion")


    def on_btnBajahab_clicked(self,widget):
        '''
        Se encarga de recoger el numero de la habitacion para darla de baja
        @param widget:
        @return:
        '''
        try:
            numhab = variables.filahab[0].get_text()
            if numhab != '':
                funcioneshab.bajahab(numhab)
                funcioneshab.limpiarentry(variables.filahab)
                funcioneshab.listadohab(variables.listhab)
            else:
                pass
        except:
            print('borrar baja hab')


    def on_btnModifhab_clicked(self, widget):
        '''
        Se encarga de recoger los datos actualizados de una habitacion para modificarla
        @param widget:
        @return:
        '''
        try:
            numhab = variables.filahab[0].get_text()
            prezo = variables.filahab[1].get_text()
            if variables.switch.get_active():
                libre = 'SI'
            else:
                libre = 'NO'

            if variables.filarbt[0].get_active():
                tipo = 'simple'
            elif variables.filarbt[1].get_active():
                tipo = 'doble'
            elif variables.filarbt[2].get_active():
                tipo = 'family'
            else:
                pass
            registro = (prezo, tipo, libre)
            if numhab != '':
                funcioneshab.modifhab(registro, numhab)
                funcioneshab.listadohab(variables.listhab)
                funcioneshab.limpiarentry(variables.filahab)
            else:
                print('falta el numhab')
        except:
            print('error modif hab')


    # eventos de los botones del toolbar
    def on_Panel_select_page(self, widget):
        '''
        Se encarga de cargar los numeros de las habitaciones en el combobox al seleccionar una pagina
        @param widget:
        @return:
        '''
        try:
            funcioneshab.listadonumhab()
        except:
            print("error boton cliente barra herramientas")

    def on_btnClitool_clicked (self, widget):
        '''
        Se encarga de mostrar la pagina 0, que es la de clientes cuando se seleccione la imagen del cliente en el toolbar
        @param widget:
        @return:
        '''
        try:
            panelactual = variables.panel.get_current_page()
            if panelactual != 0:
                variables.panel.set_current_page(0)
            else:
                pass
        except:
            print("error boton cliente barra herramientas")

    def on_btnReservatool_clicked(self, widget):
        '''
        Se encarga de mostrar la pagina 1, que es la de reservas cuando se seleccione la imagen de la reserva en el toolbar
        @param widget:
        @return:
        '''
        try:
            panelactual = variables.panel.get_current_page()
            if panelactual != 1:
                variables.panel.set_current_page(1)
                funcioneshab.listadonumhab(self)
            else:
                pass
        except:
            print("error boton cliente barra herramientas")

    def on_btnHabita_clicked(self,widget):
        '''
        Se encarga de mostrar la pagina 2, que es la de habitaciones cuando se seleccione la imagen de la habitacion en el toolbar
        @param widget:
        @return:
        '''
        try:
            panelactual = variables.panel.get_current_page()
            if panelactual != 2:
                variables.panel.set_current_page(2)
            else:
                pass
        except:
            print("error boton habitacion barra herramientas")

    def on_btnCalc_clicked(self, widget):
        '''
        Se encarga de abrir la calculadora de linux cuando se clica en la imagen de la calculadora
        @param widget:
        @return:
        '''
        try:
            os.system('/snap/bin/gnome-calculator')
        except:
            print('error lanzar calculadora')

    def on_btnRefresh_clicked(self, widget):
        '''
        Se encarga de limpiar todas las entradas de datos
        @param widget:
        @return:
        '''
        try:
            funcioneshab.limpiarentry(variables.filahab)
            funcionescli.limpiarentry(variables.filacli)
            funcionesreser.limpiarentry(variables.filareserva)
            funcionesservicios.limpiarlbls()
        except:
            print('error refresh')

    def on_menuBarbackup_activate(self, widget):
        '''
        Se encarga de llamar al metodo para hacer una copia de seguridad
        @param widget:
        @return:
        '''
        try:
            variables.filechooserbackup.show()
            variables.neobackup = funcionesvar.backup()
            variables.neobackup = str(os.path.abspath(variables.neobackup))
            print(variables.neobackup)

        except:
            print('error abrir file choorse backup')

    def on_btnGrabarbackup_clicked(self, widget):
        '''
        Se encarga de grabar el backup
        @param widget:
        @return:
        '''
        try:
            destino = variables.filechooserbackup.get_filename()
            destino = destino + '/'
            variables.menslabel[3].set_text(str(destino))
            if shutil.move(str(variables.neobackup), str(destino)):
                variables.menslabel[3].set_text('Copia de Seguridad Creada')
        except:
            print('error select fichero')


    def on_btnCancelfilechooserbackup_clicked(self, widget):
        '''
        Se encarga de cancelar la copia de seguridad y esconder la ventana de backup
        @param widget:
        @return:
        '''
        try:
            variables.filechooserbackup.connect('delete-event', lambda w, e: w.hide() or True)
            variables.filechooserbackup.hide()
        except:
            print('error cerrar file chooser')

## reservas

    def on_cmbNumres_changed(self, widget):
        '''
        Se encarga de mostrar el numero de la habitacion en el combobox de la habitacion en reservas
        @param widget:
        @return:
        '''
        try:
            index = variables.cmbhab.get_active()
            model = variables.cmbhab.get_model()
            item = model[index]
            variables.numhabres = item[0]
        except:
            print('error mostrar habitacion combo')

    def on_btnAltares_clicked(self, widget):
        '''
        Se encarga de recoger los datos necesarios para dar de alta una reserva
        @param widget:
        @return:
        '''
        try:
            if variables.reserva == 1:
                dnir = variables.menslabel[4].get_text()
                chki = variables.filareserva[2].get_text()
                chko = variables.filareserva[3].get_text()
                noches = int(variables.menslabel[2].get_text())
                registro = (dnir, variables.numhabres, chki, chko, noches)
                if funcionesreser.versilibre(variables.numhabres):
                    funcionesreser.insertares(registro)
                    funcionesreser.listadores()
                    #actualizar a NO
                    libre = ['NO']
                    funcioneshab.cambiaestadohab(libre, variables.numhabres)
                    funcioneshab.listadohab(variables.listhab)
                    funcioneshab.limpiarentry(variables.filahab)
                    funcionesreser.limpiarentry(variables.filareserva)
                else:
                    print ('habitacion ocupada')
        except:
            print ('error en alta res')

    def on_btnRefreshcmbhab_clicked(self, widget):
        '''
        Se encarga de refrescar el listado de habitaciones en el combobox de habitaciones en reservas
        @param widget:
        @return:
        '''
        try:
            variables.cmbhab.set_active(-1)
            funcioneshab.listadonumhab(self)
        except:
            print ('error limpiar combo hotel')

    def on_treeReservas_cursor_changed(self, widget):
        '''
        Se encarga de actualizar los datos segun la reserva que seleccionamos en el treeView.
        model es el modelo de la tabla de datos
        iter es el numero que identifica a la fila que marcamos
        @param widget:
        @return:
        '''
        try:
            global codRes
            model, iter = variables.treereservas.get_selection().get_selected()

            funcionesreser.limpiarentry(variables.filareserva)
            if iter != None:
                variables.codr = model.get_value(iter,0)
                codRes = variables.codr
                sdni = model.get_value(iter, 1)
                sapel = funcionesreser.buscarapelcli(str(sdni))
                snome = funcionesreser.buscarnome(str(sdni))
                snumhab =  model.get_value(iter, 2)
                lista = funcioneshab.listadonumhabres()
                m = -1
                for i, x in enumerate(lista):
                    if str(x[0]) == str(snumhab):
                        m = i
                variables.cmbhab.set_active(m)
                schki = model.get_value(iter, 3)
                schko = model.get_value(iter,4)
                snoches = model.get_value(iter, 5)
                variables.menslabel[4].set_text(str(sdni))
                variables.menslabel[5].set_text(str(sapel[0]))
                variables.menslabel[2].set_text(str(snoches))
                variables.filareserva[2].set_text(str(schki))
                variables.filareserva[3].set_text(str(schko))

                variables.mensfac[0].set_text(str(sdni))
                variables.mensfac[1].set_text(str(sapel[0]))
                variables.mensfac[2].set_text(str(variables.codr))
                variables.mensfac[3].set_text(str(snome[0]))
                variables.mensfac[4].set_text(str(snumhab))
                variables.mensfac[5].set_text(str(schko))

                variables.entradaServicios[1].set_text(str(variables.codr))
                variables.entradaServicios[2].set_text(str(snumhab))

                global datosfactura
                datosfactura = (variables.codr,snoches,sdni,snumhab,schko)
                facturacion.cargargridfactura(datosfactura)
                variables.entradaServicios[0].set_text('')
                variables.entradaServicios[3].set_text('')
                variables.entradaServicios[4].set_text('')
        except:
            print ('error cargar valores de reservas')


    def on_btnBajares_clicked(self, widget):
        '''
        Se encarga de recoger el codigo de reserva y eliminarla de la base de datos
        @param widget:
        @return:
        '''
        try:
            funcionesreser.bajareserva(variables.codr)
            funcionesreser.limpiarentry(variables.filareserva)
            funcionesreser.listadores()

        except:
            print('error baja reserva')

    def on_btnCheckout_clicked(self,widget):
        '''
        Se encarga de controlar la fecha del check-out
        @param widget:
        @return:
        '''
        try:
            chko = variables.filareserva[3].get_text()
            today = date.today()
            print(chko)
            hoy = datetime.strftime(today,'%d/%m/%Y')
            registro = (variables.numhabres)
            if str(hoy) == str(chko):
                funcioneshab.modifhabres(registro)
                funcioneshab.listadohab(variables.listhab)
            else:
                print('puede facturar')
                # cambiar el estado de la habitacion de ocupada a libre

        except:
            print('error baja checkout')

    def on_btnImprimir_clicked(self,widget):
        '''
        Se encarga de llamar a imprimir la factura
        @param widget:
        @return:
        '''

        try:
            impresion.factura(datosfactura)
        except:
            print('No lanza el pdf')

    def on_importar_activate(self,widget):
        '''
        Se encarga de importar datos de un xls
        @param widget:
        @return:
        '''
        variables.filechooserimportar.show()
        bigdata.importar()

    def on_exportar_activate(self,widget):
        '''
        Se encarga de exportar datos a un xls
        @param widget:
        @return:
        '''
        bigdata.exportar()

    def on_menuPreciosServicios_activate(self,widget):
        '''
        Se encarga de ensenar la pestana de los precios de los servicios
        @param widget:
        @return:
        '''
        try:

            variables.dialogServicios.show()
            funcionesservicios.listaserviciosprecios()

        except:
            print('error abrir menu precio servicios')

    def on_menuNuevosServicios_activate(self,widget):
        '''
        Se encarga de ensenar la pestana de los servicios nuevos
        @param widget:
        @return:
        '''
        try:
            variables.dialogNuevosServicios.show()
        except:
            print('error abrir menu nuevos servicios')


    def on_btnCancelarServicio_clicked(self,widget):
        '''
        Se encarga de esconder la pestana de los servicios nuevos
        @param widget:
        @return:
        '''
        try:
            # variables.entradaPrecioServicios[0].set_text('')
            # variables.entradaPrecioServicios[1].set_text('')
            # variables.entradaPrecioServicios[2].set_text('')
            variables.dialogServicios.hide()
        except:
            print('error al salir de la ventana de dialogo para editar precios')

    def on_btnAplicarServicio_clicked(self,widget):
        '''
        Se encarga de guardar los datos de los nuevos precios de los servicios basicos
        @param widget:
        @return:
        '''

        try:
            funcionesservicios.modifprecioservicio()
            variables.dialogServicios.hide()
            funcionesservicios.listadoser(variables.listServicios)
        except:
            print('error al aplicar cambios de la ventana de dialogo para editar precios')


    def on_btnAnadirServicio_clicked(self, widget):
        '''
        Se encarga de guardar los datos de los nuevos servicios anadidos
        @param widget:
        @return:
        '''
        try:
            funcionesservicios.altanuevoservicio()
            variables.dialogNuevosServicios.hide()
            funcionesservicios.listadoser(variables.listServicios)

        except:
            print('error al dar de alta un servicio nuevo al hotel')

    def on_btnCancelarServici_clicked(self,widget):
        '''
        Se encarga de esconder la ventana de insercion de nuevos servicios
        @param widget:
        @return:
        '''
        try:
            variables.dialogNuevosServicios.hide()
        except:
            print('error al salir de la ventana de dialogo para dar de alta servicios')

    def on_altaServicios_clicked(self,widget):
        '''
        Se encarga de dar de alta servicios
        @param widget:
        @return:
        '''

        try:
            diaout = variables.filareserva[3].get_text()
            date_out = datetime.strptime(diaout, '%d/%m/%Y').date()
            today = date.today()
            noches = (today - date_out).days
            numDesayuno = funcionesservicios.buscarservicio('desayuno')
            numComida = funcionesservicios.buscarservicio('comida')
            numAlojamiento = funcionesservicios.buscarservicio('alojamiento')
            if noches <= 0:
                if variables.entradaServicios[1].get_text() != '':
                    if variables.rbtnServicios[0].get_active():

                        concepto = 'alojamiento'
                        servicio = funcionesservicios.buscarservicio(concepto)

                        servicios = funcionesservicios.buscarserviciosreservas(codRes)
                        if (servicio in servicios):
                            variables.entradaServicios[4].set_text('Servicio ya registrado')

                        if (numComida in servicios):
                            fila = (numComida[0], codRes)
                            funcionesservicios.bajaservicio(fila)
                            filainsert = (servicio[0], codRes)
                            funcionesservicios.altaservicio(filainsert)
                            variables.entradaServicios[0].set_text('')
                            facturacion.cargargridfactura(datosfactura)
                            variables.entradaServicios[4].set_text('')
                        if (numDesayuno in servicios):
                            fila = (numDesayuno[0], codRes)
                            funcionesservicios.bajaservicio(fila)
                            filainsert = (servicio[0], codRes)
                            funcionesservicios.altaservicio(filainsert)
                            variables.entradaServicios[0].set_text('')
                            facturacion.cargargridfactura(datosfactura)
                            variables.entradaServicios[4].set_text('')


                    if variables.rbtnServicios[1].get_active():
                        concepto = 'desayuno'
                        servicio = funcionesservicios.buscarservicio(concepto)

                        servicios = funcionesservicios.buscarserviciosreservas(codRes)
                        if (servicio in servicios):
                            variables.entradaServicios[4].set_text('Servicio ya registrado')

                        if (numComida in servicios):
                            fila = (numComida[0], codRes)
                            funcionesservicios.bajaservicio(fila)
                            filainsert = (servicio[0], codRes)
                            funcionesservicios.altaservicio(filainsert)
                            variables.entradaServicios[0].set_text('')
                            facturacion.cargargridfactura(datosfactura)
                            variables.entradaServicios[4].set_text('')
                        if (numAlojamiento in servicios):
                            fila = (numAlojamiento[0], codRes)
                            funcionesservicios.bajaservicio(fila)
                            filainsert = (servicio[0], codRes)
                            funcionesservicios.altaservicio(filainsert)
                            variables.entradaServicios[0].set_text('')
                            facturacion.cargargridfactura(datosfactura)
                            variables.entradaServicios[4].set_text('')

                    if variables.rbtnServicios[2].get_active():
                        concepto = 'comida'
                        servicio = funcionesservicios.buscarservicio(concepto)

                        servicios = funcionesservicios.buscarserviciosreservas(codRes)
                        if (servicio in servicios):
                            variables.entradaServicios[4].set_text('Servicio ya registrado')

                        if (numDesayuno in servicios):
                            fila = (numDesayuno[0], codRes)
                            funcionesservicios.bajaservicio(fila)
                            filainsert = (servicio[0], codRes)
                            funcionesservicios.altaservicio(filainsert)
                            variables.entradaServicios[0].set_text('')
                            facturacion.cargargridfactura(datosfactura)
                            variables.entradaServicios[4].set_text('')
                        if (numAlojamiento in servicios):
                            fila = (numAlojamiento[0], codRes)
                            funcionesservicios.bajaservicio(fila)
                            filainsert = (servicio[0], codRes)
                            funcionesservicios.altaservicio(filainsert)
                            variables.entradaServicios[0].set_text('')
                            facturacion.cargargridfactura(datosfactura)
                            variables.entradaServicios[4].set_text('')
                    if variables.rbtnServicios[3].get_active():
                        concepto = 'parking'
                        servicio = funcionesservicios.buscarservicio(concepto)
                        fila = (servicio[0], codRes)
                        funcionesservicios.altaservicio(fila)
                        variables.entradaServicios[0].set_text('')
                        facturacion.cargargridfactura(datosfactura)
                        variables.entradaServicios[4].set_text('')

                else:
                    variables.entradaServicios[4].set_text('Debes seleccionar una reserva antes')
            else:
                variables.entradaServicios[4].set_text('Esta reserva ya expiro\n'
                                                       'No se puede dar alta servicio')
        except OperationalError as eee:
            variables.entradaServicios[4].set_text('Ya existe ese servicio para esa reserva')
            print(eee)

    def on_bajaServicios_clicked(self,widget):
        '''
        Se encarga de dar de baja un servicio
        @param widget:
        @return:
        '''

        try:
            diaout = variables.filareserva[3].get_text()
            date_out = datetime.strptime(diaout, '%d/%m/%Y').date()
            today = date.today()
            noches = (today - date_out).days
            if noches <= 0:
                if variables.entradaServicios[1].get_text() != (''):
                    if variables.rbtnServicios[0].get_active():
                        concepto = 'alojamiento'
                        servicio = funcionesservicios.buscarservicio(concepto)
                        precio = funcionesservicios.buscarprecioservicio(str(servicio))
                        fila = (servicio[0],codRes)
                        funcionesservicios.bajaservicio(fila)
                        variables.entradaServicios[0].set_text('')
                        facturacion.cargargridfactura(datosfactura)
                        variables.entradaServicios[4].set_text('')
                    if variables.rbtnServicios[1].get_active():
                        concepto = 'desayuno'
                        servicio = funcionesservicios.buscarservicio(concepto)
                        precio = funcionesservicios.buscarprecioservicio(str(servicio))
                        fila = (servicio[0], codRes)
                        funcionesservicios.bajaservicio(fila)
                        variables.entradaServicios[0].set_text('')
                        facturacion.cargargridfactura(datosfactura)
                        variables.entradaServicios[4].set_text('')
                    if variables.rbtnServicios[2].get_active():
                        concepto = 'comida'
                        servicio = funcionesservicios.buscarservicio(concepto)
                        precio = funcionesservicios.buscarprecioservicio(str(servicio))
                        fila = (servicio[0], codRes)
                        funcionesservicios.bajaservicio(fila)
                        variables.entradaServicios[0].set_text('')
                        facturacion.cargargridfactura(datosfactura)
                        variables.entradaServicios[4].set_text('')
                    if variables.rbtnServicios[3].get_active():
                        concepto = 'parking'
                        servicio = funcionesservicios.buscarservicio(concepto)
                        precio = funcionesservicios.buscarprecioservicio(str(servicio))
                        fila = (servicio[0], codRes)
                        funcionesservicios.bajaservicio(fila)
                        variables.entradaServicios[0].set_text('')
                        facturacion.cargargridfactura(datosfactura)
                        variables.entradaServicios[4].set_text('')

                else:
                    variables.entradaServicios[4].set_text('Debes seleccionar una reserva antes')
            else:
                variables.entradaServicios[4].set_text('Esta reserva ya expiro\n'
                                                   'No se puede dar baja servicio')
        except OperationalError as eee:
            print(eee)

    def on_altaServiciosAdicionales_clicked(self, widget):
        '''
        Se encarga de dar de alta servicios adicionales
        @param widget:
        @return:
        '''
        try:
            concepto = variables.entradaServicios[0].get_text().lower()
            diaout = variables.filareserva[3].get_text()
            date_out = datetime.strptime(diaout, '%d/%m/%Y').date()
            today = date.today()
            noches = (today - date_out).days
            if noches <= 0:
                if funcionesservicios.buscarservicioadicional(concepto):

                    servicios = funcionesservicios.buscarserviciosreservas(codRes)
                    servicio = funcionesservicios.buscarservicio(concepto)
                    if (servicio in servicios):
                        variables.entradaServicios[3].set_text('Servicio ya registrado')
                        variables.entradaServicios[0].set_text('')

                    else:
                        fila = (servicio[0], codRes)
                        funcionesservicios.altaservicio(fila)
                        variables.entradaServicios[0].set_text('')
                        variables.entradaServicios[3].set_text('')
                        facturacion.cargargridfactura(datosfactura)
                        variables.entradaServicios[4].set_text('')
                else:
                    variables.entradaServicios[3].set_text('No existe ese servicio en el hotel\n'
                                                           'Prueba con otro')
                    variables.entradaServicios[0].set_text('')
            else:
                variables.entradaServicios[4].set_text('Esta reserva ya expiro\n'
                                                   'No se puede dar alta al servicio adicional')
                variables.entradaServicios[0].set_text('')
                variables.entradaServicios[3].set_text('')

        except OperationalError as eee:
            print(eee)

    def on_btnBajaServicioAdicional_clicked(self, widget):
        '''
        Se encarga de dar de baja servicios adicionales
        @param widget:
        @return:
        '''
        try:
            concepto = variables.entradaServicios[0].get_text().lower()
            diaout = variables.filareserva[3].get_text()
            date_out = datetime.strptime(diaout, '%d/%m/%Y').date()
            today = date.today()
            noches = (today - date_out).days
            if noches <= 0:
                if funcionesservicios.buscarservicioadicional(concepto):
                    servicio = funcionesservicios.buscarservicio(concepto)
                    fila = (servicio[0], codRes)
                    funcionesservicios.bajaservicio(fila)
                    variables.entradaServicios[0].set_text('')
                    variables.entradaServicios[3].set_text('')
                    facturacion.cargargridfactura(datosfactura)
                    variables.entradaServicios[4].set_text('')
                else:
                    variables.entradaServicios[3].set_text('No existe ese servicio en el hotel\n'
                                                           'Prueba con otro')
                    variables.entradaServicios[0].set_text('')
            else:
                variables.entradaServicios[4].set_text('Esta reserva ya expiro\n'
                                                   'No se puede dar de baja al servicio adicional')
                variables.entradaServicios[0].set_text('')
                variables.entradaServicios[3].set_text('')

        except OperationalError as eee:
            print(eee)

    def on_treeSer_cursor_changed(self, widget):
        '''
        Se encarga de poner el servicio en entry correspondiente cuando se selecciona un servicio
        @param widget:
        @return:
        '''
        try:

            model, iter = variables.treeSer.get_selection().get_selected()
            # model es el modelo de la tabla de datos
            # iter es el numero que identifica a la fila que marcamos
            if iter != None:
                nombreServicio = model.get_value(iter,1)
                variables.entradaServicios[0].set_text(str(nombreServicio))
                variables.entradaServicios[3].set_text('')

        except:
            print ('error cargar valores de servicios')

    def on_btnAceptarImportar_clicked(self,widget):

        destino = str(variables.filechooserimportar.get_filename())
        variables.filechooserimportar.hide()
        bigdata.importar(destino)


    def on_btnCancelarImportar_clicked(self,widget):

        variables.filechooserimportar.hide()


    def on_btnListado_clicked(self,widget):

        try:
            global lista
            lista = canvas.Canvas('clientes.pdf', pagesize=A4)
            lista.setTitle('LISTADO DE CLIENTES')
            lista.setFont('Helvetica-Bold', size=16)
            lista.drawString(200, 780, 'LISTADO CLIENTES')
            lista.setFont('Helvetica-Bold', size=12)
            lista.drawString(50, 740, 'APELLIDOS')
            lista.drawString(250, 740, 'NOMBRE')
            lista.drawString(450, 740, 'DNI')
            lista.line(50, 760, 540, 760)
            lista.setFont('Helvetica', size=8)
            lista.line(50, 730, 540, 730)


            listado = funcionescli.listar()
            y = 710
            pagina = 1
            for registro in listado:

                if y > 40:
                    lista.drawString(50, y, registro[2])
                    lista.drawString(250, y, registro[3])
                    dni = "• • • • • • " + str(registro[1])[6:]
                    lista.drawString(450, y, dni)
                    # lista.line(50, y-2, 540, y-2)
                    y = y - 15
                else:

                    lista.showPage()
                    canvas.Canvas._pageNumber = pagina + 1
                    y = 710
                    lista.setFont('Helvetica-Bold', size=16)
                    lista.drawString(200, 780, 'LISTADO CLIENTES')
                    lista.drawString(550, 25, str(canvas.Canvas.getPageNumber(lista)))
                    lista.setFont('Helvetica-Bold', size=16)
                    lista.setFont('Helvetica-Bold', size=12)
                    lista.drawString(50, 740, 'APELLIDOS')
                    lista.drawString(250, 740, 'NOMBRE')
                    lista.drawString(450, 740, 'DNI')
                    lista.line(50, 760, 540, 760)
                    lista.setFont('Helvetica', size=8)
                    lista.line(50, 730, 540, 730)
                    lista.setFont('Helvetica', size=8)
                    dni = "• • • • • • " + str(registro[1])[6:]
                    lista.drawString(450, y, dni)
                    lista.drawString(50, y, registro[2])
                    lista.drawString(250, y, registro[3])
                    lista.drawString(450, y, dni)
                    # lista.line(50, y - 2, 540, y - 2)

                    y = y - 15

            canvas.Canvas._pageNumber = 1
            lista.showPage()

            lista.save()
            dir = os.getcwd()
            os.system('/usr/bin/xdg-open ' + dir + '/clientes.pdf')



        except Exception as e:
            print(e)
