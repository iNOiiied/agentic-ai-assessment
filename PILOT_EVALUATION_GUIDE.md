# Pilot Evaluation Guide (10+ real participants)

## Before sharing

- Deploy to a persistent database.
- Set a strong `ADMIN_PASSWORD` and `SECRET_KEY`.
- Run `python -m unittest discover -s tests -v`.
- Complete the flow once yourself.
- Check the admin dashboard and CSV export.

## Recruitment message

> I am testing a short web-based assessment for a coursework/research-development exercise. It takes only a few minutes and asks about personality and attitudes toward AI. Responses are stored without asking for your name or contact details. The assessment is not clinical or diagnostic. If you are willing, please complete it and optionally leave usability feedback at the end.

## Minimum evidence to retain

Use only anonymous/aggregate evidence where possible:

- screenshot of admin participant count showing at least 10 completed assessments;
- completion rate and median completion time;
- score distribution screenshot;
- item-level response distribution screenshot;
- aggregate feedback ratings;
- a short anonymized summary of open-text feedback;
- exported anonymized CSV, if permitted by your submission process.

Do not publish participants' identities.

## Analysis questions

1. Did at least 10 independent participants complete the assessment successfully?
2. Did anyone abandon the questionnaire? If yes, where might friction exist?
3. Which items had highly concentrated or unusual response patterns?
4. Did any participant feedback identify ambiguous wording?
5. Did the scoring tests and spot checks behave as expected?
6. What were the pilot Cronbach-alpha values? Treat them cautiously because the sample is tiny.
7. Did participants understand the results page?
8. What did users like/dislike?
9. What are the top 2–3 changes for the next version?

## Suggested final pilot write-up structure

- **Participants:** number completed; no unnecessary demographics.
- **Completion:** completion rate, typical duration.
- **Usability:** average ratings + common themes from comments.
- **Response patterns:** any ceiling/floor effects or odd items.
- **Scoring verification:** automated test result + one manual spot check.
- **Reliability:** alpha values with a small-sample caveat.
- **Changes made:** specific fixes based on feedback.
- **Limitations:** convenience sample, small n, exploratory AI scales, not formal validation.
