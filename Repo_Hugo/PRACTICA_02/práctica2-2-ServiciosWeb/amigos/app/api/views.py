from flask import request, abort, jsonify
from .. import db
from . import api
from ..models import Amigo

@api.route("/amigo/<int:id>")
def get_amigo(id):
    """
    Retorna JSON con información sobre el amigo cuyo id recibe como parámetro
    o un error 404 si no lo encuentra.
    """
    amigo = Amigo.query.get_or_404(id)
    amigodict = {'id': amigo.id, 'name': amigo.name,
                 'lati': amigo.lati, 'longi': amigo.longi}
    return jsonify(amigodict)
