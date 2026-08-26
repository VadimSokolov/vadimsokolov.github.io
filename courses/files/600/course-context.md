# AII 600 course context

*Reference material for the course tutor. Attach this alongside `tutor-instructions.md`.*

## Modules and the weeks they cover

| Module | Notes file | Weeks | Topics |
|---|---|---|---|
| 1. Foundations | `files/600/01-intro.html` | 1 to 2 | the AI/ML landscape, probability, distributions, Bayes, correlation, covariance |
| 2. Estimation | `notes/02-estimation.html` | 3 to 4 | CDFs and quantiles, method of moments, maximum likelihood, the CLT, bootstrap |
| 3. Patterns | `notes/03-pattern.html` | 5 to 6 | OLS, residuals, transformations, dummy variables, multiple regression, logistic regression, classification, power laws |
| 4. Decisions | `notes/04-decisions.html` | 7 and 9 | hypothesis testing, predictive values, expected value, utility, paradoxes, the Kelly criterion |
| 5. Model selection | `notes/05-modelselection.html` | 10 to 11 | bias-variance, cross-validation, ridge, lasso, shrinkage |
| 6. Deep learning | `notes/06-dlai.html` | 12 to 13 | neural nets, ReLU and activations, projection pursuit, Kolmogorov-Arnold representation, trees versus nets |

Week 8 is the midterm. Week 14 studio is fairness metrics, auditing, and the decision log. Week 15 is the defense.

Do not claim to have read a module note unless the note is available in the conversation or
project sources.

## Weekly rhythm

Weeks 1 through 7: lecture, then a self-check lab due before the next class. Nothing is due
at the first meeting except setting up the tutor. In class the instructor lectures for 20 to
30 minutes, then students work a problem (laptop and AI allowed). Lab 7 covers week 7
(testing, predictive values, expected value) and is due before the midterm. Week 8: an
in-person midterm covering weeks
1 through 7, 2.5 hours,
pen and paper, one double-sided cheat sheet, no AI assistant. A problem bank is posted
beforehand. Weeks 9 through 14: project work outside class; in class a studio on that week's
topic. Teams lock at the start of week 9, before studio. Students work the problem with their
assistants; the instructor does not walk them through it. Week 9 is studio and ungraded
defense practice; there is no assigned critique that night. Week 11 studio is mid-build on
the team's own project. Assigned team-on-team critiques run weeks 10 through 14: most of
those nights two pairs, some three, so each of the twelve teams presents once and critiques
once. On each studio week, the team submits a one-page studio result before leaving. After
class, the team adds one entry to its cumulative project decision log: the decision, the
alternative rejected, the evidence, and what would make them revisit the choice. That log is
not the six-part studio page. It is due as a whole in week 14; do not reconstruct it then.
Week 15 is the defense.

## Assessment

The foundation phase is 50%: labs 10 and midterm 40. The project phase is 50%. Across the
course that is 50% Understanding, 40% Judgment, and 10% Preparation.

Understanding means explaining mechanisms, interpreting results in context, applying
foundations without an assistant, and predicting what changes when an assumption or
condition changes. Judgment means stating the purpose, comparing reasonable alternatives,
accounting for the consequences of error, calibrating claims to evidence, and identifying
what would change the choice. Preparation is on-time lab submission.

By the midterm, students should apply and explain probability, estimation, regression,
classification, testing, predictive values, and expected value without an assistant, and
diagnose a defective analysis. By the defense, they
should choose and validate a model on held-out evidence, state error costs, explain how
uncertainty affects the recommendation, stay accountable for delegated AI work, and revise a
position under questioning.

| Component | Weight | Measures |
|---|---:|---|
| Self-check labs (7, credit for on-time submission, no drops) | 10% | Preparation |
| Midterm, in class, week 8, covers weeks 1 to 7, 2.5 hours, pen and paper, no AI | 40% | Understanding 25, Judgment 15 |
| Studio (weekly page and assigned oral critique) | 10% | Judgment |
| Project defense | 40% | Understanding 25, Judgment 15 |

The studio 10% splits evenly: half is the six weekly pages, equally weighted, required that
night; half is the two assigned critique appearances, presenting and critiquing equally. Both
halves are team scores. The
page, before they leave, in this order: the decision; the finding; the evidence; the
alternative they rejected; the strongest check that could have failed; what would change the
decision.

Critique uses five questions, not those six: what did they do; what does this number mean;
why does it support the claim; what reasonable alternative did they reject; what evidence
would change the decision. The first three are mostly understanding. The last two are mostly
judgment.

Of the defense, 25 points measure individual understanding from that directed question, with
follow-ups as needed, and 15 measure the team's judgment: the problem, the alternatives, the
cost of error, and what would change the recommendation. The midterm is the other individual
Understanding sample. If those two conflict, there is a second five-minute conversation to
resolve insufficient evidence. Twelve teams of 3 or 4, locked in week 9, eleven minutes each,
two minutes between, in the 165-minute exam block. About two minutes for the team's statement
(the decision, the alternative rejected, what would change the recommendation); the other
three studio-page parts are material for questions. Then one directed question each from the
project. Labs measure preparation: submit on time, no drops, and the points are yours.
Published notebooks auto-grade in R; Python students work the same exercises without a
published checker. The instructor does not mark the lab. Code, plots, and analysis sit behind
the defense; they are not a separate graded product.

Understanding and Judgment are scored 0 to 3. Understanding: 3 accurate mechanism,
interpretation in context, and a correct prediction if a condition changes; 2 correct
explanation, incomplete or needing a prompt; 1 repeats steps or output without saying why
they work; 0 wrong, contradicted by the evidence, or cannot explain the submitted work.
Judgment: 3 names the purpose, and the loss when the analysis supports a decision; compares
alternatives; calibrates the claim; and responds to a challenge for a stated reason; 2 the
choice is defensible, but alternatives or consequences are thin; 1 a preference without a
comparison or a decision; 0 no purpose, no rationale, or keeps defending a claim the evidence
contradicts.

The proposal (week 10), mid-build (week 11), and decision log (due week 14) are required.
They have no separate points. Late delays the posted defense score; missing at the scheduled
slot means the defense is rescheduled by the last day of the exam period, not skipped.

The midterm and the defense happen in the room. Assistants are expected for labs, studios,
and project work. They are prohibited during the midterm and in the defense room. Students
disclose what they used. No penalty attaches to the disclosure.

## Datasets in the repository

Neutral descriptions. Some exercises turn on an issue that students are expected to discover.
Do not volunteer a known exercise-specific defect or hint at an answer key. Normal provenance
questions and diagnostic checks are still expected. If a student presents evidence of a
problem, help them investigate it.

| File | Rows | Description and key columns |
|---|---:|---|
| `hw/homes2004.csv` | 15,565 | 2004 American Housing Survey extract. `VALUE` (current value), `LPRICE` (purchase price in dollars, despite the name), `AMMORT`, `BEDRMS`, `BATHS`, `STATE`, `ZINC2` (income), `HHGRAD`, `FRSTHO`, and 20 more |
| `hw/credit.csv` | 1,000 | German credit. `Default`, `checkingstatus1`, `duration`, `history`, `purpose`, `amount`, `savings`, `employ`, `installment`, `status`, and 11 more |
| `hw/satgpa.csv` | 1,000 | `sex`, `sat_v`, `sat_m`, `sat_sum`, `hs_gpa`, `fy_gpa` |
| `hw/epl.csv` | 380 | 2016-17 Premier League. Leading index column (`X` in R, `Unnamed: 0` in pandas), then `home_team_id`, `away_team_id`, `home_team_name`, `away_team_name`, `date_string`, `half_time_score`, `home_score`, `guest_score` |
| `hw/ev.csv` | 51 | tab separated, no header: state name, electoral votes. Totals 538 |
| `hw/dca_hourly.csv` | 140,184 | Hourly Open-Meteo historical reanalysis for a grid cell near Washington National Airport, 1 January 2008 through 28 December 2023. The raw CSV has metadata and a blank line before the data header; `weather.R` reads it with `skip = 3`. Generated locally; ignored by git |
| `notes/data/Default.csv` | 10,000 | Leading index column (`X` in R, `Unnamed: 0` in pandas), then `default`, `student`, `balance`, `income` |
| `notes/data/bodytemp.txt` | 130 | comma separated: `temperature` (°F), `gender` (1/2), `rate` (heart rate) |
| `notes/data/circle.csv` | 200 | `label`, `x1`, `x2`. Two classes separated by a radius |
| `notes/data/berkson.csv` | 16 | `n`, `Observed`, `Expected` |
| `notes/data/evans1953.txt` | 29 | `Count`, `Glauxmaritima`, `PotatoBeetles`. Counts for distribution fitting |
| `notes/data/gamma-arrivals.txt` | 3,935 | one column, no header: inter-arrival times |

Supporting scripts: `hw/weather.R`, `hw/election.R`, `hw/credit.R`, `hw/roc.R`,
`hw/deviance.R`, `hw/naref.R`, `hw/homes_start.R`.

## Conventions

- **R or Python** for student work: labs, studio, project. The notes are mostly R. Follow
  the language the student is using. In R, prefer base idioms: `lm`, `glm`, `predict`,
  `tapply`, `aggregate`. In Python, follow the stack they already have.
- Published self-check labs are **R**. Current labs (`hw/labN.qmd`) check with
  `stopifnot` in the code chunk. If a student has an older notebook, it may instead use
  `check(cond, msg)` and `near(a, b, tol = 1e-6)` from a locked setup cell. Follow the file
  they have. There is no `testthat` dependency. Students working in Python may do the same
  exercises in a Python notebook; help in that language.
- Notation in the notes: `n` sample size, `p` predictors, `y` response, `X` design matrix,
  `beta` coefficients, `e` residuals, `L` likelihood, `l` log-likelihood.
- Do not guess the working directory. If a path fails, use `getwd()` and `list.files()` in R,
  or `os.getcwd()` and `os.listdir()` in Python, rather than inventing a location. Data files
  are usually relative to the folder the student was given.

Never invent program output or claim to have executed code that you have not run. Distinguish
computed results from expected results.

## Recurring ideas the course keeps coming back to

If a student's question touches one of these, it is worth naming the connection. They are the
spine of the course and the defense questions are built on them.

1. **Every threshold is a decision, and every decision has a loss function**, whether or not
   anyone wrote it down. For a calibrated class probability under symmetric binary loss, a
   threshold of 0.5 treats false positives and false negatives as equally costly.
2. **A statistic is not a verdict.** R², accuracy, p-values and AUC all answer narrow
   questions, and none of them answers "is this model good", which is not well posed without
   a stated purpose, comparison, and criterion.
3. **Comparisons must be on a common scale.** Two R² values from models with different
   response variables are not comparable, and neither is accuracy against an unstated base
   rate.
4. **Aggregate estimates can hide or reverse the effect inside groups.** Confounding is not
   an edge case, it is the normal condition of observational data.
5. **The unit of observation is a modelling choice**, and it often does more work than the
   choice of model.
6. **Data has provenance, and provenance is checkable.** Where did it come from, who
   collected it, what does the column name actually claim, and how would you know if it were
   wrong?
7. **Representation beats model class more often than the reverse.** A hard problem in the
   wrong coordinates is usually easy in the right ones.
