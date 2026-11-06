import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the data
df = pd.read_csv('GPA_difference_scores.csv')
df = df.loc[:, ~df.columns.str.contains('^Unnamed')] # drop unnamed columns

x_col = 'nto_percentage'
y_col = 'GPA_difference'

# Plot general relationship between percentage of NTO submissions and difference
# in GPA scores
df.plot(x_col, y_col, kind='scatter', figsize=(7,5),
        title="GPA score difference against institution's percentage of NTO submissions",
        xlabel='Percentage of NTO submissions (%)',
        ylabel='GPA difference')

plt.axhline(0, color='gray', linestyle='-', linewidth=1.2, alpha=0.8)
plt.savefig('gpa_difference.png')

# Group results by NTO submission percentage and plot as a beeswarm
percentage = 5

# If percentages are stored as strings convert to float.
if df[x_col].dtype == 'object':
    df[x_col] = df[x_col].astype(str).astype(float)

# Create the grouping category
df['NTO_group'] = df[x_col].apply(lambda x: f'Below {percentage}%' if x < percentage else f'{percentage}% or more')
    
# Beeswarm plot
plt.figure(figsize=(8, 6))
sns.swarmplot(x='NTO_group', y=y_col, data=df, hue='NTO_group', palette='Set2', legend=False)

# Add horizontal line at 0 and label it
plt.axhline(0, color='gray', linestyle='-', linewidth=1.2, alpha=0.8)
plt.text(0.3, -0.015, 'No difference', fontsize=10, color='gray', va='bottom', ha='left')

# format and name the plot
plt.title(f'GPA scores of institutions with less or more than {percentage}% NTO submissions')
plt.xlabel('Percentage of NTO submissions (%)')
plt.ylabel('GPA difference')
plt.ylim(-0.55, 0.55)
plt.grid(axis='y', linestyle='--', alpha=0.5)
plt.savefig(f'beeswarm_diagram_{percentage}.png', dpi=300, bbox_inches='tight')
plt.show()