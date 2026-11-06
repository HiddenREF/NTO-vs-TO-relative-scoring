# -*- coding: utf-8 -*-
"""
Created on Fri Nov  6 13:34:56 2026

@author: wk1n25
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import ttest_ind, mannwhitneyu, shapiro, levene


institution_gpa = pd.read_csv('gpa_difference_scores.csv')
institution_gpa = institution_gpa.loc[:, ~institution_gpa.columns.str.contains('^Unnamed')] # drop unnamed columns

x_col = 'nto_percentage'
y_col = 'GPA_difference'

percentage = 5

# Create the grouping category
institution_gpa['NTO_group'] = institution_gpa[x_col].apply(lambda x: f'Below {percentage}%' if x < percentage else f'{percentage}% or more')

############## Statistical analysis
analysed_column = y_col 

analysis = institution_gpa[["institution", analysed_column, "nto_percentage", 
                            'NTO_group', "total_outputs", ] ].copy()

# Values of statistical variables - mean, median, std, etc.
group_summary = (analysis.groupby("NTO_group")
    .agg(
        institutions=("institution", "nunique"),
        analysed_mean=(analysed_column, "mean"),
        standard_deviation=(analysed_column, "std"),
        median_gpa=(analysed_column, "median"),
        minimum_gpa=(analysed_column, "min"),
        maximum_gpa=(analysed_column, "max"),
        mean_nto_percentage=("nto_percentage", "mean"),
        median_nto_percentage=("nto_percentage", "median"))
    .reset_index())

# Separate the two groups into dataframes
below_ = analysis.loc[
    analysis["NTO_group"].eq(f"Below {percentage}%"),
    analysed_column]

above_or_equal_ = analysis.loc[
    analysis["NTO_group"].eq(f"{percentage}% or more"),
    analysed_column]

# Calculate significance of differences in means (assumed no significance)
welch_result = ttest_ind(
    below_,
    above_or_equal_,
    equal_var=False,
    nan_policy="omit")

print("Welch t-statistic:", welch_result.statistic, ' (close to 0 means no significant difference.)')
print("Welch p-value:", welch_result.pvalue, ' (value above 0.05 shows no statistical significance.)')

median_below = below_.median()
median_above = above_or_equal_.median()
median_difference = median_above - median_below
difference_percentage = 100*median_difference/(max(group_summary['maximum_gpa'])-min(group_summary['minimum_gpa']))

print(f"Median GPA (<{percentage}% NTO): {median_below:.3f}")
print(f"Median GPA (≥{percentage}% NTO): {median_above:.3f}")
print(f"Difference: {median_difference:.3f}, which is equivalent to {difference_percentage:.1f}% of value range.")

# Potentially more interesting differences in median

quartiles = analysis.groupby(analysis["NTO_group"])[analysed_column].describe()

# Box plots for visual differences
plt.figure(figsize=(7, 5))
sns.boxplot(data=analysis, x="NTO_group", y=analysed_column, showfliers=True)
sns.stripplot(data=analysis, x="NTO_group", y=analysed_column, color="black", alpha=0.4, jitter=0.2, size=4)
plt.xlabel("NTO group")
plt.ylabel("GPA difference")
plt.title("REF2021 GPA by NTO percentage group")
plt.tight_layout()
plt.show()

# Box plot with a notch at the median value
plt.figure(figsize=(7,5))
sns.boxplot(data=analysis, x="NTO_group", y=analysed_column, notch=True)
plt.ylabel("GPA difference")
plt.xlabel("NTO group")
plt.title("Median GPA by NTO group")
plt.tight_layout()
plt.savefig(f'box_plot_{percentage}.png', dpi=300, bbox_inches='tight')
plt.show()

# Check if one group tends to have higher values (similar to comparing median values when variance is the same)
mann_whitney_result = mannwhitneyu(
    below_,
    above_or_equal_,
    alternative="two-sided")

print("Mann–Whitney U:", mann_whitney_result.statistic)
print("Mann–Whitney p-value:", mann_whitney_result.pvalue)
rank_biserial = (2 * mann_whitney_result.statistic) / (len(below_) * len(above_or_equal_)) - 1 
print(f"Rank-biserial correlation = {rank_biserial:.3f} (Negative value suggests institutions with higher NTO percentage have higher GPAs)")
print('(Rank-biserial correlation <0.1 shows (very-)small effect')

