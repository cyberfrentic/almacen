function mathRound2 (num, decimales = 2) {
  //Respuesta de Rubén modificada por mí para el caso general y números negativos
  var exponente = Math.pow(10, decimales);
  return (num >= 0 || -1) * Math.round(Math.abs(num) * exponente) / exponente;
}

function ejemplo(valor){
  var valorTd=parseFloat(document.getElementById(valor).innerText); //Encuentro el valor de una celda de una tabla 
  var valor_input = parseFloat(document.getElementsByName(valor)[0].value); // Encuentro el valor de un input dentro de una tabla
  var row = document.getElementById(valor+'-2');
  var x = row.insertCell(16);
  alert(row,valoTd, valor_input);
  if (valor != ""){
    if (valor_input>valorTd){
      alert("Existe una diferencia");
      x.innerHTML = mathRound2(valor_input-valorTd);
  }
    else if (valor_input<valorTd){
      alert("Existe una diferencia");
      x.innerHTML = mathRound2(valorTd-valor_input);             
    }
  }
}

function imprSelec(muestra){
    var ficha = document.getElementById(muestra); //obtenemos el objeto a imprimir
    var ventimp = window.open(' ','popimpr'); //abrimos una ventana vacía nueva
    ventimp.document.write(ficha.innerHTML); //imprimimos el HTML del objeto en la nueva ventana
    ventimp.document.close();  //cerramos el documento
    ventimp.print(); //imprimimos la ventana
    ventimp.close(); //cerramos la ventana
}