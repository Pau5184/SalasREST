from flask import Blueprint, request
from V1.modelReservas import Conexion

reservasBP=Blueprint('ReservasBP',__name__)

#Registrar una reserva
@reservasBP.route('/Reservas/v1',methods=['POST'])
def agregarReserva():
    data=request.get_json()
    conexion=Conexion()
    resp=conexion.agregarReserva(data)
    return resp

#Consultar disponibilidad de una reserva
@reservasBP.route('/Reservas/v1/Disponibilidad',methods=['GET'])
def consultarDisponibilidadReserva():
    data=request.get_json()
    conexion=Conexion()
    resp=conexion.consultarDisponibilidadReserva(data)
    return resp

#Consultar reservas
@reservasBP.route('/Reservas/v1',methods=['GET'])
def consultarReservas():
    conexion=Conexion()
    resp=conexion.consultarReservas()
    return resp

#Consultar reserva por id
@reservasBP.route('/Reservas/v1/<id>',methods=['GET'])
def consultarReservaPorId(id):
    conexion=Conexion()
    resp=conexion.consultarReservaPorId(id)
    return resp

#Consultar salas disponibles por fecha y hora
@reservasBP.route('/Reservas/v1/SalasDisponibles',methods=['GET'])
def consultarSalasDisponibles():
    data=request.get_json()
    conexion=Conexion()
    resp=conexion.consultarSalasDisponibles(data)
    return resp

#Modificar reserva
@reservasBP.route('/Reservas/v1',methods=['PUT'])
def modificarReserva():
    data=request.get_json()
    conexion=Conexion()
    resp=conexion.modificarReserva(data)
    return resp

#Eliminar reserva
@reservasBP.route('/Reservas/v1/<id>',methods=['PUT'])
def eliminarReserva(id):
    conexion=Conexion()
    resp=conexion.eliminarReserva(id)
    return resp