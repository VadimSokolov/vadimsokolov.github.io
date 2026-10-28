# Results by chapter <small>P = RP</small>

The results of [P = RP: A Monte Carlo Program for P versus NP](https://vsokolov.org/books/p_equals_rp/) that are new in the book, that come from the authors' own papers, or that correct one of those papers, as the book states them: 47 entries (31 proved, 7 conditional, 9 open). Results of other authors that the book presents are credited in the [chapter summaries](https://github.com/VadimSokolov/p_equals_rp/tree/main/summaries).

Status: proved; conditional (proved assuming the named statements, which the book does not prove); open (stated as an open question); counterexample (a proved counterexample); withdrawn (found wrong after release; the entry says what was wrong and which version corrects it).

## Chapter 10. The Exponential Time Hypothesis

<a id="eth_and_the_program"></a>

### ETH and the program (exponential lower bounds for samplers on hard boards)

Theorem 10.3, page 36 of Polson and Sokolov (2026), *P = RP: A Monte Carlo Program for P versus NP*, edition 1. New in this book.

Status: conditional on the hypothesis that the class E of problems decidable in time 2^{O(n)} contains a problem with no circuits of size 2^{epsilon n} for some epsilon > 0 (parts 1 and 2); the exponential time hypothesis (part 2); the randomized exponential time hypothesis, that 3 satisfiability has no randomized algorithm of time 2^{delta n} for some delta > 0 (part 3).

Statement. Write E for the class of problems decidable in time $2^{O(n)}$. (1) (Impagliazzo and Wigderson 1997, cited, not proved in the book) If E contains a problem with no circuits of size $2^{\epsilon n}$ for some $\epsilon > 0$, then $\mathrm{P} = \mathrm{BPP}$, hence $\mathrm{P} = \mathrm{RP}$. (2) Assume the exponential time hypothesis (ETH) and the hypothesis of (1). Then $\mathrm{P} = \mathrm{RP} = \mathrm{BPP} \ne \mathrm{NP}$, and consequently the queens level sets on the boards of the Gent, Jefferson and Nightingale reduction admit no polynomial time sampler, and no fully polynomial randomized approximation scheme (FPRAS) for completion counts exists. The Monte Carlo half fails on hard boards for samplers and approximation schemes; the book does not prove the corresponding statement for particular realisations of the vertical walk. (3) Assume the randomized exponential time hypothesis: there is $\delta > 0$ such that 3 satisfiability has no randomized algorithm of time $2^{\delta n}$. Then on the reduction boards of a 3CNF formula with $n$ variables, every randomized algorithm that samples completions within a polynomial factor of uniform, and every FPRAS for the completion count, has running time $2^{\Omega(n)}$ for infinitely many $n$.

Source: [`ch_eth.tex`](https://github.com/VadimSokolov/p_equals_rp/blob/v1.0.0/ch_eth.tex), label `thm:ethprogram`.

<a id="schoening_walk_for_the_queens"></a>

### A Schoening walk for the queens

Proposition 10.4, page 38 of Polson and Sokolov (2026), *P = RP: A Monte Carlo Program for P versus NP*, edition 1. New in this book.

Status: proved.

Statement. Consider the chain on placements of a board with $f \ge 2$ free rows (permutations of the free columns) which, from a placement with at least one attacking pair, picks an attacking pair uniformly, picks one of its two queens uniformly, the free one if the other is fixed, and swaps that queen's row with a uniformly random other free row. Started from a uniform random placement of the free rows and run for $f$ steps with restarts, the chain finds a completion, if one exists, in expected time at most $(2 f)^{f} \cdot \mathrm{poly}(f)$.

Source: [`ch_eth.tex`](https://github.com/VadimSokolov/p_equals_rp/blob/v1.0.0/ch_eth.tex), label `prop:schoening_queens`.

## Chapter 12. Kolmogorov, Cover and the Information in a Solution

<a id="coding_theorem_for_the_queens"></a>

### Coding theorem for the queens

Theorem 12.1, page 47 of Polson and Sokolov (2026), *P = RP: A Monte Carlo Program for P versus NP*, edition 1. New in this book.

Status: proved.

Statement. Let $Q(N; X_0)$ be the number of completions of the partial placement $X_0$ on the $N \times N$ board. The following are equivalent. (1) $\mathrm{NP} = \mathrm{RP}$. (2) There is a constant $c$ and a randomized polynomial time encoder and decoder pair, sharing a random string $\sigma$ of polynomial length, with the following properties on every board $X_0$ with $Q(N; X_0) \ge 1$. With probability at least $1 - 2^{-N^2}$ over $\sigma$, every completion $x$ is encoded by a binary string of a common length $L = L(X_0, \sigma)$, computable in polynomial time from $X_0$ and $\sigma$, with $L \le \log_2 Q(N; X_0) + c \log_2 N$, and decoded correctly. For every $\sigma$, the decoder outputs only completions or a failure symbol, and at most $N^c$ strings of length $L$ decode to any one completion.

Source: [`ch_kolmogorov.tex`](https://github.com/VadimSokolov/p_equals_rp/blob/v1.0.0/ch_kolmogorov.tex), label `thm:coding`.

## Chapter 21. Entropy, Types and the Rate Function of the Queens

<a id="attack_rate_function_conjecture"></a>

### Existence and form of the rate function of the attack count

Conjecture 21.1, page 82 of Polson and Sokolov (2026), *P = RP: A Monte Carlo Program for P versus NP*, edition 1. New in this book.

Status: open.

Statement. The rate function $I(e)$ exists, is convex on $[0, \infty)$ with $I(2/3) = 0$, and is given near $e = 0$ by a variational problem over queenon like densities with prescribed attack density $e$ (queenons proper have $e = 0$). Heuristically $I(e) = -\sup\{ \Psi(f) : f \text{ a queenon with attack density } e \}$ for the functional $\Psi$ of Simkin's upper bound, suitably extended, so that $I(0) = \alpha - 1$. Here $e$ is the energy density $S/N$, the number of attacking pairs per queen, and the widths of the energy levels satisfy $N(s)/N! = \exp(-N I(s/N) + o(N))$. The book does not prove this.

Source: [`ch_entropy.tex`](https://github.com/VadimSokolov/p_equals_rp/blob/v1.0.0/ch_entropy.tex), label `conj:ratefn`.

## Chapter 30. Rubinstein's Cross Entropy Method for Counting

<a id="product_proposals_for_the_queens"></a>

### Product proposals for the queens

Theorem 30.1, page 116 of Polson and Sokolov (2026), *P = RP: A Monte Carlo Program for P versus NP*, edition 1. New in this book.

Status: proved.

Statement. Let $N$ be a positive integer, let $\mathcal{X}^* \subseteq [N]^N$ be the set of solutions of the $N$ queens problem among row placements, with $Q(N) = |\mathcal{X}^*|$, and let $\pi^*$ be the uniform distribution on $\mathcal{X}^*$. For $i = 1, \dots, N$ let $H_i$ be the entropy of the $i$th coordinate (the column of the queen in row $i$) under $\pi^*$, let $d_i = \log N - H_i \ge 0$ and $d = \sum_{i=1}^{N} d_i$. For any proposal distribution $g$ on $[N]^N$ of product form, $g(x) = \prod_{i=1}^{N} g_i(x_i)$, the importance sampling estimator $\mathbf{1}\{X \in \mathcal{X}^*\} / g(X)$ of $Q(N)$, with $X$ drawn from $g$, has relative variance at least $\exp\big( N \log N - d - \log Q(N) \big) - 1$, with equality in the exponent at the product of the marginals of $\pi^*$. The crude estimator from the uniform distribution on $[N]^N$ has relative variance $\exp\big( N \log N - \log Q(N) \big) - 1$, so no product proposal reduces the relative second moment (one plus the relative variance) of crude Monte Carlo by more than the factor $e^{d}$.

Source: [`ch_crossentropy.tex`](https://github.com/VadimSokolov/p_equals_rp/blob/v1.0.0/ch_crossentropy.tex), label `thm:product`.

## Chapter 33. The Algorithms of Vertical Likelihood Monte Carlo

<a id="reflected_walk_mixing_conjecture"></a>

### Mixing of the reflected Laplace walk of log ordinates

Conjecture 33.1, page 133 of Polson and Sokolov (2026), *P = RP: A Monte Carlo Program for P versus NP*, edition 1. New in this book.

Status: open.

Statement. Assume that the draws of $u \mid x$ and of $x \mid u$ are exact and that $Z(\cdot)$ is known exactly. Use the truncated weight $W = 1/\max\{\eta, Z\}$, with $\eta = \rho$ for a rare event of probability $\rho$, and put $v_{max} = \log(1/\eta)$. While $v_n = -\log Z(L(X_n))$ lies in $[0, v_{max}]$ the chain of log ordinates moves as a symmetric random walk with Laplace increments. Model the chain by this walk reflected at $0$ and $v_{max}$. Then the mixing time of the reflected walk from a warm start to within total variation $\epsilon$ is $O( v_{max}^2 \log(1/\epsilon) )$, which for a rare event of probability $\rho$ is $O( \log^2(1/\rho) \log(1/\epsilon) )$, and for the $N$ queens on permutations is $O( N^2 \log(1/\epsilon) )$. The book does not prove this; its argument is a heuristic.

Source: [`ch_polsonscott.tex`](https://github.com/VadimSokolov/p_equals_rp/blob/v1.0.0/ch_polsonscott.tex), label `conj:reflectedmix`.

<a id="vertical_likelihood_polynomial_time_conjecture"></a>

### Vertical likelihood Monte Carlo is polynomial given polynomial level set draws

Conjecture 33.2, page 134 of Polson and Sokolov (2026), *P = RP: A Monte Carlo Program for P versus NP*, edition 1. New in this book.

Status: open.

Statement. Suppose the adaptive estimate of $Z(\cdot)$ converges in polynomially many steps, and suppose $\rho > 0$ (for $\rho = 0$ a stopping rule is needed, and for the queens $\log(1/\rho)$ may be replaced by its upper bound $\log N!$ when $\rho > 0$). Vertical likelihood Monte Carlo with the weight $W = 1/\max\{\eta, Z\}$ estimates $Z$ to relative error $\epsilon$ with probability $\tfrac34$ using a number of weighted slice steps polynomial in $\log(1/\rho)$ and $\epsilon^{-1}$, which is expected to be of order $\log^2(1/\rho) \cdot \epsilon^{-2}$ up to a further factor of $\log(1/\rho)$ from the stratified bound, each requiring one draw from the prior restricted to a likelihood level set within total variation of exact equal to $\epsilon$ divided by the number of steps. The algorithm runs in polynomial time if and only if those restricted draws do. In particular, for log concave $L$ and $p$ it runs in polynomial time by Frieze, Kannan and Polson (1994), and for the queens completion count it runs in polynomial time if and only if $\mathrm{NP} = \mathrm{RP}$, by the main equivalence.

Source: [`ch_polsonscott.tex`](https://github.com/VadimSokolov/p_equals_rp/blob/v1.0.0/ch_polsonscott.tex), label `conj:vlpoly`.

## Chapter 34. Rates of Convergence in the Quantile Coordinate

<a id="riemann_sums_monotone_log_rate"></a>

### Riemann sums on random grids for monotone integrands

Theorem 34.1, page 137 of Polson and Sokolov (2026), *P = RP: A Monte Carlo Program for P versus NP*, edition 1. New in this book.

Status: proved.

Statement. For any nonincreasing $\Lambda$ on $[0,1]$ with $\Lambda(0) < \infty$, the left and right Riemann sums $\hat Z$ on $n$ ordered uniforms satisfy $\mathbb{E} ( \hat Z - Z )^2 \le ( \Lambda(0) - \Lambda(1) )^2 \, \mathbb{E} ( \max_i D_i )^2 = O( \log^2 n / n^2 )$, where $Z = \int_0^1 \Lambda$ and $D_i$ are the spacings between consecutive nodes, including the endpoints $0$ and $1$.

Source: [`ch_rates.tex`](https://github.com/VadimSokolov/p_equals_rp/blob/v1.0.0/ch_rates.tex), label `thm:riemannmono`.

## Chapter 35. Weighted Monte Carlo Integration: The Yakowitz Bounds

<a id="trapezoid_lipschitz_and_bv_bounds"></a>

### Trapezoid rule on random nodes for Lipschitz and bounded variation integrands

Theorem 35.2, page 141 of Polson and Sokolov (2026), *P = RP: A Monte Carlo Program for P versus NP*, edition 1. New in this book.

Status: proved.

Statement. Let $Z = \int_0^1 \Lambda(s) \, ds$, and let $\hat Z_T$ be the trapezoidal rule on $n$ ordered independent uniform nodes together with the endpoints $0$ and $1$. If $\Lambda$ is Lipschitz with constant $C_1$, then $\mathbb{E} (\hat Z_T - Z)^2 \le 3 C_1^2 / (2 (n+2)^2)$. If $\Lambda$ is of bounded variation $V$, then $\mathbb{E} (\hat Z_T - Z)^2 = O(V^2 \log^2 n / n^2)$, and for monotone $\Lambda$ the same holds with $V = |\Lambda(1) - \Lambda(0)|$.

Source: [`ch_yakowitz.tex`](https://github.com/VadimSokolov/p_equals_rp/blob/v1.0.0/ch_yakowitz.tex), label `thm:lipbv`.

<a id="staircase_bracketing_bound"></a>

### Bracketing Riemann sums and trapezoid for a staircase with K jumps

Theorem 35.3, page 142 of Polson and Sokolov (2026), *P = RP: A Monte Carlo Program for P versus NP*, edition 1. New in this book.

Status: proved.

Statement. For a nonincreasing staircase $\Lambda$ with $K$ jumps and values $\lambda_1 > \lambda_2 > \dots > \lambda_{K+1} \ge 0$, so that $\Lambda(0) = \lambda_1$, the left and right Riemann sums $\hat Z_L$ and $\hat Z_R$ on the random grid of $n$ ordered uniforms bracket $Z = \int_0^1 \Lambda$ and satisfy $\mathbb{E} (\hat Z_L - Z)^2 \le \mathbb{E} (\hat Z_L - \hat Z_R)^2 \le \frac{6 \lambda_1^2 \, K^2}{(n+1)(n+2)}$, and the trapezoidal rule satisfies the same bound with the constant halved. The error is $O(K \lambda_1 / n)$ in root mean square.

Source: [`ch_yakowitz.tex`](https://github.com/VadimSokolov/p_equals_rp/blob/v1.0.0/ch_yakowitz.tex), label `thm:staircasebracket`.

## Chapter 36. Beyond Yakowitz: Higher Order and Stratified Vertical Rules

<a id="interpolatory_rules_high_order"></a>

### Degree k interpolatory rules on random grids

Theorem 36.1, page 144 of Polson and Sokolov (2026), *P = RP: A Monte Carlo Program for P versus NP*, edition 1. New in this book.

Status: proved.

Statement. On the random grid $0 = U_{(0)} < U_{(1)} < \dots < U_{(n+1)} = 1$ of $n$ ordered uniforms, a degree $k$ interpolatory rule approximates $\int_{U_{(i-1)}}^{U_{(i)}} \Lambda$ by the integral of the polynomial of degree $k$ that interpolates $\Lambda$ at $k + 1$ consecutive grid points including the endpoints of the cell. Let $\Lambda \in C^{k+1}[0, 1]$ with $\|\Lambda^{(k+1)}\|_\infty \le C_{k+1}$, let $Z = \int_0^1 \Lambda$ and let $\hat Z_k$ be the degree $k$ interpolatory rule on the random grid. Then $\mathbb{E} | \hat Z_k - Z | \le c_k \, C_{k+1} \, n^{-(k+1)}$ and $\mathbb{E} ( \hat Z_k - Z )^2 \le c_k' \, C_{k+1}^2 \, n^{-2(k+1)}$ for constants $c_k, c_k'$ depending only on $k$.

Source: [`ch_beyond.tex`](https://github.com/VadimSokolov/p_equals_rp/blob/v1.0.0/ch_beyond.tex), label `thm:interp`.

<a id="stratified_vertical_rule"></a>

### Stratified quadrature in the quantile coordinate

Theorem 36.2, page 145 of Polson and Sokolov (2026), *P = RP: A Monte Carlo Program for P versus NP*, edition 1. New in this book.

Status: proved.

Statement. Let $U_i$ be uniform on the $i$th of $n$ equal strata of $[0,1]$ and let $\hat Z_S = \frac1n \sum_{i=1}^n \Lambda(U_i)$ be the stratified estimator of $Z = \int_0^1 \Lambda$. Then $\hat Z_S$ is unbiased for every integrable $\Lambda$, and $\mathrm{Var} (\hat Z_S) = \frac{1}{n^2} \sum_{i=1}^{n} \mathrm{Var} ( \Lambda(U_i) ) \le \frac{1}{n^2} \sum_{i=1}^{n} \frac{ \mathrm{osc}_i(\Lambda)^2 }{4}$, where $\mathrm{osc}_i$ is the oscillation of $\Lambda$ on the $i$th stratum. In particular, for a nonincreasing staircase with $K$ jumps and values $\lambda_1 > \dots > \lambda_{K+1} \ge 0$, $\mathbb{E} (\hat Z_S - Z)^2 \le \frac{K \lambda_1^2}{4 n^2}$, and for Lipschitz $\Lambda$ with constant $C_1$, $\mathbb{E} (\hat Z_S - Z)^2 \le C_1^2 / (4 n^3)$.

Source: [`ch_beyond.tex`](https://github.com/VadimSokolov/p_equals_rp/blob/v1.0.0/ch_beyond.tex), label `thm:stratified`.

<a id="nested_sampling_exact_mean_variance"></a>

### Exact mean and variance of the nested sampling estimate under the product Beta law

Theorem 36.3, page 146 of Polson and Sokolov (2026), *P = RP: A Monte Carlo Program for P versus NP*, edition 1. New in this book.

Status: proved.

Statement. Let $n$ be the number of live points, let the latent positions be $s_k = \prod_{j=1}^{k} t_j$ with $t_j$ independent of law $\mathrm{Beta}(n, 1)$ (the maximum of $n$ uniforms), and set $s_0 = 1$. Hold the discarded likelihood sequence $(y_k)$ fixed. Then the nested sampling estimate $\hat Z = \sum_k y_k (s_{k-1} - s_k)$ has, under the law of the positions, $\mathbb{E} \hat Z = \sum_{k \ge 1} y_k \, \frac{1}{n+1} \big( \frac{n}{n+1} \big)^{k-1}$ and $\mathrm{Var} \hat Z = \sum_{k, l} y_k y_l \, \mathrm{Cov}(s_{k-1} - s_k, \, s_{l-1} - s_l)$, where $\mathbb{E} s_k = (n/(n+1))^k$, $\mathbb{E} s_k^2 = (n/(n+2))^k$, and for $k \le l$, $\mathbb{E} s_k s_l = (n/(n+2))^k (n/(n+1))^{l-k}$.

Source: [`ch_beyond.tex`](https://github.com/VadimSokolov/p_equals_rp/blob/v1.0.0/ch_beyond.tex), label `thm:nestedmoments`.

## Chapter 37. Exact Yakowitz Theory for Staircases

<a id="staircase_error_representation"></a>

### Trapezoid error as an integral against the jump measure

Theorem 37.1, page 149 of Polson and Sokolov (2026), *P = RP: A Monte Carlo Program for P versus NP*, edition 1. New in this book.

Status: proved.

Statement. Let $\Lambda$ be of bounded variation on $[0,1]$, right continuous on $(0,1)$, and let $\mu = -d\Lambda$ be the signed measure on $(0,1)$ with $\Lambda(s) = \Lambda(1) + \mu((s,1))$ and total variation $V$. Let $U_{(1)} < \dots < U_{(n)}$ be the order statistics of $n$ independent uniform variables on $[0,1]$, with $U_{(0)}=0$ and $U_{(n+1)}=1$, let $\hat Z_T$ be the trapezoidal rule for $Z=\int_0^1 \Lambda(s)\,ds$ on these nodes, let $A(s)=s-\max\{U_{(i)} \le s\}$ and $B(s)=\min\{U_{(i)}>s\}-s$ be the distances from $s$ to the nodes on either side, and let $D(s)=(B(s)-A(s))/2$. Then, almost surely, $\hat Z_T - Z = \int_0^1 D(s)\,\mu(ds)$.

Source: [`ch_staircase.tex`](https://github.com/VadimSokolov/p_equals_rp/blob/v1.0.0/ch_staircase.tex), label `thm:errrep`.

<a id="spacing_containing_a_point"></a>

### Moments of the spacing containing a fixed point

Lemma 37.2, page 150 of Polson and Sokolov (2026), *P = RP: A Monte Carlo Program for P versus NP*, edition 1. New in this book.

Status: proved.

Statement. With $A(s)$, $B(s)$ and $D(s)=(B(s)-A(s))/2$ defined from $n$ independent uniform nodes on $[0,1]$ as the distances from $s$ to the nearest node on its left and on its right (with $0$ and $1$ added as nodes), for fixed $s\in(0,1)$ one has $\mathbb{P}(A(s)>a,\,B(s)>b)=(1-a-b)^n$ for $0\le a<s$, $0\le b<1-s$, $a+b\le 1$. Consequently $\mathbb{E}D(s)=\frac{(1-s)^{n+1}-s^{n+1}}{2(n+1)}$ and $\mathbb{E}D(s)^2=\frac{1-(n+2)\,s(1-s)\big(s^n+(1-s)^n\big)}{2(n+1)(n+2)}$. In particular $|\mathbb{E}D(s)|\le \frac{1}{2(n+1)}$ and $\mathbb{E}D(s)^2\le\frac{1}{2(n+1)(n+2)}$, the second attained asymptotically at every interior $s$.

Source: [`ch_staircase.tex`](https://github.com/VadimSokolov/p_equals_rp/blob/v1.0.0/ch_staircase.tex), label `lem:spacing`.

<a id="trapezoid_single_step_exact"></a>

### Exact bias and mean squared error of the trapezoid on one step

Theorem 37.3, page 151 of Polson and Sokolov (2026), *P = RP: A Monte Carlo Program for P versus NP*, edition 1. New in this book.

Status: proved.

Statement. Let $\Lambda=\lambda_1$ on $[0,p)$ and $\Lambda=\lambda_2$ on $[p,1]$, a single step of height $h=\lambda_1-\lambda_2$ at $p\in(0,1)$, and let $\hat Z_T$ be the trapezoidal rule on $n$ independent uniform nodes ordered, with endpoints $0$ and $1$ included, for $Z=\int_0^1\Lambda$. Then $\mathbb{E}(\hat Z_T-Z)=h\,\frac{(1-p)^{n+1}-p^{n+1}}{2(n+1)}$ and $\mathbb{E}(\hat Z_T-Z)^2=h^2\,\frac{1-(n+2)\,p(1-p)\big(p^n+(1-p)^n\big)}{2(n+1)(n+2)}$.

Source: [`ch_staircase.tex`](https://github.com/VadimSokolov/p_equals_rp/blob/v1.0.0/ch_staircase.tex), label `thm:onestep`.

<a id="trapezoid_bounded_variation_no_log"></a>

### Trapezoid on random nodes for bounded variation, no logarithm

Theorem 37.4, page 151 of Polson and Sokolov (2026), *P = RP: A Monte Carlo Program for P versus NP*, edition 1. New in this book.

Status: proved.

Statement. Let $\Lambda$ have total variation $V$ on $[0,1]$ and let $\hat Z_T$ be the trapezoidal rule on $n$ independent uniform nodes, ordered, with the endpoints $0$ and $1$ included, for $Z=\int_0^1\Lambda$. Then $|\mathbb{E}(\hat Z_T-Z)|\le \frac{V}{2(n+1)}$ and $\mathbb{E}(\hat Z_T-Z)^2\le\frac{V^2}{2(n+1)(n+2)}$. For a nonincreasing staircase whose jumps all lie in $[\delta,1-\delta]$ the bias is at most $\frac{V(1-\delta)^{n+1}}{2(n+1)}$.

Source: [`ch_staircase.tex`](https://github.com/VadimSokolov/p_equals_rp/blob/v1.0.0/ch_staircase.tex), label `thm:bv`.

<a id="trapezoid_staircase_asymptotic_constant"></a>

### Asymptotic constant of the trapezoid for separated steps

Proposition 37.5, page 152 of Polson and Sokolov (2026), *P = RP: A Monte Carlo Program for P versus NP*, edition 1. New in this book.

Status: proved.

Statement. Let $\Lambda$ be a staircase with jumps of heights $h_1,\dots,h_K$ at fixed interior locations, and let $\hat Z_T$ be the trapezoidal rule on $n$ independent uniform nodes, ordered, with the endpoints included. Then $\mathbb{E}(\hat Z_T-Z)^2=\frac{\sum_k h_k^2}{2n^2}\big(1+O(1/n)\big)$, where the constant in the $O$ depends on $K$ and on the minimum gap between jumps.

Source: [`ch_staircase.tex`](https://github.com/VadimSokolov/p_equals_rp/blob/v1.0.0/ch_staircase.tex), label `prop:asym`.

<a id="stratified_rule_free_of_jump_count"></a>

### Stratified midpoint rule variance bound free of the number of steps

Theorem 37.6, page 153 of Polson and Sokolov (2026), *P = RP: A Monte Carlo Program for P versus NP*, edition 1. New in this book.

Status: proved.

Statement. Let $\hat Z_S=n^{-1}\sum_{i=1}^n\Lambda(U_i)$ with $U_i$ uniform on the $i$th of $n$ equal strata of $[0,1]$, independent. For any $\Lambda$ of bounded variation $V$, $\mathrm{Var}(\hat Z_S)\le \frac{V^2}{4n^2}$. For a staircase with jump heights $h_k$ no two of whose jumps lie in the same stratum, $\mathrm{Var}(\hat Z_S)\le\frac{\sum_k h_k^2}{4n^2}$.

Source: [`ch_staircase.tex`](https://github.com/VadimSokolov/p_equals_rp/blob/v1.0.0/ch_staircase.tex), label `thm:stratbv`.

## Chapter 41. Generative Bayesian Computation for Vertical Counting

<a id="amortised_ladder_generator_error"></a>

### Amortised ladder with a fitted level set generator

Theorem 41.3, page 170 of Polson and Sokolov (2026), *P = RP: A Monte Carlo Program for P versus NP*, edition 1. New in this book.

Status: proved.

Statement. Suppose a level set generator $G_\phi(m, \xi)$ is fitted so that for each level $m_t$ the law of $G_\phi(m_t, \xi)$ is within total variation $\delta$ of $P(\cdot \mid S \le m_t)$. Suppose also that the $T$ ratios equal a common value $\theta$. Then the ladder run with $M$ draws from $G_\phi$ at each rung estimates $\rho$ with relative mean squared error, to first order in $T(1 - \theta)/(\theta M)$ and $T\delta/\theta$, at most $T(1 - \theta)/(\theta M) + O(T^2 \delta^2/\theta^2)$, and costs $T M$ evaluations of $G_\phi$ with no Markov chain steps.

Source: [`ch_gbc.tex`](https://github.com/VadimSokolov/p_equals_rp/blob/v1.0.0/ch_gbc.tex), label `thm:amortised`.

## Chapter 42. Sufficient Statistics for the Queens

<a id="closure_minimal_sufficient_completion"></a>

### Minimal sufficiency of the closure of a board

Theorem 42.2, page 175 of Polson and Sokolov (2026), *P = RP: A Monte Carlo Program for P versus NP*, edition 1. New in this book.

Status: proved.

Statement. Let $X_0$ be a board of $k$ fixed queens in distinct rows and columns, with completion set $C(X_0)$ (the placements of $N$ non attacking queens containing $X_0$) and uniform posterior on $C(X_0)$. Define the closure $\bar X_0=\bigcap_{x\in C(X_0)}x$ and the posterior mean matrix $M(X_0)_{ic}=\mathbb{P}(x_i=c\mid X_0)=N(0;X_0\cup\{(i,c)\})/N(0;X_0)$, where $N(0;\cdot)$ is the number of completions. On boards with at least one completion, $\bar X_0$ is a minimal sufficient statistic for the completion law, and $M(X_0)$ is a sufficient statistic with $\bar X_0=\{(i,c):M(X_0)_{ic}=1\}$.

Source: [`ch_sufficient.tex`](https://github.com/VadimSokolov/p_equals_rp/blob/v1.0.0/ch_sufficient.tex), label `thm:closure`.

<a id="posterior_mean_sufficient_self_reducible"></a>

### Posterior mean sufficiency for completion problems

Theorem 42.3, page 176 of Polson and Sokolov (2026), *P = RP: A Monte Carlo Program for P versus NP*, edition 1. New in this book.

Status: proved.

Statement. Consider a problem whose instances are partial assignments $X_0$ of variables to values, whose posterior is the uniform law on the complete assignments extending $X_0$ that satisfy a fixed constraint, and suppose that extending a partial assignment by a value assigned in every completion does not change the completion set. Then the posterior mean, the vector of probabilities $\mathbb{P}(\text{variable } i=v\mid X_0)$, is a sufficient statistic for the posterior, and the set of its entries equal to one is minimal sufficient.

Source: [`ch_sufficient.tex`](https://github.com/VadimSokolov/p_equals_rp/blob/v1.0.0/ch_sufficient.tex), label `thm:pmean`.

<a id="hardness_of_sufficient_statistics_queens"></a>

### Hardness of the closure and the posterior mean matrix

Theorem 42.4, page 176 of Polson and Sokolov (2026), *P = RP: A Monte Carlo Program for P versus NP*, edition 1. New in this book.

Status: proved.

Statement. Extend the closure to boards with forbidden squares, and to boards with no completion by declaring every square to be in the closure of such a board. Deciding whether a given square belongs to the closure is then $\mathrm{coNP}$ hard. Computing the posterior mean matrix exactly is $\#\mathrm{P}$ hard. A randomized polynomial time algorithm that approximates every entry of the matrix within a factor $1\pm1/N^2$ on every board exists if and only if $\mathrm{NP}=\mathrm{RP}$.

Source: [`ch_sufficient.tex`](https://github.com/VadimSokolov/p_equals_rp/blob/v1.0.0/ch_sufficient.tex), label `thm:cost`.

<a id="learned_generator_summary_dichotomy"></a>

### Learned generators conditioning on a summary statistic

Theorem 42.5, page 178 of Polson and Sokolov (2026), *P = RP: A Monte Carlo Program for P versus NP*, edition 1. New in this book.

Status: proved.

Statement. Let $T$ be any statistic of the board and $G(\tau,T(X_0))$ a generator, a measurable function of base noise $\tau$ and the statistic, whose output law is uniform on the completion set $C(X_0)$ for every board. Then $T$ is sufficient for the completion law, and hence determines the closure. If in addition $G$ is computable in polynomial time and $T$ is computable in randomized polynomial time with error probability at most $1/4$, then $\mathrm{NP}=\mathrm{RP}$. If $T$ is the posterior mean matrix $M$ and $G(\tau,M)=(G_1(\tau_1,M_{1\cdot}),\dots,G_N(\tau_N,M_{N\cdot}))$ has independent coordinates, then the divergence of the uniform completion law from the output law $P_G$ of $G$ satisfies $D(\pi(\cdot\mid X_0)\,\|\,P_G)\ge\sum_i H_i-\log N(0;X_0)$, where $H_i$ is the entropy of row $i$ of $M(X_0)$ and $N(0;X_0)$ is the number of completions; for the unconditioned problem this mean field gap equals $\alpha N-d+o(N)$, where $\alpha$ is the constant in $Q(N)=\big((1+o(1))Ne^{-\alpha}\big)^N$ and $d=\sum_{i=1}^{N}(\log N-H_i)$ is the entropy deficit of the row entropies on the empty board, so it is linear in $N$ if $d/N$ stays below $\alpha$.

Source: [`ch_sufficient.tex`](https://github.com/VadimSokolov/p_equals_rp/blob/v1.0.0/ch_sufficient.tex), label `thm:gbcsuff`.

<a id="planted_sampling_board_law"></a>

### Planted sampling gives the posterior mean but weights boards by completions

Theorem 42.6, page 180 of Polson and Sokolov (2026), *P = RP: A Monte Carlo Program for P versus NP*, edition 1. New in this book.

Status: proved.

Statement. Draw a uniform solution $x$ of the $N$ queens problem, of which there are $Q(N)$, draw a uniform $k$ subset of its rows, and keep the queens of $x$ in those rows as the board $X_0$; write $P_k$ for the joint law of $(x,X_0)$. Under $P_k$ the conditional law of $x$ given $X_0$ is the uniform law on the completion set $C(X_0)$, so the regression function $\mathbb{E}_{P_k}[\mathbf 1\{x_i=c\}\mid X_0]$ is the posterior mean matrix $M(X_0)$, and the population minimiser of the squared loss under $P_k$ is $M(X_0)$ on every board with a completion. The marginal law of the board is $P_k(X_0)=\frac{N(0;X_0)}{Q(N)\binom{N}{k}}$, where $N(0;X_0)$ is the number of completions of $X_0$, so that a board is seen with probability proportional to its number of completions and the expected number of planted pairs needed to see a given board once is $Q(N)\binom Nk/N(0;X_0)$.

Source: [`ch_sufficient.tex`](https://github.com/VadimSokolov/p_equals_rp/blob/v1.0.0/ch_sufficient.tex), label `thm:planted`.

<a id="learning_problem_equivalent_to_np_rp"></a>

### Learning the posterior mean matrix is equivalent to NP equals RP

Theorem 42.7, page 181 of Polson and Sokolov (2026), *P = RP: A Monte Carlo Program for P versus NP*, edition 1. New in this book.

Status: proved.

Statement. The following are equivalent. (1) $\mathrm{NP}=\mathrm{RP}$. (2) There is a randomized algorithm which, given any board $X_0$ with completions, outputs in time polynomial in $N$ a matrix $\tilde M$ with $\tilde M_{ic}\in(1\pm1/N^2)M(X_0)_{ic}$ for every entry, where $M(X_0)$ is the posterior mean matrix of the uniform completion law, with probability at least $3/4$. (3) There is a uniform family of circuits $C_N$ of size polynomial in $N$, produced from $N$ by a polynomial time algorithm, which, given a board $X_0$ with completions and a random string, outputs such a matrix with probability at least $3/4$.

Source: [`ch_sufficient.tex`](https://github.com/VadimSokolov/p_equals_rp/blob/v1.0.0/ch_sufficient.tex), label `thm:jwequiv`.

## Chapter 43. The Monte Carlo Program for P versus NP

<a id="conditional_fpras_vertical_walk"></a>

### Conditional FPRAS for the vertical walk with stratified quadrature

Theorem 43.1, page 185 of Polson and Sokolov (2026), *P = RP: A Monte Carlo Program for P versus NP*, edition 1. New in this book.

Status: conditional on a level set sampler producing, in time C(N, delta), a sample within total variation delta of uniform on every sublevel set; the ladder hypothesis, that the ladder has at most 2K rungs and consecutive rung size ratios at least one half; for the optimality remark only, for the optimality remark only, that relative error epsilon in the product requires relative error of order epsilon over the square root of K in each rung ratio, which the book assumes and does not prove.

Statement. Let $S$ be an energy on a finite set $\mathcal{X}$ of known size, taking at most $K + 1$ values with $N(0) > 0$, and suppose a level set sampler is available that produces, in time $C(N, \delta)$, a sample within total variation $\delta$ of uniform on $\{ S \le m \}$ for any $m$. Suppose also that the ladder of level sets used by the walk has at most $2K$ rungs and that consecutive rungs have size ratio at least $\tfrac12$. Then for any $\epsilon \in (0, 1)$ the vertical walk with stratified quadrature produces an estimate $\hat N(0)$ of the ground state count with $\mathbb{P}( |\hat N(0) / N(0) - 1| > \epsilon ) \le \tfrac14$, in time $O\big( \frac{K^2}{\epsilon^2} \cdot C(N, \epsilon / K) \big)$, and for estimators that estimate each rung ratio separately the dependence on $K$ and $\epsilon$ cannot be improved by more than logarithmic factors (the book does not prove a lower bound for arbitrary estimators).

Source: [`ch_program.tex`](https://github.com/VadimSokolov/p_equals_rp/blob/v1.0.0/ch_program.tex), label `thm:condfpras`.

<a id="fpras_unconditioned_queens_count_sketch"></a>

### FPRAS for the unconditioned queens count under mixing hypotheses (sketch)

Proposition 43.2, page 187 of Polson and Sokolov (2026), *P = RP: A Monte Carlo Program for P versus NP*, edition 1. New in this book.

Status: conditional on the sublevel set of energy at most 2 is connected under swaps; polynomial mixing time of the swap chain on every sublevel set of energy at most m for every m at least 2; consecutive ratios of the sublevel sets on the integer ladder are at least inverse polynomial in N; polynomial mixing of the swap chain on the giant component of the sublevel set of energy at most 1, with a membership test and with the giant component holding all but an N to the minus c fraction of the solutions; closing the two gaps the book names in its proof sketch (ratios only inverse polynomial instead of at least one half, and no bound on the size of the giant component relative to the sublevel set).

Statement. Suppose that for the unconditioned $N$ queens problem the level set $\{ S \le 2 \}$ is connected under swaps, that the swap chain on $\{ S \le m \}$ has polynomial mixing time for every $m \ge 2$, that consecutive ratios $|\{ S \le m-1 \}| / |\{ S \le m \}|$ on the integer ladder are at least inverse polynomial in $N$, and that the swap chain on the giant component $G$ of $\{ S \le 1 \}$ has polynomial mixing time, with a membership test for $G$ and with $G$ holding a $1 - O(N^{-c})$ fraction of the solutions for some $c > 0$ (small $N$ being handled by enumeration). Then there is an FPRAS for $Q(N)$, the number of solutions of the $N$ queens problem. The last hypothesis can be dropped at the cost of replacing the bottom rung by the direct Bernoulli estimate of $Q(N) / |\{ S \le 2 \}|$, which is polynomial if that ratio is at least inverse polynomial.

Source: [`ch_program.tex`](https://github.com/VadimSokolov/p_equals_rp/blob/v1.0.0/ch_program.tex), label `prop:fpras_unconditioned`.

## Chapter 44. The Quantile Reordering of a Randomized Algorithm

<a id="rp_decided_by_quantile_median"></a>

### An RP language is decided by the median of the quantile function of its algorithm

Proposition 44.1, page 190 of Polson and Sokolov (2026), *P = RP: A Monte Carlo Program for P versus NP*, edition 1. New in this book.

Status: proved.

Statement. Let $L \in \mathrm{RP}$ with an algorithm $A$ that accepts every $x \in L$ with probability $p(x) > \tfrac12$ (one round of amplification gives one), and never accepts $x \notin L$. Let $\Lambda_x$ be the quantile function of the algorithm on input $x$, the step function equal to $1$ for $s < p(x)$ and $0$ otherwise. Then for every input $x$, $x \in L$ if and only if $\Lambda_x(\tfrac12) = \operatorname{med}_r A(x, r) = 1$, where the median is over a uniform random string $r$.

Source: [`p_equals_rp.tex`](https://github.com/VadimSokolov/p_equals_rp/blob/v1.0.0/p_equals_rp.tex), label `prop:median`.

<a id="p_equals_rp_iff_medians"></a>

### P = RP if and only if medians of RP type Boolean functions are computable in P

Theorem 44.2, page 190 of Polson and Sokolov (2026), *P = RP: A Monte Carlo Program for P versus NP*, edition 1. New in this book.

Status: proved.

Statement. $\mathrm{P} = \mathrm{RP}$ if and only if the following holds. For every polynomial time computable Boolean function $f(x, r)$, $r \in \{0,1\}^{m(|x|)}$, such that for every $x$ either $f(x, \cdot) \equiv 0$ or $\mathbb{P}_r(f(x, r) = 1) > \tfrac12$, the median $\operatorname{med}_r f(x, r)$ is computable in deterministic polynomial time.

Source: [`p_equals_rp.tex`](https://github.com/VadimSokolov/p_equals_rp/blob/v1.0.0/p_equals_rp.tex), label `thm:medians`.

## Chapter 45. Vertical Likelihood and P = RP

<a id="conditional_fpras_integer_ladder"></a>

### Conditional FPRAS with an integer ladder from a polynomial level set sampler

Theorem 45.1, page 193 of Polson and Sokolov (2026), *P = RP: A Monte Carlo Program for P versus NP*, edition 1. New in this book.

Status: conditional on a polynomial level set sampler for the energy; every ratio of consecutive level sets is at least 1/q for a polynomial q.

Statement. Let $S : \mathcal{X} \to \{0, 1, \dots, K\}$ be an energy on a finite set $\mathcal{X}$ with $|\mathcal{X}|$ known and $K$ polynomial in the input size. Say that $S$ admits a polynomial level set sampler if there is a randomized polynomial time procedure which, given a level $m$ and an accuracy $\delta$, produces a sample from the uniform distribution on $\{ x : S(x) \le m \}$ to within total variation $\delta$ in time polynomial in the input size and $\log(1/\delta)$. If $S$ admits a polynomial level set sampler, and every ratio $Z_{t-1} / Z_t$ of consecutive level sets is at least $1/q$ for a polynomial $q$, then there is an FPRAS for $N(0) = \#\{ x : S(x) = 0 \}$, and hence for every cumulative count $\#\{ x : S(x) \le s \}$. The FPRAS runs the vertical likelihood walk with the ladder $m_t = t$ for $t = K, K-1, \dots, 0$, estimating each ratio $Z_{t-1} / Z_t$ by $O(K q / \epsilon^2)$ conditioned samples at level $t$, for a total of $O(K^2 q \, \epsilon^{-2})$ samples.

Source: [`p_equals_rp.tex`](https://github.com/VadimSokolov/p_equals_rp/blob/v1.0.0/p_equals_rp.tex), label `thm:vertical_condfpras`.

<a id="queens_energy_sampler_implies_np_rp"></a>

### A polynomial level set sampler for the queens energy gives NP = RP

Corollary 45.2, page 193 of Polson and Sokolov (2026), *P = RP: A Monte Carlo Program for P versus NP*, edition 1. New in this book.

Status: conditional on a polynomial level set sampler for the queens energy on partially filled boards; the ratios of consecutive level sets of the queens energy are at least inverse polynomial.

Statement. If the queens energy, the number of attacking pairs on a partially filled board, admits a polynomial level set sampler, and the ratios of consecutive level sets are at least inverse polynomial, then there is an FPRAS for the queens completion count, and therefore $\mathrm{NP} = \mathrm{RP}$.

Source: [`p_equals_rp.tex`](https://github.com/VadimSokolov/p_equals_rp/blob/v1.0.0/p_equals_rp.tex), label `cor:queens_nprp`.

<a id="queens_conjecture_vertical_form"></a>

### Vertical form of the queens conjecture

Conjecture 45.7, page 195 of Polson and Sokolov (2026), *P = RP: A Monte Carlo Program for P versus NP*, edition 1. New in this book.

Status: open.

Statement. The queens energy on partial boards does not admit a polynomial level set sampler. In particular, every Markov chain on partial queens placements whose transitions are computable in polynomial time and which is ergodic on each level set $\{ S \le m \}$ has mixing time superpolynomial in $N$ for some $m$ and some partial board.

Source: [`p_equals_rp.tex`](https://github.com/VadimSokolov/p_equals_rp/blob/v1.0.0/p_equals_rp.tex), label `conj:queens_vertical`.

## Chapter 49. A Cluster Chain for the Queens

<a id="block_chain_reversible_irreducible"></a>

### The block chain is reversible and irreducible when the level set is connected

Proposition 49.1, page 209 of Polson and Sokolov (2026), *P = RP: A Monte Carlo Program for P versus NP*, edition 1. New in this book.

Status: proved.

Statement. The block chain with binomially distributed block size and exact resampling of each block conditional on the level set is reversible with respect to the uniform distribution on the level set, and is irreducible on it whenever the level set is connected under moves that permute any $k$ rows at once for $k$ up to the maximal block size attained.

Source: [`ch_swendsen.tex`](https://github.com/VadimSokolov/p_equals_rp/blob/v1.0.0/ch_swendsen.tex), label `prop:blockvalid`.

<a id="block_chain_mixing_conjecture"></a>

### Mixing of the block chain on unconditioned and reduction boards

Conjecture 49.2, page 210 of Polson and Sokolov (2026), *P = RP: A Monte Carlo Program for P versus NP*, edition 1. New in this book.

Status: open.

Statement. Let $q$ be the probability with which each row is included in the random block. For the block chain on $\{ S \le 1 \}$ for the unconditioned $N$ queens problem, the mixing time is polynomial in $N$ for every constant $q \in (0, 1)$. For the block chain on $\{ S \le 1 \}$ for the completion problem with partial placements drawn from the Gent, Jefferson and Nightingale reduction applied to hard satisfiability instances, the mixing time is superpolynomial for every $q$ bounded away from one.

Source: [`ch_swendsen.tex`](https://github.com/VadimSokolov/p_equals_rp/blob/v1.0.0/ch_swendsen.tex), label `conj:blockmix`.

## Chapter 56. Towards a Mixing Proof on Unconditioned Boards

<a id="swap_chain_mixing_conjecture"></a>

### Polynomial mixing of the swap chain on the bottom level set of the queens

Conjecture 56.1, page 235 of Polson and Sokolov (2026), *P = RP: A Monte Carlo Program for P versus NP*, edition 1. New in this book.

Status: open.

Statement. Let $S(x)$ be the number of attacking pairs of queens in the permutation $x \in S_N$, let $A_N = \{ x \in S_N : S(x) \le 1 \}$, and let $G_N$ be the connected component of $A_N$, under swaps of two rows, that contains the most solutions (permutations with $S(x) = 0$). The swap chain on $G_N$ chooses a pair of rows uniformly among the $\binom{N}{2}$ pairs, swaps their columns to get $y$, and moves to $y$ if $S(y) \le 1$ and otherwise stays. Conjecture: there is a constant $c$ such that for all $N \ge 8$ the swap chain on $G_N$ has mixing time at most $N^c$. Moreover $|G_N \cap \{ S = 0 \}| \ge (1 - o(1))\, Q(N)$, where $Q(N)$ is the number of solutions of the $N$ queens problem.

Source: [`ch_mixingproof.tex`](https://github.com/VadimSokolov/p_equals_rp/blob/v1.0.0/ch_mixingproof.tex), label `conj:mixing`.

<a id="swap_chain_basic_facts"></a>

### Reversibility, irreducibility and aperiodicity of the swap chain on the giant component

Lemma 56.2, page 235 of Polson and Sokolov (2026), *P = RP: A Monte Carlo Program for P versus NP*, edition 1. New in this book.

Status: proved.

Statement. The swap chain on $G_N$, the connected component of $\{ x \in S_N : S(x) \le 1 \}$ under swaps of two rows that contains the most solutions, with moves given by swapping the columns of two rows chosen uniformly among the $\binom{N}{2}$ pairs and rejecting moves that leave the set, is reversible with respect to the uniform distribution on $G_N$, is irreducible on $G_N$ by the definition of $G_N$, and is aperiodic for $N \ge 8$. Its off diagonal transition probabilities are $0$ or $1 / \binom{N}{2}$.

Source: [`ch_mixingproof.tex`](https://github.com/VadimSokolov/p_equals_rp/blob/v1.0.0/ch_mixingproof.tex), label `lem:chainfacts`.

<a id="swap_from_solution_at_most_four"></a>

### A swap of a solution creates at most four attacks

Lemma 56.3, page 236 of Polson and Sokolov (2026), *P = RP: A Monte Carlo Program for P versus NP*, edition 1. New in this book.

Status: proved.

Statement. Let $x$ be a solution of the $N$ queens problem, a permutation with $S(x) = 0$ attacking pairs, and let $y$ be obtained from $x$ by swapping the columns of two rows $i$ and $j$. Then $S(y) \le 4$.

Source: [`ch_mixingproof.tex`](https://github.com/VadimSokolov/p_equals_rp/blob/v1.0.0/ch_mixingproof.tex), label `lem:four`.

<a id="expansion_of_the_bottom_level_set"></a>

### Expansion of the bottom level set

Conjecture 56.4, page 237 of Polson and Sokolov (2026), *P = RP: A Monte Carlo Program for P versus NP*, edition 1. New in this book.

Status: open.

Statement. Let $S(x)$ be the number of attacking pairs of queens in $x \in S_N$, let $G_N$ be the connected component of $\{ x \in S_N : S(x) \le 1 \}$, under swaps of two rows, that contains the most solutions, and let $\Phi_N$ be the conductance of the swap chain on $G_N$, that is, the minimum over subsets $A \subseteq G_N$ with $|A| \le |G_N|/2$ of the number of swap edges leaving $A$ divided by $\binom{N}{2} |A|$. Conjecture: there is a constant $c'$ such that $\Phi_N \ge N^{-c'}$ for all $N \ge 8$.

Source: [`ch_mixingproof.tex`](https://github.com/VadimSokolov/p_equals_rp/blob/v1.0.0/ch_mixingproof.tex), label `conj:expansion`.

<a id="expansion_equivalent_to_mixing"></a>

### Expansion of the bottom level set is equivalent to polynomial mixing

Theorem 56.5, page 237 of Polson and Sokolov (2026), *P = RP: A Monte Carlo Program for P versus NP*, edition 1. New in this book.

Status: proved.

Statement. Let $G_N$ be the connected component of $\{ x \in S_N : S(x) \le 1 \}$, under swaps of two rows, that contains the most solutions of the $N$ queens problem, where $S(x)$ is the number of attacking pairs, and let $\Phi_N$ be the conductance of the swap chain on $G_N$, the minimum over $A \subseteq G_N$ with $|A| \le |G_N|/2$ of the number of swap edges leaving $A$ divided by $\binom{N}{2} |A|$. If $\Phi_N \ge N^{-c'}$ for all $N \ge 8$, then the lazy version of the swap chain has mixing time $\tau(\epsilon) \le \frac{4}{\Phi_N^2} \big( N \log N + \log(1/\epsilon) \big) \le 4 N^{2c'} \big( N \log N + \log(1/\epsilon) \big)$, where $\tau(\epsilon)$ is the time to reach total variation distance $\epsilon$ from the uniform distribution on $G_N$. Conversely, if the swap chain on $G_N$ has mixing time at most $N^c$ for all $N \ge 8$, then $\Phi_N \ge N^{-(c+1)}$, so the expansion bound holds with $c' = c + 1$.

Source: [`ch_mixingproof.tex`](https://github.com/VadimSokolov/p_equals_rp/blob/v1.0.0/ch_mixingproof.tex), label `thm:reduction`.

## Chapter 58. Rigorous Theorems on P, NP and RP

<a id="main_equivalence_np_rp_queens_sampling"></a>

### The main equivalence, NP = RP if and only if queens completions can be sampled or counted in polynomial time

Theorem 58.1, page 242 of Polson and Sokolov (2026), *P = RP: A Monte Carlo Program for P versus NP*, edition 1. New in this book.

Status: proved.

Statement. The following are equivalent. (1) $\mathrm{NP} = \mathrm{RP}$. (2) There is a fully polynomial almost uniform sampler for the completions of a partial queens placement. That is, there is a randomized algorithm which, given $(N, X_0)$ and $\delta > 0$, outputs in time polynomial in $N$ and $\log(1/\delta)$ a placement whose law is within total variation $\delta$ of uniform on the set of completions, or reports correctly that there are none. (3) There is a fully polynomial almost uniform sampler which, given $(N, X_0, m)$ and $\delta > 0$, samples the level set $\{ x : S(x) \le m, \, x \supseteq X_0 \}$ of the queens energy $S$ on partial boards, in time polynomial in $N$ and $\log(1/\delta)$, uniformly in $m$. (4) There is a fully polynomial randomized approximation scheme for the number of completions $\#\mathrm{QUEENS}(N, X_0)$.

Source: [`ch_theorems.tex`](https://github.com/VadimSokolov/p_equals_rp/blob/v1.0.0/ch_theorems.tex), label `thm:mainequiv`.

<a id="derandomization_equivalence_prrp_prp"></a>

### Median form of the hitting set characterisation of prRP = prP

Theorem 58.2, page 244 of Polson and Sokolov (2026), *P = RP: A Monte Carlo Program for P versus NP*, edition 1. New in this book.

Status: conditional on the extension to promise problems of the Buhrman and Fortnow theorem, that prRP = prP implies prBPP = prP (used only for (1) implies (2)).

Statement. Let $\mathrm{prRP}$ and $\mathrm{prP}$ denote the promise versions of $\mathrm{RP}$ and $\mathrm{P}$, in which an algorithm is required to be correct only on inputs satisfying the promise. The following are equivalent. (1) $\mathrm{prRP} = \mathrm{prP}$. (2) For every polynomial time computable $f : \{0,1\}^* \times \{0,1\}^{m(n)} \to \{0, 1\}$ there is a deterministic polynomial time algorithm which, on input $x$ with $|x| = n$, outputs a point $r$ with $f(x, r) = 1$ whenever $\mathbb{P}_r(f(x, r) = 1) \ge \tfrac12$. (3) For every such $f$ the median of $f(x, \cdot)$ over $r$, defined as $1$ if $\mathbb{P}_r(f(x,r) = 1) \ge \tfrac12$ and $0$ otherwise, is computable in deterministic polynomial time on the promise that either $f(x, \cdot) \equiv 0$ or $\mathbb{P}_r(f(x,r) = 1) \ge \tfrac12$. Moreover (3) restricted to the pairs $(f, x)$ arising from $\mathrm{RP}$ languages is equivalent to $\mathrm{P} = \mathrm{RP}$.

Source: [`ch_theorems.tex`](https://github.com/VadimSokolov/p_equals_rp/blob/v1.0.0/ch_theorems.tex), label `thm:derandequiv`.

<a id="limits_of_monte_carlo_for_queens"></a>

### Limits of Monte Carlo for the queens completion problem

Theorem 58.5, page 245 of Polson and Sokolov (2026), *P = RP: A Monte Carlo Program for P versus NP*, edition 1. New in this book.

Status: proved.

Statement. No randomized algorithm decides $\mathrm{QUEENS}$ with one sided error in polynomial time unless $\mathrm{NP} = \mathrm{RP}$. No randomized algorithm approximates $\#\mathrm{QUEENS}$ to within any polynomial factor in polynomial time unless $\mathrm{NP} = \mathrm{RP}$. No randomized algorithm samples the completions of a partial board to within any constant total variation distance in polynomial time unless $\mathrm{NP} = \mathrm{RP}$.

Source: [`ch_theorems.tex`](https://github.com/VadimSokolov/p_equals_rp/blob/v1.0.0/ch_theorems.tex), label `thm:limitsmc`.

<a id="conditional_fpras_explicit_rates"></a>

### Conditional FPRAS with explicit rates for the stratified vertical walk

Theorem 58.6, page 245 of Polson and Sokolov (2026), *P = RP: A Monte Carlo Program for P versus NP*, edition 1. New in this book.

Status: proved.

Statement. Let $S$ be an energy on a finite set $\mathcal{X}$ with $|\mathcal{X}|$ known and at most $K + 1$ levels, and let the level set chain at level $m$ be a reversible lazy chain whose stationary law is uniform on the level set, with relaxation time $t_{rel}(m)$. Let $t^* = \max_m t_{rel}(m)$, and assume that the successive ratios $\theta_t$ of the product estimator are bounded below by a constant $\theta_0 > 0$. Then the stratified vertical walk estimates $N(0)$ to relative error $\epsilon$ with probability $\tfrac34$ using at most $O\big( \frac{K^2}{\epsilon^2} \cdot t^* \cdot ( \log |\mathcal{X}| + \log(K / \epsilon) ) \big)$ chain steps, and the quadrature contribution to the root mean squared error is at most $\lambda_1 \sqrt{K} / (2n)$ for $n$ stratified nodes per rung, where $\lambda_1$ is the largest step value of the quantile staircase.

Source: [`ch_theorems.tex`](https://github.com/VadimSokolov/p_equals_rp/blob/v1.0.0/ch_theorems.tex), label `thm:condfpras_rates`.

## Chapter 60. Open Problems: Status and Approaches

<a id="rung_skipping"></a>

### Rung skipping, the walk that starts at a connected level set

Theorem 60.20, page 264 of Polson and Sokolov (2026), *P = RP: A Monte Carlo Program for P versus NP*, edition 1. New in this book.

Status: conditional on the swap chain on every sublevel set of energy at most j, for j at least m, is irreducible and mixes in polynomial time T; the rung ratios are at least 1/q(N) for a polynomial q; the ratio of the number of ground states to the size of the sublevel set at m is at least 1/p(N) for a polynomial p.

Statement. Let $B$ be a board with completions and let $m \ge m_c(B)$, where $m_c(B)$ is the shattering depth of $B$. Suppose the swap chain on the conditioned level set $\{ S \le j \}$ is irreducible and mixes in time $T$, polynomial in $N$, for every $j \ge m$, that $|\{ S \le j \}| / |\{ S \le j + 1 \}| \ge 1 / q(N)$ for every $j \ge m$ and a polynomial $q$, and that $N(0) / |\{ S \le m \}| \ge 1 / p(N)$ for a polynomial $p$. Let $K$ be the number of rungs above $m$, that is, the number of $j \ge m$ with $\{ S \le j \}$ not the whole board. Then the vertical walk that estimates $N(0) / |\{ S \le m \}|$ directly, as the fraction of ground states among samples from $\{ S \le m \}$, and the ratios $|\{ S \le j \}| / |\{ S \le j + 1 \}|$ for $j \ge m$ by the product estimator, is an FPRAS for the completion count with cost $O((K^3 q(N) + p(N)) \epsilon^{-2} T \log (K/\delta))$ for confidence $1 - \delta$.

Source: [`ch_open3.tex`](https://github.com/VadimSokolov/p_equals_rp/blob/v1.0.0/ch_open3.tex), label `thm:rungskip`.

<a id="shattering_depth_conjecture"></a>

### Shattering depth on hard boards

Conjecture 60.21, page 266 of Polson and Sokolov (2026), *P = RP: A Monte Carlo Program for P versus NP*, edition 1. New in this book.

Status: open.

Statement. There is a family of boards $B_N$ from the Gent, Jefferson and Nightingale reduction applied to hard formulas with $m_c(B_N) \ge c N$ for a constant $c > 0$, where $m_c(B_N)$ is the shattering depth, and for such boards the ratio $N(0) / |\{ S \le m_c(B_N) \}|$ is exponentially small in $N$.

Source: [`ch_open3.tex`](https://github.com/VadimSokolov/p_equals_rp/blob/v1.0.0/ch_open3.tex), label `conj:shatterdepth`.

<a id="depth_growth_conjecture"></a>

### Depth growth on random boards

Conjecture 60.25, page 269 of Polson and Sokolov (2026), *P = RP: A Monte Carlo Program for P versus NP*, edition 1. New in this book.

Status: open.

Statement. On random boards with a fixed number of fixed queens, $m_c(B) = O(1)$ with high probability, so that the price of rung skipping is inverse polynomial. The data to $N = 16$ do not exclude slow growth, since $m_c(B) = O(\log N)$ would make the price quasi polynomial, and the alternative, $m_c(B) \ge cN$, would make the vertical walk exponential on random boards.

Source: [`ch_open4.tex`](https://github.com/VadimSokolov/p_equals_rp/blob/v1.0.0/ch_open4.tex), label `conj:depthgrowth`.

***

<small>License: Text, figures and PDF: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Code: [MIT](https://opensource.org/license/mit).</small>

<small>This page is generated from the book's repository ([main](https://github.com/VadimSokolov/p_equals_rp/tree/main)). The numbers and pages are those of the PDF, [version 1.0.0](https://github.com/VadimSokolov/p_equals_rp/releases/tag/v1.0.0).</small>

<!-- Generated by bookrepo.py from book.yaml and results.yaml. Edit those files, not this one. -->
