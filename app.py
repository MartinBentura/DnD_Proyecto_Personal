from flask import Flask, render_template, request, redirect,url_for

app = Flask(__name__)

characters = []


@app.route("/")
def home():
    return render_template("index.html", characters=characters )

@app.route("/delete/<int:index>")
def delete_character(index):
    if 0 <= index < len(characters):
        characters.pop(index)
    return redirect("/")

@app.route("/create", methods=["GET", "POST"])
def create_character():
    if request.method == "POST":
        name = request.form["name"]
        race = request.form["race"]
        character_class = request.form["character_class"]
        level = request.form["level"]

        new_character = {
            "name": name,
            "race": race,
            "character_class": character_class,
            "level": level
        }

        characters.append(new_character)

        return redirect(url_for("home"))

    return render_template("create_character.html")


if __name__ == "__main__":
    app.run(debug=True)