from flask import Blueprint, request
from V1.modelReservas import Conexion
from flask_httpauth import HTTPBasicAuth

reservasBP=Blueprint('ReservasBP',__name__)

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

#Registrar una reserva
@reservasBP.route('/Reservas/v1',methods=['POST'])
@auth.login_required(role=['A','E'])
def agregarReserva():
    data=request.get_json()
    conexion=Conexion()
    resp=conexion.agregarReserva(data)
    return resp

#Consultar disponibilidad de una reserva
@reservasBP.route('/Reservas/v1/Disponibilidad',methods=['GET'])
@auth.login_required(role=['A','E','D'])
def consultarDisponibilidadReserva():
    data=request.get_json()
    conexion=Conexion()
    resp=conexion.consultarDisponibilidadReserva(data)
    return resp

#Consultar reservas
@reservasBP.route('/Reservas/v1',methods=['GET'])
@auth.login_required(role=['A','E','D'])
def consultarReservas():
    conexion=Conexion()
    resp=conexion.consultarReservas()
    return resp

#Consultar reserva por id
@reservasBP.route('/Reservas/v1/<id>',methods=['GET'])
@auth.login_required(role=['A','E','D'])
def consultarReservaPorId(id):
    conexion=Conexion()
    resp=conexion.consultarReservaPorId(id)
    return resp

#Consultar salas disponibles por fecha y hora
@reservasBP.route('/Reservas/v1/SalasDisponibles',methods=['GET'])
@auth.login_required(role=['A','E','D'])
def consultarSalasDisponibles():
    data=request.get_json()
    conexion=Conexion()
    resp=conexion.consultarSalasDisponibles(data)
    return resp

#Modificar reserva
@reservasBP.route('/Reservas/v1',methods=['PUT'])
@auth.login_required(role=['A','E'])
def modificarReserva():
    data=request.get_json()
    conexion=Conexion()
    resp=conexion.modificarReserva(data)
    return resp

#Eliminar reserva
@reservasBP.route('/Reservas/v1/<id>',methods=['PUT'])
@auth.login_required(role=['A','E'])
def eliminarReserva(id):
    conexion=Conexion()
    resp=conexion.eliminarReserva(id)
    return resp