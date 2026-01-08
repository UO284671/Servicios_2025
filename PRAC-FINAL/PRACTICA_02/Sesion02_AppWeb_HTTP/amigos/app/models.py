from app import db

class Amigo(db.Model):
    __tablename__ = 'amigos'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), index=True, unique=True)
    lati = db.Column(db.String(20))
    longi = db.Column(db.String(20))
    device = db.Column(db.String(255)) # Token FCM

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'lati': self.lati,
            'longi': self.longi
        }

# --- FUNCIÓN SUELTA AL FINAL (SIN ESPACIOS DELANTE) ---
def get_all_devices():
    amigos = Amigo.query.filter(Amigo.device != None, Amigo.device != "").all()
    lista = [a.device for a in amigos]
    return lista