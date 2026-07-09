# Last Mile Logistics Auditor

**Delivery Performance & Customer Satisfaction Analysis**

---

## Executive Summary

This project analyzes last-mile delivery performance for Veridi Logistics using real transactional data from the Olist Brazilian E-Commerce dataset. The analysis examines over 99,000 delivered orders to determine whether delivery delays are concentrated in specific regions and whether late deliveries negatively impact customer satisfaction. Results show clear geographic patterns in delivery failures, with some states experiencing late delivery rates exceeding 30%. There is a strong correlation between delivery delays and lower customer review scores, confirming that late deliveries directly affect customer satisfaction. Based on these findings, I developed a State Risk Score metric to help prioritize logistics improvements in the most critical regions.

---

## Project Links

| Resource | Status |
|----------|--------|
| Notebook | [logistics_audit.ipynb](notebooks/logistics_audit.ipynb) |
| Dashboard | [Run locally](#how-to-run-locally) |
| Presentation | [presentation_outline.md](presentation_outline.md) |
| Interview Notes | [interview_notes.md](interview_notes.md) |

---

## Business Problem

Veridi Logistics, a Brazilian e-commerce logistics company, noticed increasing negative customer reviews related to delivery delays. Management needed answers to two key questions:

1. **Are delivery delays happening in specific geographic regions?**
2. **Are late deliveries causing negative customer reviews?**

This project was designed to answer both questions through data analysis and provide actionable recommendations.

---

## Dataset Used

**Source:** [Olist Brazilian E-Commerce Public Dataset](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce) (Kaggle)

| Dataset | Description |
|---------|-------------|
| `olist_orders_dataset.csv` | Order dates, delivery dates, status |
| `olist_order_reviews_dataset.csv` | Customer review scores |
| `olist_customers_dataset.csv` | Customer location (city, state) |
| `olist_order_items_dataset.csv` | Products in each order |
| `olist_products_dataset.csv` | Product details and category |
| `product_category_name_translation.csv` | Portuguese to English category names |

> **Note:** Raw Kaggle CSV files are not included in the repository due to file size. The dashboard uses the cleaned processed file in `outputs/`.

---

## Tools Used

| Tool | Purpose |
|------|---------|
| **Python** | Core programming language |
| **Pandas** | Data manipulation and analysis |
| **NumPy** | Numerical computations |
| **Plotly** | Interactive visualizations |
| **Streamlit** | Dashboard framework |
| **Jupyter Notebook** | Data exploration and pipeline development |

---

## Data Cleaning

The following cleaning steps were applied:

1. **Removed canceled orders** - Orders with status `canceled` or `unavailable` were excluded
2. **Removed incomplete records** - Orders without a delivery date were removed
3. **Converted timestamps** - Date columns converted to datetime format for calculations
4. **Deduplicated records** - After joining multiple tables, kept one record per order

---

## Feature Engineering

| Feature | Description |
|---------|-------------|
| `delay_days` | Actual delivery date minus estimated delivery date (positive = late) |
| `days_difference` | Estimated delivery date minus actual delivery date (positive = early) |
| `delivery_status` | Categorized as "On Time", "Late", or "Super Late" |
| `is_late` | Binary flag (1 = Late or Super Late) |
| `risk_score` | State Risk Score combining delay rate and customer dissatisfaction |

---

## Dashboard Features

The interactive Streamlit dashboard includes:

- **KPI Cards** - Total orders, late delivery %, average review score, super late %
- **Geographic Analysis** - Bar chart showing late delivery % by state
- **Sentiment Analysis** - Delivery status vs customer review scores
- **Scatter Plot** - Delay days vs review score with color coding
- **Category Analysis** - Top 10 product categories by late delivery rate
- **State Risk Score** - Table ranking states by combined risk metric
- **Executive Insights** - Dynamic business summary and recommendations

---

## Candidate Choice: State Risk Score

### What is State Risk Score?

A custom metric that combines delivery performance with customer satisfaction to identify regions requiring priority attention.

### Formula

```
Risk Score = Late Delivery Percentage × (5 - Average Review Score)
```

### Business Value

- **High Risk Score** = Many late deliveries AND low customer satisfaction
- **Low Risk Score** = Few late deliveries OR high customer satisfaction

This metric helps management prioritize logistics improvements in regions where delivery problems are causing the biggest customer experience problems.

---

## How to Run Locally

### Prerequisites

- Python 3.8+
- pip

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/last-mile-logistics-auditor.git
   cd last-mile-logistics-auditor
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the dashboard:
   ```bash
   streamlit run dashboard/app.py
   ```

4. Dashboard opens at `http://localhost:8501`

---

## Submission Checklist

- [x] `dashboard/app.py` - Streamlit dashboard with safe path configuration
- [x] `notebooks/logistics_audit.ipynb` - Data engineering notebook
- [x] `notebooks/logistics_audit.html` - Exported notebook with outputs
- [x] `outputs/cleaned_delivery_data.csv` - Cleaned dataset for dashboard
- [x] `README.md` - Professional documentation
- [x] `requirements.txt` - Python dependencies
- [x] `.gitignore` - Excludes raw data and sensitive files
- [x] `presentation_outline.md` - 8-slide interview presentation
- [x] `interview_notes.md` - Q&A preparation guide
- [x] Raw data files excluded from repository

---

## Dashboard QA Checklist

- [x] App loads successfully
- [x] State filter works
- [x] Product category filter works
- [x] KPI cards update
- [x] All charts update
- [x] Empty filter selections show friendly warning instead of crashing
- [x] Streamlit Cloud deployment works

---

## License

This project is for portfolio and interview demonstration purposes.
