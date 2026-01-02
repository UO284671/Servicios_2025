from flask import Blueprint, request, jsonify, abort
from app import db
from app.models import Amigo, get_all_devices
from app import fcm # Importamos nuestro nuevo módulo

api = Blueprint("api", __name__)

@api.route("/amigos", methods=["GET"])
def get_amigos():
    amigos = Amigo.query.all()
    amigos_list = [a.to_dict() for a in amigos]
    return jsonify(amigos_list)

@api.route("/amigo/<int:id>", methods=["GET"])
def get_amigo(id):
    amigo = Amigo.query.get_or_404(id)
    return jsonify(amigo.to_dict())

@api.route("/amigo/byName/<string:name>", methods=["GET"])
def get_amigo_by_name(name):
    amigo = Amigo.query.filter_by(name=name).first_or_404()
    return jsonify(amigo.to_dict())

@api.route("/amigo/<int:id>", methods=["PUT"])
def edit_amigo(id):
    amigo = Amigo.query.get_or_404(id)

    if not request.json:
        abort(422, "No se ha enviado JSON")

    name = request.json.get("name")
    lati = request.json.get("lati")
    longi = request.json.get("longi")
    device = request.json.get("device") # Token FCM

    cambio_posicion = False

    if name:
        amigo.name = name
    if lati:
        amigo.lati = lati
        cambio_posicion = True
    if longi:
        amigo.longi = longi
        cambio_posicion = True
    if device:
        amigo.device = device

    if name or lati or longi or device:
        db.session.commit()
        
        # --- NOTIFICACIÓN AUTOMÁTICA ---
        # Si ha cambiado la posición, avisamos a todos
        if cambio_posicion:
            try:
                tokens = get_all_devices()
                fcm.notificar_amigos(tokens, f"¡{amigo.name} se ha movido!")
            except Exception as e:
                print(f"Error notificando: {e}")
        # -------------------------------

    # Retornamos el diccionario completo incuyendo device para verificar
    datos = amigo.to_dict()
    datos['device'] = amigo.device
    return jsonify(datos)