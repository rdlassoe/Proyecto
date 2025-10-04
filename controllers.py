from flask import Blueprint, request, jsonify
from models import TareaModel, SuperModel

tarea_bp = Blueprint("tareas", __name__)
venta_bp = Blueprint("ventas", __name__)


@tarea_bp.route("/tareas", methods=["POST"])
def create_tarea():
    data = request.json
    tarea_id = TareaModel.create_tarea(data)
    return jsonify({"message": "tarea creada", "id": int(tarea_id)}), 201

@tarea_bp.route("/tareas", methods=["GET"])
def get_tareas():
    tareas = TareaModel.get_all_tarea()
    for u in tareas:
        u["_id"] = int(u["_id"])
    return jsonify(tareas)

@tarea_bp.route("/tareas/<tarea_id>", methods=["GET"])
def get_tarea(tarea_id):
    tarea = TareaModel.get_tarea(int(tarea_id))
    if tarea:
        tarea["_id"] = int(tarea["_id"])
        return jsonify(tarea)
    return jsonify({"error": "tarea no encontrada"}), 404

@tarea_bp.route("/tareas/<tarea_id>", methods=["PUT"])
def update_tarea(tarea_id):
    data = request.json
    result = TareaModel.update_tarea(tarea_id, data)
    if result.modified_count > 0:
        return jsonify({"message": "tarea actualizada"})
    return jsonify({"error": "No se actualizó ningún tarea"}), 404

@tarea_bp.route("/tareas/<tarea_id>", methods=["DELETE"])
def delete_tarea(tarea_id):
    result = TareaModel.delete_tarea(tarea_id)
    if result.deleted_count > 0:
        return jsonify({"message": "tarea eliminada"})
    return jsonify({"error": "No se eliminó ninguna tarea"}),

@tarea_bp.route("/tareas/consulta", methods=["Get"])
def Consuta ():
    tareas = TareaModel.pipeline()
    return jsonify(tareas)

@venta_bp.route("/ventas", methods=["GET"])
def get_ventas():
    ventas = SuperModel.get_all_venta()
    for u in ventas:
        u["_id"] = int(u["_id"])
    return jsonify(ventas)

