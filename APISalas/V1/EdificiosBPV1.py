from flask import Blueprint, request
from V1.modelEdificios import Conexion
from flask_httpauth import HTTPBasicAuth

edificiosBP=Blueprint('EdificiosBP',__name__)

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

#Registrar un edificio
@edificiosBP.route('/Edificios/v1',methods=['POST'])
@auth.login_required(role='A')
def registrarEdificio():
    data=request.get_json()
    conexion=Conexion()
    resp=conexion.registrarEdificio(data)
    return resp

#Consultar edificios
@edificiosBP.route('/Edificios/v1',methods=['GET'])
@auth.login_required(role=['A','E','D'])
def consultarEdificios():
    conexion=Conexion()
    resp=conexion.consultarEdificios()
    return resp

#Consultar edificio por id
@edificiosBP.route('/Edificios/v1/<id>',methods=['GET'])
@auth.login_required(role=['A','E','D'])
def consultarEdificioPorId(id):
    conexion=Conexion()
    resp=conexion.consultarEdificioPorId(id)
    return resp

#Modificar edificio
@edificiosBP.route('/Edificios/v1',methods=['PUT'])
@auth.login_required(role='A')
def modificarEdificio():
    data=request.get_json()
    conexion=Conexion()
    resp=conexion.modificarEdificio(data)
    return resp

#Dar de baja un edificio
@edificiosBP.route('/Edificios/v1/<id>',methods=['PUT'])
@auth.login_required(role='A')
def darDeBajaEdificio(id):
    conexion=Conexion()
    resp=conexion.darDeBajaEdificio(id)
    return resp