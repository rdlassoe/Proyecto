from flask import Flask, jsonify
from flask_pymongo import PyMongo
from controllers import tarea_bp, venta_bp
from models import TareaModel, SuperModel
from pymongo import MongoClient


app = Flask(__name__)

# Configuración de la base de datos
client = MongoClient("mongodb://localhost:27017/")
#app.config["MONGO_URI"] = "mongodb://localhost:27017/tareas"
dbtareas = client["tareas"]
dbsupermarket = client["supermarket"]

# mongo = PyMongo(app)

#Inicializar el modelo con la colección 'usuarios'
# TareaModel.init(mongo)
# SuperModel.init(mongo)


#Registrar el blueprint
app.register_blueprint(tarea_bp)
app.register_blueprint(venta_bp)


# @app.route("/")
# def index():
#     return "API Flask + MongoDB funcionando en la colección 'tarea'"

@app.route("/home")
def home():
    tarea = list(dbtareas["tarea"].find({}, {"_id": 0}))
    ventas = list(dbsupermarket["ventas"].find({}, {"_id": 0}))
    return jsonify({
        "tareas": tarea,
        "supermarket": ventas
    })

if __name__ == "__main__":
    app.run(debug=True)



@app.route("/pipeline")
def consulta():
    pipeline = [
        {
            "$unwind": "$items"
        },
        {
            "$lookup": {
                "from": "productos",
                "localField": "items.producto_id",
                "foreignField": "_id",
                "as": "producto"
            }
        },
        {
            "$unwind": "$producto"
        },
        {
            "$group": {
                "_id": "$_id",
                "cliente_id": {"$first": "$cliente_id"},
                "fecha": {"$first": "$fecha"},
                "total": {"$first": "$total"},
                "productos": {
                    "$push": {
                        "nombre": "$producto.nombre",
                        "precio": "$producto.precio",
                        "cantidad": "$items.cantidad"
                    }
                }
            }
        },
        {
            "$project": {
                "cliente_id": 1,
                "fecha": 1,
                "total": 1,
                "productos": 1
            }
        }
    ]

    resultado = list(dbsupermarket["ventas"].aggregate(pipeline))
    return jsonify(resultado)
