# Last Mile Logistics Auditor
## Delivery Performance & Customer Satisfaction Analysis

---

## A. Executive Summary

Veridi Logistics experienced increasing negative customer reviews and needed to determine whether inaccurate delivery estimates were causing customer dissatisfaction. This project analyzed the Olist Brazilian E-Commerce dataset by combining order, customer, product, and review data into a single analytical dataset. The analysis found that delivery performance varies across regions, with some states experiencing higher late delivery rates. Late and super late deliveries showed lower customer review scores, confirming that logistics performance directly affects customer satisfaction. The final dashboard helps identify high-risk regions where logistics improvements should be prioritized.

---

## B. Project Links

### Notebook
[logistics_audit.ipynb](notebooks/logistics_audit.ipynb)

### Dashboard
https://last-mile-logistics-auditorgit-cgkkhm3ufokdaoyvkl3xnh.streamlit.app/

### Presentation
[Google Slides Presentation](https://docs.google.com/presentation/d/1MmSwxPIsFqK3bw5nUsLOsnjTN29Ck2Cm/edit?usp=sharing&ouid=110080855562115636061&rtpof=true&sd=true)

---

## C. Technical Explanation

### Data Cleaning

The original dataset was provided as multiple relational CSV files. The data preparation process included:

- Loading Orders, Reviews, Customers, Order Items, and Product datasets.
- Joining datasets using relational keys:
  - order_id
  - customer_id
  - product_id
- Removing canceled and unavailable orders from delivery analysis.
- Handling missing delivery dates.
- Converting date columns into datetime format.
- Creating new delivery performance features:
  - delay_days
  - days_difference
  - delivery_status
- Translating product categories from Portuguese to English.
- Exporting a cleaned dataset for dashboard analysis.

### Candidate's Choice Addition: State Risk Score

I added a State Risk Score metric to help Veridi Logistics prioritize improvement areas.

**Formula:**

```
State Risk Score = Late Delivery Percentage × (5 - Average Review Score)
```

This combines operational performance and customer satisfaction into one metric. A state with frequent late deliveries and poor customer reviews receives a higher score, helping managers identify regions where logistics improvements will create the highest business impact.

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

## How to Run Locally

### Prerequisites

- Python 3.8+
- pip

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/ineza741/last-mile-logistics-auditor.git
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

- [x] GitHub public: [Repository](https://github.com/ineza741/last-mile-logistics-auditor)
- [x] Notebook uploaded: [logistics_audit.ipynb](notebooks/logistics_audit.ipynb)
- [x] HTML export uploaded: [logistics_audit.html](notebooks/logistics_audit.html)
- [x] Dashboard deployed: [Live App](https://last-mile-logistics-auditorgit-cgkkhm3ufokdaoyvkl3xnh.streamlit.app/)
- [x] Presentation uploaded: [Google Slides](https://docs.google.com/presentation/d/1MmSwxPIsFqK3bw5nUsLOsnjTN29Ck2Cm/edit?usp=sharing&ouid=110080855562115636061&rtpof=true&sd=true)
- [x] Candidate choice explained: State Risk Score in README and dashboard

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
