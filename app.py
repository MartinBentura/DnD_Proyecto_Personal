from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import math

app = Flask(__name__)

# Configuración de BD SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///characters.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modelo en BD
class Personaje(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    race = db.Column(db.String(80), nullable=False)
    character_class = db.Column(db.String(80), nullable=False)
    level = db.Column(db.Integer, default=1)

    # Stats
    str = db.Column(db.Integer, default=10)
    dex = db.Column(db.Integer, default=10)
    con = db.Column(db.Integer, default=10)
    int = db.Column(db.Integer, default=10)
    wis = db.Column(db.Integer, default=10)
    cha = db.Column(db.Integer, default=10)


with app.app_context():
    db.create_all()


# Función para calcular modificadores de D&D
def get_modifier(stat):
    return math.floor((stat - 10) / 2)


@app.route("/")
def home():
    characters = Personaje.query.all()
    return render_template("index.html", characters=characters)

@app.route("/character/<int:id>")
def view_character(id):
    character = Personaje.query.get(id)
    if not character:
        return redirect(url_for("home"))
    return render_template("character.html", character=character, get_modifier=get_modifier, getattr=getattr)


@app.route("/delete/<int:id>")
def delete_character(id):
    character = Personaje.query.get(id)
    if character:
        db.session.delete(character)
        db.session.commit()
    return redirect(url_for("home"))


@app.route("/create", methods=["GET", "POST"])
def create_character():
    if request.method == "POST":
        new_char = Personaje(
            name=request.form["name"],
            race=request.form["race"],
            character_class=request.form["character_class"],
            level=int(request.form["level"]),
            str=int(request.form["str"]),
            dex=int(request.form["dex"]),
            con=int(request.form["con"]),
            int=int(request.form["int"]),
            wis=int(request.form["wis"]),
            cha=int(request.form["cha"])
        )

        db.session.add(new_char)
        db.session.commit()
        return redirect(url_for("home"))

    return render_template("create_character.html")


@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_character(id):
    character = Personaje.query.get_or_404(id)

    if request.method == "POST":
        character.name = request.form["name"]
        character.race = request.form["race"]
        character.character_class = request.form["character_class"]
        character.level = int(request.form["level"])
        character.str = int(request.form["str"])
        character.dex = int(request.form["dex"])
        character.con = int(request.form["con"])
        character.int = int(request.form["int"])
        character.wis = int(request.form["wis"])
        character.cha = int(request.form["cha"])

        db.session.commit()
        return redirect(url_for("home"))

    return render_template("edit.html", character=character, getattr=getattr)


if __name__ == "__main__":
    app.run(debug=True)
