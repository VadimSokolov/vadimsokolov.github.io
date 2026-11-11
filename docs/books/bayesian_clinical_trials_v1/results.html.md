# Results by chapter <small>Bayesian Clinical Trials and Personalized Medicine</small>

The results of [Bayesian Clinical Trials and Personalized Medicine: Volume I: Bayesian Clinical Trials](https://vsokolov.org/books/bayesian_clinical_trials_v1/) that are new in the book, that come from the authors' own papers, or that correct one of those papers, as the book states them: 12 entries (5 proved, 7 computed). Results of other authors that the book presents are credited in the [chapter summaries](https://github.com/VadimSokolov/bayesian_clinical_trials_v1/tree/main/summaries).

Status: proved; computed (established by a computation that the book reports and the entry names, such as an exact census or a fit to one, and not proved for every case); conditional (proved assuming the named statements, which the book does not prove); open (stated as an open question); counterexample (a proved counterexample); withdrawn (found wrong after release; the entry says what was wrong and which version corrects it).

## Chapter 6. Prior, Likelihood, Posterior

<a id="bnt162b2_beta_binomial_reproduction"></a>

### Reproduction of the BNT162b2 beta binomial analysis

Section 6.12.1, page 136 of Sokolova, Sokolov and Polson (2026), *Bayesian Clinical Trials and Personalized Medicine: Volume I: Bayesian Clinical Trials*, edition 1. New in this book.

Status: computed.

Statement. With the plan's prior $p \sim \mathrm{Beta}(0.700102, 1)$ and $s_1 = 8$ cases in the vaccine arm out of $s = 170$, the posterior is $\mathrm{Beta}(0.700102 + 8, 1 + 162)$. The posterior probability that vaccine efficacy exceeds 30 per cent is $1 - 2\times 10^{-28}$, which clears the final analysis threshold 0.986. The 95 per cent credible interval for vaccine efficacy is about $(90.4\%, 97.6\%)$ and the point estimate is 95.1 per cent (plug in) or 94.9 per cent (posterior median), against the published 95.0 per cent with interval 90.3 to 97.6, without modeling the small difference in surveillance time between the arms.

Source: [`05-bayes.qmd`](https://github.com/VadimSokolov/bayesian_clinical_trials_v1/blob/v1.1.1/05-bayes.qmd), label `res-bnt162b2-reproduction`.

## Chapter 7. Weighing Evidence: p-values, Bayes Factors, and Posterior Probabilities

<a id="bayes_bar_crossing_46"></a>

### The Bayes factor bar exceeds the fixed level bar once information times prior variance passes about 46

Section 7.5.1, page 148 of Sokolova, Sokolov and Polson (2026), *Bayesian Clinical Trials and Personalized Medicine: Volume I: Bayesian Clinical Trials*, edition 1. New in this book.

Status: computed.

Statement. At one sided $\alpha = 0.025$ the fixed level test acts when $Z_n \ge z_\alpha = 1.96$ (that is, $Z_n > 0$ and $Z_n^2 \ge 3.84$), and the Bayes rule with equal prior odds acts, asymptotically, when $Z_n > 0$ and $Z_n^2 \ge L_n$ with $L_n = \log(1 + I_n\tau^2) \approx \log n$. They cross at $n^\ast = e^{3.84} \approx 46$, that is at $I_n\tau^2 \approx 46$ (the exact Gaussian expression gives 41.6), which is $n > 46$ for a unit information prior. At $\tau = 0.25$ on the log hazard ratio scale this needs $I_n > 730$, about 2,900 events (exact crossing 41.6: 666 and about 2,660 events). Beyond the crossing the Bayesian bar against a single unadjusted look is the higher one.

Source: [`06-evidence.qmd`](https://github.com/VadimSokolov/bayesian_clinical_trials_v1/blob/v1.1.1/06-evidence.qmd), label `res-bayes-bar-crossing`.

## Chapter 9. Error Rates, Power, and Sample Size

<a id="moderate_deviation_sample_size"></a>

### Moderate deviation sample size equation

Section 9.3.2, page 202 of Sokolova, Sokolov and Polson (2026), *Bayesian Clinical Trials and Personalized Medicine: Volume I: Bayesian Clinical Trials*, edition 1. First stated in Polson and Sokolov (2026), Bayesian versus Standard Clinical Trial Design: Theory, Evidence, and Protocol, working paper.

Status: proved.

Statement. For the moderate deviation rule, which acts when $Z_n^2 \ge \log n + C$ (with $Z_n > 0$ for a one sided claim), the power against an effect $\theta$ with information $I$ per unit of $n$ is $\Phi\big(\sqrt{nI}\,|\theta| - \sqrt{\log n + C}\big) + o(1)$. Setting this equal to $1-\beta$ gives the sample size equation $n I \theta^2 = \big(\sqrt{\log n + C} + z_\beta\big)^2$, which is the textbook equation with $z_\alpha$ replaced by $\sqrt{\log n + C}$. The formula is an asymptotic approximation; it is not claimed to predict the size of any particular trial, including SELECT, whose planned size (1,225 events for a design hazard ratio of 0.83; the textbook formula gives about 1,211) is close to the textbook calculation at its own design alternative.

Source: [`08-power.qmd`](https://github.com/VadimSokolov/bayesian_clinical_trials_v1/blob/v1.1.1/08-power.qmd), label `res-md-sample-size`.

<a id="moderate_deviation_select_comparison"></a>

### Moderate deviation and textbook sizes at the SELECT hazard ratio of 0.80 (not a prediction of SELECT's size)

Section 9.3.6, page 207 of Sokolova, Sokolov and Polson (2026), *Bayesian Clinical Trials and Personalized Medicine: Volume I: Bayesian Clinical Trials*, edition 1. First stated in Polson and Sokolov (2026), Bayesian versus Standard Clinical Trial Design: Theory, Evidence, and Protocol, working paper.

Status: computed.

Statement. For a hazard ratio of 0.80 ($|\log\mathrm{HR}| = 0.2231$, $Z = |\log\mathrm{HR}|\sqrt{d}/2$ in terms of $d$ events) and 90 per cent power, the textbook calculation at one sided 0.025 calls for 844 events, and the moderate deviation calculation calls for 1,067 events at equal prior odds and 1,255 at prior odds of two to one against. SELECT was designed for a hazard ratio of 0.83 with 90 per cent power, one sided 0.025 and 1,225 planned events, with one interim at two thirds of them (Ryan et al. 2020), and the observed hazard ratio was 0.80 on 1,270 events (Lincoff et al. 2023). The textbook calculation at the design hazard ratio gives about 1,211 events, close to the plan, so the comparison at 0.80 changes the design alternative and does not show that the moderate deviation formula predicts or explains SELECT\'s size.

Source: [`08-power.qmd`](https://github.com/VadimSokolov/bayesian_clinical_trials_v1/blob/v1.1.1/08-power.qmd), label `res-md-select-prediction`.

## Chapter 10. Multiplicity and Shrinkage

<a id="ulcer_bonferroni_vs_posterior"></a>

### Four operation ulcer example, adjusted p value against posterior probability

Section 10.5.3, page 232 of Sokolova, Sokolov and Polson (2026), *Bayesian Clinical Trials and Personalized Medicine: Volume I: Bayesian Clinical Trials*, edition 1. First stated in Polson and Sokolov (2026), Bayesian versus Standard Clinical Trial Design: Theory, Evidence, and Protocol, working paper.

Status: computed.

Statement. In the four operation ulcer example (counts illustrative, at the scale of the 1965 trial of Novick and Grizzle), the Bonferroni adjusted $p$-value for best against worst is $0.0855$, while the hierarchical posterior probability that drainage and vagotomy is worse than 75 per cent resection is $0.952$, on a contrast shrunk from $1.053$ to $0.464$. A posterior probability of $0.952$ is not a claim of statistical significance under strong familywise error control.

Source: [`09-multiplicity.qmd`](https://github.com/VadimSokolov/bayesian_clinical_trials_v1/blob/v1.1.1/09-multiplicity.qmd), label `res-ulcer-reading`.

## Chapter 11. Interim Looks and the Three Deviation Scales

<a id="evidence_tolls_three_scales"></a>

### The three deviation scales (evidence tolls)

Section 11.9.2, page 253 of Sokolova, Sokolov and Polson (2026), *Bayesian Clinical Trials and Personalized Medicine: Volume I: Bayesian Clinical Trials*, edition 1. First stated in Polson and Sokolov (2026), Bayesian versus Standard Clinical Trial Design: Theory, Evidence, and Protocol, working paper.

Status: proved.

Statement. Let $Z_n$ be the standardized score at information $I_n$, $q = I_n\tau^2$ for a normal prior of scale $\tau$, and $L_n = \log(1+q)$ the Ockham penalty. The one sided fixed level test at level $\alpha$ acts when $Z_n \ge z_\alpha$. For the symmetric normal mixture, the exact Bayes factor rule with threshold $b$ acts when $Z_n^2 \ge (1 + 1/q)\{\log(1+q) + 2\log b\}$ with $Z_n > 0$ for a one sided claim, and the anytime valid rule at level $\alpha$ is the same with $b = 1/\alpha$. In the large information approximation these bars are $Z_n^2 \ge L_n + 2\log b$ and $Z_n^2 \ge L_n + 2\log(1/\alpha)$, so that the anytime valid rule requires about $2\log(1/\alpha) = 7.38$ more, in squared standardized units, than the Bayes rule at $b = 1$ (exactly $7.38(1 + 1/q)$). This is a property of the normal mixture construction and not a universal cost of anytime validity: other e processes, such as iterated logarithm confidence sequences, behave differently.

Source: [`10-sequential.qmd`](https://github.com/VadimSokolov/bayesian_clinical_trials_v1/blob/v1.1.1/10-sequential.qmd), label `res-evidence-tolls`.

<a id="surcharge_seventy_percent"></a>

### The surcharge for validity at every stopping time is about 70 per cent of the fixed trial requirement, as a comparison of boundary terms

Section 11.9.4, page 256 of Sokolova, Sokolov and Polson (2026), *Bayesian Clinical Trials and Personalized Medicine: Volume I: Bayesian Clinical Trials*, edition 1. First stated in Polson and Sokolov (2026), Bayesian versus Standard Clinical Trial Design: Theory, Evidence, and Protocol, working paper.

Status: proved.

Statement. With per observation standardized effect $\theta$, the information needed to act satisfies, in the large information approximation, $n_{\mathrm{MD}}\theta^2 = \log n_{\mathrm{MD}} + C$ for the Bayes rule and $n_{\mathrm{LD}}\theta^2 = \log n_{\mathrm{LD}} + C + 2\log(1/\alpha)$ for the anytime valid rule. Subtracting gives $(n_{\mathrm{LD}} - n_{\mathrm{MD}})\theta^2 = 2\log(1/\alpha) + \log(n_{\mathrm{LD}}/n_{\mathrm{MD}})$, and the last term is positive. On the standardized scale the surcharge $2\log(1/\alpha) = 7.38$ at $\alpha = 0.025$ is about 70 per cent of the fixed trial requirement $(z_\alpha + z_\beta)^2 = 10.51$ at 90 per cent power ($7.38/10.51 \approx 0.70$). This compares boundary terms asymptotically. It is not an exact sample size identity (at $\theta = 0.20$ and $C = 0$ the larger roots differ by about 80 per cent of the fixed requirement), and the exact surcharge is $7.38(1 + 1/q)$. The baseline is the uncalibrated Bayes factor bar; a calibrated Bayesian rule has already paid part of the surcharge, so calibration narrows the realized gap.

Source: [`10-sequential.qmd`](https://github.com/VadimSokolov/bayesian_clinical_trials_v1/blob/v1.1.1/10-sequential.qmd), label `res-seventy-percent`.

## Chapter 14. Operating Characteristics by Simulation

<a id="null_maximum_calibration"></a>

### Calibration of a posterior probability rule by the null maximum

Section 14.4.1, page 309 of Sokolova, Sokolov and Polson (2026), *Bayesian Clinical Trials and Personalized Medicine: Volume I: Bayesian Clinical Trials*, edition 1. New in this book.

Status: proved.

Statement. Let $M$ be, for one simulated null trial, the largest posterior probability $\Pr(p_1 - p_0 > a \mid \text{data})$ that the trial reaches at any look it attends. The rule "success if the probability exceeds $c$ at any look" rejects exactly when $M > c$, so its type I error is $\Pr(M > c)$, and the smallest $c$ with type I error at most $\alpha$ is the $(1-\alpha)$ quantile of $M$. The $(1-\alpha)$ quantile of $M$ over the null simulations is a Monte Carlo estimate of it: it fixes the rejection proportion in the calibration sample and not the population error (the binomial standard error near 0.025 is about 0.0008 at 40,000 runs), so the threshold should be validated on independent null simulations. A single simulation serves every candidate $c$ (common random numbers). If futility stopping is part of the design, $M$ is the maximum over the looks the trial actually reaches.

Source: [`12-simulation.qmd`](https://github.com/VadimSokolov/bayesian_clinical_trials_v1/blob/v1.1.1/12-simulation.qmd), label `res-null-max-calibration`.

## Chapter 15. Predictive Probability, Interim Monitoring, and Stopping

<a id="backward_induction_states"></a>

### Exact backward induction for binary endpoints on a cubic lattice

Section 15.6.2, page 342 of Sokolova, Sokolov and Polson (2026), *Bayesian Clinical Trials and Personalized Medicine: Volume I: Bayesian Clinical Trials*, edition 1. First stated in Polson and Sokolov (2026), Bayesian Adaptive Clinical Trials: Priors, Thompson Sampling, Predictive Stopping and Backward Induction, manuscript submitted to Statistics in Medicine.

Status: proved.

Statement. For fixed prior parameters and horizon $T$ pairs, in a two arm trial with binary outcomes and independent beta priors, the optimal policy at stage $k$ is a function of $(s_1, s_0, k)$ only, where $s_1$ and $s_0$ are the success counts in the two arms, and the Bellman recursion evaluates $\sum_{k=0}^{T}(k+1)^2 = (T+1)(T+2)(2T+3)/6 = O(T^3)$ states, each in constant time.

Source: [`13-predictive.qmd`](https://github.com/VadimSokolov/bayesian_clinical_trials_v1/blob/v1.1.1/13-predictive.qmd), label `res-backward-induction-states`.

<a id="utility_only_rule_null_declaration"></a>

### A utility only backward induction rule declares treatment better half the time under the null

Section 15.6.3, page 345 of Sokolova, Sokolov and Polson (2026), *Bayesian Clinical Trials and Personalized Medicine: Volume I: Bayesian Clinical Trials*, edition 1. First stated in Polson and Sokolov (2026), Bayesian Adaptive Clinical Trials: Priors, Thompson Sampling, Predictive Stopping and Backward Induction, manuscript submitted to Statistics in Medicine.

Status: computed.

Statement. In the calculation of Polson and Sokolov with $\kappa = 0.0005$ and a maximum of 100 pairs, utility only backward induction declares treatment better with probability 0.513 under the null (Monte Carlo standard error 0.005) and 0.98 at the large effect, with an expected sample size of 14.4 per arm. The classification loss version with $\gamma = 0.975$ has a null declaration probability of 0.026, power 0.903 and an expected sample size of 54.3 per arm at the large effect. This is a simulation result for the stated loss, prior and horizon.

Source: [`13-predictive.qmd`](https://github.com/VadimSokolov/bayesian_clinical_trials_v1/blob/v1.1.1/13-predictive.qmd), label `res-utility-only-null`.

## Chapter 20. Master Protocols and Platform Trials

<a id="shared_control_false_positive_counts"></a>

### Shared control false positive counts for four arms

Section 20.4.1, page 452 of Sokolova, Sokolov and Polson (2026), *Bayesian Clinical Trials and Personalized Medicine: Volume I: Bayesian Clinical Trials*, edition 1. New in this book.

Status: computed.

Statement. For four null arms each tested at one sided level 0.025, four independent trials give at least one false positive with probability 9.6 per cent and two or more with probability 0.4 per cent. With a shared control and equal allocation these are 7.8 and 1.7 per cent, and with square root allocation (control $\sqrt{k}$ times an experimental arm) they are 8.6 and 1.2 per cent. The mean count is 0.10 in every case. The shared control values are Monte Carlo (400,000 draws).

Source: [`17-platform.qmd`](https://github.com/VadimSokolov/bayesian_clinical_trials_v1/blob/v1.1.1/17-platform.qmd), label `res-shared-control-counts`.

## Chapter 21. Case Studies: Cardiovascular, Alzheimer's and Vaccine Trials

<a id="select_reconstruction_medians"></a>

### SELECT reconstruction, median events at decision with conditioning

Section 21.1.2, page 476 of Sokolova, Sokolov and Polson (2026), *Bayesian Clinical Trials and Personalized Medicine: Volume I: Bayesian Clinical Trials*, edition 1. First stated in Polson and Sokolov (2026), Bayesian versus Standard Clinical Trial Design: Theory, Evidence, and Protocol, working paper.

Status: computed.

Statement. In the SELECT reconstruction (true hazard ratio 0.80, normal prior of scale 0.25 on the log hazard ratio, at most 1,270 events, rules evaluated at every second event, 40,000 simulated paths, SELECT designed for hazard ratio 0.83 with 90 per cent power, 1,225 planned events and one interim at two thirds, Ryan et al. 2020), the median number of events at decision among simulated trials that declare efficacy is 464 for the Bayesian rule calibrated to 2.5 per cent one sided, 612 for the e value rule and 952 for a hypothetical four look O\'Brien-Fleming design. Over all trials, counting a trial that never crosses at its maximum, the medians are 486, 714 and 952. Power is 0.947, 0.831 and 0.977, and the realized one sided type I errors are 0.025, 0.0058 and 0.0255 (the Bayesian rule is calibrated to 2.5 per cent, the e value rule is bounded by it). SELECT\'s planned design (interim at 817 of 1,225 events with Lan-DeMets O\'Brien-Fleming type spending, then final) has median 817 in both senses, power 0.974 and type I error 0.0254. A single unadjusted look would cross at 309 events on the mean path, a mean path approximation and not a stopping time. The reconstruction is ours and not the sponsor\'s, and it is a counterfactual, not a power calculation made before the trial.

Source: [`18-cases.qmd`](https://github.com/VadimSokolov/bayesian_clinical_trials_v1/blob/v1.1.1/18-cases.qmd), label `res-select-reconstruction`.

***

<small>License: Text, figures and PDF: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Code: [MIT](https://opensource.org/license/mit).</small>

<small>This page is generated from the book's repository ([main](https://github.com/VadimSokolov/bayesian_clinical_trials_v1/tree/main)). The numbers and pages are those of the PDF, [version 1.1.1](https://github.com/VadimSokolov/bayesian_clinical_trials_v1/releases/tag/v1.1.1).</small>

<!-- Generated by bookrepo.py from book.yaml and results.yaml. Edit those files, not this one. -->
