import xlwt, os, datetime


#crea un archivo a excell
def ToExcel(query_sets, titulo):
    libro = xlwt.Workbook()
    hoja1 = libro.add_sheet(titulo)
    # Lista de titulos de columna
    data = ['Núm.','Id', 'Proveedor', 'Fol. Entrada', 'Fecha', 'Factura', 'Núm. Factura', 'Orden Comp', 'Dep. Soli', 'Núm. Req.', 'Ofi. Soli', 'Total', 'Observaciones', 'Gasto', 'Activo']
    fila = hoja1.row(1)
    for index, col in enumerate(data):
        valor = (col)
        fila.write(index, valor)
    num=1
    index=0
    print(query_sets)
    for item in query_sets:
        index+=1
        fila = hoja1.row(num+1)
        fila.write(0, str(index))
        fila.write(1, item[0])
        fila.write(2, item[1])
        fila.write(3, item[2])
        fila.write(4, item[3])
        fila.write(5, "Factura" if item[4] == "F" else "Nota")
        fila.write(6, item[5])
        fila.write(7, item[6])
        fila.write(8, item[7])
        fila.write(9, item[8])
        fila.write(10, item[9])
        fila.write(11, item[10])
        fila.write(12, item[11])
        fila.write(13, item[12])
        fila.write(14, item[13])
        num+=1
    file_name = titulo +".xls"
    hojas = os.path.join(os.path.abspath("static/excell/"), file_name)
    libro.save(hojas)
    return file_name


#convierte el tiempo de excel en fechas
def exceldate(serial):
    seconds = (serial - 25569) * 86400.0
    d = datetime.datetime.utcfromtimestamp(seconds)
    return d.strftime('%Y-%m-%d')