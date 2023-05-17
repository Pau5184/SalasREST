from pymongo import MongoClient
from bson import ObjectId

class Conexion():
    def __init__(self):
        self.cliente=MongoClient()
        self.db=self.cliente.SalasREST

    def registrarEdificio(self, data):
        resp = {"estatus":"","mensaje":""}
        edificio=self.db.Edificios.find_one({"nombreEdificio":data["nombreEdificio"]})
        if edificio==None:
            data["estatus"]="Activo"
            self.db.Edificios.insert_one(data)
            resp["estatus"]="OK"
            resp["mensaje"]="Edificio registrado correctamente"
        elif edificio["estatus"]=="Inactivo":
            resp["estatus"]="ERROR"
            resp["mensaje"]="Este edificio ya existe pero está dado de baja"
        else:
            resp["estatus"]="ERROR"
            resp["mensaje"]="Este edificio ya existe, no se puede registrar"
        return resp

    def consultarEdificios(self):
        resp={"estatus":"","mensaje":""}
        edificios=self.db.Edificios.find({"estatus":"Activo"}) 
        lista=[]
        for s in edificios:
            print(s)
            lista.append({"_id":str(s["_id"]),"nombreEdificio":s["nombreEdificio"],"descripcion":s["descripcion"]})
        if len(lista)>0:
            resp["estatus"]="OK"
            resp["mensaje"]="Lista de edificios"
            resp["edificios"]=lista
        else:
            resp["estatus"]="ERROR"
            resp["mensaje"]="No hay edificios registrados"
        return resp
    
    def consultarEdificioPorId(self, id):
        resp={"estatus":"","mensaje":""}
        edificio=self.db.Edificios.find_one({"_id":ObjectId(id)})
        if edificio:
            resp["estatus"]="OK"
            resp["mensaje"]="Edificio encontrado"
            resp["edificio"]={"_id":str(edificio["_id"]),"nombreEdificio":edificio["nombreEdificio"],"descripcion":edificio["descripcion"]}
        else:
            resp["estatus"]="ERROR"
            resp["mensaje"]="Edificio no encontrado"
        return resp

#Para modificar un edificio se debe validar que el edificio exista y que esté activo
    def modificarEdificio(self, data):
        resp={"estatus":"","mensaje":""}
        edificio=self.db.Edificios.find_one({"_id":ObjectId(data["idEdificio"])})
        if edificio:
            if edificio["estatus"]=="Activo":
                self.db.Edificios.update_one({"_id":ObjectId(data["idEdificio"])},{"$set":{"nombreEdificio":data["nombre"],"descripcion":data["descripcion"]}})
                resp["estatus"]="OK"
                resp["mensaje"]="Edificio modificado correctamente"
            else:
                resp["estatus"]="ERROR"
                resp["mensaje"]="Este edificio está dado de baja, no se puede modificar"
        else:
            resp["estatus"]="ERROR"
            resp["mensaje"]="Edificio no encontrado"
        return resp
    
    def darDeBajaEdificio(self, id):
        resp={"estatus":"","mensaje":""}
        edificio=self.db.Edificios.find_one({"_id":ObjectId(id)})
        if edificio:
            if edificio["estatus"]=="Activo":
                self.db.Edificios.update_one({"_id":ObjectId(id)},{"$set":{"estatus":"Inactivo"}})
                resp["estatus"]="OK"
                resp["mensaje"]="Edificio dado de baja correctamente"
            else:
                resp["estatus"]="ERROR"
                resp["mensaje"]="Este edificio ya está dado de baja"
        else:
            resp["estatus"]="ERROR"
            resp["mensaje"]="Edificio no encontrado"
        return resp
    
    def validarCredenciales(self,usuario,password):
        user=self.db.Usuarios.find_one({"email":usuario,"password":password,"estatus":"A"})
        if user:
            return user
        else:
            return None

    
            