#coding=latin-1
from bottle import Bottle, route, run, response, hook, request, static_file
from dbserver import DBServer
from json import dumps


Rafam = Bottle()

@Rafam.route('/<:re:.*>', method='OPTIONS')
def dummy():
    return


@Rafam.route('/devolverCuentas',method='POST')
def devolverCuentas():
    db = DBServer()

    ejercicio = request.json['ejercicio']

    orden = "Select cuenta,nro_cuenta,num_sucursal from cta_cuentas\
         where ejercicio = {} and cod_banco = 'BP'\
        order by cuenta DESC "
    datos = db.contestarQuery(orden.format(ejercicio))

    datosFinales = []
    for cuenta in datos:
        datosFinales.append({
            'nro_cuenta':cuenta[0],
            'cuenta':cuenta[1],
            'sucursal':cuenta[2],
        })

    return dumps(datosFinales)

