# %% [markdown]
# # Telecom Customer Churn Analysis
# **Dataset:** Telco Customer Churn (Kaggle)
# 
# This notebook contains the complete Python analysis including data cleaning,
# churn factor analysis, correlation study, and executive dashboard.

# %% [markdown]
# ## Setup & Data Loading

# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('WA_Fn-UseC_-Telco-Customer-Churn.csv')

# Fix TotalCharges (stored as text with blank values)
df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce').fillna(0)

# Create binary churn column for calculations
df['churned'] = (df['Churn'] == 'Yes').astype(int)

print(f"Dataset shape: {df.shape}")
print(f"Churn rate: {df['churned'].mean()*100:.2f}%")
print(f"\nChurn distribution:")
print(df['Churn'].value_counts())

# %% [markdown]
# ## Data Exploration

# %%
# Overview of all columns
print("=== DATA TYPES ===")
print(df.dtypes)
print(f"\n=== MISSING VALUES ===")
print(df.isnull().sum())
print(f"\n=== BASIC STATS ===")
print(df[['tenure', 'MonthlyCharges', 'TotalCharges']].describe().round(2))

# %% [markdown]
# ## Question 1: Overall Churn Rate

# %%
churn_counts = df['Churn'].value_counts()
churn_pct = df['Churn'].value_counts(normalize=True).mul(100).round(2)

print("=== OVERALL CHURN ===")
print(f"Total customers: {len(df)}")
print(f"Churned: {churn_counts['Yes']} ({churn_pct['Yes']}%)")
print(f"Retained: {churn_counts['No']} ({churn_pct['No']}%)")

plt.figure(figsize=(6, 6))
plt.pie(churn_counts, labels=['Retained', 'Churned'], autopct='%1.1f%%',
        colors=['#27ae60', '#e74c3c'], startangle=90)
plt.title('Overall Customer Churn Rate', fontsize=14, fontweight='bold')
plt.show()

# %% [markdown]
# **Insight:** 26.54% churn rate — roughly 1 in 4 customers is leaving.

# %% [markdown]
# ## Question 2: Churn by Contract Type

# %%
contract_churn = df.groupby('Contract').agg(
    total=('customerID', 'count'),
    churned=('churned', 'sum')
).reset_index()
contract_churn['churn_rate'] = round(contract_churn['churned'] / contract_churn['total'] * 100, 2)

print(contract_churn)

plt.figure(figsize=(8, 5))
colors = ['#e74c3c' if x > 30 else '#f39c12' if x > 15 else '#27ae60' for x in contract_churn['churn_rate']]
plt.bar(contract_churn['Contract'], contract_churn['churn_rate'], color=colors)
plt.title('Churn Rate by Contract Type', fontsize=14, fontweight='bold')
plt.ylabel('Churn Rate (%)')
plt.show()

# %% [markdown]
# **Insight:** Month-to-month customers churn at 42.71% — 15x the rate of two-year contracts (2.83%).

# %% [markdown]
# ## Question 3: Churn by Internet Service

# %%
internet_churn = df.groupby('InternetService').agg(
    total=('customerID', 'count'),
    churned=('churned', 'sum')
).reset_index()
internet_churn['churn_rate'] = round(internet_churn['churned'] / internet_churn['total'] * 100, 2)

print(internet_churn)

plt.figure(figsize=(8, 5))
colors = ['#e74c3c' if x > 30 else '#f39c12' if x > 15 else '#27ae60' for x in internet_churn['churn_rate']]
plt.bar(internet_churn['InternetService'], internet_churn['churn_rate'], color=colors)
plt.title('Churn Rate by Internet Service', fontsize=14, fontweight='bold')
plt.ylabel('Churn Rate (%)')
plt.show()

# %% [markdown]
# **Insight:** Fiber optic customers churn at 41.89% despite being the premium service.
# Higher charges drive price sensitivity.

# %% [markdown]
# ## Question 4: Churn by Payment Method

# %%
payment_churn = df.groupby('PaymentMethod').agg(
    total=('customerID', 'count'),
    churned=('churned', 'sum')
).reset_index()
payment_churn['churn_rate'] = round(payment_churn['churned'] / payment_churn['total'] * 100, 2)
payment_churn = payment_churn.sort_values('churn_rate', ascending=False)

print(payment_churn)

plt.figure(figsize=(10, 5))
colors = ['#e74c3c' if x > 30 else '#f39c12' if x > 15 else '#27ae60' for x in payment_churn['churn_rate']]
plt.barh(payment_churn['PaymentMethod'], payment_churn['churn_rate'], color=colors)
plt.title('Churn Rate by Payment Method', fontsize=14, fontweight='bold')
plt.xlabel('Churn Rate (%)')
plt.tight_layout()
plt.show()

# %% [markdown]
# **Insight:** Electronic check at 45.28% — nearly 3x higher than automatic payment methods.
# Autopay creates friction to leaving.

# %% [markdown]
# ## Question 5: Revenue Impact of Churn

# %%
revenue_impact = df.groupby('Churn').agg(
    total_monthly_revenue=('MonthlyCharges', 'sum'),
    avg_monthly_charges=('MonthlyCharges', 'mean'),
    total_lifetime_revenue=('TotalCharges', 'sum')
).round(2)

print("=== REVENUE IMPACT ===")
print(revenue_impact)
print(f"\nMonthly revenue at risk from churn: ${revenue_impact.loc['Yes', 'total_monthly_revenue']:,.2f}")
print(f"Total revenue already lost: ${revenue_impact.loc['Yes', 'total_lifetime_revenue']:,.2f}")
print(f"\nChurned customers pay MORE on average: ${revenue_impact.loc['Yes', 'avg_monthly_charges']:.2f} vs ${revenue_impact.loc['No', 'avg_monthly_charges']:.2f}")

# %%
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

axes[0].bar(['Retained', 'Churned'],
            [revenue_impact.loc['No', 'avg_monthly_charges'], revenue_impact.loc['Yes', 'avg_monthly_charges']],
            color=['#27ae60', '#e74c3c'])
axes[0].set_title('Average Monthly Charges: Churned vs Retained', fontweight='bold')
axes[0].set_ylabel('Average Monthly Charges ($)')

axes[1].pie([revenue_impact.loc['No', 'total_monthly_revenue'], revenue_impact.loc['Yes', 'total_monthly_revenue']],
            labels=['Retained', 'Churned'], autopct='%1.1f%%', colors=['#27ae60', '#e74c3c'], startangle=90)
axes[1].set_title('Monthly Revenue Split', fontweight='bold')

plt.tight_layout()
plt.show()

# %% [markdown]
# **Insight:** Churned customers pay $74.44/month vs $61.27 for retained. 
# The company is losing its higher-value customers. $2.86M in lifetime revenue already lost.

# %% [markdown]
# ## Question 6: Churn by Tenure

# %%
df['tenure_bucket'] = pd.cut(df['tenure'], 
                              bins=[0, 12, 24, 48, 72],
                              labels=['New (0-12)', 'Short (13-24)', 'Mid (25-48)', 'Long (49-72)'],
                              include_lowest=True)

tenure_churn = df.groupby('tenure_bucket', observed=True).agg(
    total=('customerID', 'count'),
    churned=('churned', 'sum')
).reset_index()
tenure_churn['churn_rate'] = round(tenure_churn['churned'] / tenure_churn['total'] * 100, 2)

print(tenure_churn)

plt.figure(figsize=(8, 5))
colors = ['#e74c3c', '#f39c12', '#f39c12', '#27ae60']
plt.bar(tenure_churn['tenure_bucket'].astype(str), tenure_churn['churn_rate'], color=colors)
plt.title('Churn Rate by Customer Tenure', fontsize=14, fontweight='bold')
plt.ylabel('Churn Rate (%)')
plt.xlabel('Tenure Bucket')
plt.show()

# %% [markdown]
# **Insight:** 47.44% of new customers (0-12 months) churn. The first year is make-or-break.
# By year 4+, only 9.51% leave.

# %% [markdown]
# ## Churn Factor Analysis — All Attributes

# %%
cat_columns = ['gender', 'SeniorCitizen', 'Partner', 'Dependents',
               'PhoneService', 'MultipleLines', 'InternetService',
               'OnlineSecurity', 'OnlineBackup', 'DeviceProtection',
               'TechSupport', 'StreamingTV', 'StreamingMovies',
               'Contract', 'PaperlessBilling', 'PaymentMethod']

fig, axes = plt.subplots(4, 4, figsize=(20, 16))
fig.suptitle('Churn Rate by Customer Attribute', fontsize=20, fontweight='bold')

for i, col in enumerate(cat_columns):
    row = i // 4
    col_idx = i % 4
    churn_rate = df.groupby(col)['churned'].mean().sort_values(ascending=True) * 100
    colors = ['#e74c3c' if x > 30 else '#f39c12' if x > 20 else '#27ae60' for x in churn_rate]
    churn_rate.plot(kind='barh', ax=axes[row, col_idx], color=colors)
    axes[row, col_idx].set_title(col, fontweight='bold')
    axes[row, col_idx].set_xlabel('Churn Rate %')

plt.tight_layout()
plt.savefig('churn_all_factors.png', dpi=150, bbox_inches='tight')
plt.show()

# %% [markdown]
# **Insight:** Red bars (>30% churn) consistently appear for: month-to-month contracts,
# fiber optic, electronic check, no tech support, no online security. 
# Green bars (<20%) appear for: two-year contracts, DSL, automatic payments.

# %% [markdown]
# ## Correlation Analysis

# %%
df_encoded = df.copy()

# Encode Yes/No columns
yes_no_cols = ['Partner', 'Dependents', 'PhoneService', 'PaperlessBilling', 'Churn']
for col in yes_no_cols:
    df_encoded[col] = (df_encoded[col] == 'Yes').astype(int)

# Encode key categorical features
df_encoded['Contract_Monthly'] = (df_encoded['Contract'] == 'Month-to-month').astype(int)
df_encoded['Fiber_Optic'] = (df_encoded['InternetService'] == 'Fiber optic').astype(int)
df_encoded['Electronic_Check'] = (df_encoded['PaymentMethod'] == 'Electronic check').astype(int)
df_encoded['No_TechSupport'] = (df_encoded['TechSupport'] == 'No').astype(int)
df_encoded['No_OnlineSecurity'] = (df_encoded['OnlineSecurity'] == 'No').astype(int)

# Correlation with churn
corr_cols = ['churned', 'tenure', 'MonthlyCharges', 'SeniorCitizen',
             'Partner', 'Dependents', 'PaperlessBilling',
             'Contract_Monthly', 'Fiber_Optic', 'Electronic_Check',
             'No_TechSupport', 'No_OnlineSecurity']

correlation = df_encoded[corr_cols].corr()['churned'].drop('churned').sort_values()

fig, ax = plt.subplots(figsize=(10, 8))
colors = ['#e74c3c' if x > 0 else '#27ae60' for x in correlation]
correlation.plot(kind='barh', color=colors, ax=ax)
ax.set_title('Correlation with Churn', fontsize=16, fontweight='bold')
ax.set_xlabel('Correlation Coefficient')
ax.axvline(x=0, color='black', linewidth=0.5)
plt.tight_layout()
plt.savefig('churn_correlation.png', dpi=150, bbox_inches='tight')
plt.show()

print("\nCorrelation values:")
print(correlation.round(3))

# %% [markdown]
# **Insight:** Strongest positive correlations (churn drivers): month-to-month contract,
# no online security, no tech support. Strongest negative (retention): tenure, dependents, partner.

# %% [markdown]
# ## Risk Profile Dashboard

# %%
fig, axes = plt.subplots(2, 2, figsize=(16, 12))
fig.suptitle('Telco Customer Churn — Risk Profile Dashboard', fontsize=18, fontweight='bold')

# 1. Tenure distribution
axes[0,0].hist(df[df['Churn']=='Yes']['tenure'], bins=30, alpha=0.7, label='Churned', color='#e74c3c')
axes[0,0].hist(df[df['Churn']=='No']['tenure'], bins=30, alpha=0.7, label='Retained', color='#27ae60')
axes[0,0].set_title('Tenure Distribution: Churned vs Retained', fontweight='bold')
axes[0,0].set_xlabel('Tenure (months)')
axes[0,0].set_ylabel('Count')
axes[0,0].legend()

# 2. Monthly charges
sns.boxplot(x='Churn', y='MonthlyCharges', data=df, ax=axes[0,1], palette={'Yes':'#e74c3c', 'No':'#27ae60'})
axes[0,1].set_title('Monthly Charges: Churned vs Retained', fontweight='bold')

# 3. Contract x Internet Service
pivot = df.pivot_table(values='churned', index='Contract', columns='InternetService', aggfunc='mean') * 100
pivot.plot(kind='bar', ax=axes[1,0], colormap='RdYlGn_r')
axes[1,0].set_title('Churn Rate: Contract × Internet Service', fontweight='bold')
axes[1,0].set_ylabel('Churn Rate %')
axes[1,0].set_xticklabels(axes[1,0].get_xticklabels(), rotation=0)
axes[1,0].legend(title='Internet')

# 4. Revenue impact
revenue = df.groupby('Churn')['MonthlyCharges'].sum()
axes[1,1].pie(revenue, labels=['Retained', 'Churned'], autopct='%1.1f%%',
              colors=['#27ae60', '#e74c3c'], startangle=90,
              textprops={'fontsize': 12, 'fontweight': 'bold'})
axes[1,1].set_title('Monthly Revenue: Retained vs Lost', fontweight='bold')

plt.tight_layout()
plt.savefig('churn_risk_dashboard.png', dpi=150, bbox_inches='tight')
plt.show()

# %% [markdown]
# ## High-Risk Customer Profile

# %%
high_risk = df[
    (df['Contract'] == 'Month-to-month') &
    (df['InternetService'] == 'Fiber optic') &
    (df['PaymentMethod'] == 'Electronic check') &
    (df['tenure'] <= 12)
]

print("=== HIGH-RISK CUSTOMER SEGMENT ===")
print(f"Count: {len(high_risk)}")
print(f"Churn rate: {high_risk['churned'].mean()*100:.2f}%")
print(f"Avg monthly charges: ${high_risk['MonthlyCharges'].mean():.2f}")
print(f"Avg tenure: {high_risk['tenure'].mean():.1f} months")
print(f"\nCompare to overall churn rate: {df['churned'].mean()*100:.2f}%")

# %% [markdown]
# ## Executive Summary

# %% [markdown]
# ### Key Findings
# 1. **26.54% overall churn rate** — 1 in 4 customers is leaving
# 2. **Contract type is the #1 driver** — month-to-month at 42.71% vs 2.83% for two-year
# 3. **Fiber optic paradox** — premium service has highest churn (41.89%) due to price sensitivity
# 4. **First year is critical** — 47.44% of new customers churn within 12 months
# 5. **Losing high-value customers** — churned pay $74.44/month vs $61.27 retained
# 6. **$2.86M already lost** in total revenue from churned customers
# 
# ### Recommendations
# 1. Incentivize long-term contracts with discounts
# 2. Focus retention heavily on first 12 months
# 3. Promote automatic payments to create switching friction
# 4. Bundle tech support and online security with fiber optic
# 5. Review fiber optic pricing competitiveness
# 6. Proactively target high-risk profile customers
