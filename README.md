# Internship Ranker

Ranks Summer 2027 software engineering internships against a resume profile
(C++/Java, systems background, U.S. Army veteran, Los Angeles preferred).

## How it works

1. Reads the public [SimplifyJobs Summer 2027 internship list](https://github.com/SimplifyJobs/Summer2027-Internships) (`.github/scripts/listings.json`).
2. Keeps active, visible Summer 2027 software roles in the U.S. that accept bachelor's students.
3. Scores each posting:

| Signal | Points |
|---|---|
| LA / Orange County | +30 |
| Elsewhere in California | +12 |
| Remote option | +8 |
| Core software engineering title | +15 |
| C++ / Java / embedded / systems / backend / game / tools | +8 |
| Early-career or pipeline program | +10 |
| Defense / aerospace company | +6 |
| Posted this week / this month | +10 / +5 |
| ML, research or quant focus | -6 |
| Web / mobile stack | -2 |
| Posted 4+ months ago | -5 |

4. Assigns a tier: **Strong** (45+), **Good** (25–44), **Possible** (below 25).

## Run it

```bash
git clone --depth 1 https://github.com/SimplifyJobs/Summer2027-Internships.git data
python3 rank.py data/.github/scripts/listings.json ranked.json
```

`ranked.json` holds every match sorted by score, with the reasons (`why`) and warnings (`flags`) for each.
