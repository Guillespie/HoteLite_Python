# -*- coding: utf-8 -*-

'''
el main contiene los elementos necesarios para lanzar la aplicacion
asi como la declaracion de los widgets que se usaran. Tambien los modulos
que tenemos que importar de las librerias graficas

'''

import gi

import funcionesservicios

gi.require_version('Gtk','3.0')
from gi.repository import Gtk, Gdk

import eventos, conexion, variables
import funcionescli, funcioneshab, funcionesreser,funcionesvar



class Empresa:
    def __init__(self):
        #iniciamos la libreria Gtk
        self.b = Gtk.Builder()
        self.b.add_from_file('ventana.glade')

        #cargamos los widgets con algun evente asociado o que son referenciados
        vprincipal = self.b.get_object('venPrincipal')
        self.vendialog = self.b.get_object('venDialog')
        variables.venacercade = self.b.get_object('venAcercade')
        variables.panel = self.b.get_object('Panel')
        variables.filechooserbackup = self.b.get_object('fileChooserbackup')
        variables.filechooserimportar = self.b.get_object('filechooserimportar')
        menubar = self.b.get_object('menuBar').get_style_context()

        #declaracion de wigdets
        entdni = self.b.get_object('entDni')
        entapel = self.b.get_object('entApel')
        entnome = self.b.get_object('entNome')
        entdatacli = self.b.get_object('entDatacli')
        lblerrdni = self.b.get_object('lblErrdni')
        lblcodcli = self.b.get_object('lblCodcli')
        lblnumnoches = self.b.get_object('lblNumnoches')
        lbldirbackup = self.b.get_object('lblFolderbackup')
        lbldnires = self.b.get_object('lblDnires')
        lblapelres = self.b.get_object('lblApelres')

        lbldnifac = self.b.get_object('lbldnifac')
        lblapelidosfac = self.b.get_object('lblapelidosfac')
        lblnomefac = self.b.get_object('lblnomefac')
        lblcodresfac = self.b.get_object('lblcodresfac')
        lblhabfac = self.b.get_object('lblhabfac')
        lblDataFactura = self.b.get_object('lblDataFactura')

        variables.mensfac = (lbldnifac, lblapelidosfac, lblnomefac, lblcodresfac, lblhabfac,lblDataFactura)

        #Facturacion

        variables.gridfactura = []
        for i in range(0, 36):
            variables.gridfactura.append(
                self.b.get_object('lblf' + str(i))
            )




        variables.vencalendar = self.b.get_object('venCalendar')
        variables.vendialogsalir = self.b.get_object('vendialogSalir')
        variables.calendar = self.b.get_object('Calendar')
        variables.filacli = (entdni, entapel, entnome, entdatacli)
        variables.listclientes = self.b.get_object('listClientes')
        variables.treereservas = self.b.get_object('treeReservas')
        variables.listreservas = self.b.get_object('listReservas')
        variables.treeclientes = self.b.get_object('treeClientes')
        variables.treeSer = self.b.get_object('treeSer')
        variables.listServicios = self.b.get_object('listServicios')
        variables.menslabel = (lblerrdni, lblcodcli, lblnumnoches, lbldirbackup, lbldnires, lblapelres)


        #widgets habitaciones

        entnumhab = self.b.get_object('entNumhab')
        entprezohab = self.b.get_object('entPrezohab')
        rbtsimple = self.b.get_object('rbtSimple')
        rbtdoble = self.b.get_object('rbtDoble')
        rbtfamily = self.b.get_object('rbtFamily')
        variables.treehab = self.b.get_object('treeHab')
        variables.listhab = self.b.get_object('listHab')
        variables.filahab = (entnumhab, entprezohab)
        variables.filarbt = (rbtsimple, rbtdoble, rbtfamily)
        variables.listcmbhab = self.b.get_object('listcmbHab')
        variables.cmbhab = self.b.get_object('cmbNumres')
        variables.switch = self.b.get_object('switch')

        #widgtes reservas

        entdatain = self.b.get_object('entDatain')
        entdataout = self.b.get_object('entDataout')

        # widgts SERVICIOS

        rbtnAlojamiento = self.b.get_object('rbtnAlojamiento')
        rbtnDesayuno = self.b.get_object('rbtnDesayuno')
        rbtnComida = self.b.get_object('rbtnComida')
        rbtnParking = self.b.get_object('rbtnParking')

        variables.rbtnServicios = (rbtnAlojamiento,rbtnDesayuno,rbtnComida,rbtnParking)

        variables.filareserva = (entdni, entapel, entdatain, entdataout)

        # Dialogs Servicios
        variables.dialogNuevosServicios = self.b.get_object('dialogNuevosServicios')
        variables.dialogServicios = self.b.get_object('dialogServicios')

        #widgets entrada datos precio servicios

        entDesayuno = self.b.get_object('entDesayuno')
        entComida = self.b.get_object('entComida')
        entParking = self.b.get_object('entParking')
        variables.entradaPrecioServicios = (entDesayuno,entComida,entParking)

        # widgets entrada datos nuevos servicios

        entNuevoServicio = self.b.get_object('entNuevoServicio')
        entPrecioNuevoServicio = self.b.get_object('entPrecioNuevoServicio')
        variables.entradaNuevosServicios = (entNuevoServicio, entPrecioNuevoServicio)

        # widgets entrada  servicios adicionales

        entTipoServicioAdicional = self.b.get_object('entTipoServicioAdicional')
        lblCodigoReserva = self.b.get_object('lblCodigoReserva')
        lblCodigoHabitacion = self.b.get_object('lblCodigoHabitacion')
        lblErrorServicio = self.b.get_object('lblErrorServicio')
        lblErrorAltaServicio = self.b.get_object('lblErrorAltaServicio')
        lblTotalFactura  = self.b.get_object('lblTotalFactura')
        lblIva = self.b.get_object('lblIva')
        lblSubtotal = self.b.get_object('lblSubtotal')

        variables.entradaServicios = (entTipoServicioAdicional, lblCodigoReserva,lblCodigoHabitacion,lblErrorServicio,lblErrorAltaServicio,lblTotalFactura,lblIva,lblSubtotal)

        #conectamos
        self.b.connect_signals(eventos.Eventos())

        #conexion estilos

        self.set_style()
        menubar.add_class('menuBar')

        s = Gdk.Screen.get_default()
        a = s.get_width()
        b = s.get_height()
        vprincipal.show_all()
        vprincipal.resize(a, b)
        vprincipal.maximize()
        conexion.Conexion().abrirbbdd()
        funcionesreser.listadores()
        funcioneshab.listadonumhab(self)
        funcionescli.listadocli(variables.listclientes)
        funcioneshab.listadohab(variables.listhab)
        funcionesservicios.listadoser(variables.listServicios)
        funcionesvar.controlhab()


    def set_style(self):
        '''
        Definimos los estilos css
        @return:
        '''
        css_provider = Gtk.CssProvider()
        css_provider.load_from_path('estilos.css')
        Gtk.StyleContext().add_provider_for_screen(
            Gdk.Screen.get_default(),
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )


if __name__=='__main__':
    main = Empresa()
    Gtk.main()

