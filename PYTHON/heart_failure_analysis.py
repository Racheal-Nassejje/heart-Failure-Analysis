
# (QN 1) DATASET DESCRIPTION


''' Dataset Title: Heart Failure Clinical Records
 Source: Kaggle (https://www.kaggle.com)
 Number of Rows: 918
 Number of Columns: 12

 Variable Descriptions:
 Age               - Age of the patient (years)
 Sex               - Gender of the patient (M/F)
 ChestPainType     - Type of chest pain (ATA, NAP, ASY, TA)
 RestingBP         - Resting blood pressure (mm Hg)
 Cholesterol       - Serum cholesterol level (mg/dL)
 FastingBS         - Fasting blood sugar (1 = >120 mg/dL, 0 = normal)
 RestingECG        - Resting ECG results (Normal, ST, LVH)
 MaxHR             - Maximum heart rate achieved
 ExerciseAngina    - Exercise-induced angina (Y/N)
 Oldpeak           - ST depression induced by exercise
 ST_Slope          - Slope of peak exercise ST segment
 HeartDisease      - Target variable (1 = disease, 0 = no disease)'''

print("Dataset described successfully")
print("\n  ")



# (QN 2) DATA LOADING AND INSPECTION

import pandas as pd

# Load the dataset
df = pd.read_csv(r"C:\Users\Raquel\OneDrive\Desktop\heart_failure_analysis\heart_failure_clinical_records.csv")

# Display first 5 rows
print("=== FIRST 5 ROWS ===")
print(df.head())

# Dataset structure
print("\n=== DATASET STRUCTURE ===")
print(df.info())

# Missing values
print("\n=== MISSING VALUES ===")
print(df.isnull().sum())
print("\n  ")



# (QN 3) DATA CLEANING

# Check for duplicates
print("=== DUPLICATE ROWS ===")
print(df.duplicated().sum())

# Remove duplicates if any
df = df.drop_duplicates()
print("Rows after removing duplicates:", len(df))

# Check data types
print("\n=== DATA TYPES ===")
print(df.dtypes)

# Rename DEATH_EVENT column to a cleaner name
df = df.rename(columns={"DEATH_EVENT": "death_event"})
print("\n=== COLUMNS AFTER RENAMING ===")
print(df.columns.tolist())

# Confirm no missing values
print("\n=== CONFIRMING NO MISSING VALUES ===")
print(df.isnull().sum())
print("\n  ")



# (QN 4) SUMMARY STATISTICS

print(" SUMMARY STATISTICS ")
print(df.describe())

# Mean of numeric columns
print("\n MEAN ")
print(df.mean(numeric_only=True))

# Median of numeric columns
print("\n MEDIAN ")
print(df.median(numeric_only=True))

# Standard deviation of numeric columns
print("\n STANDARD DEVIATION ")
print(df.std(numeric_only=True))
print("\n  ")

#Key Insight here
'''-Creatinine phosphokinase and platelets showed the highest variability 
  meaning the presence of outliers in the variables'''



# (QN 5) UNIVARIATE VISUALIZATION

import matplotlib.pyplot as plt

# Chart 1: Histogram of Age
plt.figure(figsize=(8,5))
plt.hist(df['age'], bins=20, color='steelblue', edgecolor='black')
plt.title('Distribution of Patient Age')
plt.xlabel('Age')
plt.ylabel('Number of Patients')
plt.savefig('chart1_age_histogram.png')
plt.show()
print("\n ")

#   Description of the chart
'''-  Most of the patient are between 55 and 70 years old
-  The distribution is fairly bell-shaped
-  Very few patients below 40 and above 90
-  Majority of heart failure patients are aged between 55-70 so older adults are more at risk '''


# Chart 2: Boxplot of Serum Creatinine
plt.figure(figsize=(8,5))
plt.boxplot(df['serum_creatinine'], patch_artist=True,
            boxprops=dict(facecolor='lightcoral'))
plt.title('Boxplot of Serum Creatinine')
plt.ylabel('Serum Creatinine Level')
plt.savefig('chart2_serum_boxplot.png')
plt.show()
print("\n ")
#Description of the chart
'''-The pink box is very small and low ie most values are between 0.9 and 1.4,
   -The many circles above are outliers, some patients have extremely high creatinine levels
   -This confirms what we saw in QN 4 with the high standard deviation
   -Serum creatinine has many outliers, indicating some patients have 
   -dangerously high kidney related values'''
   

# (QN 6) BIVARIATE ANALYSIS


import matplotlib.pyplot as plt

# Scatterplot: Age vs Serum Creatinine
plt.figure(figsize=(8,5))
plt.scatter(df['age'], df['serum_creatinine'], 
            color='steelblue', alpha=0.5)
plt.title('Age vs Serum Creatinine')
plt.xlabel('Age')
plt.ylabel('Serum Creatinine')
plt.savefig('chart3_scatter.png')
plt.show()
print("\n ")
# Description
'''- Most patients have creatinine levels below 2 regardless of the age.
   - Few patients across all ages have very high creatinine(outliers above 4)
   - There is no stronger linear relationship between age and serum creatinine, 
   though outliers with high creatinine levels appear across all age group'''


# Grouped Boxplot: Ejection Fraction by Death Event
plt.figure(figsize=(8,5))
died = df[df['death_event'] == 1]['ejection_fraction']
survived = df[df['death_event'] == 0]['ejection_fraction']
plt.boxplot([survived, died], labels=['Survived', 'Died'],
            patch_artist=True,
            boxprops=dict(facecolor='lightgreen'))
plt.title('Ejection Fraction by Patient Outcome')
plt.ylabel('Ejection Fraction')
plt.savefig('chart4_grouped_boxplot.png')
plt.show()
print("\n ")
# Description
'''- Survived group has a high median ejection fraction(-40)
   - Died group has a lower median ejection fraction(-30)
   Patients who died had noticebly lower ejection fraction than those who survived so
   ejecting fraction is the key indicator of heart failure outcomes'''
   
   

#(QN 7) CORRELATION ANALYSIS


import matplotlib.pyplot as plt
import seaborn as sns

# Compute correlation matrix
corr_matrix = df.corr(numeric_only=True)

print(" CORRELATION MATRIX ")
print(corr_matrix)

# Plot heatmap
plt.figure(figsize=(10,8))
sns.heatmap(corr_matrix, 
            annot=True, 
            fmt='.2f', 
            cmap='coolwarm',
            linewidths=0.5)
plt.title('Correlation Heatmap')
plt.tight_layout()
plt.savefig('chart5_correlation_heatmap.png')
plt.show()
print("\n")
# Description
# Strongest Positive Relationship:
'''- Sex and Smoking = 0.41 
	   - Males are more likely to be smokers in this dataset
	   - The strongest positive correlation is between sex and 
          smoking (0.41), suggesting male patients are more likely to smoke '''
# Strongest Negative Relationship:
''' -	Time and Death Event = -0.51 
	-	The longer a patient was monitored, the less likely they died
	-	Write this: “The strongest negative correlation is between time and death event (-0.51), 
        meaning patients monitored for longer periods had better survival outcomes”
Other Important findings:
	-	Ejection fraction and death event = -0.27 → lower ejection fraction links to death (confirms Task 6!)
	-	Serum creatinine and death event = 0.29 → higher creatinine links to death risk
	-	Serum creatinine and serum sodium = -0.26 → as creatinine rises, sodium drops'''
 

# (QN 8) SUBPLOTS VISUALIZATION

import matplotlib.pyplot as plt

fig, axes = plt.subplots(1, 3, figsize=(15, 5))

# Plot 1: Distribution of Age
axes[0].hist(df['age'], bins=20, 
             color='steelblue', edgecolor='black')
axes[0].set_title('Distribution of Age')
axes[0].set_xlabel('Age')
axes[0].set_ylabel('Number of Patients')

# Plot 2: Distribution of Ejection Fraction
axes[1].hist(df['ejection_fraction'], bins=20, 
             color='lightcoral', edgecolor='black')
axes[1].set_title('Distribution of Ejection Fraction')
axes[1].set_xlabel('Ejection Fraction')
axes[1].set_ylabel('Number of Patients')

# Plot 3: Distribution of Serum Creatinine
axes[2].hist(df['serum_creatinine'], bins=20, 
             color='lightgreen', edgecolor='black')
axes[2].set_title('Distribution of Serum Creatinine')
axes[2].set_xlabel('Serum Creatinine')
axes[2].set_ylabel('Number of Patients')

plt.suptitle('Distribution of Key Health Variables', 
             fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('chart6_subplots.png')
plt.show()
print("\n")


# (QN 9) INTERPRETATION OF FINDINGS


print("=== KEY INSIGHTS FROM ANALYSIS ===")

print("""
1. OLDER PATIENTS ARE MORE AT RISK
   - Most heart failure patients are aged 55-70 years.
   - This shows age is a significant risk factor 
     for heart failure.

2. EJECTION FRACTION PREDICTS SURVIVAL
   - Patients who died had lower ejection fraction 
     (~30) compared to survivors (~40).
   - Low ejection fraction is a strong warning sign
     of poor heart health.

3. FOLLOW-UP TIME AFFECTS SURVIVAL
   - Time had the strongest negative correlation 
     with death (-0.51).
   - Patients monitored longer had better survival,
     showing importance of regular medical checkups.

4. SERUM CREATININE HAS EXTREME OUTLIERS
   - Most patients had creatinine near 1.0 but 
     some exceeded 8.0.
   - High creatinine indicates kidney problems 
     which worsen heart failure outcomes.

5. DATASET HAD SIGNIFICANT DUPLICATE RECORDS
   - 3680 out of 5000 rows were duplicates.
   - After cleaning only 1320 valid records remained,
     highlighting importance of data cleaning.

6. SMOKING IS MORE COMMON IN MALE PATIENTS
   - Sex and smoking had a correlation of 0.41,
     suggesting male patients smoke more frequently.

7. CREATININE PHOSPHOKINASE SHOWS HIGH VARIABILITY
   - Std deviation of 970, meaning enzyme levels 
     vary greatly between patients.
   - Extremely high levels may indicate muscle or 
     heart damage.
""")


