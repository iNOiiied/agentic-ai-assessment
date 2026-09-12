# AI Development Record

## Goal decomposition

The agent decomposed the challenge into six deliverable areas: participant consent, questionnaire UX, scoring correctness, data persistence, research analytics, and evidence/reporting. The design intentionally separates participant-facing interpretation from researcher-facing aggregate analysis.

## Important agent interactions

### 1. Instrument and construct selection
**Instruction to agent:** use an established Big Five framework, avoid inventing a personality model, and choose an attitude construct that can be measured clearly without making unsupported validation claims.

**Agent contribution:** selected the 20-item Mini-IPIP for Big Five coverage and proposed a separate exploratory construct around responsible AI adoption/critical checking.

**Human verification:** checked that Mini-IPIP uses four items per Big Five factor and verified the keying direction against IPIP-published item lists. Confirmed that IPIP materials are public domain.

### 2. Scoring architecture
**Instruction to agent:** keep participant scale scores interpretable on the original 1–5 metric, handle negatively keyed items correctly, and make the scoring testable independently from the UI.

**Agent contribution:** implemented `score_response(raw, reverse)` and `calculate_scale_scores(...)` as pure functions. Reverse scoring is `6 - response`; each scale is the mean of its keyed items.

**Verification:** automated tests check both endpoints (1↔5), neutral invariance (3 remains 3), and a synthetic case where positive items are answered 5 and reverse items 1; every scale must score 5.0.

### 3. Research dashboard
**Instruction to agent:** cover all minimum dashboard requirements and add useful but defensible pilot statistics.

**Agent contribution:** added participant count, average scores, score distributions, item-level distributions, completion rate/time, Cronbach's alpha, correlations, feedback summary, and CSV export.

**Verification:** reliability is computed on scored (reverse-corrected) item values. The UI labels alpha as pilot/internal-consistency evidence and explicitly warns that n≈10 is not formal validation.

### 4. Privacy and consent
**Instruction to agent:** meet the brief while minimizing PII.

**Agent contribution:** uses random participant UUIDs, collects no names/emails/phone numbers, explains research use, marks feedback as optional, and includes a non-clinical disclaimer.

## Examples of AI mistakes/risks and corrections

1. **Risk: treating a tiny pilot as validation.** The implementation explicitly describes 10 participants as a pilot and warns against interpreting reliability coefficients as validation.
2. **Risk: reverse-keying errors.** Item direction is encoded in one source-of-truth item table and tested with synthetic response patterns.
3. **Risk: conflating AI adoption with unquestioning trust.** The design separates `AI Adoption Attitude` from `Critical AI Use` instead of using one ambiguous total score.
4. **Risk: ephemeral deployment storage.** Local SQLite is convenient for development, but the README recommends managed PostgreSQL for production persistence.
5. **Risk: unsupported psychological interpretation.** Participant results report relative tendencies and score meanings without diagnostic labels or normative claims.

## What remains a human responsibility

- Deploying the app to a public hosting account.
- Recruiting at least 10 independent participants.
- Ensuring participants actually consent.
- Reviewing the pilot data for anomalies.
- Deciding what changes to make after feedback.
- Confirming final repository/URL accessibility before submission.

This record is intentionally selective: it documents high-impact AI interactions and verification rather than dumping every generated prompt.
