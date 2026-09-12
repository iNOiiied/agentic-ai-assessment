# Short Technical Report — Assessment Lab

**Deployed application:** https://inoiiied.pythonanywhere.com  
**Source repository:** https://github.com/iNOiiied/agentic-ai-assessment

## 1. What did I build?

I built **Assessment Lab**, a deployed web-based interactive assessment platform. It presents an informed-consent page, a 30-item questionnaire, automatic scoring, a participant results page, anonymous data storage, optional usability feedback, and a password-protected researcher dashboard. The dashboard reports participation/completion statistics, average scale scores, score distributions, item-level response distributions, Cronbach's alpha, Pearson correlations, usability summaries, and CSV export.

The deployed pilot uses Flask on PythonAnywhere. Data are stored in a persistent SQLite database within the hosting account. No names, email addresses, phone numbers, or other unnecessary personally identifiable information are requested; participants are represented by random UUIDs.

## 2. What psychological/personality constructs did I measure?

### Personality
I measured the five broad Big Five domains using the 20-item Mini-IPIP framework:

- Extraversion (E)
- Agreeableness (A)
- Conscientiousness (C)
- Neuroticism (N)
- Openness / Intellect (O)

Each Big Five domain is represented by four items.

### Attitudes / behavioural tendencies
I also implemented two exploratory AI-related scales created for this challenge:

- **AI Adoption Attitude (6 items):** willingness to learn, experiment with, and use AI tools when they may be useful.
- **Critical AI Use (4 items):** tendency to verify important AI-generated claims and compare AI suggestions with other evidence.

The AI scales are explicitly presented as exploratory and are not claimed to be validated psychological instruments.

## 3. Why did I select these constructs?

The Big Five was selected because it is a well-established personality framework and the assignment specifically encouraged using an established framework rather than inventing a new personality model. The Mini-IPIP offered a practical balance between psychometric structure and questionnaire length for a small web-based pilot.

AI-related attitudes were selected because they are directly relevant to an agentic-AI development task. I separated **AI adoption** from **critical AI use** so that enthusiasm for AI would not automatically be interpreted as uncritical trust in AI outputs.

## 4. How does the scoring system work?

All questionnaire items use a 1–5 Likert-type response scale. Positively keyed items retain their raw score. Negatively keyed items are reverse-scored using:

`reverse_scored = 6 - raw_response`

Each scale score is the arithmetic mean of its scored items, so all final scores remain on the original 1–5 metric.

The scoring logic is separated from the Flask routes in `scoring.py`. I ran six automated tests covering positive scoring, reverse-scoring endpoints, neutral-response invariance, a known maximum-score response pattern, rejection of incomplete submissions, and a known Cronbach-alpha case. All six tests passed in the deployed Python environment.

I also independently recalculated the seven exported scale means and the Pearson correlation matrix from the 15-row pilot export. The recalculated values matched the dashboard values to rounding, providing an additional check that dashboard aggregation was behaving as intended.

## 5. What technologies did I use?

- Python 3.13
- Flask
- Flask-SQLAlchemy
- SQLite for the deployed pilot database
- Jinja templates
- Vanilla JavaScript
- Chart.js
- Python `unittest`
- Git and GitHub for version control/source delivery
- PythonAnywhere for public deployment

The project also includes Gunicorn/Docker configuration so the same application can be moved to another production host or a managed PostgreSQL deployment later if needed.

## 6. How did I use agentic AI?

I used an AI coding assistant throughout the project as a development agent rather than simply copying generated code. The AI helped me:

- decompose the open-ended brief into consent, questionnaire, scoring, storage, results, admin analytics, testing, deployment, and reporting tasks;
- choose a compact Big Five implementation and define two clearly scoped exploratory AI-attitude constructs;
- generate and revise Flask routes, templates, data models, scoring functions, tests, dashboard calculations, and documentation;
- reason about reverse-keyed scoring and reliability calculations;
- diagnose local setup, Git networking, deployment, and virtual-environment problems;
- interpret the pilot results while keeping conclusions appropriately cautious.

I verified AI output with unit tests, manual end-to-end testing, exported-data recalculation, production deployment checks, and a real-user pilot. Important AI mistakes and corrections are summarized in `AI_DEVELOPMENT_RECORD_FINAL.md`.

## 7. What did I learn from the pilot participants?

### Participation and completion

The deployed dashboard recorded:

- **Started:** 21
- **Completed:** 15
- **Completion rate:** 71.4%
- **Median recorded completion time:** 1.5 minutes
- **Usability feedback responses:** 12 (80% of completers)

The 15 completed submissions exceed the assignment's minimum of 10 completed participants. Because I also performed a pre-launch developer test, the final submission should describe the evidence conservatively as **15 completed submissions and at least 10 independent pilot participants**, rather than implying that every stored completion necessarily came from an independent participant.

The 71.4% completion rate indicates that most starters finished the assessment, but six starts did not reach completion. This is useful evidence for a future version: I would add step-level drop-off logging to determine whether users leave at consent, during the questionnaire, or before feedback.

The median time of 1.5 minutes is surprisingly short for 30 items. It may reflect a fast one-page response flow, but it should not be interpreted as evidence of strong engagement. In a future version I would record page-level timing and possibly add a simple response-quality check.

### Scale-level descriptive results

| Scale | Mean | SD | Observed range | Cronbach's alpha |
|---|---:|---:|---:|---:|
| Extraversion | 2.87 | 0.65 | 2.00–4.00 | 0.465 |
| Agreeableness | 3.33 | 0.59 | 2.75–4.75 | 0.255 |
| Conscientiousness | 3.05 | 0.61 | 2.00–4.50 | 0.257 |
| Neuroticism | 2.80 | 0.75 | 1.75–4.25 | 0.516 |
| Openness / Intellect | 3.50 | 0.78 | 2.00–4.50 | 0.692 |
| AI Adoption Attitude | 3.96 | 0.64 | 3.00–5.00 | 0.490 |
| Critical AI Use | 3.52 | 0.66 | 2.25–4.75 | 0.164 |

Within this small sample, AI Adoption had the highest mean (3.96), followed by Critical AI Use (3.52) and Openness / Intellect (3.50). These values are descriptive only; no population norms or diagnostic cut-offs were used.

### Reliability

Reliability estimates varied substantially. Openness / Intellect had the highest alpha (0.692), followed by Neuroticism (0.516). Agreeableness, Conscientiousness, and especially Critical AI Use showed low alpha values. With only 15 completed cases and very short scales, these estimates are unstable and should not be treated as formal validation.

The low alpha for Critical AI Use (0.164) is particularly useful as a design finding: the four AI-generated items are related conceptually, but they may not function as one sufficiently coherent scale. A future version should revise or expand the item pool and test it with a larger sample before making stronger claims.

### Item-level patterns

The AI Adoption items show a clear positive-attitude pattern. For example, 14 of 15 participants selected 4 or 5 for the statement that AI can help with learning complex topics, and 13 of 15 selected 4 or 5 for willingness to experiment with useful new AI tools. Several negatively worded AI-adoption items also clustered toward disagreement. This produces limited variation in some items and may partly explain the modest internal consistency.

The Critical AI Use items also show generally responsible self-reported behaviour, but their weak alpha suggests that verifying claims, comparing evidence, and resisting confident-sounding answers may be distinct behaviours rather than a single tight construct in this pilot.

### Exploratory correlations

The strongest observed Pearson correlations were:

- Openness / Intellect with AI Adoption: **r = 0.632**
- AI Adoption with Critical AI Use: **r = 0.589**
- Openness / Intellect with Critical AI Use: **r = 0.526**
- Agreeableness with Openness / Intellect: **r = 0.488**
- Agreeableness with AI Adoption: **r = 0.429**

These are exploratory patterns only. With n=15, correlations can change substantially with one or two additional participants, and no causal interpretation is justified.

### Usability feedback

Among the 12 participants who submitted usability ratings:

- **Question understandability:** 4.42 / 5
- **Ease of use:** 4.33 / 5
- **Results clarity:** 4.67 / 5

Results clarity was the strongest usability outcome: every feedback respondent rated it either 4 or 5. Nine of 12 respondents gave question understandability a 5, and eight of 12 gave ease of use a 5. One respondent gave relatively low ratings for understandability (1) and ease of use (2), showing that the positive averages should not hide individual usability problems.

The supplied export contains rating fields but no qualitative comments, so I cannot make strong claims about specific likes/dislikes beyond these rating patterns. A future version should collect optional free-text comments such as “What was confusing?” and “What would you change?”.

## 8. What problems did I encounter?

Several practical problems occurred during development and deployment:

1. **Local file/directory confusion.** Duplicate Windows filenames such as `app (1).py` and `app (2).py` led to the wrong file being executed, producing a syntax error from Markdown text. I fixed this by returning to a clean project directory and running the root `app.py`.
2. **GitHub connectivity.** Git was installed correctly, but direct HTTPS access to GitHub port 443 was blocked on the current network. The browser was already using Clash, so I configured Git to use the local HTTP proxy at `127.0.0.1:7890`, after which the repository pushed successfully.
3. **Render account verification.** My initial deployment plan used Render, but the account required card verification even for the Free tier. Rather than adding payment details, I changed the deployment plan to PythonAnywhere.
4. **PythonAnywhere dependency environment.** An early dependency install occurred outside the intended virtual environment, producing Flask/Werkzeug compatibility warnings with a preinstalled Dash package. I created and activated a dedicated `assessment-env`, verified `which python`/`which pip`, and reinstalled the requirements cleanly.
5. **Development server port conflict.** `python app.py` reported that port 5000 was already in use on PythonAnywhere. This was not a production blocker because the deployed application runs through PythonAnywhere's WSGI configuration rather than the Flask development server.

## 9. What mistakes did the AI agent make?

The AI agent was useful, but several outputs required correction rather than blind acceptance:

- It initially recommended Render as the straightforward free deployment path without accounting for the possibility of account-specific card verification. The deployment plan had to be changed.
- The setup workflow did not initially enforce verification that the Python virtual environment was active before dependency installation. This allowed an install into the user site-packages and exposed dependency conflicts.
- The first deployment guidance treated PostgreSQL as the preferred production answer in all cases. For this small PythonAnywhere pilot, persistent SQLite was sufficient; PostgreSQL remains a better scaling option rather than a strict requirement.
- Most importantly, the AI-generated Critical AI Use scale looked conceptually reasonable before data collection, but its pilot alpha was only 0.164. This is direct evidence that plausible AI-generated questionnaire items should not be assumed to form a psychometrically coherent scale.

## 10. How did I verify and correct those mistakes?

I used several layers of verification:

- six automated unit tests for scoring/reliability logic, all passing;
- manual end-to-end testing of consent, questionnaire submission, results, feedback, admin login, and data persistence;
- a password-protected admin dashboard to inspect item-level and scale-level output;
- a CSV/Excel export of the completed pilot data;
- independent recalculation of the seven scale means and the Pearson correlation matrix from the export, which matched the dashboard values to rounding;
- direct inspection of reverse-keyed item distributions;
- real-user usability feedback from 12 respondents;
- cautious interpretation of alpha and correlation results because the pilot is too small for formal psychometric validation.

When the data contradicted assumptions—for example the very low Critical AI Use alpha—I treated that as a result to report and improve rather than hiding it.

## 11. If I had another week, what would I improve?

I would prioritize five improvements:

1. Recruit a larger and more diverse sample before drawing psychometric conclusions.
2. Rewrite and expand the Critical AI Use items, then perform item-total analysis and reliability testing on the revised scale.
3. Add optional free-text usability feedback and step-level drop-off logging to explain incomplete starts.
4. Add automated browser/end-to-end tests for the deployed UI, including mobile accessibility checks.
5. Export participant-by-item scored data (not only scale scores) so that reliability, item-total correlations, and alternative scoring can be independently reproduced outside the dashboard.

## Conclusion

The project meets the main goal of the challenge: it is a working, publicly deployed, testable assessment platform with automated scoring, anonymous data collection, participant results, a researcher dashboard, real-user pilot evidence, and documented AI-assisted development. The pilot supports the usability of the platform but also revealed genuine measurement limitations—especially the weak internal consistency of several short scales. Those limitations are reported explicitly rather than presented as formal validation.

## References

Donnellan, M. B., Oswald, F. L., Baird, B. M., & Lucas, R. E. (2006). The Mini-IPIP scales: Tiny-yet-effective measures of the Big Five factors of personality. *Psychological Assessment, 18*(2), 192–203.

International Personality Item Pool (IPIP): https://ipip.ori.org/
