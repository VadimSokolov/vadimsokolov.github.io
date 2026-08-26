# AI 600 course context

*Reference material for the course tutor. Attach this alongside `tutor-instructions.md`.*

## Modules and the weeks they cover

| Module | Notes file | Weeks | Topics |
|---|---|---|---|
| 1. Foundations | `01-intro.html` | 1 to 2 | the AI/ML landscape, probability, distributions, Bayes, dummy variables |
| 2. Estimation | `02-estimation.html` | 3 to 4 | CDFs and quantiles, method of moments, maximum likelihood, the CLT, bootstrap |
| 3. Patterns | `03-pattern.html` | 5 to 6 | correlation, OLS, residuals, transformations, multiple regression, power laws |
| 4. Decisions | `04-decisions.html` | 8 to 9 | hypothesis testing, predictive values, expected value, utility, paradoxes, the Kelly criterion |
| 5. Model selection | `05-modelselection.html` | 10 to 11 | bias-variance, cross-validation, ridge, lasso, shrinkage |
| 6. Deep learning | `06-dlai.html` | 12 to 13 | neural nets, ReLU and activations, projection pursuit, Kolmogorov-Arnold representation, trees versus nets |
| Responsible AI | | 14 | fairness metrics, auditing, the decision log |

Week 7 is the midterm. Week 15 is project presentations and defenses.

## Weekly rhythm

Weeks 1 through 6: reading and a self-check lab before class; lecture and worked examples in
class. Week 7: a review lab, then an in-person midterm with no AI assistant. Weeks 8 through
14: project work outside class; in class a live analysis, a team studio, and an assigned
team-on-team critique. After studio each team writes one decision-log entry. Week 15 is
project defenses.

## Assessment

The grade is half midterm, half project.

| Component | Weight |
|---|---:|
| Self-check labs (7, lowest 2 dropped) | 10% |
| Midterm, in class, week 7, no AI | 40% |
| Studio pages | 10% |
| Project defense | 25% |
| Final project | 15% |

The midterm and the defense happen in the room. Assistants are expected. Students disclose
what they used. No penalty attaches to the disclosure.

## Datasets in the repository

Neutral descriptions. Several of these are used in exercises that turn on something not
mentioned here, so do not speculate about their quality unprompted; if a student has found
something and asks you to confirm it, engage with what they found.

| File | Rows | Columns |
|---|---:|---|
| `hw/homes2004.csv` | 15,565 | 2004 American Housing Survey extract. `VALUE` (current value), `LPRICE` (purchase price in dollars, despite the name), `AMMORT`, `BEDRMS`, `BATHS`, `STATE`, `ZINC2` (income), `HHGRAD`, `FRSTHO`, and 20 more |
| `hw/credit.csv` | 1,000 | German credit. `Default`, `checkingstatus1`, `duration`, `history`, `purpose`, `amount`, `savings`, `employ`, `installment`, `status`, and 11 more |
| `hw/satgpa.csv` | 1,000 | `sex`, `sat_v`, `sat_m`, `sat_sum`, `hs_gpa`, `fy_gpa` |
| `hw/epl.csv` | 380 | 2016-17 Premier League. `home_team_name`, `away_team_name`, `date_string`, `half_time_score`, `home_score`, `guest_score` |
| `hw/ev.csv` | 51 | tab separated, no header: state name, electoral votes. Totals 538 |
| `hw/dca_hourly.csv` | 140,184 | hourly weather at Washington National, 2008 to 2023, downloaded by `hw/weather.R` from the Open-Meteo archive (ERA5). Not tracked in git; the script fetches it |
| `notes/data/Default.csv` | 10,000 | `default`, `student`, `balance`, `income` |
| `notes/data/bodytemp.txt` | 130 | comma separated: `temperature` (°F), `gender` (1/2), `rate` (heart rate) |
| `notes/data/circle.csv` | 200 | `label`, `x1`, `x2`. Two classes separated by a radius |
| `notes/data/berkson.csv` | 16 | `n`, `Observed`, `Expected` |
| `notes/data/evans1953.txt` | 29 | `Count`, `Glauxmaritima`, `PotatoBeetles`. Counts for distribution fitting |
| `notes/data/gamma-arrivals.txt` | 3,935 | one column, no header: inter-arrival times |

Supporting scripts: `hw/weather.R`, `hw/election.R`, `hw/credit.R`, `hw/roc.R`,
`hw/deviance.R`, `hw/naref.R`, `hw/homes_start.R`.

## Conventions

- **R**, base idioms. `lm`, `glm`, `predict`, `tapply`, `aggregate`. Module 6 has some Python.
- Notebooks run on **IRkernel**. Concept-check tests use two helpers defined in each
  notebook's locked setup cell: `check(cond, msg)` and `near(a, b, tol = 1e-6)`. There is no
  `testthat` dependency.
- Notation in the notes: `n` sample size, `p` predictors, `y` response, `X` design matrix,
  `beta` coefficients, `e` residuals, `L` likelihood, `l` log-likelihood.
- Data paths in student code are usually relative to the repository root.

## Recurring ideas the course keeps coming back to

If a student's question touches one of these, it is worth naming the connection. They are the
spine of the course and the defense questions are built on them.

1. **Every threshold is a decision, and every decision has a loss function**, whether or not
   anyone wrote it down. A default of 0.5 is a claim that the two errors cost the same.
2. **A statistic is not a verdict.** R², accuracy, p-values and AUC all answer narrow
   questions, and none of them answers "is this model good", which is not well posed without
   a decision.
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
