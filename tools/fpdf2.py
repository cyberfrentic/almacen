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
        self.set_fill_color(184, 188, 191)



    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-25)
        # Arial italic 8
        self.set_font('Arial', 'B', 8)
        # Texto de pie de pagina
        if Titulo == "Salida":
            self.cell(50, 5, str(datos1[2])[:55], 'B', 0, 'C')
            self.cell(20, 10, '', 0, 0, 'L')
            self.cell(50, 5, 'LIC. E. JOAQUIN CORREA RUIZ','B',0,'C')
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
        elif Titulo == "SalidaP":
            self.cell(50, 5, str(datos1[2])[:55], 'B', 0, 'C')
            self.cell(20, 10, '', 0, 0, 'L')
            self.cell(50, 5, 'LIC. E. JOAQUIN CORREA RUIZ','B',0,'C')
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
        elif Titulo=="Entrada":
            self.cell(50, 5, str(datos1[13]), 'B', 0, 'C')
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
        elif Titulo == 'Entrada Reimpresa':
            self.cell(50, 5, str(datos1[13]), 'B', 0, 'C')
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
        elif Titulo == 'Salida Reimpresa':
            self.cell(50, 5, str(datos1[2])[:55], 'B', 0, 'C')
            self.cell(20, 10, '', 0, 0, 'L')
            self.cell(50, 5, 'LIC. E. JOAQUIN CORREA RUIZ','B',0,'C')
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


def InventarioQuery(listado, titulo):
    global Titulo, lista, datos1, nombCom
    Titulo = titulo
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
    pdf.set_font('Arial', '', 8.0)


    # Effective page width, or just epw
    epw = pdf.w - 2 * pdf.l_margin
    col_width = epw / 6
    data3 = ('Código', 'Descripción', 'Unidad', 'Cantidad', 'P. U.', 'Total')

    # Text height is the same as current font size
    th = pdf.font_size
    #########################################
    ###       Cuerpo del procedimiento    ###
    #########################################
    pdf.ln(12)
    for item in data3:
        if item == "Descripción":
            pdf.cell(col_width*2.5, th+2, str(item), fill=True,border=1,align='C')
        else:
            pdf.cell(col_width/2+5, th+2, str(item),fill=True,border=1,align='C')
    pdf.ln()
    i=1
    for item in listado:
        if i%2==0:
            pdf.set_fill_color(184, 188, 191)
            if item.actividad=="a":
                pdf.cell(col_width/2+5, th+2, str(item.id_item),fill=True,border=1,align='C')
            else:
                pdf.cell(col_width/2+5, th+2, str(item.id_prod),fill=True,border=1,align='C')
            pdf.cell(col_width*2.5, th+2, str(item.nom_prod)+" *S*", fill=True,border=1,align='C')
            pdf.cell(col_width/2+5, th+2, str(item.um),fill=True,border=1,align='C')
            pdf.cell(col_width/2+5, th+2, str(item.cant_dispon),fill=True,border=1,align='C')
            pdf.cell(col_width/2+5, th+2, str(SetMoneda(item.costo_unit)),fill=True,border=1,align='C')
            pdf.cell(col_width/2+5, th+2, str(SetMoneda(float(item.cant_dispon)*float(item.costo_unit))),fill=True,border=1,align='C')
            pdf.ln()
        else:
            pdf.set_fill_color(255, 255, 255)
            if item.actividad=="a":
                pdf.cell(col_width/2+5, th+2, str(item.id_item),fill=True,border=1,align='C')
            else:
                pdf.cell(col_width/2+5, th+2, str(item.id_prod),fill=True,border=1,align='C')
            pdf.cell(col_width*2.5, th+2, str(item.nom_prod), fill=True,border=1,align='C')
            pdf.cell(col_width/2+5, th+2, str(item.um),fill=True,border=1,align='C')
            pdf.cell(col_width/2+5, th+2, str(item.cant_dispon),fill=True,border=1,align='C')
            pdf.cell(col_width/2+5, th+2, str(SetMoneda(item.costo_unit)),fill=True,border=1,align='C')
            pdf.cell(col_width/2+5, th+2, str(SetMoneda(float(item.cant_dispon)*float(item.costo_unit))),fill=True,border=1,align='C')
            pdf.ln()
        i+=1
    pdf.ln()

    #########################################
    response = make_response(pdf.output(dest='S').encode('latin-1'))
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=%s.pdf' % 'reporte'
    return response


def entradasQuery():
    pass