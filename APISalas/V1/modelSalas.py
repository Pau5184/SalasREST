from pymongo import MongoClient
from bson import ObjectId

class Conexion():
    def __init__(self):
        self.cliente=MongoClient()
        self.db=self.cliente.SalasREST

    def registrarSala(self,data):
        resp={"estatus":"","mensaje":""}
        edificio=self.db.Edificios.find_one({"nombreEdificio":data["edificio"]})
        if edificio:
            if edificio["estatus"]=="Activo":
                sala=self.db.Salas.find_one({"nombreSala":data["nombreSala"]})
                if sala==None:
                    data["estatus"]="Activo"
                    data["edificio"]=edificio["_id"]
                    self.db.Salas.insert_one(data)
                    resp["estatus"]="OK"
                    resp["mensaje"]="Sala registrada correctamente"
                elif sala["estatus"]=="Inactivo":
                    resp["estatus"]="ERROR"
                    resp["mensaje"]="Esta sala ya existe pero está dada de baja"
                else:
                    resp["estatus"]="ERROR"
                    resp["mensaje"]="Esta sala ya existe, no se puede registrar"
            else:
                resp["estatus"]="ERROR"
                resp["mensaje"]="El edificio está inactivo, no se puede registrar la sala"
        else:
            resp["estatus"]="ERROR"
            resp["mensaje"]="El edificio no existe, no se puede registrar la sala"
        return resp
    
    def consultarSalas(self):
        resp={"estatus":"","mensaje":""}
        salas=self.db.Salas.find({"estatus":"Activo"})
        lista=[]
        for s in salas:
            edificio=self.db.Edificios.find_one({"_id":ObjectId(s["edificio"])})
            if edificio:
                lista.append({"_id":str(s["_id"]),"nombreSala":s["nombreSala"],"descripcion":s["descripcion"],"capacidad":s["capacidad"],"edificio":edificio["nombreEdificio"],"mobiliario":s["mobiliario"]})
        if len(lista)>0:
            resp["estatus"]="OK"
            resp["mensaje"]="Lista de salas"
            resp["salas"]=lista
        else:
            resp["estatus"]="ERROR"
            resp["mensaje"]="No hay salas registradas"
        return resp   

    def consultarSalaPorId(self, id):
        resp={"estatus":"","mensaje":""}
        sala=self.db.Salas.find_one({"_id":ObjectId(id),"estatus":"Activo"})
        if sala:
            edificio=self.db.Edificios.find_one({"_id":ObjectId(sala["edificio"])})

            resp["estatus"]="OK"
            resp["mensaje"]="Sala encontrada"
            resp["sala"]={"_id":str(sala["_id"]),"nombreSala":sala["nombreSala"],"descripcion":sala["descripcion"],"capacidad":sala["capacidad"],"edificio":edificio["nombreEdificio"],"mobiliario":sala["mobiliario"]}
        else:
            resp["estatus"]="ERROR"
            resp["mensaje"]="La sala no existe o está dada de baja"
        return resp
    
    def consultarSalasPorEdificio(self, idEdificio):
        resp={"estatus":"","mensaje":""}
        edificio=self.db.Edificios.find_one({"_id":ObjectId(idEdificio),"estatus":"Activo"})
        if edificio:
            salas=self.db.Salas.find({"edificio":ObjectId(idEdificio),"estatus":"Activo"})
            lista=[]
            for s in salas:
                lista.append({"_id":str(s["_id"]),"nombreSala":s["nombreSala"],"descripcion":s["descripcion"],"capacidad":s["capacidad"]})
            if len(lista)>0:
                resp["estatus"]="OK"
                resp["mensaje"]="Lista de salas del edificio: " + edificio["nombreEdificio"]
                resp["salas"]=lista
            else:
                resp["estatus"]="ERROR"
                resp["mensaje"]="No hay salas registradas en este edificio"
        else:
            resp["estatus"]="ERROR"
            resp["mensaje"]="El edificio no existe o está inactivo"
        return resp

    def modificarSala(self,data):
        resp={"estatus":"","mensaje":""}
        sala=self.db.Salas.find_one({"_id":ObjectId(data["idSala"]),"estatus":"Activo"})
        if sala:
            self.db.Salas.update_one({"_id":ObjectId(data["idSala"])},{"$set":{"nombreSala":data["nombreSala"],"descripcion":data["descripcion"],"capacidad":data["capacidad"]}})
            resp["estatus"]="OK"
            resp["mensaje"]="Sala modificada correctamente"
        else:
            resp["estatus"]="ERROR"
            resp["mensaje"]="La sala no existe o está dada de baja"
        return resp

    def eliminarSala(self,id):
        resp={"estatus":"","mensaje":""}
        sala=self.db.Salas.find_one({"_id":ObjectId(id),"estatus":"Activo"})
        if sala:
            self.db.Salas.update_one({"_id":ObjectId(id)},{"$set":{"estatus":"Inactivo"}})
            resp["estatus"]="OK"
            resp["mensaje"]="Sala eliminada correctamente"
        else:
            resp["estatus"]="ERROR"
            resp["mensaje"]="La sala no existe o ya está dada de baja"
        return resp

    def agregarMobiliarioASala(self,id,data):
        resp={"estatus":"","mensaje":""}
        sala=self.db.Salas.find_one({"_id":ObjectId(id),"estatus":"Activo"})
        if sala:
            mobiliario=self.db.Salas.find_one({"mobiliario":{ "$elemMatch": {"numModelo": data["numModelo"]}}})
            if mobiliario:
                resp["estatus"]="ERROR"
                resp["mensaje"]="El mobiliario ya existe en la sala"
            else:
                self.db.Salas.update_one({"_id":ObjectId(id)},{"$push":{"mobiliario":data}})
                resp["estatus"]="OK"
                resp["mensaje"]="Mobiliario agregado correctamente"
        else:
            resp["estatus"]="ERROR"
            resp["mensaje"]="La sala no existe o está inactiva"
        return resp
    
    def editarMobiliarioSala(self,id,data):
        resp={"estatus":"","mensaje":""}
        sala=self.db.Salas.find_one({"_id":ObjectId(id),"estatus":"Activo"})
        if sala:
            mobiliario=self.db.Salas.find_one({"mobiliario":{ "$elemMatch": { "numModelo": data["numModelo"]}}})
            if mobiliario:
                self.db.Salas.update_one({"_id":ObjectId(id),"mobiliario.numModelo":data["numModelo"]},{"$set":{"mobiliario.$.nombre":data["nombre"],"mobiliario.$.descripcion":data["descripcion"],"mobiliario.$.cantidad":data["cantidad"]}}) 
                resp["estatus"]="OK"
                resp["mensaje"]="Mobiliario editado correctamente"
            else:
                resp["estatus"]="ERROR"
                resp["mensaje"]="El mobiliario no existe en la sala"
        else:
            resp["estatus"]="ERROR"
            resp["mensaje"]="La sala no existe o está inactiva"
        return resp
    
    def eliminarMobiliarioSala(self,id,data):
        resp={"estatus":"","mensaje":""}
        sala=self.db.Salas.find_one({"_id":ObjectId(id),"estatus":"Activo"})
        if sala:
            mobiliario=self.db.Salas.find_one({"mobiliario":{ "$elemMatch": { "numModelo": data["numModelo"]}}})
            if mobiliario:
                self.db.Salas.update_one({"_id":ObjectId(id)},{"$pull":{"mobiliario":{"numModelo":data["numModelo"]}}})
                resp["estatus"]="OK"
                resp["mensaje"]="Mobiliario eliminado correctamente"
            else:
                resp["estatus"]="ERROR"
                resp["mensaje"]="El mobiliario no existe en la sala"
        else:
            resp["estatus"]="ERROR"
            resp["mensaje"]="La sala no existe o está inactiva"
        return resp
