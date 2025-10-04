from bson.objectid import ObjectId

class TareaModel:
    """
    Modelo de dominio para la colección 'usuarios' en MongoDB.
    Implementa operaciones CRUD usando métodos estáticos.
    """
    collection = None  # atributo de clase que guardará la referencia a la colección

    @staticmethod
    def init(mongo):
        TareaModel.collection = mongo.db.tarea

    @staticmethod
    def create_tarea(data):
        return TareaModel.collection.insert_one(dexitata).inserted_id

    @staticmethod
    def get_all_tarea():
        return list(TareaModel.collection.find())

    @staticmethod
    def get_tarea(tarea_id:int):
        return TareaModel.collection.find_one({"_id": tarea_id})

    @staticmethod
    def update_tarea(tarea_id:int, data):
        return TareaModel.collection.update_one(
            {"_id": tarea_id},
            {"$set": data}
        )

    @staticmethod
    def delete_tarea(tarea_id:int):
        return TareaModel.collection.delete_one({"_id":tarea_id})

    @staticmethod
    def pipeline():
        pipeline = [
            {"$lookup":{"from":"proyecto","localField":"id_proyecto",
            "foreignField":"_id",
            "as":"proyNombre"}},
            {"$unwind":"$proyNombre"},
            {"$lookup":{"from":"responsable","localField":"id_responsable",
            "foreignField":"_id",
            "as":"respoNombre"}},
            {"$unwind":"$respoNombre"},
            {"$lookup":{"from":"responsable","localField":"id_responsable"
            ,"foreignField":"_id",
            "as":"respoApellido"}},
            {"$unwind":"$respoApellido"},
            {"$lookup":{"from":"responsable","localField":"id_responsable",
            "foreignField":"_id",
            "as":"respoEdad"}},
            {"$unwind":"$respoEdad"},
            {"$lookup":{
                "from":"estado_tarea","localField":"id_estado_tarea","foreignField":"_id",
                "as":"estado"}},
                {"$unwind":"$estado"},{"$project":
                {"_id":0,
                "nombre_tarea":1,
                "estado":"$estado.estado_tarea",
                "proyNombre":"$proyNombre.nombre_proyecto",
                "respoNombre":"$respoNombre.nombre_responsable",
                "respoApellido":"$respoApellido.apellido_responsable",
                "respoEdad":"$respoEdad.edad",
                "grupo_etareo":{
                    "$cond":{
                        "if":{
                            "$and":[
                                {"$gt":["$respoEdad.edad",17]},{"$lte":["$respoEdad.edad",30]}]},
                                "then":"Adulto Joven",
                                "else":{
                                    "$cond":{
                                        "if":{
                                            "$and":[
                                                {"$gt":["$respoEdad.edad",30]},{"$lte":["$respoEdad.edad",50]}]},
                                                "then":"Adulto Medio",
                                                "else":"Adulto Mayor"}}}}}},
                                                #{"$match":{
                                                    #"$and":[
                                                        #{"respoEdad":{"$gt":30}},{"respoEdad":{"$lte":50}}]}},
                                                        #{"$match":
                                                        #{
                                                            #"$or":[
                                                        #{"respoEdad":{"$lte":25}},{"respoEdad":{"$lte":55}}]
                                                        #}},
                                                        {"$sort":{
                                                            "respoNombre":1}}
        ]
        return list(TareaModel.collection.aggregate(pipeline))



class SuperModel:

    collection = None  

    @staticmethod
    def init(mongo):
        SuperModel.collection = mongo.db.venta

    @staticmethod
    def get_all_venta():
        return list(SuperModel.collection.find())

    