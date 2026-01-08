from flask import Blueprint, render_template, request, redirect, url_for
from app import db
from app.models import Amigo, get_all_devices
from app import fcm

html = Blueprint("html", __name__)

# 1. Listar amigos
@html.route("/amigos")
def amigos():
    lista = Amigo.query.all()
    return render_template("tabla_amigos.html", amigos=lista)

# 2. Mostrar formulario para CREAR (GET)
@html.route("/new_amigo/")
def amigo_add():
    # Renderiza la plantilla vacía
    return render_template("edit_amigo.html", amigo=None)

# 3. Mostrar formulario para EDITAR (GET)
@html.route("/edit_amigo/<int:id>")
def amigo_edit(id):
    amigo = Amigo.query.get_or_404(id)
    return render_template("edit_amigo.html", amigo=amigo)

# 4. GUARDAR (POST) - ¡ESTA ES LA QUE FALTABA!
# Tu HTML envía aquí los datos tanto al crear como al editar
@html.route("/save_amigo", methods=["POST"])
def save_amigo():
    id = request.form.get("id") # Campo oculto en el HTML
    name = request.form["name"]
    lati = request.form["lati"]
    longi = request.form["longi"]

    if id:
        # --- ES UNA EDICIÓN ---
        amigo = Amigo.query.get_or_404(id)
        
        # Guardamos datos viejos para detectar movimiento
        lat_old = amigo.lati
        long_old = amigo.longi
        
        # Actualizamos
        amigo.name = name
        amigo.lati = lati
        amigo.longi = longi
        db.session.commit()

        # Notificación FCM si se mueve
        if lat_old != amigo.lati or long_old != amigo.longi:
            print(f"📡 Web: Movimiento de {amigo.name}")
            try:
                tokens = get_all_devices()
                fcm.notificar_amigos(tokens, f"Web: {amigo.name} se ha movido")
            except Exception as e:
                print(f"❌ Error notificando: {e}")

    else:
        # --- ES UNO NUEVO ---
        nuevo = Amigo(name=name, lati=lati, longi=longi)
        db.session.add(nuevo)
        db.session.commit()

    return redirect(url_for("html.amigos"))

# 5. Borrar amigo
@html.route("/delete_amigo/<int:id>")
def amigo_delete(id):
    amigo = Amigo.query.get_or_404(id)
    db.session.delete(amigo)
    db.session.commit()
    return redirect(url_for("html.amigos"))