import os
import json
from datetime import datetime
from flask import Flask, render_template, request, send_file
from db import db, Result, save_result, get_filtered_results, export_results_to_csv
from ld_logic import evaluate_dyslexia, evaluate_dyscalculia, evaluate_memory
from werkzeug.middleware.proxy_fix import ProxyFix

# Optional Firebase Admin
firebase_enabled = False
try:
    import firebase_admin
    from firebase_admin import credentials, firestore
except Exception:
    firebase_admin = None
    firestore = None

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret")
app.wsgi_app = ProxyFix(app.wsgi_app)

# DB config
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///users.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

def init_firebase_if_available():
    global firebase_enabled
    if firebase_admin is None:
        return
    creds_json = os.environ.get("FIREBASE_CREDENTIALS_JSON")
    if not creds_json:
        return
    try:
        cred = credentials.Certificate(json.loads(creds_json))
        firebase_admin.initialize_app(cred)
        firebase_enabled = True
        print("Firebase initialized")
    except Exception as e:
        print("Firebase init failed:", e)

with app.app_context():
    db.create_all()
init_firebase_if_available()

def firebase_save(result_dict):
    if not firebase_enabled:
        return
    try:
        client = firestore.client()
        client.collection("results").add(result_dict)
    except Exception as e:
        print("Firestore save failed:", e)

@app.context_processor
def inject_globals():
    return {"year": datetime.utcnow().year}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/test/dyslexia", methods=["GET", "POST"])
def test_dyslexia():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        answers = [request.form.get(f"q{i}") for i in range(1, 6)]
        breakdown = {
            "q1": {"correct": "b", "given": answers[0]},
            "q2": {"correct": "b", "given": answers[1]},
            "q3": {"correct": "a", "given": answers[2]},
            "q4": {"correct": "a", "given": answers[3]},
            "q5": {"correct": "b", "given": answers[4]},
        }
        result = evaluate_dyslexia(answers)
        result["total_questions"] = 5
        result["breakdown"] = breakdown
        save_result(name, email, result["type"], result["score"], result["flag"], result["message"], details=breakdown)
        firebase_save({"name":name,"email":email,"test_type":result["type"],"score":result["score"],"flag":bool(result["flag"]),"message":result["message"],"timestamp":datetime.utcnow().isoformat(),"details":breakdown})
        return render_template("results.html", result=result)
    return render_template("test_dyslexia.html")

@app.route("/test/dyscalculia", methods=["GET", "POST"])
def test_dyscalculia():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        answers = [request.form.get(f"q{i}") for i in range(1, 6)]
        breakdown = {
            "q1": {"correct": "c", "given": answers[0]},
            "q2": {"correct": "b", "given": answers[1]},
            "q3": {"correct": "a", "given": answers[2]},
            "q4": {"correct": "a", "given": answers[3]},
            "q5": {"correct": "b", "given": answers[4]},
        }
        result = evaluate_dyscalculia(answers)
        result["total_questions"] = 5
        result["breakdown"] = breakdown
        save_result(name, email, result["type"], result["score"], result["flag"], result["message"], details=breakdown)
        firebase_save({"name":name,"email":email,"test_type":result["type"],"score":result["score"],"flag":bool(result["flag"]),"message":result["message"],"timestamp":datetime.utcnow().isoformat(),"details":breakdown})
        return render_template("results.html", result=result)
    return render_template("test_dyscalculia.html")

from glob import glob
import random

def list_memory_images(app):
    base = os.path.join(app.root_path, "static", "images", "memory")
    os.makedirs(base, exist_ok=True)
    items = []
    for fn in os.listdir(base):
        if fn.lower().endswith((".jpg",".jpeg",".png")):
            label = os.path.splitext(fn)[0].title()
            items.append({"label": label, "url": f"/static/images/memory/{fn}"})
    return items

@app.route("/test/memory", methods=["GET", "POST"])
def test_memory():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        correct_labels = request.form.get("correct_labels","")
        correct = [c for c in correct_labels.split(",") if c]
        selected = request.form.getlist("recall")
        result = evaluate_memory(selected, correct)
        result["total_questions"] = len(correct)
        result["breakdown"] = {
            "true_positives": [s for s in selected if s in correct],
            "false_positives": [s for s in selected if s not in correct],
            "missed": [c for c in correct if c not in selected],
            "correct_set": correct,
            "selected_set": selected
        }
        save_result(name, email, result["type"], result["score"], result["flag"], result["message"], details=result["breakdown"])
        firebase_save({"name":name,"email":email,"test_type":result["type"],"score":result["score"],"flag":bool(result["flag"]),"message":result["message"],"timestamp":datetime.utcnow().isoformat(),"details":result["breakdown"]})
        return render_template("results.html", result=result)
    items = list_memory_images(app)
    if len(items) < 8:
        defaults = ["Apple","Book","Tiger","Spoon","Car","Banana","Clock","Tree"]
        existing = set(i["label"] for i in items)
        for lbl in defaults:
            if lbl not in existing:
                items.append({"label": lbl, "url": f"/static/images/memory/{lbl.lower()}.jpg"})
    random.shuffle(items)
    targets = items[:4]
    distractors = items[4:8]
    recall_grid = targets + distractors
    random.shuffle(recall_grid)
    return render_template("test_memory.html", targets=targets, recall_grid=recall_grid, correct_labels=",".join([t["label"] for t in targets]))

@app.route("/admin")
def admin_dashboard():
    email = request.args.get("email","").strip()
    test_type = request.args.get("test_type","").strip()
    results = get_filtered_results(email=email or None, test_type=test_type or None)
    return render_template("admin_dashboard.html", results=results, email=email, test_type=test_type)

@app.route("/admin/export")
def admin_export():
    email = request.args.get("email","").strip()
    test_type = request.args.get("test_type","").strip()
    filename = export_results_to_csv(email=email or None, test_type=test_type or None)
    return send_file(filename, as_attachment=True)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
