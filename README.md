# Agentic AI Web Assessment Challenge — Assessment Lab

A deployable Flask web application for a pilot assessment covering:

1. **Big Five personality** using the 20-item Mini-IPIP (4 items per trait).
2. **AI attitudes / behavioural tendencies** using two explicitly exploratory, self-authored scales:
   - AI Adoption Attitude (6 items)
   - Critical AI Use (4 items)

The platform includes informed consent, an interactive 30-item questionnaire, automatic reverse-keyed scoring, participant result charts, anonymous response storage, optional user feedback, a password-protected research dashboard, item distributions, completion statistics, Cronbach's alpha, correlations, and CSV export.

## Why this design

The task prioritizes a working, carefully evaluated system over unnecessary complexity. This implementation is intentionally small enough to inspect and test while still covering every platform requirement.

### Personality instrument

The Mini-IPIP is a 20-item short form of an IPIP Big Five measure described by Donnellan et al. (2006). IPIP items/scales are public domain. The app uses a 1–5 accuracy response scale and reverse-scores negatively keyed items using:

```text
reverse_scored = 6 - raw_response
```

Each Big Five score is the **mean of four scored items**, keeping the result on a 1–5 scale.

### AI attitude construct

The AI section is **not claimed to be validated**. It is a pilot measure created for this challenge:

- **AI Adoption Attitude:** willingness to learn, experiment with, and use AI where useful.
- **Critical AI Use:** tendency to check important claims and compare AI suggestions with other evidence.

Reverse-keyed items are scored with the same `6 - response` rule. Scale scores are item means.

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env             # then export/set variables as needed
python app.py
```

Open `http://127.0.0.1:5000`.

Admin dashboard: `http://127.0.0.1:5000/admin`

Default local admin password: `change-me` (set `ADMIN_PASSWORD` in production).

## Tests

```bash
python -m unittest discover -s tests -v
```

Tests explicitly verify positive scoring, reverse scoring, neutral-response invariance, application of keying across all scales, incomplete submissions, and Cronbach-alpha behavior on perfectly consistent data.

## Data model

- `Participant`: anonymous UUID and timing metadata
- `ResponseItem`: item-level raw and scored responses
- `Score`: scale-level scores
- `Feedback`: optional usability ratings and comments

No names, emails, phone numbers, or other unnecessary PII are requested.

## Research dashboard

`/admin` displays:

- started/completed participant counts
- completion rate and median completion time
- average scale scores
- score distributions
- raw item-level response distributions
- Cronbach's alpha for each scale
- scale-score Pearson correlations
- aggregate usability ratings
- CSV export

**Important:** Cronbach's alpha from a pilot of ~10 people is unstable. Treat it as a diagnostic check, not evidence of formal validation.

## Production deployment

The app is container-ready (`Dockerfile`) and supports either:

- local SQLite (default), or
- PostgreSQL via `DATABASE_URL` (recommended for deployment).

Set these secrets in the hosting platform:

```text
SECRET_KEY=<long random value>
ADMIN_PASSWORD=<strong password>
DATABASE_URL=<managed PostgreSQL URL>
```

Then deploy the repository using a Python/Docker host such as Render, Railway, Fly.io, or another comparable service. The start command is:

```text
gunicorn app:app
```

For a real pilot, use persistent PostgreSQL rather than ephemeral container storage.

## Pilot evaluation procedure

1. Deploy and verify `/health` returns `{ "status": "ok" }`.
2. Run the automated scoring tests.
3. Complete one manual test using known response patterns.
4. Share the public URL with **at least 10 independent volunteers**.
5. Ask participants to complete the assessment and the optional usability feedback.
6. Use `/admin` to inspect completion, distributions, unusual patterns, reliability, and comments.
7. Export anonymized CSV for the submission evidence/analysis.
8. Summarize what changed based on feedback.

Do **not** replace this step with fabricated data. Demo data can be useful for UI testing, but it is not evidence of the required real-user pilot.

## Suggested repository structure

```text
.
├── app.py
├── requirements.txt
├── Dockerfile
├── Procfile
├── README.md
├── REPORT.md
├── AI_DEVELOPMENT_RECORD.md
├── PILOT_EVALUATION_GUIDE.md
├── templates/
├── static/
├── tests/
└── data/
```

## Sources

- International Personality Item Pool (IPIP): https://ipip.ori.org/
- Donnellan, M. B., Oswald, F. L., Baird, B. M., & Lucas, R. E. (2006). *The Mini-IPIP Scales: Tiny-Yet-Effective Measures of the Big Five Factors of Personality*. Psychological Assessment, 18(2), 192–203. DOI: 10.1037/1040-3590.18.2.192.

## Limitations

- The Mini-IPIP is intentionally short and does not provide facet-level personality assessment.
- Individual scores are descriptive and should not be treated as diagnoses or high-stakes judgments.
- The AI attitude scales are self-authored for this exercise and require future validation.
- A 10-person pilot is a usability/pipeline check, not psychometric validation.
- Correlations and alpha estimates from tiny samples can be highly unstable.
