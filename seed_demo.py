"""Generate clearly labeled synthetic data for UI testing only.
Never use this output as evidence for the required real-user pilot.
"""
import random
from datetime import timedelta
from app import app, db, Participant, ResponseItem, Score, Feedback, ALL_ITEMS, calculate_scale_scores, score_response, utcnow

with app.app_context():
    for _ in range(12):
        pid = __import__('uuid').uuid4().__str__()
        start = utcnow() - timedelta(minutes=random.randint(2, 12))
        p = Participant(id=pid, consent_at=start, started_at=start, completed_at=utcnow())
        db.session.add(p)
        answers = {item_id: random.randint(1, 5) for item_id, *_ in ALL_ITEMS}
        scores = calculate_scale_scores(answers)
        for item_id, text, scale, rev in ALL_ITEMS:
            raw = answers[item_id]
            db.session.add(ResponseItem(participant_id=pid, item_id=item_id, scale=scale, raw_value=raw, scored_value=score_response(raw, rev), reverse_keyed=rev))
        for scale, value in scores.items():
            db.session.add(Score(participant_id=pid, scale=scale, score=value))
        db.session.add(Feedback(participant_id=pid, understandable=random.randint(3,5), easy_to_use=random.randint(3,5), results_clear=random.randint(3,5), liked="Synthetic demo feedback", improvements="Synthetic demo only"))
    db.session.commit()
    print("Inserted 12 SYNTHETIC demo participants. Do not use as real pilot evidence.")
