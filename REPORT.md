# Short Technical Report — Assessment Lab

## 1. What did I build?

I built a web-based interactive assessment platform that collects anonymous responses, automatically scores them, gives participants a visual summary, stores item-level data, collects optional usability feedback, and provides a researcher dashboard for aggregate analysis. The application is implemented in Flask and can use SQLite locally or PostgreSQL in production.

## 2. What constructs did I measure?

### Personality
I measured the Big Five domains using the 20-item Mini-IPIP:
- Extraversion
- Agreeableness
- Conscientiousness
- Neuroticism
- Openness / Intellect

### Attitudes / behavioural tendencies
I created two exploratory AI-related scales for this exercise:
- **AI Adoption Attitude:** willingness to learn, experiment with, and use useful AI tools.
- **Critical AI Use:** tendency to verify important AI claims and compare AI suggestions with other evidence.

The AI scales are explicitly described as exploratory rather than validated instruments.

## 3. Why did I select these constructs?

The Big Five is an established framework and fits the task's request for a defensible personality model. AI attitudes are directly relevant to an agentic-AI development challenge. Separating adoption from critical use avoids equating enthusiasm for AI with responsible reliance on AI.

## 4. How does the scoring system work?

Every response uses a 1–5 scale. Positively keyed items keep their raw score. Negatively keyed items are reverse scored as:

`scored = 6 - raw`

Each construct score is the arithmetic mean of its scored items, so the resulting scale remains 1–5. Big Five domains each contain four items. AI Adoption contains six items; Critical AI Use contains four.

Scoring is isolated in pure Python functions and covered by automated tests. Tests verify reverse-scoring endpoints, neutral scores, expected maximum-score patterns, incomplete submissions, and a known reliability case.

## 5. What technologies did I use?

- Python / Flask
- Flask-SQLAlchemy
- SQLite for local development; PostgreSQL supported for deployment
- Jinja templates
- Vanilla JavaScript
- Chart.js for participant/admin visualization
- Gunicorn for production serving
- Docker for portable deployment
- Python `unittest` for scoring verification

## 6. How did I use agentic AI?

The AI agent was used to decompose the open-ended brief, choose an appropriate implementation scope, generate application structure and code, design the scoring tests, identify deployment/privacy risks, and draft the research-reporting materials. I did not treat generated output as automatically correct: the scoring logic was separated for testing, reverse-keyed items were verified, and the interpretation language was deliberately constrained.

See `AI_DEVELOPMENT_RECORD.md` for selected high-impact interactions and corrections.

## 7. What did I learn from the 10 participants?

**Complete this section only after the real-user pilot. Do not fabricate results.**

Suggested fields:
- Completed participants: [N]
- Completion rate: [X%]
- Median completion time: [X min]
- Most common usability feedback: [theme]
- Any confusing item(s): [item IDs / summary]
- Any unusual response pattern: [summary]
- Changes made after feedback: [changes]

## 8. What problems did I encounter?

Key implementation risks included reverse-scoring mistakes, presenting exploratory measures too confidently, and deployment persistence. The application addresses these with explicit keying metadata/tests, cautious interpretation text, and PostgreSQL support for production deployments.

Add any deployment-specific issues encountered during the actual hosting step here.

## 9. What mistakes did the AI agent make?

The main risks identified in AI-generated designs were conceptual rather than syntactic: overclaiming what a 10-person pilot can establish, accidentally combining AI enthusiasm with uncritical trust, and using local SQLite as though it were always production-persistent. These were corrected by adding caveats, separating AI subscales, and documenting persistent production storage.

If the agent makes additional code/deployment mistakes during your real deployment, record the concrete example here.

## 10. How did I verify and correct those mistakes?

I used automated scoring tests, synthetic response patterns, a single source of truth for item keying, explicit consent/privacy text, cautious result interpretations, and a dashboard that reports pilot statistics without claiming formal validation. Before submission I will also run a manual end-to-end test and compare one participant's hand-calculated scores with the application output.

## 11. If I had another week, what would I improve?

I would increase pilot size; conduct item-level cognitive interviews; add accessibility testing; validate the exploratory AI scales with a larger sample; add more formal missing-data and careless-response checks; add automated browser tests; improve mobile chart accessibility; and add database migration/versioning support.

## Pilot results appendix

After real-user testing, add:
- participant-count evidence;
- aggregate feedback summary;
- score distributions;
- item-level anomalies;
- Cronbach-alpha values with a small-sample warning;
- final changes made from the first deployed version.
