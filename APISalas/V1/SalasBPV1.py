from flask import Blueprint, request
from V1.modelSalas import Conexion

salasBP=Blueprint('SalasBP',__name__)

#Registrar una sala
@salasBP.route('/Salas/v1',methods=['POST'])
def registrarSala():
    data=request.get_json()
    conexion=Conexion()
    resp=conexion.registrarSala(data)
    return resp

#Consultar salas
@salasBP.route('/Salas/v1',methods=['GET'])
def consultarSalas():
    conexion=Conexion()
    resp=conexion.consultarSalas()
    return resp

#Consultar sala por id
@salasBP.route('/Salas/v1/<id>',methods=['GET'])
def consultarSalaPorId(id):
    conexion=Conexion()
    resp=conexion.consultarSalaPorId(id)
    return resp

#Consultar salas por edificio
@salasBP.route('/Salas/v1/Edificio/<id>',methods=['GET'])
def consultarSalasPorEdificio(id):
    conexion=Conexion()
    resp=conexion.consultarSalasPorEdificio(id)
    return resp

#Modificar sala
@salasBP.route('/Salas/v1',methods=['PUT'])
def modificarSala():
    data=request.get_json()
    conexion=Conexion()
    resp=conexion.modificarSala(data)
    return resp

#Dar de baja una sala
@salasBP.route('/Salas/v1/<id>',methods=['PUT'])
def darDeBajaSala(id):
    conexion=Conexion()
    resp=conexion.eliminarSala(id)
    return resp

#Agregar mobiliario a una sala
@salasBP.route('/Salas/v1/Mobiliario/<id>',methods=['PUT'])
def agregarMobiliario(id):
    data=request.get_json()
    conexion=Conexion()
    resp=conexion.agregarMobiliarioASala(id,data)
    return resp

#Editar mobiliario de una sala
@salasBP.route('/Salas/v1/Mobiliario/Editar/<id>',methods=['PUT'])
def editarMobiliario(id):
    data=request.get_json()
    conexion=Conexion()
    resp=conexion.editarMobiliarioSala(id,data)
    return resp

#Eliminar mobiliario de una sala
@salasBP.route('/Salas/v1/Mobiliario/Eliminar/<id>',methods=['PUT'])
def eliminarMobiliario(id):
    data=request.get_json()
    conexion=Conexion()
    resp=conexion.eliminarMobiliarioSala(id,data)
    return resp