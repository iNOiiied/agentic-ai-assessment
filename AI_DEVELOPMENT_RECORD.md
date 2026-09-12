# AI Development Record — Assessment Lab

## Development approach

I used an AI coding assistant as an agent throughout the project. The agent helped decompose the brief, generate and modify code, reason about scoring, write tests, troubleshoot deployment, and interpret pilot results. I did not treat generated output as automatically correct; I repeatedly tested, inspected, and revised it.

## Selected high-impact interactions

### 1. Turning the brief into an architecture
**Instruction:** break the assignment into the smallest system that still meets every required deliverable.

**AI contribution:** proposed separate components for consent, questionnaire, scoring, participant results, anonymous storage, feedback, admin analytics, testing, deployment, and documentation.

**Human verification/correction:** checked the architecture against the assignment line by line and kept the scope deliberately simple rather than adding unnecessary features.

### 2. Construct and item design
**Instruction:** use an established Big Five framework and add an AI-related attitude/behaviour component without making unsupported clinical claims.

**AI contribution:** used a 20-item Mini-IPIP structure and proposed two exploratory AI scales: AI Adoption Attitude and Critical AI Use.

**Human verification/correction:** kept Big Five interpretation descriptive, labeled the AI scales exploratory, and avoided diagnostic/normative language. The later pilot alpha for Critical AI Use (0.164) demonstrated that sensible-looking AI-generated items still require empirical validation.

### 3. Scoring and reverse-keying
**Instruction:** keep all final scale scores on a 1–5 metric and make reverse scoring independently testable.

**AI contribution:** implemented reverse scoring as `6 - response`, scale means, and pure scoring functions.

**Human verification/correction:** ran six automated tests covering forward scoring, reverse endpoints, neutral responses, an all-maximum known pattern, incomplete submissions, and a known alpha case. All six passed.

### 4. Dashboard and psychometric summaries
**Instruction:** satisfy the required admin metrics and add useful pilot diagnostics without claiming formal validation.

**AI contribution:** implemented participant counts, completion statistics, means, score distributions, item distributions, Cronbach's alpha, Pearson correlations, usability summaries, and CSV export.

**Human verification/correction:** independently recalculated all seven scale means and the correlation matrix from the 15 completed rows in the exported workbook. Values matched the dashboard to rounding. Alpha estimates were explicitly labeled unstable in a small pilot.

### 5. Deployment troubleshooting
**Instruction:** obtain a public URL without exposing secrets or participant data.

**AI contribution:** first proposed Render, then helped move the application to PythonAnywhere when Render required card verification. It also helped configure GitHub access, the Python virtual environment, WSGI, static files, and admin secrets.

**Human verification/correction:** several deployment recommendations needed adjustment in response to the real environment, as documented below.

## Concrete AI mistakes or weak assumptions

1. **Render was treated as a universally frictionless free deployment path.** My account required card verification even on the Free tier, so the recommendation was not usable. I switched to PythonAnywhere.
2. **The environment setup did not initially force a `which python` / `which pip` check before package installation.** Dependencies were installed into the user site, triggering compatibility warnings with preinstalled Dash. I corrected this by creating and activating `assessment-env` and reinstalling requirements there.
3. **The early deployment documentation over-emphasized PostgreSQL as mandatory for production.** For this small PythonAnywhere pilot, persistent SQLite was adequate. PostgreSQL remains a future scaling choice rather than a requirement for the current study.
4. **The AI-authored Critical AI Use items were not psychometrically strong in the pilot.** Cronbach's alpha was 0.164, so I did not present the scale as validated. This is the clearest example of why generated questionnaire content must be empirically checked.
5. **The AI could have encouraged over-interpretation of small-sample statistics.** I corrected the reporting language so that correlations and alpha values are treated as exploratory diagnostics only.

## How I identified and corrected the mistakes

- Read actual terminal errors instead of applying generic fixes.
- Re-ran the project from a clean directory after duplicate Windows filenames caused the wrong file to be executed.
- Diagnosed GitHub connectivity by testing port 443 and then configuring Git to use the existing Clash proxy (`127.0.0.1:7890`).
- Changed hosting platform after Render's card requirement blocked deployment.
- Verified the PythonAnywhere virtual environment before reinstalling packages.
- Ran all six unit tests successfully in the deployment environment.
- Completed a production end-to-end submission and confirmed the record appeared in `/admin`.
- Exported the final data and recomputed means/correlations independently.
- Used the pilot alpha values as evidence for scale revision rather than ignoring weak results.

## What remained my responsibility

The AI did not recruit participants, provide consent on their behalf, decide whether the pilot was ethically appropriate, or validate the measures. I remained responsible for the final code, deployment, participant recruitment, data handling, statistical interpretation, and the limitations stated in the report.
