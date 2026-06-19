"""
Toy-paper analysis: AI-tool adoption and self-reported job satisfaction
among professional developers (Stack Overflow 2025 Developer Survey).

Research question (descriptive only):
    Among professional developers, is reported AI-tool adoption associated
    with reported job satisfaction, controlling for years of professional
    experience and primary developer role?

Outputs:
    results_table.csv                          (machine-readable key numbers)
    paper/figures/fig1_satisfaction_by_ai_use.pdf
    paper/figures/fig2_years_experience.pdf

Run:  python analysis/analysis.py
"""

from pathlib import Path
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
CSV = ROOT / "data" / "results.csv"
FIGDIR = ROOT / "paper" / "figures"
FIGDIR.mkdir(parents=True, exist_ok=True)
RESULTS_CSV = ROOT / "results_table.csv"

# ----------------------------------------------------------------- load
COLS = ["MainBranch", "AISelect", "JobSat", "WorkExp", "DevType"]
raw = pd.read_csv(CSV, usecols=COLS, low_memory=False)
n_total = len(raw)

# Restrict to professional developers (the population in the research question).
pro = raw[raw["MainBranch"] == "I am a developer by profession"].copy()
n_pro = len(pro)

# ----------------------------------------------------------------- recode
# AI-use frequency ordering and a binary "AI user" indicator.
FREQ_ORDER = [
    "No, and I don't plan to",
    "No, but I plan to soon",
    "Yes, I use AI tools monthly or infrequently",
    "Yes, I use AI tools weekly",
    "Yes, I use AI tools daily",
]
USES_AI = {
    "Yes, I use AI tools daily": 1,
    "Yes, I use AI tools weekly": 1,
    "Yes, I use AI tools monthly or infrequently": 1,
    "No, but I plan to soon": 0,
    "No, and I don't plan to": 0,
}
pro["ai_user"] = pro["AISelect"].map(USES_AI)
pro["ai_freq"] = pd.Categorical(
    pro["AISelect"], categories=FREQ_ORDER, ordered=True)
# Ordinal score 0..4 for a robustness specification.
pro["ai_freq_score"] = pro["ai_freq"].cat.codes.replace(-1, np.nan)

# ----------------------------------------------------------------- analysis frame
frame = pro.dropna(subset=["JobSat", "ai_user", "WorkExp", "DevType"]).copy()
# Keep DevType categories with enough support for stable fixed effects.
counts = frame["DevType"].value_counts()
keep = counts[counts >= 30].index
frame = frame[frame["DevType"].isin(keep)].copy()
n_frame = len(frame)

# ----------------------------------------------------------------- descriptives
by_cat = (frame.groupby("AISelect")["JobSat"]
          .agg(["count", "mean", "median", "std"])
          .reindex([c for c in FREQ_ORDER if c in frame["AISelect"].unique()]))

mean_user = frame.loc[frame["ai_user"] == 1, "JobSat"].mean()
mean_nonuser = frame.loc[frame["ai_user"] == 0, "JobSat"].mean()

# ----------------------------------------------------------------- regressions
# Main specification: binary AI-user indicator + experience + role FE.
m_main = smf.ols("JobSat ~ ai_user + WorkExp + C(DevType)", data=frame).fit()

# Unadjusted (raw) bivariate, for comparison.
m_raw = smf.ols("JobSat ~ ai_user", data=frame).fit()

# Robustness 1: ordinal AI-frequency score instead of binary.
m_ord = smf.ols("JobSat ~ ai_freq_score + WorkExp + C(DevType)", data=frame).fit()

# Robustness 2: restrict to experienced developers (>5 years).
exp = frame[frame["WorkExp"] > 5]
m_exp = smf.ols("JobSat ~ ai_user + WorkExp + C(DevType)", data=exp).fit()


def grab(model, term):
    return dict(
        coef=model.params[term],
        se=model.bse[term],
        t=model.tvalues[term],
        p=model.pvalues[term],
        ci_low=model.conf_int().loc[term, 0],
        ci_high=model.conf_int().loc[term, 1],
        n=int(model.nobs),
        r2=model.rsquared,
    )

main = grab(m_main, "ai_user")
raw_b = grab(m_raw, "ai_user")
ordv = grab(m_ord, "ai_freq_score")
expv = grab(m_exp, "ai_user")
we = grab(m_main, "WorkExp")

# ----------------------------------------------------------------- results_table.csv
rows = []
def add(label, d):
    rows.append({
        "quantity": label, "estimate": d["coef"], "std_error": d["se"],
        "t_stat": d["t"], "p_value": d["p"], "ci_low": d["ci_low"],
        "ci_high": d["ci_high"], "n": d["n"], "r_squared": d["r2"],
    })

add("ai_user_unadjusted", raw_b)
add("ai_user_adjusted_main", main)
add("workexp_adjusted_main", we)
add("ai_freq_score_adjusted", ordv)
add("ai_user_experienced_gt5y", expv)
res = pd.DataFrame(rows)
res.to_csv(RESULTS_CSV, index=False)

# Also append the by-category satisfaction means as a second block.
by_out = by_cat.reset_index().rename(columns={"AISelect": "ai_use_category"})
by_out.to_csv(ROOT / "results_satisfaction_by_ai_use.csv", index=False)

# ----------------------------------------------------------------- figures
# Fig 1: mean satisfaction by AI-use category, with 95% CI error bars.
labels_short = {
    "No, and I don't plan to": "No, no plans",
    "No, but I plan to soon": "No, plan to",
    "Yes, I use AI tools monthly or infrequently": "Yes, monthly",
    "Yes, I use AI tools weekly": "Yes, weekly",
    "Yes, I use AI tools daily": "Yes, daily",
}
ci = 1.96 * by_cat["std"] / np.sqrt(by_cat["count"])
fig, ax = plt.subplots(figsize=(7, 4.2))
xs = range(len(by_cat))
ax.bar(xs, by_cat["mean"], yerr=ci, capsize=4, color="#4878a8", alpha=0.9)
ax.set_xticks(list(xs))
ax.set_xticklabels([labels_short[i] for i in by_cat.index], rotation=20, ha="right")
ax.set_ylabel("Mean job satisfaction (0–10)")
ax.set_ylim(6.5, 7.6)
ax.set_title("Mean job satisfaction by reported AI-tool use")
for x, m, c in zip(xs, by_cat["mean"], by_cat["count"]):
    ax.text(x, m + ci.iloc[x] + 0.02, f"{m:.2f}\n(n={int(c):,})",
            ha="center", va="bottom", fontsize=7)
fig.tight_layout()
fig.savefig(FIGDIR / "fig1_satisfaction_by_ai_use.pdf")
plt.close(fig)

# Fig 2: distribution of years of professional experience.
fig, ax = plt.subplots(figsize=(7, 4.2))
ax.hist(frame["WorkExp"], bins=range(0, 51, 2), color="#5b8a5b", alpha=0.9,
        edgecolor="white")
med = frame["WorkExp"].median()
ax.axvline(med, color="#b33", linestyle="--", linewidth=1.5,
           label=f"median = {med:.0f} years")
ax.set_xlabel("Years of professional work experience")
ax.set_ylabel("Number of respondents")
ax.set_title("Distribution of professional experience (analysis sample)")
ax.set_xlim(0, 50)
ax.legend()
fig.tight_layout()
fig.savefig(FIGDIR / "fig2_years_experience.pdf")
plt.close(fig)

# ----------------------------------------------------------------- console report
print("=" * 70)
print("ANALYSIS SUMMARY")
print("=" * 70)
print(f"Total respondents in CSV:            {n_total:,}")
print(f"Professional developers:             {n_pro:,}")
print(f"Analysis frame (complete cases):     {n_frame:,}")
print(f"  DevType categories retained:       {frame['DevType'].nunique()}")
print()
print("Mean / median job satisfaction by AI-use category:")
print(by_cat.round(3).to_string())
print()
print(f"Mean JobSat, AI users:     {mean_user:.3f}")
print(f"Mean JobSat, non-users:    {mean_nonuser:.3f}")
print(f"Raw difference:            {mean_user - mean_nonuser:+.3f}")
print()
print("MAIN OLS: JobSat ~ ai_user + WorkExp + C(DevType)")
print(f"  ai_user coef = {main['coef']:+.4f}  SE = {main['se']:.4f}  "
      f"t = {main['t']:.2f}  p = {main['p']:.3g}")
print(f"  95% CI = [{main['ci_low']:+.4f}, {main['ci_high']:+.4f}]")
print(f"  WorkExp coef = {we['coef']:+.4f}  SE = {we['se']:.4f}  p = {we['p']:.3g}")
print(f"  n = {main['n']:,}   R^2 = {main['r2']:.4f}")
print()
print(f"Unadjusted ai_user coef = {raw_b['coef']:+.4f} (p = {raw_b['p']:.3g})")
print(f"Ordinal ai_freq_score coef = {ordv['coef']:+.4f} (p = {ordv['p']:.3g})")
print(f">5y experience ai_user coef = {expv['coef']:+.4f} "
      f"(p = {expv['p']:.3g}, n = {expv['n']:,})")
print()
print(f"Wrote: {RESULTS_CSV.name}, results_satisfaction_by_ai_use.csv")
print(f"Wrote: {FIGDIR/'fig1_satisfaction_by_ai_use.pdf'}")
print(f"Wrote: {FIGDIR/'fig2_years_experience.pdf'}")
