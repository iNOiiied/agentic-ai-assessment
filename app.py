import json
import math
import os
import statistics
import uuid
from collections import Counter, defaultdict
from datetime import datetime, timezone
from functools import wraps

from flask import Flask, Response, flash, redirect, render_template, request, session, url_for
from flask_sqlalchemy import SQLAlchemy

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DEFAULT_DB = "sqlite:///" + os.path.join(BASE_DIR, "data", "assessment.db")
DATABASE_URL = os.environ.get("DATABASE_URL", DEFAULT_DB)
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

app = Flask(__name__)
app.config.update(
    SECRET_KEY=os.environ.get("SECRET_KEY", "dev-only-change-me"),
    SQLALCHEMY_DATABASE_URI=DATABASE_URL,
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
)
db = SQLAlchemy(app)

from scoring import (
    ALL_ITEMS, ATTITUDE_ITEMS, ITEM_BY_ID, PERSONALITY_ITEMS, SCALE_LABELS,
    calculate_scale_scores, cronbach_alpha, pearson, score_response,
)


class Participant(db.Model):
    id = db.Column(db.String(36), primary_key=True)
    consent_at = db.Column(db.DateTime(timezone=True), nullable=False)
    started_at = db.Column(db.DateTime(timezone=True), nullable=False)
    completed_at = db.Column(db.DateTime(timezone=True), nullable=True)


class ResponseItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    participant_id = db.Column(db.String(36), db.ForeignKey("participant.id"), nullable=False, index=True)
    item_id = db.Column(db.String(8), nullable=False)
    scale = db.Column(db.String(20), nullable=False)
    raw_value = db.Column(db.Integer, nullable=False)
    scored_value = db.Column(db.Integer, nullable=False)
    reverse_keyed = db.Column(db.Boolean, nullable=False, default=False)


class Score(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    participant_id = db.Column(db.String(36), db.ForeignKey("participant.id"), nullable=False, index=True)
    scale = db.Column(db.String(20), nullable=False)
    score = db.Column(db.Float, nullable=False)


class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    participant_id = db.Column(db.String(36), db.ForeignKey("participant.id"), nullable=False, unique=True)
    understandable = db.Column(db.Integer, nullable=True)
    easy_to_use = db.Column(db.Integer, nullable=True)
    results_clear = db.Column(db.Integer, nullable=True)
    liked = db.Column(db.Text, nullable=True)
    disliked = db.Column(db.Text, nullable=True)
    improvements = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


def utcnow():
    return datetime.now(timezone.utc)


def admin_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not session.get("admin_ok"):
            return redirect(url_for("admin_login", next=request.path))
        return view(*args, **kwargs)
    return wrapped


@app.before_request
def ensure_db():
    db.create_all()


@app.get("/")
def index():
    return render_template("consent.html")


@app.post("/start")
def start():
    if request.form.get("consent") != "yes":
        flash("You must provide consent before starting.")
        return redirect(url_for("index"))
    participant = Participant(id=str(uuid.uuid4()), consent_at=utcnow(), started_at=utcnow())
    db.session.add(participant)
    db.session.commit()
    session["participant_id"] = participant.id
    return redirect(url_for("questionnaire"))


@app.route("/questionnaire", methods=["GET", "POST"])
def questionnaire():
    participant_id = session.get("participant_id")
    if not participant_id:
        return redirect(url_for("index"))
    participant = db.session.get(Participant, participant_id)
    if not participant:
        return redirect(url_for("index"))

    if request.method == "GET":
        return render_template(
            "questionnaire.html",
            personality_items=PERSONALITY_ITEMS,
            attitude_items=ATTITUDE_ITEMS,
        )

    raw_answers = {}
    try:
        for item_id, _, _, _ in ALL_ITEMS:
            value = int(request.form[item_id])
            if value not in range(1, 6):
                raise ValueError
            raw_answers[item_id] = value
    except (KeyError, ValueError):
        flash("Please answer every item using a response from 1 to 5.")
        return render_template(
            "questionnaire.html",
            personality_items=PERSONALITY_ITEMS,
            attitude_items=ATTITUDE_ITEMS,
            previous=request.form,
        ), 400

    scale_scores = calculate_scale_scores(raw_answers)
    ResponseItem.query.filter_by(participant_id=participant_id).delete()
    Score.query.filter_by(participant_id=participant_id).delete()
    for item_id, raw in raw_answers.items():
        _, _, scale, reverse_keyed = ITEM_BY_ID[item_id]
        db.session.add(ResponseItem(
            participant_id=participant_id,
            item_id=item_id,
            scale=scale,
            raw_value=raw,
            scored_value=score_response(raw, reverse_keyed),
            reverse_keyed=reverse_keyed,
        ))
    for scale, score in scale_scores.items():
        db.session.add(Score(participant_id=participant_id, scale=scale, score=score))
    participant.completed_at = utcnow()
    db.session.commit()
    return redirect(url_for("results", participant_id=participant_id))


@app.get("/results/<participant_id>")
def results(participant_id):
    if session.get("participant_id") != participant_id and not session.get("admin_ok"):
        return "Not authorized", 403
    scores = {s.scale: s.score for s in Score.query.filter_by(participant_id=participant_id).all()}
    if not scores:
        return "Results not found", 404
    personality_order = ["E", "A", "C", "N", "O"]
    personality = [(SCALE_LABELS[s], scores[s]) for s in personality_order]
    attitudes = [(SCALE_LABELS[s], scores[s]) for s in ["AI_ADOPT", "AI_CRIT"]]
    return render_template(
        "results.html",
        participant_id=participant_id,
        personality=personality,
        attitudes=attitudes,
        chart_labels=json.dumps([x[0] for x in personality]),
        chart_values=json.dumps([x[1] for x in personality]),
    )


@app.post("/feedback/<participant_id>")
def feedback(participant_id):
    if session.get("participant_id") != participant_id:
        return "Not authorized", 403
    existing = Feedback.query.filter_by(participant_id=participant_id).first()
    if existing:
        flash("Feedback already submitted. Thank you.")
        return redirect(url_for("results", participant_id=participant_id))

    def optional_rating(name):
        val = request.form.get(name, "").strip()
        return int(val) if val in {"1", "2", "3", "4", "5"} else None

    db.session.add(Feedback(
        participant_id=participant_id,
        understandable=optional_rating("understandable"),
        easy_to_use=optional_rating("easy_to_use"),
        results_clear=optional_rating("results_clear"),
        liked=request.form.get("liked", "").strip()[:3000],
        disliked=request.form.get("disliked", "").strip()[:3000],
        improvements=request.form.get("improvements", "").strip()[:3000],
    ))
    db.session.commit()
    flash("Thanks — your feedback was recorded anonymously.")
    return redirect(url_for("results", participant_id=participant_id))


@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        configured = os.environ.get("ADMIN_PASSWORD", "change-me")
        if request.form.get("password") == configured:
            session["admin_ok"] = True
            return redirect(request.args.get("next") or url_for("admin_dashboard"))
        flash("Incorrect admin password.")
    return render_template("admin_login.html")


@app.post("/admin/logout")
def admin_logout():
    session.pop("admin_ok", None)
    return redirect(url_for("index"))


def build_admin_data():
    participants = Participant.query.all()
    completed = [p for p in participants if p.completed_at]
    completed_ids = {p.id for p in completed}
    scores = Score.query.filter(Score.participant_id.in_(completed_ids)).all() if completed_ids else []
    responses = ResponseItem.query.filter(ResponseItem.participant_id.in_(completed_ids)).all() if completed_ids else []
    feedbacks = Feedback.query.filter(Feedback.participant_id.in_(completed_ids)).all() if completed_ids else []

    by_scale = defaultdict(list)
    for s in scores:
        by_scale[s.scale].append(s.score)
    averages = {scale: round(statistics.mean(vals), 3) for scale, vals in by_scale.items() if vals}

    bins = [(1.0, 1.8), (1.8, 2.6), (2.6, 3.4), (3.4, 4.2), (4.2, 5.01)]
    distributions = {}
    for scale, vals in by_scale.items():
        counts = []
        for low, high in bins:
            counts.append(sum(1 for v in vals if low <= v < high))
        distributions[scale] = counts

    item_distributions = {}
    for item_id, text, scale, reverse in ALL_ITEMS:
        raw = [r.raw_value for r in responses if r.item_id == item_id]
        c = Counter(raw)
        item_distributions[item_id] = {
            "text": text,
            "scale": scale,
            "reverse": reverse,
            "counts": [c.get(i, 0) for i in range(1, 6)],
        }

    reliability = {}
    for scale in SCALE_LABELS:
        scale_items = [i[0] for i in ALL_ITEMS if i[2] == scale]
        matrix = []
        for pid in completed_ids:
            rows = {r.item_id: r.scored_value for r in responses if r.participant_id == pid and r.scale == scale}
            if len(rows) == len(scale_items):
                matrix.append([rows[item_id] for item_id in scale_items])
        reliability[scale] = cronbach_alpha(matrix)

    # Scale-score correlations, pairwise complete (all completed users have all scales here).
    score_lookup = defaultdict(dict)
    for s in scores:
        score_lookup[s.participant_id][s.scale] = s.score
    scales = list(SCALE_LABELS.keys())
    correlations = {}
    for a in scales:
        correlations[a] = {}
        for b in scales:
            pairs = [(d[a], d[b]) for d in score_lookup.values() if a in d and b in d]
            if a == b and pairs:
                correlations[a][b] = 1.0
            else:
                correlations[a][b] = pearson([p[0] for p in pairs], [p[1] for p in pairs])

    durations = []
    for p in completed:
        if p.started_at and p.completed_at:
            started = p.started_at
            ended = p.completed_at
            # SQLite may return naive datetimes; subtraction still works when both are consistent.
            try:
                durations.append((ended - started).total_seconds())
            except TypeError:
                durations.append((ended.replace(tzinfo=None) - started.replace(tzinfo=None)).total_seconds())

    feedback_summary = {
        "n": len(feedbacks),
        "understandable": round(statistics.mean([f.understandable for f in feedbacks if f.understandable]), 2) if any(f.understandable for f in feedbacks) else None,
        "easy_to_use": round(statistics.mean([f.easy_to_use for f in feedbacks if f.easy_to_use]), 2) if any(f.easy_to_use for f in feedbacks) else None,
        "results_clear": round(statistics.mean([f.results_clear for f in feedbacks if f.results_clear]), 2) if any(f.results_clear for f in feedbacks) else None,
    }

    return {
        "started": len(participants),
        "completed": len(completed),
        "completion_rate": round((len(completed) / len(participants) * 100), 1) if participants else 0,
        "median_duration_min": round(statistics.median(durations) / 60, 1) if durations else None,
        "averages": averages,
        "distributions": distributions,
        "item_distributions": item_distributions,
        "reliability": reliability,
        "correlations": correlations,
        "feedback_summary": feedback_summary,
        "feedbacks": feedbacks,
    }


@app.get("/admin")
@admin_required
def admin_dashboard():
    data = build_admin_data()
    return render_template(
        "admin.html",
        **data,
        labels=SCALE_LABELS,
        distribution_bins=["1.0–1.79", "1.8–2.59", "2.6–3.39", "3.4–4.19", "4.2–5.0"],
    )


@app.get("/admin/export.csv")
@admin_required
def export_csv():
    completed_ids = [p.id for p in Participant.query.filter(Participant.completed_at.isnot(None)).all()]
    scores = Score.query.filter(Score.participant_id.in_(completed_ids)).all() if completed_ids else []
    feedbacks = {f.participant_id: f for f in Feedback.query.all()}
    score_lookup = defaultdict(dict)
    for s in scores:
        score_lookup[s.participant_id][s.scale] = s.score

    import csv
    import io
    out = io.StringIO()
    writer = csv.writer(out)
    writer.writerow(["participant_id", *SCALE_LABELS.keys(), "feedback_understandable", "feedback_easy_to_use", "feedback_results_clear"])
    for pid in completed_ids:
        f = feedbacks.get(pid)
        writer.writerow([
            pid,
            *[score_lookup[pid].get(s, "") for s in SCALE_LABELS.keys()],
            f.understandable if f else "",
            f.easy_to_use if f else "",
            f.results_clear if f else "",
        ])
    return Response(out.getvalue(), mimetype="text/csv", headers={"Content-Disposition": "attachment; filename=assessment_export.csv"})


@app.get("/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=os.environ.get("FLASK_DEBUG") == "1")
