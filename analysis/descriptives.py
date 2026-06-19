"""
Descriptive statistics for the Stack Overflow 2025 Developer Survey.

Focus: the variables behind the toy-paper research question --
AI-tool adoption, job satisfaction, professional experience, and developer role.

Run:  python analysis/descriptives.py
Writes a markdown report to analysis/descriptives.md
"""

from pathlib import Path
import textwrap
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
CSV = ROOT / "data" / "results.csv"
OUT = ROOT / "analysis" / "descriptives.md"

KEY = [
    "MainBranch", "Age", "Employment", "YearsCode", "WorkExp",
    "DevType", "AISelect", "AISent", "JobSat",
    "ConvertedCompYearly", "Country",
]

# Order categories sensibly for display where there is a natural order.
AISELECT_ORDER = [
    "Yes, I use AI tools daily",
    "Yes, I use AI tools weekly",
    "Yes, I use AI tools monthly or infrequently",
    "No, but I plan to soon",
    "No, and I don't plan to",
]
AISENT_ORDER = [
    "Very favorable", "Favorable", "Indifferent", "Unsure",
    "Unfavorable", "Very unfavorable",
]

lines = []
def w(s=""):
    lines.append(s)

df = pd.read_csv(CSV, usecols=KEY, low_memory=False)
n = len(df)

w("# Descriptive statistics — Stack Overflow 2025 Developer Survey")
w()
w(f"Source file: `data/results.csv`  |  Respondents: **{n:,}**")
w()
w("> Self-reported, observational, non-random sample. Descriptive only.")
w()

# ---------------------------------------------------------------- missingness
w("## 1. Missingness of key variables")
w()
miss = pd.DataFrame({
    "non_null": df[KEY].notna().sum(),
    "missing": df[KEY].isna().sum(),
})
miss["pct_missing"] = (100 * miss["missing"] / n).round(1)
w("| variable | non-null | missing | % missing |")
w("|---|---:|---:|---:|")
for v in KEY:
    r = miss.loc[v]
    w(f"| {v} | {int(r.non_null):,} | {int(r.missing):,} | {r.pct_missing} |")
w()

# ---------------------------------------------------------------- numeric
w("## 2. Numeric variables")
w()
num = ["WorkExp", "YearsCode", "JobSat", "ConvertedCompYearly"]
# YearsCode has text codes like "Less than 1 year" / "More than 50 years"
yc = pd.to_numeric(
    df["YearsCode"].replace({
        "Less than 1 year": 0.5, "More than 50 years": 51,
    }), errors="coerce")
tmp = df.copy()
tmp["YearsCode"] = yc
desc = tmp[num].describe(percentiles=[.25, .5, .75]).T
desc["missing"] = [int(tmp[c].isna().sum()) for c in num]
w("| variable | n | mean | std | min | 25% | median | 75% | max | missing |")
w("|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|")
for c in num:
    r = desc.loc[c]
    w(f"| {c} | {int(r['count']):,} | {r['mean']:.1f} | {r['std']:.1f} | "
      f"{r['min']:.0f} | {r['25%']:.0f} | {r['50%']:.0f} | {r['75%']:.0f} | "
      f"{r['max']:.0f} | {r['missing']:,} |")
w()
w("*JobSat is a 0–10 self-rating. ConvertedCompYearly is annual USD comp "
  "(heavily right-skewed; see median vs mean).*")
w()

# ---------------------------------------------------------------- categoricals
def cat_block(title, col, order=None, top=None, note=""):
    w(f"### {title}")
    w()
    vc = df[col].value_counts(dropna=False)
    if order:
        idx = [c for c in order if c in vc.index]
        idx += [c for c in vc.index if c not in idx and pd.notna(c)]
        if df[col].isna().any():
            idx += [float("nan")]
        vc = vc.reindex(idx)
    if top:
        vc = vc.head(top)
    w("| category | n | % |")
    w("|---|---:|---:|")
    for k, v in vc.items():
        label = "(missing)" if pd.isna(k) else str(k)
        w(f"| {label} | {int(v):,} | {100*v/n:.1f} |")
    if note:
        w()
        w(f"*{note}*")
    w()

w("## 3. Categorical variables")
w()
cat_block("AI-tool adoption (AISelect)", "AISelect", order=AISELECT_ORDER)
cat_block("Sentiment toward AI tools (AISent)", "AISent", order=AISENT_ORDER)
cat_block("Main branch", "MainBranch")
cat_block("Age group", "Age")
cat_block("Developer role (DevType) — top 12", "DevType", top=12,
          note="Long tail of roles truncated to top 12.")
cat_block("Country — top 12", "Country", top=12,
          note="Long tail of countries truncated to top 12.")

# ---------------------------------------------------------------- crosstab
w("## 4. Job satisfaction by AI-tool adoption")
w()
w("Mean JobSat (0–10) within each AI-adoption category, professional "
  "developers only (MainBranch = 'I am a developer by profession').")
w()
pro = df[df["MainBranch"] == "I am a developer by profession"].copy()
grp = (pro.dropna(subset=["AISelect", "JobSat"])
          .groupby("AISelect")["JobSat"]
          .agg(["count", "mean", "median", "std"]))
order = [c for c in AISELECT_ORDER if c in grp.index]
grp = grp.reindex(order)
w("| AI adoption | n | mean JobSat | median | std |")
w("|---|---:|---:|---:|---:|")
for k, r in grp.iterrows():
    w(f"| {k} | {int(r['count']):,} | {r['mean']:.2f} | "
      f"{r['median']:.0f} | {r['std']:.2f} |")
w()
overall = pro["JobSat"].mean()
w(f"*Professional-developer overall mean JobSat: {overall:.2f} "
  f"(n = {pro['JobSat'].notna().sum():,}).*")
w()
w("> Differences are small and unadjusted; this is a raw association, "
  "not a controlled or causal estimate.")
w()

OUT.write_text("\n".join(lines), encoding="utf-8")
print("\n".join(lines))
print(f"\n[written to {OUT}]")
