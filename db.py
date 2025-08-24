from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import csv
import json

db = SQLAlchemy()

class Result(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=True)
    email = db.Column(db.String(150), nullable=True)
    test_type = db.Column(db.String(50), nullable=False)
    score = db.Column(db.Integer, nullable=False, default=0)
    flag = db.Column(db.Boolean, default=False)
    message = db.Column(db.String(255), nullable=False)
    total_questions = db.Column(db.Integer, default=0)
    details = db.Column(db.Text, nullable=True)  # JSON
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

def save_result(name, email, test_type, score, flag, message, details=None):
    r = Result(
        name=name,
        email=email,
        test_type=test_type,
        score=score,
        flag=bool(flag),
        message=message,
        total_questions=(details.get("total_questions") if isinstance(details, dict) and details.get("total_questions") else None),
        details=(json.dumps(details) if details is not None and not isinstance(details, str) else details)
    )
    db.session.add(r)
    db.session.commit()
    return r

def get_filtered_results(email=None, test_type=None):
    q = Result.query.order_by(Result.timestamp.desc())
    if email:
        q = q.filter(Result.email.ilike(f"%{email}%"))
    if test_type:
        q = q.filter(Result.test_type == test_type)
    return q.all()

def export_results_to_csv(email=None, test_type=None):
    results = get_filtered_results(email=email, test_type=test_type)
    filename = f"exported_results_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}.csv"
    with open(filename, "w", newline="", encoding="utf-8") as f:
        import csv
        writer = csv.writer(f)
        writer.writerow(["Name","Email","Test Type","Score","Flag","Message","Total Questions","Details JSON","Timestamp"])
        for r in results:
            writer.writerow([r.name, r.email, r.test_type, r.score, "Yes" if r.flag else "No", r.message, r.total_questions or "", r.details or "", r.timestamp])
    return filename
