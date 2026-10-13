## Evidence on the relative performance of Not-Traditionally Submitted Outputs (NTOs) vs Traditional Outputs (TOs) in REF2021

![GPA difference chart](nto-vs-to-gpa-diff.png)

![GPA difference beeswarm_chart](beeswarm_diagram_5.png)

These visualisations explore whether submitting a higher proportion of Not-Traditionally Submitted Outputs (NTOs) in REF2021 was associated changes to assessment outcomes. The work supports the aims of the [Hidden REF](https://hidden-ref.org/), which seeks to improve recognition for the full range of outputs and roles that contribute to excellent research.

Each point represents a university REF submission. In the first chart, horizontal axis shows the proportion of outputs submitted as NTOs, while the vertical axis shows the difference between the submission’s **Outputs GPA** and its **Overall GPA**:

`GPA difference = Outputs GPA − Overall GPA`

A positive value means that the Outputs GPA was higher than the Overall GPA; a negative value means it was lower.

The second chart shows the same GPA difference as a beeswarm plot. It splits submissions into two groups, below 5% NTOs and 5% or more, so their spread can be compared directly.

The results do not indicate a relative disadvantage for submissions with 5% or more NTOs (the threshold for the [Hidden REF's 5% Manifesto](https://hidden-ref.org/5-manifesto/)). The mean GPA difference for this group was −0.01, compared with −0.03 for submissions with fewer than 5% NTOs. Using a 3% threshold, submissions with at least 3% NTOs had a mean difference of +0.01, while those below 3% averaged −0.03.

Taken cautiously, these findings suggest that increasing the proportion of NTOs need not be associated with a relative penalty in Outputs GPA. They do not establish that NTOs improve performance, nor do they identify an optimal submission percentage. The apparent 3–5% “sweet spot” is an exploratory observation only, and may reflect factors not represented in the chart.

*Visualisation and description based on materials supplied by Simon Kerridge in June 2025*

Suggested reference:

  - Wioleta Kijewska, James Baker, Simon Hettrick, Lyndsey Ballantyne, Michael Donnay, Gemma Derrick, Ben Thomas, and Ola Thomson, *Evidence on the relative performance of Not-Traditionally Submitted Outputs (NTOs) vs Traditional Outputs (TOs) in REF2021* (The Hidden REF, 2026) https://github.com/HiddenREF/NTO-vs-TO-relative-scoring

### Files

- `GPA_difference_scores.csv` – the underlying data (NTO percentage and GPA difference per submission)
- `nto-vs-to-gpa-diff.png` – scatter plot of GPA difference against NTO percentage
- `beeswarm_diagram_5.png` – beeswarm plot comparing submissions below and at or above 5% NTOs
- `plot_beeswarm.py` – Python script that generates the beeswarm plot

#### Reproducing the beeswarm plot

Requires `pandas`, `matplotlib`, and `seaborn`. Run `python plot_beeswarm.py` from the repository root. To use a different threshold (e.g. 3%), change `percentage` in the script; the output is saved as `beeswarm_diagram_<percentage>.png`.
