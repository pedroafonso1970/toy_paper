# Descriptive statistics — Stack Overflow 2025 Developer Survey

Source file: `data/results.csv`  |  Respondents: **49,191**

> Self-reported, observational, non-random sample. Descriptive only.

## 1. Missingness of key variables

| variable | non-null | missing | % missing |
|---|---:|---:|---:|
| MainBranch | 49,191 | 0 | 0.0 |
| Age | 49,191 | 0 | 0.0 |
| Employment | 48,339 | 852 | 1.7 |
| YearsCode | 43,042 | 6,149 | 12.5 |
| WorkExp | 42,893 | 6,298 | 12.8 |
| DevType | 43,680 | 5,511 | 11.2 |
| AISelect | 33,720 | 15,471 | 31.5 |
| AISent | 33,467 | 15,724 | 32.0 |
| JobSat | 26,670 | 22,521 | 45.8 |
| ConvertedCompYearly | 23,947 | 25,244 | 51.3 |
| Country | 35,437 | 13,754 | 28.0 |

## 2. Numeric variables

| variable | n | mean | std | min | 25% | median | 75% | max | missing |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| WorkExp | 42,893 | 13.4 | 10.8 | 1 | 5 | 10 | 20 | 100 | 6,298.0 |
| YearsCode | 43,042 | 16.6 | 11.8 | 1 | 8 | 14 | 24 | 100 | 6,149.0 |
| JobSat | 26,670 | 7.2 | 2.0 | 0 | 6 | 8 | 8 | 10 | 22,521.0 |
| ConvertedCompYearly | 23,947 | 101761.5 | 461756.9 | 1 | 38171 | 75320 | 120596 | 50000000 | 25,244.0 |

*JobSat is a 0–10 self-rating. ConvertedCompYearly is annual USD comp (heavily right-skewed; see median vs mean).*

## 3. Categorical variables

### AI-tool adoption (AISelect)

| category | n | % |
|---|---:|---:|
| Yes, I use AI tools daily | 15,883 | 32.3 |
| Yes, I use AI tools weekly | 5,958 | 12.1 |
| Yes, I use AI tools monthly or infrequently | 4,628 | 9.4 |
| No, but I plan to soon | 1,797 | 3.7 |
| No, and I don't plan to | 5,454 | 11.1 |
| (missing) | 15,471 | 31.5 |

### Sentiment toward AI tools (AISent)

| category | n | % |
|---|---:|---:|
| Very favorable | 7,677 | 15.6 |
| Favorable | 12,311 | 25.0 |
| Indifferent | 5,880 | 12.0 |
| Unsure | 759 | 1.5 |
| Unfavorable | 3,621 | 7.4 |
| Very unfavorable | 3,219 | 6.5 |
| (missing) | 15,724 | 32.0 |

### Main branch

| category | n | % |
|---|---:|---:|
| I am a developer by profession | 37,467 | 76.2 |
| I am not primarily a developer, but I write code sometimes as part of my work/studies | 4,894 | 9.9 |
| I am learning to code | 2,585 | 5.3 |
| I code primarily as a hobby | 1,924 | 3.9 |
| I used to be a developer by profession, but no longer am | 1,325 | 2.7 |
| I work with developers or my work supports developers but am not a developer by profession | 996 | 2.0 |

### Age group

| category | n | % |
|---|---:|---:|
| 25-34 years old | 16,519 | 33.6 |
| 35-44 years old | 13,241 | 26.9 |
| 18-24 years old | 9,210 | 18.7 |
| 45-54 years old | 6,275 | 12.8 |
| 55-64 years old | 2,626 | 5.3 |
| 65 years or older | 942 | 1.9 |
| Prefer not to say | 378 | 0.8 |

### Developer role (DevType) — top 12

| category | n | % |
|---|---:|---:|
| Developer, full-stack | 12,351 | 25.1 |
| Developer, back-end | 6,453 | 13.1 |
| (missing) | 5,511 | 11.2 |
| Student | 3,008 | 6.1 |
| Architect, software or solutions | 2,684 | 5.5 |
| Developer, front-end | 1,974 | 4.0 |
| Developer, desktop or enterprise applications | 1,919 | 3.9 |
| Other (please specify): | 1,825 | 3.7 |
| Developer, mobile | 1,391 | 2.8 |
| Developer, embedded applications or devices | 1,274 | 2.6 |
| Academic researcher | 1,131 | 2.3 |
| Engineering manager | 1,068 | 2.2 |

*Long tail of roles truncated to top 12.*

### Country — top 12

| category | n | % |
|---|---:|---:|
| (missing) | 13,754 | 28.0 |
| United States of America | 7,233 | 14.7 |
| Germany | 3,025 | 6.1 |
| India | 2,547 | 5.2 |
| United Kingdom of Great Britain and Northern Ireland | 2,042 | 4.2 |
| France | 1,409 | 2.9 |
| Canada | 1,305 | 2.7 |
| Ukraine | 964 | 2.0 |
| Poland | 888 | 1.8 |
| Netherlands | 867 | 1.8 |
| Italy | 835 | 1.7 |
| Brazil | 825 | 1.7 |

*Long tail of countries truncated to top 12.*

## 4. Job satisfaction by AI-tool adoption

Mean JobSat (0–10) within each AI-adoption category, professional developers only (MainBranch = 'I am a developer by profession').

| AI adoption | n | mean JobSat | median | std |
|---|---:|---:|---:|---:|
| Yes, I use AI tools daily | 12,599 | 7.29 | 8 | 1.96 |
| Yes, I use AI tools weekly | 4,353 | 7.14 | 7 | 1.89 |
| Yes, I use AI tools monthly or infrequently | 3,188 | 7.11 | 7 | 2.02 |
| No, but I plan to soon | 1,135 | 7.11 | 8 | 2.08 |
| No, and I don't plan to | 3,643 | 7.14 | 8 | 2.12 |

*Professional-developer overall mean JobSat: 7.20 (n = 26,670).*

> Differences are small and unadjusted; this is a raw association, not a controlled or causal estimate.
