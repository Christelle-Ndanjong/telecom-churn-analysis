# Telecom Customer Churn Analysis

## Overview
End-to-end analysis of customer churn at a telecommunications company using SQL Server, Python (pandas + seaborn), and Power BI. The project identifies key churn drivers, quantifies revenue impact, and provides actionable recommendations to reduce customer attrition.

## Dataset
**Source:** [Kaggle - Telco Customer Churn](https://www.kaggle.com/datasets/blastchar/telco-customer-churn)

- **7,043 customers** with 21 attributes
- Features include demographics, services, account info, and churn status
- **26.54% overall churn rate**

## Tools Used
- **SQL Server (SSMS)** — data exploration, segmentation, churn rate analysis
- **Python (pandas, seaborn, matplotlib)** — correlation analysis, advanced visualizations
- **Power BI** — interactive executive dashboard
- **DAX** — custom measures for churn rate calculations

## Key Findings

### 1. Contract Type is the #1 Churn Driver
| Contract | Churn Rate |
|----------|-----------|
| Month-to-month | 42.71% |
| One year | 11.27% |
| Two year | 2.83% |

Month-to-month customers churn at 15x the rate of two-year contract customers.

### 2. Fiber Optic Customers Churn the Most
| Internet Service | Churn Rate |
|-----------------|-----------|
| Fiber optic | 41.89% |
| DSL | 18.96% |
| No internet | 7.40% |

Despite being the premium service, fiber optic has the highest churn — driven by higher monthly charges and price sensitivity.

### 3. New Customers are Most At Risk
| Tenure | Churn Rate |
|--------|-----------|
| 0-12 months | 47.44% |
| 13-24 months | 28.71% |
| 25-48 months | 20.39% |
| 49-72 months | 9.51% |

Nearly half of customers in their first year leave. The first 12 months are the critical retention window.

### 4. Churned Customers Pay More
- Churned avg monthly charge: **$74.44**
- Retained avg monthly charge: **$61.27**
- Total revenue lost from churned customers: **$2.86M**

The company is losing its higher-value customers.

### 5. Payment Method Matters
| Payment Method | Churn Rate |
|---------------|-----------|
| Electronic check | 45.28% |
| Mailed check | 19.11% |
| Bank transfer (auto) | 16.71% |
| Credit card (auto) | 15.24% |

Automatic payment methods create friction to leaving, reducing churn by nearly 3x.

### 6. High-Risk Customer Profile
The typical churned customer is:
- On a **month-to-month** contract
- Uses **fiber optic** internet
- Pays by **electronic check**
- Has **no tech support** or online security add-ons
- Is in their **first 12 months**
- Pays **above-average** monthly charges

## Recommendations
1. **Incentivize long-term contracts** — Offer discounts for switching from month-to-month to annual plans
2. **Focus on first-year retention** — Implement onboarding programs, check-ins at months 3, 6, and 12
3. **Promote automatic payments** — Offer a small discount for enrolling in autopay
4. **Bundle support services** — Include online security and tech support in fiber optic packages
5. **Review fiber optic pricing** — The highest-paying customers are leaving; evaluate if pricing is competitive
6. **Target at-risk customers proactively** — Use the risk profile to identify and engage customers before they churn

## Project Structure
```
├── README.md
├── sql_queries/
│   └── churn_analysis.sql
├── python/
│   └── churn_analysis.ipynb
├── powerbi/
│   └── churn_dashboard.pbix
└── images/
    ├── correlation_chart.png
    ├── risk_dashboard.png
    └── powerbi_dashboard.png
```

## Visualizations

### Correlation with Churn
Shows which factors most strongly drive or prevent churn. Month-to-month contracts, lack of support services, and fiber optic internet are the top risk factors. Tenure, having dependents, and having a partner are protective factors.

### Risk Profile Dashboard
Four-panel visualization showing tenure distribution, monthly charges comparison, contract × internet service interaction, and revenue impact.

### Power BI Dashboard
Interactive dashboard with churn rate card, contract analysis, internet service breakdown, and tenure-based churn rates.

## SQL Techniques Used
- Conditional aggregation (CASE WHEN inside SUM/COUNT)
- TRY_CAST for safe type conversion
- Window functions for percentage calculations
- CASE WHEN for tenure bucketing

## Python Techniques Used
- pandas groupby and pivot tables
- Correlation analysis
- seaborn statistical visualizations (boxplot, histplot, heatmap)
- matplotlib multi-panel dashboards
- Feature encoding for correlation analysis

## Author
Built as part of a self-taught Data Analyst portfolio. Second project in a series demonstrating SQL, Python, and Power BI skills applied to real business problems.
