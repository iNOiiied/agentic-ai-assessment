# Assessment Lab — Agentic AI Web Assessment

Public pilot web application for the Agentic AI Web Assessment Challenge.

**Live site:** https://inoiiied.pythonanywhere.com  
**Repository:** https://github.com/iNOiiied/agentic-ai-assessment

## What the platform measures

- **Big Five personality** via a 20-item Mini-IPIP structure (4 items per trait): Extraversion, Agreeableness, Conscientiousness, Neuroticism, and Openness / Intellect.
- **AI Adoption Attitude** (6 exploratory items).
- **Critical AI Use** (4 exploratory items).

All items use a 1–5 response scale. Reverse-keyed items are scored as `6 - response`, and each scale is the mean of its scored items.

## Main features

- introduction and consent
- 30-item interactive questionnaire
- automatic reverse-keyed scoring
- participant results page with charts and cautious interpretation
- anonymous UUID-based response storage
- optional usability feedback
- password-protected `/admin` dashboard
- participant/completion statistics
- average scores and score distributions
- item-level response distributions
- Cronbach's alpha
- Pearson scale correlations
- CSV export

## Deployment

The current pilot is deployed on **PythonAnywhere** using Python 3.13, Flask, Flask-SQLAlchemy, Jinja templates, JavaScript/Chart.js, and a persistent SQLite database in the hosting account.

The repository also contains Gunicorn/Docker configuration for migration to another host. For a larger study, moving to managed PostgreSQL would be preferable, but persistent SQLite was adequate for this small pilot.

## Local setup

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Admin dashboard: `http://127.0.0.1:5000/admin`

Set a strong `ADMIN_PASSWORD` and `SECRET_KEY` outside the repository for deployment.

## Tests

```bash
python -m unittest discover -s tests -v
```

The six tests cover forward scoring, reverse scoring, neutral responses, known maximum patterns, incomplete submissions, and a known reliability case.

## Pilot outcome

Final pilot dashboard:

- 21 starts
- 15 completed submissions
- 71.4% completion rate
- 1.5 min median recorded completion time
- 12 usability feedback responses

Usability means were 4.42/5 for understandability, 4.33/5 for ease of use, and 4.67/5 for result clarity.

These results are **pilot evidence, not formal psychometric validation**. Several reliability coefficients were low, particularly the exploratory Critical AI Use scale, which will need item revision and a larger sample.

## Privacy and limitations

No names, emails, phone numbers, or other unnecessary PII are requested. Participant IDs are random UUIDs. Individual results are descriptive and are not clinical/medical diagnoses or high-stakes psychological judgments.

## References

Donnellan, M. B., Oswald, F. L., Baird, B. M., & Lucas, R. E. (2006). *The Mini-IPIP scales: Tiny-yet-effective measures of the Big Five factors of personality*. Psychological Assessment, 18(2), 192–203.

International Personality Item Pool: https://ipip.ori.org/
