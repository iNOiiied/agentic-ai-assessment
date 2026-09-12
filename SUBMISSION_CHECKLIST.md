# Submission Checklist

## A. Deployed Web Application
- [ ] Create production PostgreSQL database.
- [ ] Set `SECRET_KEY`, `ADMIN_PASSWORD`, `DATABASE_URL`.
- [ ] Deploy the repository.
- [ ] Confirm public `/health` endpoint works.
- [ ] Confirm assessment can be completed on desktop and mobile.
- [ ] Record public URL here: ______________________________

## B. Source Code
- [ ] Create GitHub/equivalent repository.
- [ ] Push all files except `.env` and local database.
- [ ] Confirm README renders correctly.
- [ ] Record repository URL here: __________________________

Suggested commands:

```bash
git init
git add .
git commit -m "Build assessment platform"
git branch -M main
git remote add origin <YOUR_REPOSITORY_URL>
git push -u origin main
```

## C. AI Development Record
- [x] `AI_DEVELOPMENT_RECORD.md` created.
- [ ] Add any deployment-stage AI mistakes/corrections you actually encounter.

## D. Pilot Evaluation
- [ ] Recruit at least 10 independent participants.
- [ ] Keep participant identities private.
- [ ] Save screenshot showing at least 10 completed responses.
- [ ] Save aggregate dashboard screenshots/CSV as appropriate.
- [ ] Summarize usability feedback and unusual response patterns.

## E. Short Technical Report
- [x] `REPORT.md` drafted for sections 1–6 and 8–11.
- [ ] Complete section 7 only after the real pilot.
- [ ] Add actual deployment problems/mistakes if encountered.
- [ ] Add final pilot evidence/results appendix.

## Final verification
- [ ] Run `python -m unittest discover -s tests -v`.
- [ ] Manually calculate one participant's reverse-scored results and compare.
- [ ] Verify admin dashboard is password protected.
- [ ] Verify no real participant PII is shown in screenshots or exports.
- [ ] Verify the report does not describe synthetic/demo data as real-user evidence.
