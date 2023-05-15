from pymongo import MongoClient
from bson import ObjectId
from datetime import date, timedelta, datetime

class Conexion():
    def __init__(self):
        self.cliente=MongoClient()
        self.db=self.cliente.SalasREST

#Entrada:{
# “tipo”:String,
# “motivo”:String,
# “horaInicio”: String,
# “horaFin”: String,
# “fechaInicio”: String,
# “fechaFin”: String,
# “sala”: int
# }
#Validar que la sala donde se desea hacer la reserva esté disponible y esté activa. Para esto, se debe validar que no exista una reserva en el mismo horario, y que la fecha de inicio y fin de la reserva no se encuentre entre la fecha de inicio y fin de otra reserva.
    def agregarReserva(self,data):
        resp={"estatus":"","mensaje":""}
        datos={}
        datos["sala"]=data["sala"]
        datos["fechaInicio"]=data["fechaInicio"]
        datos["fechaFin"]=data["fechaFin"]
        datos["horaInicio"]=data["horaInicio"]
        datos["horaFin"]=data["horaFin"]
        datos["idReserva"]=""

        #print(self.consultarDisponibilidadReserva(datos))
        res=self.consultarDisponibilidadReserva(datos)
        if res["disponible"]==True:
            data["estatus"]="Activo"
            data["sala"]=ObjectId(data["sala"])
            self.db.Reservas.insert_one(data)
            resp["estatus"]="OK"
            resp["mensaje"]="Reserva registrada correctamente"
        else:
            resp["estatus"]="ERROR"
            resp["mensaje"]=res["mensaje"]
        return resp

    def consultarDisponibilidadReserva(self,data):
        resp={"estatus":"OK","mensaje":"La sala está disponible","disponible":True}
        sala=self.db.Salas.find_one({"_id":ObjectId(data["sala"]),"estatus":"Activo"})
        #convertir horaInicio y horaFin a timedelta
        horaInicio=datetime.strptime(data["horaInicio"], '%H:%M')
        horaFin=datetime.strptime(data["horaFin"], '%H:%M')
        print(data["fechaInicio"])
        if sala:
            if data["fechaInicio"]>data["fechaFin"] :
                resp["estatus"]="ERROR"
                resp["mensaje"]="La fecha de inicio no puede ser mayor a la fecha de fin"
                resp["disponible"]=False
                return resp
            elif horaInicio > horaFin: 
                resp["estatus"]="ERROR"
                resp["mensaje"]="La hora de inicio no puede ser mayor a la hora de fin"
                resp["disponible"]=False
                return resp
            elif data["fechaInicio"]<str(date.today()):
                resp["estatus"]="ERROR"
                resp["mensaje"]="La fecha de inicio no puede ser menor a la fecha actual"
                resp["disponible"]=False
                return resp
            #Solo se puede reservar entre las 7:00 y las 20:00
            elif horaInicio<datetime.strptime("07:00", '%H:%M') or horaInicio>datetime.strptime("20:00", '%H:%M') or horaFin<datetime.strptime("07:00", '%H:%M') or horaFin>datetime.strptime("20:00", '%H:%M'):
                resp["estatus"]="ERROR"
                resp["mensaje"]="La hora de inicio y fin de la reserva debe estar entre las 7:00 y las 20:00"
                resp["disponible"]=False
                return resp
            else:
                reservas=self.db.Reservas.find({"sala":ObjectId(data["sala"]),"estatus":"Activo"}) 
                for r in reservas:
                    print(r)
                    rHoraInicio=datetime.strptime(r["horaInicio"], '%H:%M')
                    rHoraFin=datetime.strptime(r["horaFin"], '%H:%M')
                    idReserva=str(r["_id"])
                    if(idReserva!=data["idReserva"]):
                        #Si la reserva no esta cancelada o finalizada y la fecha de inicio o fin de la reserva no esta entre la fecha de inicio y fin de otra reserva   
                        if r["estatus"]!="Cancelado" or r["estatus"]!="Finalizado":
                            if (data["fechaInicio"]>=r["fechaInicio"] and data["fechaInicio"]<=r["fechaFin"]) or (data["fechaFin"]>=r["fechaInicio"] and data["fechaFin"]<=r["fechaFin"]) or (data["fechaInicio"]==r["fechaInicio"] and data["fechaFin"]==r["fechaFin"]):
                                if (horaInicio>=rHoraInicio and horaInicio<=rHoraFin) or (horaFin>=rHoraInicio and horaFin<=rHoraFin) or (horaInicio<=rHoraInicio and horaFin>=rHoraFin) or (horaInicio<=rHoraInicio and horaFin>=rHoraInicio) or (horaInicio<=rHoraFin and horaFin>=rHoraFin):
                                    resp["estatus"]="ERROR"
                                    resp["mensaje"]="La sala ya está reservada en ese horario"
                                    resp["disponible"]=False
                                    sala=self.db.Salas.find_one({"_id":ObjectId(r["sala"])})
                                    resp["reserva"]={"sala":sala["nombreSala"],"tipo":r["tipo"],"motivo":r["motivo"],"fechaInicio":str(r["fechaInicio"]),"fechaFin":str(r["fechaFin"]),"horaInicio":str(r["horaInicio"]),"horaFin":str(r["horaFin"])}
                                    return resp
                            else:
                                resp["estatus"]="OK"
                                resp["mensaje"]="La sala está disponible"
                                
                        else:
                            resp["estatus"]="OK"
                            resp["mensaje"]="La sala está disponible"
                        
        else:
            resp["estatus"]="ERROR"
            resp["mensaje"]="La sala no existe o está inactiva"
            resp["disponible"]=False
        return resp
    
    def consultarReservas(self):
        resp={"estatus":"","mensaje":""}
        reservas=[]
        data=self.db.Reservas.find({})
        for d in data:
            sala=self.db.Salas.find_one({"_id":ObjectId(d["sala"])})
            d["sala"]=sala["nombreSala"]
            reservas.append({"idReserva":str(d["_id"]),"tipo":d["tipo"],"motivo":d["motivo"],"fechaInicio":str(d["fechaInicio"]),"fechaFin":str(d["fechaFin"]),"horaInicio":str(d["horaInicio"]),"horaFin":str(d["horaFin"]),"sala":d["sala"],"estatus":d["estatus"]})
        if len(reservas)>0:
            resp["estatus"]="OK"
            resp["mensaje"]="Lista de reservas"
            resp["reservas"]=reservas
        else:
            resp["estatus"]="ERROR"
            resp["mensaje"]="No hay reservas registradas"
        return resp
    
    def consultarReservaPorId(self,idReserva):
        resp={"estatus":"","mensaje":""}
        reserva=self.db.Reservas.find_one({"_id":ObjectId(idReserva)})
        if reserva:
            sala=self.db.Salas.find_one({"_id":ObjectId(reserva["sala"])})
            reserva["sala"]=sala["nombreSala"]
            resp["estatus"]="OK"
            resp["mensaje"]="Reserva encontrada"
            resp["reserva"]={"idReserva":str(reserva["_id"]),"tipo":reserva["tipo"],"motivo":reserva["motivo"],"fechaInicio":str(reserva["fechaInicio"]),"fechaFin":str(reserva["fechaFin"]),"horaInicio":str(reserva["horaInicio"]),"horaFin":str(reserva["horaFin"]),"sala":reserva["sala"],"estatus":reserva["estatus"]}
        else:
            resp["estatus"]="ERROR"
            resp["mensaje"]="La reserva no existe"
        return resp

    def consultarSalasDisponibles(self,data):
        resp={"estatus":"","mensaje":""}
        lsalas=[]
        horaInicio=datetime.strptime(data["horaInicio"], '%H:%M')
        horaFin=datetime.strptime(data["horaFin"], '%H:%M')
        if data["fechaInicio"]>data["fechaFin"] :
                resp["estatus"]="ERROR"
                resp["mensaje"]="La fecha de inicio no puede ser mayor a la fecha de fin"
                resp["disponible"]=False
                return resp
        elif horaInicio > horaFin: 
                resp["estatus"]="ERROR"
                resp["mensaje"]="La hora de inicio no puede ser mayor a la hora de fin"
                resp["disponible"]=False
                return resp
        elif data["fechaInicio"]<str(date.today()):
                resp["estatus"]="ERROR"
                resp["mensaje"]="La fecha de inicio no puede ser menor a la fecha actual"
                resp["disponible"]=False
                return resp
        #Solo se puede reservar entre las 7:00 y las 20:00
        elif horaInicio<datetime.strptime("07:00", '%H:%M') or horaInicio>datetime.strptime("20:00", '%H:%M') or horaFin<datetime.strptime("07:00", '%H:%M') or horaFin>datetime.strptime("20:00", '%H:%M'):
                resp["estatus"]="ERROR"
                resp["mensaje"]="La hora de inicio y fin de la reserva debe estar entre las 7:00 y las 20:00"
                resp["disponible"]=False
                return resp
        else:
            salas=self.db.Salas.find({"estatus":"Activo"})
            for s in salas:
                respSala=self.consultarDisponibilidadReserva({"sala":str(s["_id"]),"horaInicio":data["horaInicio"],"horaFin":data["horaFin"],"fechaInicio":data["fechaInicio"],"fechaFin":data["fechaFin"],"idReserva":""})
                if respSala["disponible"]==True:
                    lsalas.append({"idSala":str(s["_id"]),"nombreSala":s["nombreSala"]})
            if len(lsalas)>0:
                resp["estatus"]="OK"
                resp["mensaje"]="Lista de salas disponibles"
                resp["salas"]=lsalas
            else:
                resp["estatus"]="ERROR"
                resp["mensaje"]="No hay salas disponibles"
        return resp

    def modificarReserva(self,data):
        resp={"estatus":"","mensaje":""}
        reserva=self.db.Reservas.find_one({"_id":ObjectId(data["idReserva"]),"estatus":"Activo"})
        datos={}
        datos["sala"]=data["sala"]
        datos["fechaInicio"]=data["fechaInicio"]
        datos["fechaFin"]=data["fechaFin"]
        datos["horaInicio"]=data["horaInicio"]
        datos["horaFin"]=data["horaFin"]
        datos["idReserva"]=data["idReserva"]

        if reserva:
            res=self.consultarDisponibilidadReserva(datos)
            if res["disponible"]==True:
                data["estatus"]="Activo"
                data["sala"]=ObjectId(data["sala"])
                self.db.Reservas.update_one({"_id":ObjectId(data["idReserva"])},{"$set":{"tipo":data["tipo"],"motivo":data["motivo"],"horaInicio":data["horaInicio"],"horaFin":data["horaFin"],"fechaInicio":data["fechaInicio"],"fechaFin":data["fechaFin"],"sala":data["sala"]}})
                resp["estatus"]="OK"
                resp["mensaje"]="Reserva actualizada correctamente"
            else:
                resp["estatus"]="ERROR"
                resp["mensaje"]=res["mensaje"]
        else:
            resp["estatus"]="ERROR"
            resp["mensaje"]="La reserva no existe o ya está cancelada o finalizada"
        return resp



    def eliminarReserva(self,id):
        resp={"estatus":"","mensaje":""}
        reserva=self.db.Reservas.find_one({"_id":ObjectId(id),"estatus":"Activo"})
        if reserva:
            self.db.Reservas.update_one({"_id":ObjectId(id)},{"$set":{"estatus":"Cancelado"}})
            resp["estatus"]="OK"
            resp["mensaje"]="Reserva cancelada correctamente"
        else:
            resp["estatus"]="ERROR"
            resp["mensaje"]="La reserva no existe o ya está cancelada o finalizada"
        return resp
