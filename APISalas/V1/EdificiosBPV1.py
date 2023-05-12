from flask import Blueprint, request
from V1.modelEdificios import Conexion

edificiosBP=Blueprint('EdificiosBP',__name__)

#Registrar un edificio
@edificiosBP.route('/Edificios/v1',methods=['POST'])
def registrarEdificio():
    data=request.get_json()
    conexion=Conexion()
    resp=conexion.registrarEdificio(data)
    return resp

#Consultar edificios
@edificiosBP.route('/Edificios/v1',methods=['GET'])
def consultarEdificios():
    conexion=Conexion()
    resp=conexion.consultarEdificios()
    return resp

#Consultar edificio por id
@edificiosBP.route('/Edificios/v1/<id>',methods=['GET'])
def consultarEdificioPorId(id):
    conexion=Conexion()
    resp=conexion.consultarEdificioPorId(id)
    return resp

#Modificar edificio
@edificiosBP.route('/Edificios/v1',methods=['PUT'])
def modificarEdificio():
    data=request.get_json()
    conexion=Conexion()
    resp=conexion.modificarEdificio(data)
    return resp

#Dar de baja un edificio
@edificiosBP.route('/Edificios/v1/<id>',methods=['PUT'])
def darDeBajaEdificio(id):
    conexion=Conexion()
    resp=conexion.darDeBajaEdificio(id)
    return resp