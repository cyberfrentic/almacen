import xlwt, os, datetime


#crea un archivo a excell
def ToExcel(query_sets, titulo):
    libro = xlwt.Workbook()
    hoja1 = libro.add_sheet(titulo)
    # Lista de titulos de columna
    data = ['Núm.','Id', 'Proveedor', 'Fol. Entrada', 'Fecha', 'Factura', 'Núm. Factura', 'Orden Comp', 'Dep. Soli', 'Núm. Req.', 'Ofi. Soli', 'Total', 'Observaciones']
    fila = hoja1.row(1)
    for index, col in enumerate(data):
        valor = (col)
        fila.write(index, valor)
    num=1
    index=0
    for item in query_sets:
        index+=1
        fila = hoja1.row(num+1)
        fila.write(0, str(index))
        fila.write(1, item.id)
        fila.write(2, item.proveedor)
        fila.write(3, item.fol_entrada)
        fila.write(4, item.fecha)
        fila.write(5, "Factura" if item.factura == "F" else "Nota")
        fila.write(6, item.nFactura)
        fila.write(7, item.ordenCompra)
        fila.write(8, item.depSolici)
        fila.write(9, item.nReq)
        fila.write(10, item.oSolicitnte)
        fila.write(11, item.total)
        fila.write(12, item.observaciones)
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