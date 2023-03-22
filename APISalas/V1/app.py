from flask import Flask

app=Flask(__name__)

@app.route('/',methods=['GET'])
def init():
    return "Escuchando el Servicio REST de Salas"

@app.route('/Solicitudes')
def listadoSalas():
    respuesta={"estatus":"200","mensaje":"Listado de solicitudes"}
    return respuesta

@app.route('/Solicitudes/evidencias')
def listadoEvidencias():
    respuesta={"estatus":"200","mensaje":"Listado de evidencias de las solicitudes"}
    return respuesta

@app.route('/Solicitudes/<int:id>')
def eliminarSolicitud(id):
    respuesta={"estatus":"200","mensaje":"Eliminando la solicitud con id: "+str(id)}
    return respuesta

@app.route('/Solicitudes/<string:nc>')
def consultarSolicitud(nc):
    respuesta={"estatus":"200","mensaje":"Buscando la solicitud del alumno con nc: "+str(nc)}
    return respuesta

if __name__=='__main__':
    app.run(debug=True)