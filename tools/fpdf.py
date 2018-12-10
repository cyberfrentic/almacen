from fpdf import FPDF
import os, time
from datetime import datetime
from flask import make_response



class PDF(FPDF):
    def header(self):
        # Ruta del la carpeta imagenes del servidor
        imagenes = os.path.abspath("static/img/")
        # Logo  con esta ruta se dirige al server y no a la maquina cliente
        if tamaño:
            self.image(os.path.join(imagenes, "sintitulo.png"), 10, 5, 200)
        else:
            self.image(os.path.join(imagenes, "sintitulo.png"), 10, 5, 270)
        # Arial bold 15
        self.set_font('Arial', 'B', 8)
        self.ln(2)
        # Move to the right
        # self.cell(100)
        # Title
        self.ln(1)
        self.cell(0, 10, 'Comision de Agua Potable y alcantarillado', 0, 0, 'C')
        self.ln(4)
        self.cell(0, 10, 'del Estado de Quintana Roo', 0, 0, 'C')
        self.ln(4)
        self.cell(0, 10, 'Direccion de Recursos Materiales', 0, 0, 'C')
        self.ln(4)
        self.cell(0, 10, 'Departamento de Almacen General', 0, 0, 'C')
        self.ln(4)
        self.cell(0, 10, 'Formato de {} de Materiales al Almacen'.format(Titulo), 0, 0, 'C')
        # Line break
        self.ln(4)
        self.cell(150, 10, '', 0, 0)
        self.set_fill_color(184, 188, 191)
        self.cell(20, 8, Titulo, 0, 0, 'C', True)
        self.ln(8)
        #self.set_fill_color(255, 255, 255)
        self.cell(20, 8, lista[0], 'TL' , 0, 'L')
        self.cell(130, 8,str(datos1[0])[:40], 'TB',0,'L', 'True' )
        self.cell(10, 8, "", 'T',0,'C', 'True' )
        self.cell(10, 8, 'Fecha: ', 'T' , 0, 'L')
        self.cell(19, 8, str(datos1[1]), 'TBR',0,'R', 'True' )
        self.ln(8)
        self.cell(30, 8, lista[1], 'L' , 0, 'L')
        self.cell(120, 8, str(datos1[2]), 'B',0,'C', 'True' )
        self.cell(10, 8, "", 0,0,'C', 'True' )
        self.cell(10, 8, 'Folio: ', 0 , 0, 'L')
        self.cell(19, 8, str(datos1[3]), 'RB',0,'C')
        self.ln(8)
        self.cell(40, 8, 'Factura, Nota o Cotización:', 'L' , 0, 'L')
        self.cell(25, 8, str(datos1[4]), 'B',0,'C', 'True' )
        self.cell(70, 8, str(datos1[5]), 'B',0,'C', 'True' )
        self.cell(10, 8, "", 0,0,'C', 'True' )
        self.cell(25, 8, 'Orden de Compra: ', 0 , 0, 'L')
        self.cell(19, 8, str(datos1[6]), 'RB',0,'C')
        self.ln(8)
        self.cell(40, 8, 'Departamento Solicitante:', 'L' , 0, 'L')
        self.cell(80, 8, str(datos1[7])[:40], 'B',0,'L', 'True' )
        self.cell(10, 8, "", 0,0,'C', 'True' )
        self.cell(40, 8, 'Tipo de Compra o Contrato: ', 0 , 0, 'L')
        self.cell(19, 8, str(datos1[8]), 'RB',0,'L')
        self.ln(8)
        self.cell(189, 3, "", 'LRB',0,'L')


    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-25)
        # Arial italic 8
        self.set_font('Arial', 'B', 8)
        # Texto de pie de pagina
        self.cell(50, 5, 'LIC.  N. JOAQUIN CORREA RUIZ', 'B', 0, 'C')
        self.cell(20, 10, '', 0, 0, 'L')
        self.cell(50, 5, 'LIC. N. JOAQUIN CORREA RUIZ','B',0,'C')
        self.cell(20, 10, '', 0, 0, 'L')
        self.cell(50, 5, 'LAE. E. RODRIGO ELJURE FAYAD','B',0,'C')
        self.ln(5)
        self.set_font('Arial', 'B', 6)
        self.cell(50, 5, 'RECIBE', 0, 0, 'C')
        self.cell(20, 10, '', 0, 0, 'L')
        self.cell(50, 5, 'VISTO BUENO',0,0,'C')
        self.cell(20, 10, '', 0, 0, 'L')
        self.cell(50, 5, 'VISTO BUENO',0,0,'C')
        self.ln(3)
        self.set_font('Arial', 'B', 6)
        self.cell(50, 5, '', 0, 0, 'C')
        self.cell(20, 10, '', 0, 0, 'L')
        self.cell(50, 5, '',0,0,'C')
        self.cell(20, 10, '', 0, 0, 'L')
        self.cell(50, 5, 'DIRECTOR DE RECURSOS MATERIALES',0,0,'C')
        self.ln(3)
        # Page number
        self.set_font('Arial', 'B', 8)
        self.cell(0, 10, 'Página ' + str(self.page_no()) + '/{nb}', 0, 0, 'C')


def letras():
    meses = {
        '01': 'Enero',
        '02': 'Febrero',
        '03': 'Marzo',
        '04': 'Abril',
        '05': 'Mayo',
        '06': 'Junio',
        '07': 'Julio',
        '08': 'Agosto',
        '09': 'Septiembre',
        '10': 'Octubre',
        '11': 'Noviembre',
        '12': 'Diciembre',
    }
    dias = {
        '01': 'Primero',
        '02': 'Dos',
        '03': 'Tres',
        '04': 'Cuatro',
        '05': 'Cinco',
        '06': 'Seis',
        '07': 'Siete',
        '08': 'Ocho',
        '09': 'Nueve',
        '10': 'Diez',
        '11': 'Once',
        '12': 'Doce',
        '13': 'Trece',
        '14': 'Catorce',
        '15': 'Quince',
        '16': 'Dieciseis',
        '17': 'Diecisiete',
        '18': 'Dieciocho',
        '19': 'Diecinueve',
        '20': 'Veinte',
        '21': 'VeintiUno',
        '22': 'VeintiDos',
        '23': 'VeintiTres',
        '24': 'VeintiCuatro',
        '25': 'VeintiCinco',
        '26': 'VeintiSeis',
        '27': 'VeintiSiete',
        '28': 'VeintiOcho',
        '29': 'VeintiNueve',
        '30': 'Treinta',
        '31': 'Treinta y uno',
    }
    anios = {
        '2018': 'Dos mil dieciocho',
        '2019': 'Dos mil diecinueve',
        '2020': 'Dos mil veinte',
        '2021': 'Dos mil veintiuno',
        '2022': 'Dos mil veintidos',
    }
    dia = str(datetime.today())[8:10]
    mes = str(datetime.today())[5:7]
    anio = str(datetime.today())[:4]
    return (dias[dia] + ' dias del mes de ' + meses[mes] + ' de ' + anios[anio]).upper()


def SetMoneda(num, simbolo="$", n_decimales=2):
    """Convierte el numero en un string en formato moneda
    SetMoneda(45924.457, 'RD$', 2) --> 'RD$ 45,924.46'     
    """
    #con abs, nos aseguramos que los dec. sea un positivo.
    n_decimales = abs(n_decimales)
    
    #se redondea a los decimales idicados.
    num = round(num, n_decimales)

    #se divide el entero del decimal y obtenemos los string
    num, dec = str(num).split(".")

    #si el num tiene menos decimales que los que se quieren mostrar,
    #se completan los faltantes con ceros.
    dec += "0" * (n_decimales - len(dec))
    
    #se invierte el num, para facilitar la adicion de comas.
    num = num[::-1]
    
    #se crea una lista con las cifras de miles como elementos.
    l = [num[pos:pos+3][::-1] for pos in range(0,50,3) if (num[pos:pos+3])]
    l.reverse()
    
    #se pasa la lista a string, uniendo sus elementos con comas.
    num = str.join(",", l)
    
    #si el numero es negativo, se quita una coma sobrante.
    try:
        if num[0:2] == "-,":
            num = "-%s" % num[2:]
    except IndexError:
        pass
    
    #si no se especifican decimales, se retorna un numero entero.
    if not n_decimales:
        return "%s %s" % (simbolo, num)
        
    return "%s %s.%s" % (simbolo, num, dec)


def fecha_actual():
    meses = {
        '01': 'Enero',
        '02': 'Febrero',
        '03': 'Marzo',
        '04': 'Abril',
        '05': 'Mayo',
        '06': 'Junio',
        '07': 'Julio',
        '08': 'Agosto',
        '09': 'Septiembre',
        '10': 'Octubre',
        '11': 'Noviembre',
        '12': 'Diciembre',
    }
    dia = str(datetime.today())[8:10]
    mes = str(datetime.today())[5:7]
    anio = str(datetime.today())[:4]
    return (dia + ' de ' + meses[mes] + ' de ' + anio).upper()


def entradaPdf(titulo, listas, datos, data2):
    global Titulo, lista, datos1
    Titulo=titulo
    lista = listas
    datos1 = datos
    global tamaño
    tamaño = True #Vertical True
    # Instantiation of inherited class
    pdf = PDF("P", 'mm', 'LETTER')
    pdf.alias_nb_pages()
    pdf.add_page()
    pdf.set_fill_color( 184, 184, 187 )
    pdf.set_text_color(64)
    pdf.set_draw_color(0, 0, 0)
    pdf.set_line_width(.3)
    pdf.set_font('', 'B')
    pdf.set_font('Times', '', 10.0)

    # Effective page width, or just epw
    epw = pdf.w - 2 * pdf.l_margin
    col_width = epw / 6
    data3 = ('Cantidad', 'Unidad', 'Codigo', 'Concepto', 'P. U.', 'Subtotal.')

    # Text height is the same as current font size
    th = pdf.font_size
    #########################################
    ###       Cuerpo del procedimiento    ###
    #########################################
    pdf.ln()
    pdf.ln()
    for item in data3:
        if item == "Concepto":
            pdf.cell(col_width*2.5, th+2, str(item), fill=True,border=1,align='C')
        else:
            pdf.cell(col_width/2+5, th+2, str(item),fill=True,border=1,align='C')
    pdf.ln()
    lista = len(data2)
    banda=0
    for i in data2:
        banda+=1
        print(i[5],i[7])
        if banda == lista:
            pdf.cell(col_width*3.46, th+2, ('observaciones: '+datos[12])[:97], 0,0,'L')
            pdf.cell(col_width, th+2, "", border=0,align='C')
            pdf.cell(col_width/2+5, th+2, "Total", border=1,align='C')
            pdf.cell(col_width/2+5, th+2, str(datos[11]), border=1,align='C')
        else:
            m = banda % 2
            if m == 0:
                pdf.cell(col_width/2+5, th+2, str(i[7]), border=1,align='C', fill=True)
                pdf.cell(col_width/2+5, th+2, str(i[3]), border=1,align='C', fill=True)
                pdf.cell(col_width/2+5, th+2, str(i[0]), border=1,align='C', fill=True)
                pdf.cell(col_width*2.5, th+2, str(i[1]), border=1,align='C', fill=True)
                pdf.cell(col_width/2+5, th+2, str(i[5]), border=1,align='C', fill=True)
                pdf.cell(col_width/2+5, th+2, str((float(i[5])*float(i[7]))), border=1,align='R', fill=True)
            else:
                pdf.cell(col_width/2+5, th+2, str(i[7]), border=1,align='C', fill=False)
                pdf.cell(col_width/2+5, th+2, str(i[3]), border=1,align='C', fill=False)
                pdf.cell(col_width/2+5, th+2, str(i[0]), border=1,align='C', fill=False)
                pdf.cell(col_width*2.5, th+2, str(i[1]), border=1,align='C', fill=False)
                pdf.cell(col_width/2+5, th+2, str(i[5]), border=1,align='C', fill=False)
                pdf.cell(col_width/2+5, th+2, str((float(i[5])*float(i[7]))), border=1,align='R', fill=False)                
            pdf.ln()

    pdf.ln()
    pdf.ln()
    pdf.ln()
    pdf.ln()

    #########################################
    response = make_response(pdf.output(dest='S').encode('latin-1'))
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=%s.pdf' % 'reporte'
    return response