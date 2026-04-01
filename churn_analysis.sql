-- ============================================================
-- Telecom Customer Churn Analysis
-- Dataset: Telco Customer Churn (Kaggle)
-- Database: SQL Server (T-SQL)
-- ============================================================

USE TelcoChurn;
GO

-- ============================================================
-- DATA PREPARATION
-- Fix TotalCharges column (stored as text with blank values)
-- ============================================================

-- Identify problematic rows
SELECT customerID, tenure, MonthlyCharges, TotalCharges
FROM customers
WHERE TRY_CAST(TotalCharges AS FLOAT) IS NULL;
-- Result: 11 customers with tenure = 0 (brand new, no charges yet)

-- Fix: Set blank TotalCharges to 0
UPDATE customers
SET TotalCharges = '0'
WHERE TRY_CAST(TotalCharges AS FLOAT) IS NULL;


-- ============================================================
-- QUESTION 1: Overall Churn Rate
-- Business Context: Establish the baseline churn metric
-- ============================================================

SELECT
    Churn,
    COUNT(*) AS customer_count,
    CAST(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER() AS DECIMAL(10,2)) AS percentage
FROM customers
GROUP BY Churn;
-- Result: 26.54% churn rate (1,869 out of 7,043 customers)


-- ============================================================
-- QUESTION 2: Churn Rate by Contract Type
-- Business Context: Determine if contract length affects retention
-- ============================================================

SELECT
    Contract AS contract_type,
    COUNT(customerID) AS total_customers,
    SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) AS churned_customers,
    CAST(SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(customerID) AS DECIMAL(10,2)) AS churn_rate
FROM customers
GROUP BY Contract
ORDER BY churn_rate DESC;
-- Result: Month-to-month 42.71%, One year 11.27%, Two year 2.83%


-- ============================================================
-- QUESTION 3: Churn Rate by Internet Service Type
-- Business Context: Identify if specific services drive churn
-- ============================================================

SELECT
    InternetService,
    COUNT(customerID) AS total_customers,
    SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) AS churned_customers,
    CAST(SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(customerID) AS DECIMAL(10,2)) AS churn_rate
FROM customers
GROUP BY InternetService
ORDER BY churn_rate DESC;
-- Result: Fiber optic 41.89%, DSL 18.96%, No internet 7.40%


-- ============================================================
-- QUESTION 4: Churn Rate by Payment Method
-- Business Context: Understand if payment friction affects retention
-- ============================================================

SELECT
    PaymentMethod,
    COUNT(customerID) AS total_customers,
    SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) AS churned_customers,
    CAST(SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(customerID) AS DECIMAL(10,2)) AS churn_rate
FROM customers
GROUP BY PaymentMethod
ORDER BY churn_rate DESC;
-- Result: Electronic check 45.28%, Mailed check 19.11%, Bank transfer 16.71%, Credit card 15.24%


-- ============================================================
-- QUESTION 5: Revenue Impact of Churn
-- Business Context: Quantify the financial cost of customer churn
-- ============================================================

SELECT
    Churn AS customer_status,
    ROUND(SUM(MonthlyCharges), 2) AS total_monthly_revenue,
    ROUND(AVG(MonthlyCharges), 2) AS avg_monthly_charges,
    ROUND(SUM(CAST(TotalCharges AS DECIMAL(10,2))), 2) AS total_revenue
FROM customers
GROUP BY Churn;
-- Result: Churned customers pay more on average ($74.44 vs $61.27)
-- Total revenue lost: $2,862,926.90


-- ============================================================
-- QUESTION 6: Churn Rate by Tenure Bucket
-- Business Context: Identify the critical retention window
-- ============================================================

SELECT
    CASE
        WHEN tenure <= 12 THEN 'New Customers (0-12)'
        WHEN tenure BETWEEN 13 AND 24 THEN 'Short Term (13-24)'
        WHEN tenure BETWEEN 25 AND 48 THEN 'Middle Term (25-48)'
        ELSE 'Long Term (49-72)'
    END AS tenure_bucket,
    COUNT(customerID) AS total_customers,
    SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) AS churned_customers,
    ROUND(
        CAST(SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) AS FLOAT) /
        NULLIF(CAST(COUNT(customerID) AS FLOAT), 0) * 100, 2
    ) AS churn_rate
FROM customers
GROUP BY
    CASE
        WHEN tenure <= 12 THEN 'New Customers (0-12)'
        WHEN tenure BETWEEN 13 AND 24 THEN 'Short Term (13-24)'
        WHEN tenure BETWEEN 25 AND 48 THEN 'Middle Term (25-48)'
        ELSE 'Long Term (49-72)'
    END
ORDER BY MIN(tenure);
-- Result: New customers 47.44%, Short term 28.71%, Middle 20.39%, Long term 9.51%


-- ============================================================
-- QUESTION 7: Churn by Demographics
-- Business Context: Understand demographic patterns in churn
-- ============================================================

-- Senior Citizens
SELECT
    CASE WHEN SeniorCitizen = 1 THEN 'Senior' ELSE 'Non-Senior' END AS customer_type,
    COUNT(*) AS total_customers,
    SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) AS churned,
    CAST(SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS DECIMAL(10,2)) AS churn_rate
FROM customers
GROUP BY SeniorCitizen;

-- Partner and Dependents
SELECT
    Partner,
    Dependents,
    COUNT(*) AS total_customers,
    SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) AS churned,
    CAST(SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS DECIMAL(10,2)) AS churn_rate
FROM customers
GROUP BY Partner, Dependents
ORDER BY churn_rate DESC;


-- ============================================================
-- QUESTION 8: High-Risk Customer Profile
-- Business Context: Identify customers most likely to churn
-- for proactive retention campaigns
-- ============================================================

SELECT
    COUNT(*) AS high_risk_customers,
    ROUND(AVG(MonthlyCharges), 2) AS avg_monthly_charges,
    ROUND(AVG(tenure), 0) AS avg_tenure_months
FROM customers
WHERE Contract = 'Month-to-month'
    AND InternetService = 'Fiber optic'
    AND PaymentMethod = 'Electronic check'
    AND tenure <= 12;

-- Churn rate for this specific high-risk segment
SELECT
    CAST(SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS DECIMAL(10,2)) AS high_risk_churn_rate
FROM customers
WHERE Contract = 'Month-to-month'
    AND InternetService = 'Fiber optic'
    AND PaymentMethod = 'Electronic check'
    AND tenure <= 12;
