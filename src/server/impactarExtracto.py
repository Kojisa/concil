import datetime
from dbserver import DBServer
from json import dumps

EQUIVALENCIAS = {
    'CHEQUE POR VENTANILLA ':'CM',
    'CHEQUE DE CAMARA ' :'CM',
    'BIP CR TR ':'CRED',
    'BIP DB TR ':'EB',
    'BIP DB.TR.':'EB'
}

POSFECHA = 0
POSTIPO = 1
MONTO = 2
FECHACORTA = 3
ESTADOCAJA = 4


def _leerArchivo(entrada,resumen,hasta,salida):

    db = DBServer()

    lista = []

    ordenTipos = "SELECT COMPROB_TIPO,ABREV_BANCARIA FROM TES_TIPO_MOVIMIENTOS_CONC WHERE CODIGO = '{}'"

    orden = 'INSERT INTO TES_RESUMENES_BANCARIOS_MOV(NUMERO,FECHA,ORDEN,COMPROB_TIPO,COMPROB_NRO,COD_MOV,DEBITO,CREDITO,SALDO,ESTADO,ORIGEN_TIPO,ORIGEN_NRO,FECHA_CONCILIA)\
    VALUES({resumen},TO_DATE(\'{fecha}\',\'DD/MM/YYYY\'),{indice},\'{tipo}\',{comprobantenro},\'{tipomov}\',{debito},{credito},0,\'N\',\'{codbanco}\',{valorextra},NULL)'
    
    saldoanterior = 0

    indice = 0
    for linearaw in entrada:
        indice += 1
        if(indice < 11):
            continue

        dic = {}
        linea = linearaw.split(',')
        if(len(linea) <= 1):
            continue

        if(linea[POSTIPO] == 'SALDO ANTERIOR'):
            saldoanterior = float(linea[ESTADOCAJA])
            continue

        fecha = linea[POSFECHA]

        fechaObj = datetime.datetime.strptime(fecha,'%d/%m/%Y')
        if(fechaObj > datetime.datetime.strptime(hasta,'%d/%m/%Y')):
            continue 


        signo = linea[MONTO][0]
        monto = linea[MONTO].replace('-','')
        tipo = linea[POSTIPO]

        #comparo los tipos exclusivos
        for clave in EQUIVALENCIAS.keys():

            if(clave in tipo):

                if(EQUIVALENCIAS[clave] == 'CM'):
                    valorExtra = tipo[len(clave):len(clave) + 9].replace('\n','').replace(' ','')
                    comprobantenro = valorExtra

                elif(clave == 'BIP DB.TR.'):
                    valorExtra = tipo[len(clave)+8:len(clave)+15].replace(' ','')
                    comprobantenro = valorExtra

                else:
                    valorExtra = tipo[len(clave)+8:len(clave)+20].replace('\n','')
                    comprobantenro = valorExtra

                equivalencia = EQUIVALENCIAS[clave]
                break
            else:

                if(signo == '-'):
                    equivalencia = 'DEB'
                else:
                    equivalencia = 'CRED'

                comprobantenro = indice
                valorExtra = indice
        
        tipo,codbanco = db.contestarQuery(ordenTipos.format(equivalencia))[0]

        dic['fecha'] = fecha
        debito,credito = (monto,0) if signo == '-' else (0,monto)
        dic['debito'] = float(debito)
        dic['credito'] = float(credito)
        dic['indice'] = indice
        dic['resumen'] = resumen
        dic['tipo'] = tipo
        dic['codbanco'] = codbanco
        dic['valorextra'] = valorExtra
        dic['tipomov'] = equivalencia
        dic['comprobantenro'] = comprobantenro

        salida.write(orden.format(**dic) + '\n')
        db.contestarQuery(orden.format(**dic),None,False)
        db.aceptarCambios()

        lista.append(orden.format(**dic))

    db.desconectar()
    return lista,saldoanterior


def _generarCabecera(desde,hasta,cuentabanco,cuentacontable,sucursal,salida):

    db = DBServer()

    ordenConsulta = "select numero from tes_resumenes_bancarios where numero like '{}{}%' order by numero DESC".format(desde[8:],desde[3:5])
    nroresumen = db.contestarQuery(ordenConsulta)
    print nroresumen
    nroBase = int('{}{}000'.format(desde[8:], desde[3:5]))
    if(len(nroresumen ) < 1):
        nroresumen = int('{}{}001'.format(desde[8:],desde[3:5]))
    else:
        if(nroresumen[0][0] > 1000000):
            nroresumen = nroresumen[0][0] + 1
        else:
            nroresumen = int('{}{}001'.format(desde[8:],desde[3:5]))

    ordenCabecera = "INSERT INTO TES_RESUMENES_BANCARIOS( NUMERO, FECHA, PERIODO1, PERIODO2, BANCO, SUCURSAL, CUENTA, CUENTA_BAN, SALDO_ANT)\
         values({},{},TO_DATE('{}',\'DD/MM/YYYY\'),TO_DATE('{}',\'DD/MM/YYYY\'),'{}','{}','{}','{}',{})".format(nroresumen,'SYSDATE',desde,hasta,'BP',sucursal,cuentacontable,cuentabanco,0)
    
    print db.contestarQuery('select sysdate from dual')
    salida.write(ordenCabecera + '\n')
    print ordenCabecera
    db.contestarQuery(ordenCabecera,None,False)
    db.aceptarCambios()

    db.desconectar()
    return nroresumen

def _actualizarCabecera(nroresumen,saldoanterior,salida):

    db = DBServer()

    orden = 'update tes_resumenes_bancarios set saldo_ant = {} where numero = {}'.format(saldoanterior,nroresumen)
    salida.write(orden + '\n')
    db.contestarQuery(orden,None,False)
    db.aceptarCambios()

    db.desconectar()



def guardarExtracto(entrada,desde,hasta,cuentabanco,cuentacontable,sucursal):
    salida = open('salida.sql','w')
    nroresumen = _generarCabecera(desde,hasta,cuentabanco,cuentacontable,sucursal,salida)
    listado,saldoanterior = _leerArchivo(entrada,nroresumen,hasta,salida)
    _actualizarCabecera(nroresumen,saldoanterior,salida)
    salida.close()

    return nroresumen

