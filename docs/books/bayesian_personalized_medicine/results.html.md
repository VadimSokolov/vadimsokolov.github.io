# Results by chapter <small>Bayesian Personalized Medicine</small>

The results of [Bayesian Personalized Medicine: Utility, Value and Decision](https://vsokolov.org/books/bayesian_personalized_medicine/) that are new in the book, that come from the authors' own papers, or that correct one of those papers, as the book states them: 7 entries (7 proved). Results of other authors that the book presents are credited in the [chapter summaries](https://github.com/VadimSokolov/bayesian_personalized_medicine/tree/main/summaries).

Status: proved; conditional (proved assuming the named statements, which the book does not prove); open (stated as an open question); counterexample (a proved counterexample); withdrawn (found wrong after release; the entry says what was wrong and which version corrects it).

## Chapter 3. Modal Doctor, Bayesian Patient

<a id="severity_monotone_divergence"></a>

### Severity monotone divergence of the Bayes and MAP actions

Proposition 3.1, page 26 of Sokolova, Sokolov and Polson (2026), *Bayesian Personalized Medicine: Utility, Value and Decision*, edition 1. New in this book.

Status: proved.

Statement. Let the disease states be ordered by severity, $\theta_1 \leq \cdots \leq \theta_K$, and the actions ordered by aggressiveness. Let $U(\theta,a)$ be the utility of action $a$ in state $\theta$, and suppose $U$ has increasing differences in $(\theta,a)$: for an action $a'$ less aggressive than $a$, the difference $U(\theta,a)-U(\theta,a')$ is nondecreasing in $\theta$. Let $\pi$ be the posterior over states, with mode $\hat\theta=\arg\max_\theta \pi(\theta\mid x)$, let $\delta_{\mathrm{MAP}}(x)=\arg\max_a U(\hat\theta(x),a)$ be the action that maximizes utility at the modal state, and let $\delta_{\mathrm{B}}(x)=\arg\max_a \mathbb{E}_\pi[U(\theta,a)\mid x]$ be the action that maximizes posterior expected utility. If $\pi$ puts no mass below the mode $\hat\theta$, then some Bayes action $\delta_{\mathrm{B}}$ is at least as aggressive as $\delta_{\mathrm{MAP}}$.

Source: [`03-modal-doctor.qmd`](https://github.com/VadimSokolov/bayesian_personalized_medicine/blob/v1.0.0/03-modal-doctor.qmd), label `prp-md-divergence`.

<a id="wedge_lower_bound"></a>

### Wedge lower bound for the Bayes advantage of aggressive treatment

Proposition 3.2, page 26 of Sokolova, Sokolov and Polson (2026), *Bayesian Personalized Medicine: Utility, Value and Decision*, edition 1. New in this book.

Status: proved.

Statement. Let $a_+$ be an aggressive action and $a_-$ a conservative one, let $\hat\theta$ be the modal state of the posterior $\pi$, and let $\theta_{\mathrm{crit}}$ be a critical state. Put $\pi_{\mathrm{tail}}=\pi(\theta\geq\theta_{\mathrm{crit}})$, $\Delta U_{\mathrm{tail}}=U(\theta_{\mathrm{crit}},a_+)-U(\theta_{\mathrm{crit}},a_-)>0$, and $\Delta C=U(\hat\theta,a_-)-U(\hat\theta,a_+)>0$, the certain morbidity cost at the modal state, measured as a loss of utility (QALYs) and not money. Suppose the advantage $U(\theta,a_+)-U(\theta,a_-)$ is at least $\Delta U_{\mathrm{tail}}$ at every state $\theta\geq\theta_{\mathrm{crit}}$ and at least $-\Delta C$ at every state below $\theta_{\mathrm{crit}}$. Then $\mathbb{E}_\pi[U(\theta,a_+)-U(\theta,a_-)]\geq \pi_{\mathrm{tail}}\,\Delta U_{\mathrm{tail}}-\Delta C$. In particular, whenever $\pi_{\mathrm{tail}}\Delta U_{\mathrm{tail}}>\Delta C$ the Bayes rule prefers $a_+$ to $a_-$, even if the modal rule recommends $a_-$.

Source: [`03-modal-doctor.qmd`](https://github.com/VadimSokolov/bayesian_personalized_medicine/blob/v1.0.0/03-modal-doctor.qmd), label `prp-md-wedge`.

<a id="undervaluation_of_posterior_yielding_actions"></a>

### Undervaluation of posterior yielding actions by direct utility

Proposition 3.3, page 28 of Sokolova, Sokolov and Polson (2026), *Bayesian Personalized Medicine: Utility, Value and Decision*, edition 1. New in this book.

Status: proved.

Statement. Consider a two stage decision problem with first stage utility $U(\theta,a)$, second stage action set $\mathcal{A}_2$, second stage utility $U_2$ and discount factor $\beta=e^{-r}$. The sequential value of a first stage action $a$ with information channel $\psi_a$ is $V(a)=\mathbb{E}_\theta[U(\theta,a)]+\beta\,\mathbb{E}_{y\sim\psi_a}\bigl[\max_{a'\in\mathcal{A}_2}\mathbb{E}_{\theta\mid y}U_2(\theta,a')\bigr]$, where $\mathbb{E}_{\theta\mid y}$ is the expectation under the post action posterior $\pi_y$, obtained from the prior by Bayes' rule after observing $y$. Let $a_y$ be posterior yielding with channel $\psi_y$ (the expected Shannon entropy of the posterior after observing $y$ is smaller than the entropy of the prior), and let $a_z$ be posterior absorbing, leaving the prior unchanged and a subset of $\mathcal{A}_2$ available. If the direct utilities are equal, $\mathbb{E}_\theta[U(\theta,a_y)]=\mathbb{E}_\theta[U(\theta,a_z)]$, then $V(a_y)-V(a_z)\geq\beta\bigl\{\mathbb{E}_{y\sim\psi_y}\bigl[\max_{a'\in\mathcal{A}_2}\mathbb{E}_{\theta\mid y}U_2(\theta,a')\bigr]-\max_{a'\in\mathcal{A}_2}\mathbb{E}_\theta U_2(\theta,a')\bigr\}\geq 0$, and the term in braces is zero if and only if one second stage action is optimal under every post action posterior $\pi_y$ for $y$ in the support of $\psi_y$.

Source: [`03-modal-doctor.qmd`](https://github.com/VadimSokolov/bayesian_personalized_medicine/blob/v1.0.0/03-modal-doctor.qmd), label `prp-md-undervaluation`.

## Chapter 5. Causal Effects: Models, Accounting and Randomization

<a id="exchangeable_models_are_coherent"></a>

### Exchangeable de Finetti models satisfy the McCullagh coherence requirements

Proposition 5.1, page 45 of Sokolova, Sokolov and Polson (2026), *Bayesian Personalized Medicine: Utility, Value and Decision*, edition 1. First stated in Polson and Sokolov (2026), Bayesian Causality: Models, Accounting and the Bayesian Alternative to Double Machine Learning, version 1.2.1, doi:10.5281/zenodo.23985916.

Status: proved.

Statement. Every model defined by a de Finetti representation $p(z_1,\ldots,z_n)=\int\prod_{i=1}^n p(z_i\mid\theta)\,\pi(d\theta)$ of the unit records $z_i=(x_i,t_i,y_i)$, with the same prior $\pi$ for every $n$, satisfies two of McCullagh's three requirements for a statistical model: the model for $n$ units is the marginal of the model for $n+1$ units (requirement 1), and relabelling the units or reparametrizing the covariates transforms the model in the obvious way (requirement 3). If, in addition, the conditional law $f(y\mid t,x,\theta)$ of the outcome given treatment and covariates is specified at every treatment and covariate value of interest, including values outside the support of the observed covariates, the model also satisfies requirement 2, that the model is defined at covariate values not observed.

Source: [`04a-causal.qmd`](https://github.com/VadimSokolov/bayesian_personalized_medicine/blob/v1.0.0/04a-causal.qmd), label `prp-exchangeable`.

## Chapter 7. Causal Decisions

<a id="regret_of_the_bayes_policy"></a>

### Regret of the Bayes policy under a Lipschitz value and posterior contraction

Proposition 7.1, page 80 of Sokolova, Sokolov and Polson (2026), *Bayesian Personalized Medicine: Utility, Value and Decision*, edition 1. First stated in Polson and Sokolov (2026), Bayesian Causality: Models, Accounting and the Bayesian Alternative to Double Machine Learning, version 1.2.1, doi:10.5281/zenodo.23985916.

Status: proved.

Statement. Let D be a class of policies, equipped with a norm \|\cdot\|, V_theta(d) the value of policy d under parameter theta, theta_0 the true parameter, d_0^* a maximizer of V_{theta_0}(d) over D (the oracle policy), and \hat d_n a maximizer over D of \int V_\theta(d)\,\pi_n(d\theta), where \pi_n is the posterior (the Bayes policy). Suppose that \sup_{d\in D}|V_\theta(d)-V_{\theta_0}(d)|\le L\,\|\theta-\theta_0\| for all \theta, and that \int\|\theta-\theta_0\|\,\pi_n(d\theta)\le\varepsilon_n. Then the regret satisfies V_{\theta_0}(d_0^*)-V_{\theta_0}(\hat d_n)\le 2L\varepsilon_n. If moreover V_{\theta_0}(d_0^*)-V_{\theta_0}(d)\ge c\,\|d-d_0^*\|^2 for all d\in D, then \|\hat d_n-d_0^*\|^2\le 2L\varepsilon_n/c.

Source: [`05a-causal-decisions.qmd`](https://github.com/VadimSokolov/bayesian_personalized_medicine/blob/v1.0.0/05a-causal-decisions.qmd), label `prp-regret`.

## Chapter 12. Regulatory Mechanisms and Strategic Experimentation

<a id="enforcement_substitutes_for_restriction"></a>

### Enforcement substitutes for restriction of the permitted analysis set

Proposition 12.1, page 122 of Sokolova, Sokolov and Polson (2026), *Bayesian Personalized Medicine: Utility, Value and Decision*, edition 1. First stated in Polson (2026), Regulate the prior, not the protocol: clinical trials as market design, working paper.

Status: proved.

Statement. Let $\mathcal{A}$ be the set of analyses the sponsor may perform, indexed by a scalar measure of richness, and let $\Delta\pi(\mathcal{A})$ be the sponsor's gain from deviating, increasing in $\mathcal{A}$. The regulator audits with probability $q$ at cost $\chi$ and imposes penalty $F \le \bar F$ on a detected deviation. The regulator chooses $(\mathcal{A}, q, F)$ to minimize $q\chi + \Lambda(\mathcal{A})$ subject to $qF \ge \Delta\pi(\mathcal{A})$ and $F \le \bar F$, where $\Lambda(\mathcal{A})$ is the welfare cost of restricting analysis, decreasing in the richness of $\mathcal{A}$. Suppose $\Delta\pi(\mathcal{A}) \le \bar F$ so that $q \le 1$. At an interior optimum, $\Lambda'(\mathcal{A}) = -\chi\,\Delta\pi'(\mathcal{A})/\bar F$. Both constraints bind, so the objective is $(\chi/\bar F)\,\Delta\pi(\mathcal{A}) + \Lambda(\mathcal{A})$, whose cross partial in $\mathcal{A}$ and $\chi/\bar F$ is $\Delta\pi'(\mathcal{A}) > 0$, so the optimal $\mathcal{A}$ falls as $\chi/\bar F$ rises. Hence a higher maximum penalty $\bar F$, or a cheaper audit technology, optimally buys a larger permitted analysis set, not a smaller one.

Source: [`11-mechanisms.qmd`](https://github.com/VadimSokolov/bayesian_personalized_medicine/blob/v1.0.0/11-mechanisms.qmd), label `prp-audit`.

## Chapter 13. Implications for the Biotech Industry

<a id="phase2_specificity_cost_per_approval"></a>

### Phase II specificity and cost per approved drug

Proposition 13.1, page 135 of Sokolova, Sokolov and Polson (2026), *Bayesian Personalized Medicine: Utility, Value and Decision*, edition 1. New in this book.

Status: proved.

Statement. Let $\pi$ be the prior probability that a drug works, $s$ the probability that Phase II recommends going on when the drug works (sensitivity), $f$ the probability that it recommends no go when the drug does not work (specificity), $q$ the probability that Phase III succeeds when the drug works (a drug that does not work never succeeds in Phase III), and $c_2$ and $c_3$ the costs of Phase II and Phase III. The probability of going to Phase III is $g = \pi s + (1-\pi)(1-f)$, the probability that a drug taken to Phase III works is $\pi s/g$, and the expected cost per approved drug is $C = (c_2 + g\,c_3)/(\pi s q)$. Specificity enters only the numerator, through $g$, and reduces $C$ by $(1-\pi)c_3/(\pi s q)$ per unit. Sensitivity enters both numerator and denominator. Raising $f$ lowers $C$ more than the same rise in $s$ whenever $(1-\pi)(s+f-1)c_3 > c_2$.

Source: [`12-biotech.qmd`](https://github.com/VadimSokolov/bayesian_personalized_medicine/blob/v1.0.0/12-biotech.qmd), label `prp-specificity`.

***

<small>License: Text, figures and PDF: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Code: [MIT](https://opensource.org/license/mit).</small>

<small>This page is generated from the book's repository ([main](https://github.com/VadimSokolov/bayesian_personalized_medicine/tree/main)). The numbers and pages are those of the PDF, [version 1.0.0](https://github.com/VadimSokolov/bayesian_personalized_medicine/releases/tag/v1.0.0).</small>

<!-- Generated by bookrepo.py from book.yaml and results.yaml. Edit those files, not this one. -->
