# Last Mile Logistics Auditor

## Executive Summary

Veridi Logistics was getting more negative customer reviews and wanted to know if late deliveries were the cause. I analyzed the Olist Brazilian E-Commerce dataset to see if delivery delays were concentrated in certain regions. I combined orders, customers, products, and reviews into one dataset and found that some states have much higher late delivery rates than others. Late deliveries also had lower review scores. I built a dashboard that shows which regions need improvement.

---

## Project Links

### Notebook
Jupyter Notebook (.ipynb):  
https://github.com/ineza741/last-mile-logistics-auditor/blob/main/notebooks/logistics_audit.ipynb

Notebook HTML Export:  
https://github.com/ineza741/last-mile-logistics-auditor/blob/main/notebooks/logistics_audit.html

### Dashboard
https://last-mile-logistics-auditorgit-cgkkhm3ufokdaoyvkl3xnh.streamlit.app/

### Presentation
https://docs.google.com/presentation/d/1MmSwxPIsFqK3bw5nUsLOsnjTN29Ck2Cm/edit?usp=sharing&ouid=110080855562115636061&rtpof=true&sd=true

---

## Technical Explanation

### Data Loading and Joins

The dataset came as separate CSV files. I loaded orders, reviews, customers, order items, and products, then joined them using `order_id`, `customer_id`, and `product_id`.

### Cleaning

- Removed canceled and unavailable orders
- Removed orders with no delivery date
- Converted date columns to datetime format

### Feature Engineering

- `delay_days` = actual delivery date minus estimated delivery date
- `delivery_status` = "On Time", "Late", or "Super Late"
- `risk_score` = combines late delivery rate and review score

### Dashboard

Built with Streamlit. Reads the cleaned CSV and shows KPIs, charts, and filters by state and product category.

---

## Candidate Choice: State Risk Score

I created a State Risk Score to help find which states need the most attention.

**Formula:**

```
State Risk Score = Late Delivery % × (5 - Average Review Score)
```

A high score means the state has many late deliveries and unhappy customers. This helps prioritize where to improve logistics.

---

## Dataset

**Source:** [Olist Brazilian E-Commerce Dataset](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce) (Kaggle)

| File | Description |
|------|-------------|
| `olist_orders_dataset.csv` | Order and delivery dates |
| `olist_order_reviews_dataset.csv` | Customer review scores |
| `olist_customers_dataset.csv` | Customer location |
| `olist_order_items_dataset.csv` | Products per order |
| `olist_products_dataset.csv` | Product details |
| `product_category_name_translation.csv` | Portuguese to English categories |

Raw CSV files are not in the repo. The dashboard uses `outputs/cleaned_delivery_data.csv`.

---

## Tools

- Python
- Pandas
- NumPy
- Plotly
- Streamlit
- Jupyter Notebook

---

## Dashboard Features

- KPI cards (total orders, late %, avg review, super late %)
- Bar chart: late delivery % by state
- Bar chart: delivery status vs review score
- Scatter plot: delay days vs review score
- Bar chart: top 10 categories by late delivery rate
- Risk score table
- Executive summary with recommendations
