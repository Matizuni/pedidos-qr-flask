from flask import Flask, render_template, request, redirect, send_file
from flask_sqlalchemy import SQLAlchemy
import json
import qrcode
import io
import os

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# =========================
# MODELO
# =========================
class Pedido(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    categoria = db.Column(db.String(50))
    producto = db.Column(db.String(50))
    opciones = db.Column(db.Text)
    estado = db.Column(db.String(20), default="pendiente")

# =========================
# RUTAS
# =========================
@app.route("/")
def menu():
    return render_template("menu.html")


@app.route("/pedido", methods=["POST"])
def crear_pedido():
    opciones = {}
    for key in request.form:
        if key.startswith("opt_"):
            opciones[key.replace("opt_", "")] = True
    if "mayo" in request.form:
        opciones["mayo"] = request.form["mayo"]

    nuevo = Pedido(
        categoria=request.form["categoria"],
        producto=request.form["producto"],
        opciones=json.dumps(opciones, ensure_ascii=False)
    )
    db.session.add(nuevo)
    db.session.commit()

    return """
    <h2>Pedido enviado ✅</h2>
    <a href="/">Volver al menú</a>
    """


@app.route("/admin")
def admin():
    pedidos = Pedido.query.order_by(Pedido.id.desc()).all()
    return render_template("admin.html", pedidos=pedidos, json=json)


@app.route("https://pedidos-qr-flask.onrender.com")
def generar_qr():
    url = "https://pedidos-qr-flask.onrender.com"   # URL de Render
    img = qrcode.make(url)
    ruta = "static/qr_menu.png"
    img.save(ruta)
    return send_file(ruta, mimetype='image/png')



# =========================
# INIT
# =========================
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    # Esto permite que sea accesible desde otros dispositivos en la red
    app.run(host="0.0.0.0", port=5000, debug=True)
