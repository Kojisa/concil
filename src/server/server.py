from bottle import Bottle, route, run, response, hook, request, static_file
import paste
import bottle
import dbserver
import obtenerDatos
import impactarExtracto
from json import dumps

default = Bottle()


bottle.BaseRequest.MEMFILE_MAX = (1024 * 1024) * 3 #maximo 3mb


@default.hook('after_request')
def enable_cors():
    """
    You need to add some headers to each request.
    Don't use the wildcard '*' for Access-Control-Allow-Origin in production.
    """
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'PUT, GET, POST, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'



@default.route('/<:re:.*>', method='OPTIONS')
def dummy():
    return


#ejemplo para importar modulos 'ruta principal', modulo)
#default.mount('/modulo',modulo.modulo)

default.mount('/datos',obtenerDatos.Rafam)

@default.route('/extracto/impactar',method='POST')
def impactar():
    datos = request.json
    entrada = datos['entrada']
    desde = datos['desde']
    hasta = datos['hasta']
    cuentabanco = datos['cuentabancaria']
    cuentacontable = datos['cuentacontable']
    sucursal = datos['sucursal']

    nro = impactarExtracto.guardarExtracto(entrada,desde,hasta,cuentabanco,cuentacontable,sucursal)
    return dumps(nro)

@default.route('/static/<tipo>/<modulo>')
def devolverStatic(tipo,modulo):
    return static_file(modulo,root="../../build/static/"+tipo)

@default.route('/<modulo>')
def devolverModulo(modulo):
    return static_file(modulo,root="../../build/")

@default.route('/')
def devolverPagina():
    return static_file("index.html",root="../../build/")

run(default,host = '0.0.0.0', port = 1700)
