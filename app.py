from flask import Flask, render_template, request, redirect, url_for
import sqlite3, os
import pytesseract
from PIL import Image
from googletrans import Translator

app = Flask(__name__)
DB = "database.db"
UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
translator = Translator()

# Ensure database exists
def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS patients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT, age INTEGER, dosha TEXT
    )""")
    conn.commit()
    conn.close()

init_db()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/patients", methods=["GET", "POST"])
def patients():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    if request.method == "POST":
        name = request.form["name"]
        age = request.form["age"]
        dosha = request.form["dosha"]
        c.execute("INSERT INTO patients (name, age, dosha) VALUES (?, ?, ?)", (name, age, dosha))
        conn.commit()
    c.execute("SELECT * FROM patients")
    patients = c.fetchall()
    conn.close()
    return render_template("patients.html", patients=patients)

# Dummy nutrient DB
nutrients = {
    "rice": {"calories": 130, "protein": 2.7, "ayurveda": "Good for Pitta, heavy for Kapha"},
    "milk": {"calories": 42, "protein": 3.4, "ayurveda": "Balancing for Vata and Pitta"},
    "cucumber": {"calories": 16, "protein": 0.7, "ayurveda": "Cooling, good for Pitta"}
}

@app.route("/diet_plan", methods=["GET", "POST"])
def diet_plan():
    plan = []
    if request.method == "POST":
        foods = request.form["foods"].split(",")
        for food in foods:
            f = food.strip().lower()
            if f in nutrients:
                plan.append({"food": f, **nutrients[f]})
            else:
                plan.append({"food": f, "calories": "?", "protein": "?", "ayurveda": "No data"})
        return render_template("diet_plan.html", plan=plan)
    return render_template("diet_plan.html", plan=None)

@app.route("/ocr", methods=["POST"])
def ocr():
    if "file" not in request.files:
        return "No file uploaded", 400
    file = request.files["file"]
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
    file.save(filepath)
    text = pytesseract.image_to_string(Image.open(filepath))
    return render_template("ocr_result.html", text=text)

@app.route("/translate", methods=["POST"])
def translate_text():
    text = request.form["text"]
    lang = request.form["lang"]
    translated = translator.translate(text, dest=lang)
    return render_template("export.html", text=translated.text, lang=lang)

if __name__ == "__main__":
    app.run(debug=True)
