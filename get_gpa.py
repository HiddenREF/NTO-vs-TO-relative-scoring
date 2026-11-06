# -*- coding: utf-8 -*-
"""
Created on Wed Nov  4 11:36:59 2026

@author: wk1n25
"""

import pandas as pd

# Paths and names of files
data_path = '../data/REF2021/'
results_file = 'REF2021-results.csv'
submissions_file = 'ref2021_submissions_full.csv'

# Load data
results = pd.read_csv(data_path+results_file)
results = results.loc[:, ~results.columns.str.contains('^Unnamed')] # drop unnamed columns

submissions = pd.read_csv(data_path+submissions_file)
submissions = submissions.loc[:, ~submissions.columns.str.contains('^Unnamed')] # drop unnamed columns
submissions = submissions.rename(columns={"institution_ukprn_code":"institution_code_ukprn"})

score_columns = ['4_stars', '3_stars', '2_stars', '1_stars', 'unclassified']

# Convert '-' and other non-numeric values to NaN
for col in score_columns+['institution_code_ukprn']:
    results[col] = pd.to_numeric(results[col], errors="coerce")

# Calculate overall GPA for each field
results["GPA"] = (
                results["4_stars"].fillna(0) * 4
                + results["3_stars"].fillna(0) * 3
                + results["2_stars"].fillna(0) * 2
                + results["1_stars"].fillna(0)
                ) / 100

results_overall = results.loc[results["profile"].eq("Overall")].copy()

results_overall["weighted_GPA"] = results_overall["GPA"] * results_overall["fte_of_submitted_staff"]

# Group by institution
institution_gpa = results_overall.groupby(
        ["institution_code_ukprn", "institution"],
        as_index=False
    ).agg(
        submitted_FTE=("fte_of_submitted_staff", "sum"),
        weighted_GPA_overall=("weighted_GPA", "sum"),
        #Number_of_Submissions=("unit_of_assessment_number", "count")
    )

institution_gpa["overall_GPA"] = institution_gpa["weighted_GPA_overall"] / institution_gpa["submitted_FTE"]

# Calculate GPA the same way for Outputs
results_outputs = results.loc[results["profile"].eq("Outputs")].copy()
results_outputs["weighted_GPA"] = results_outputs["GPA"] * results_outputs["fte_of_submitted_staff"]

# Group by institution
institution_gpa_outputs = results_outputs.groupby(
        ["institution_code_ukprn", "institution"],
        as_index=False
    ).agg(
        submitted_FTE=("fte_of_submitted_staff", "sum"),
        weighted_GPA_outputs=("weighted_GPA", "sum"),
        #Number_of_Submissions=("unit_of_assessment_number", "count")
    )

institution_gpa_outputs["outputs_GPA"] = institution_gpa_outputs["weighted_GPA_outputs"] / institution_gpa_outputs["submitted_FTE"]

# Merge results to one DataFrame and calculate the GPA difference
institution_gpa = pd.merge(institution_gpa, institution_gpa_outputs, on=['institution_code_ukprn', 'institution', 'submitted_FTE']) 

institution_gpa['GPA_difference'] =  institution_gpa['outputs_GPA'] - institution_gpa['overall_GPA']

# Label submissions as NTO or TO
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

# Output types R and U are text-based, but not always considered NTOs. 
# Their inclusion does not seem to affect the results.
to_types = {'A', 'B', 'C', 'D', 'E'}#, 'R', 'U'}

nto_types = set(output_type_names.keys()) - to_types

submissions['is_nto'] = submissions['output_type'].isin(nto_types)

# group by institution
institution_nto = (
    submissions
    .groupby(["institution_code_ukprn", "institution"], as_index=False)
    .agg(total_outputs=("is_nto", "size"), nto_outputs=("is_nto", "sum")))

# Calculate percentage of NTO submissions for each institution
institution_nto["nto_percentage"] = (
    institution_nto["nto_outputs"]
    / institution_nto["total_outputs"]
    * 100)

institution_nto["nto_percentage"] = (institution_nto["nto_percentage"].round(2))

institution_nto = institution_nto.sort_values(
    ["nto_percentage", "total_outputs"],
    ascending=[False, False]
).reset_index(drop=True)

# Merge NTO labels and calculations to the main DataFrame
institution_gpa = pd.merge(institution_gpa, institution_nto, on=['institution_code_ukprn', 'institution'])

# Save the resulting dataset
institution_gpa.to_csv('GPA_difference_scores.csv')

