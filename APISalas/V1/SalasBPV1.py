from flask import Blueprint, request
from V1.modelSalas import Conexion
from flask_httpauth import HTTPBasicAuth

salasBP=Blueprint('SalasBP',__name__)

auth=HTTPBasicAuth()

#Autenticación
@auth.verify_password
def verify_password(username,password):
    conexion=Conexion()
    user=conexion.validarCredenciales(username,password)
    if user!=None:
        return user
    else:
        return False
    
@auth.get_user_roles
def get_user_roles(user):
    return user["tipo"]

@auth.error_handler
def error_handler():
    return {"estatus":"Error","mensaje":"No tiene autorización para realizar la ejecución de la operación"},401

#Registrar una sala
@salasBP.route('/Salas/v1',methods=['POST'])
@auth.login_required(role='A')
def registrarSala():
    data=request.get_json()
    conexion=Conexion()
    resp=conexion.registrarSala(data)
    return resp

#Consultar salas
@salasBP.route('/Salas/v1',methods=['GET'])
@auth.login_required(role=['A','E','D'])
def consultarSalas():
    conexion=Conexion()
    resp=conexion.consultarSalas()
    return resp

#Consultar sala por id
@salasBP.route('/Salas/v1/<id>',methods=['GET'])
@auth.login_required(role=['A','E','D'])
def consultarSalaPorId(id):
    conexion=Conexion()
    resp=conexion.consultarSalaPorId(id)
    return resp

#Consultar salas por edificio
@salasBP.route('/Salas/v1/Edificio/<id>',methods=['GET'])
@auth.login_required(role=['A','E','D'])
def consultarSalasPorEdificio(id):
    conexion=Conexion()
    resp=conexion.consultarSalasPorEdificio(id)
    return resp

#Modificar sala
@salasBP.route('/Salas/v1',methods=['PUT'])
@auth.login_required(role='A')
def modificarSala():
    data=request.get_json()
    conexion=Conexion()
    resp=conexion.modificarSala(data)
    return resp

#Dar de baja una sala
@salasBP.route('/Salas/v1/<id>',methods=['PUT'])
@auth.login_required(role='A')
def darDeBajaSala(id):
    conexion=Conexion()
    resp=conexion.eliminarSala(id)
    return resp

#Agregar mobiliario a una sala
@salasBP.route('/Salas/v1/Mobiliario/<id>',methods=['PUT'])
@auth.login_required(role='A')
def agregarMobiliario(id):
    data=request.get_json()
    conexion=Conexion()
    resp=conexion.agregarMobiliarioASala(id,data)
    return resp

#Editar mobiliario de una sala
@salasBP.route('/Salas/v1/Mobiliario/Editar/<id>',methods=['PUT'])
@auth.login_required(role='A')
def editarMobiliario(id):
    data=request.get_json()
    conexion=Conexion()
    resp=conexion.editarMobiliarioSala(id,data)
    return resp

#Eliminar mobiliario de una sala
@salasBP.route('/Salas/v1/Mobiliario/Eliminar/<id>',methods=['PUT'])
@auth.login_required(role='A')
def eliminarMobiliario(id):
    data=request.get_json()
    conexion=Conexion()
    resp=conexion.eliminarMobiliarioSala(id,data)
    return resp