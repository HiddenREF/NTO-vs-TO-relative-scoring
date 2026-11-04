# -*- coding: utf-8 -*-
"""
Created on Wed Nov  4 11:36:59 2026

@author: wk1n25
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

data_path = '../data/REF2021/'

results_file = 'REF2021-results.csv'
submissions_file = 'ref2021_submissions_full.csv'

results = pd.read_csv(data_path+results_file)
results = results.loc[:, ~results.columns.str.contains('^Unnamed')] # drop unnamed columns


submissions = pd.read_csv(data_path+submissions_file)
submissions = submissions.loc[:, ~submissions.columns.str.contains('^Unnamed')] # drop unnamed columns
submissions = submissions.rename(columns={"institution_ukprn_code":"institution_code_ukprn"})



score_columns = ['4_stars', '3_stars', '2_stars', '1_stars', 'unclassified']

# Convert '-' and other non-numeric values to NaN
for col in score_columns+['institution_code_ukprn']:
    results[col] = pd.to_numeric(results[col], errors="coerce")

results["GPA"] = (
                results["4_stars"].fillna(0) * 4
                + results["3_stars"].fillna(0) * 3
                + results["2_stars"].fillna(0) * 2
                + results["1_stars"].fillna(0)
                ) / 100

results_overall = results.loc[results["profile"].eq("Overall")].copy()

results_overall["Weighted_GPA"] = results_overall["GPA"] * results_overall["fte_of_submitted_staff"]

institution_gpa = results_overall.groupby(
        ["institution_code_ukprn", "institution"],
        as_index=False
    ).agg(
        Submitted_FTE=("fte_of_submitted_staff", "sum"),
        Weighted_GPA_Overall=("Weighted_GPA", "sum"),
        #Number_of_Submissions=("unit_of_assessment_number", "count")
    )

institution_gpa["Overall_GPA"] = institution_gpa["Weighted_GPA_Overall"] / institution_gpa["Submitted_FTE"]

#institution_gpa = (
#    institution_gpa
#    .drop(columns="Weighted_GPA_Total")
#    .sort_values(
#        ["Overall_GPA", "Submitted_FTE"],
#        ascending=[False, False]
#    )
#    .reset_index(drop=True)
#)

results_outputs = results.loc[results["profile"].eq("Outputs")].copy()
results_outputs["Weighted_GPA"] = results_outputs["GPA"] * results_outputs["fte_of_submitted_staff"]

institution_gpa_outputs = results_outputs.groupby(
        ["institution_code_ukprn", "institution"],
        as_index=False
    ).agg(
        Submitted_FTE=("fte_of_submitted_staff", "sum"),
        Weighted_GPA_Outputs=("Weighted_GPA", "sum"),
        #Number_of_Submissions=("unit_of_assessment_number", "count")
    )

institution_gpa_outputs["Outputs_GPA"] = institution_gpa_outputs["Weighted_GPA_Outputs"] / institution_gpa_outputs["Submitted_FTE"]

institution_gpa = pd.merge(institution_gpa, institution_gpa_outputs, on=['institution_code_ukprn', 'institution', 'Submitted_FTE']) 

institution_gpa['GPA_difference'] =  institution_gpa['Outputs_GPA'] - institution_gpa['Overall_GPA']


output_type_names = {
    "A": "Authored book",
    "B": "Edited book",
    "C": "Chapter in book",
    "D": "Journal article",
    "E": "Conference contribution",
    "F": "Patent or published patent application",
    "G": "Software",
    "H": "Website content",
    "I": "Performance",
    "J": "Composition",
    "K": "Design",
    "L": "Artefact",
    "M": "Exhibition",
    "N": "Research report for external body",
    "P": "Devices and products",
    "Q": "Digital or visual media",
    "R": "Scholarly edition",
    "S": "Research data sets and databases",
    "T": "Other",
    "U": "Working paper",
    "V": "Translation",
}

to_types = {'A', 'B', 'C', 'D', 'E'}#, 'R', 'U'}

nto_types = set(output_type_names.keys()) - to_types

submissions['is_nto'] = submissions['output_type'].isin(nto_types)

institution_nto = (
    submissions
    .groupby(
        ["institution_code_ukprn", "institution"],
        as_index=False
    )
    .agg(
        total_outputs=("is_nto", "size"),
        nto_outputs=("is_nto", "sum")
    )
)

institution_nto["nto_percentage"] = (
    institution_nto["nto_outputs"]
    / institution_nto["total_outputs"]
    * 100
)

institution_nto["nto_percentage"] = (
    institution_nto["nto_percentage"].round(2)
)

institution_nto = institution_nto.sort_values(
    ["nto_percentage", "total_outputs"],
    ascending=[False, False]
).reset_index(drop=True)

institution_gpa = pd.merge(institution_gpa, institution_nto, on=['institution_code_ukprn', 'institution']) 

institution_gpa.plot('nto_percentage', 'GPA_difference', kind='scatter')

x_col = 'nto_percentage'
y_col = 'GPA_difference'

percentage = 5

# Create the grouping category
institution_gpa['NTO_Group'] = institution_gpa[x_col].apply(lambda x: f'Below {percentage}%' if x < percentage else f'{percentage}% or more')
    
# Plot
plt.figure(figsize=(8, 6))
sns.swarmplot(x='NTO_Group', y=y_col, data=institution_gpa, hue='NTO_Group', palette='Set2', legend=False)

# Add horizontal line at 0 and label it
plt.axhline(0, color='gray', linestyle='-', linewidth=1.2, alpha=0.8)
plt.text(0.25, -0.015, 'No difference', fontsize=10, color='gray', va='bottom', ha='left')

plt.title(f'GPA scores of institutions with less or more than {percentage}% NTO submissions')
plt.xlabel('Percentage of NTO submissions')
plt.ylabel('GPA difference')
plt.ylim(-0.55, 0.55)
plt.grid(axis='y', linestyle='--', alpha=0.5)
#plt.savefig(f'beeswarm_diagram_{percentage}.png', dpi=300, bbox_inches='tight')
plt.show()
