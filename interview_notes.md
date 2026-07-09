# Last Mile Logistics Auditor — Interview Notes

Simple explanations for common data engineering interview questions.

---

## 1. Why did you choose Pandas?

**Answer:**
Pandas is the standard Python library for data manipulation. I chose it because:
- It handles tabular data (like CSV files) very efficiently
- It has built-in functions for merging, grouping, and filtering data
- It works well with other libraries like Plotly for visualization
- It's the most common tool used in data engineering roles

**Simple explanation:**
"Pandas is like Excel for Python — but much faster and can handle millions of rows. It was the right tool for joining multiple CSV files and performing calculations."

---

## 2. How did you join the datasets?

**Answer:**
I used `pd.merge()` to join tables step by step:

```python
# Step 1: orders + reviews (on order_id)
master_df = pd.merge(orders, reviews, on='order_id', how='left')

# Step 2: + customers (on customer_id)
master_df = pd.merge(master_df, customers, on='customer_id', how='left')

# Step 3: + order_items (on order_id)
master_df = pd.merge(master_df, order_items, on='order_id', how='left')

# Step 4: + products (on product_id)
master_df = pd.merge(master_df, products, on='product_id', how='left')

# Step 5: + translations (on product_category_name)
master_df = pd.merge(master_df, translations, on='product_category_name', how='left')
```

**Why left join?**
Left join keeps all records from the main table (orders) even if there's no match in the other table. This ensures we don't lose any orders.

**Simple explanation:**
"I joined tables one by one using their common columns, like connecting pieces of a puzzle. Each join added more information to our main orders table."

---

## 3. How did you prevent duplicate records?

**Answer:**
After joining, one order could appear multiple times because an order can have multiple items. To fix this:

```python
master_df = master_df.drop_duplicates(subset='order_id', keep='first')
```

This keeps only one record per order_id, which is correct for delivery analysis because delivery happens at the order level, not the item level.

**Simple explanation:**
"An order with 3 items would appear 3 times after joining. Since we're analyzing delivery (which happens once per order), I kept only the first record for each order."

---

## 4. How did you handle missing values?

**Answer:**
I handled missing values in different ways depending on the column:

1. **Orders without delivery date:** Removed these rows because we can't calculate delay without a delivery date:
   ```python
   master_df = master_df.dropna(subset=['order_delivered_customer_date'])
   ```

2. **Canceled/unavailable orders:** Removed because they were never delivered:
   ```python
   master_df = master_df[~master_df['order_status'].isin(['canceled', 'unavailable'])]
   ```

3. **Missing product categories:** These stayed as NaN and didn't affect the analysis since we focused on delivery metrics.

**Simple explanation:**
"I removed orders that couldn't be analyzed — like canceled orders or orders without a delivery date — because they would give incorrect results."

---

## 5. How does the delay calculation work?

**Answer:**
The delay is calculated by subtracting the estimated delivery date from the actual delivery date:

```python
master_df['delay_days'] = (
    master_df['order_delivered_customer_date'] - 
    master_df['order_estimated_delivery_date']
).dt.days
```

- **Positive value:** Order arrived AFTER the estimated date (late)
- **Negative value:** Order arrived BEFORE the estimated date (early)
- **Zero:** Order arrived exactly on time

**Simple explanation:**
"I subtracted the promised delivery date from the actual delivery date. If the result is positive, the order was late. If negative, it was early."

---

## 6. Why did you create the delivery_status column?

**Answer:**
The delivery_status column categorizes delay_days into three meaningful groups:

```python
def categorize_delivery(delay):
    if delay <= 0:
        return 'On Time'
    elif delay <= 5:
        return 'Late'
    else:
        return 'Super Late'

master_df['delivery_status'] = master_df['delay_days'].apply(categorize_delivery)
```

**Why this helps:**
- Makes it easier to group and aggregate data
- Creates clear categories for visualization
- Helps calculate percentages (e.g., "30% of orders were Super Late")
- More intuitive for business stakeholders than raw numbers

**Simple explanation:**
"Instead of showing '3 days late' or '7 days late', I grouped them into 'Late' and 'Super Late' categories. This makes the analysis easier to understand and visualize."

---

## 7. How does the dashboard connect to the cleaned data?

**Answer:**
The dashboard reads the cleaned CSV file that was exported from the notebook:

```python
# In dashboard/app.py
@st.cache_data
def load_data():
    df = pd.read_csv('../outputs/cleaned_delivery_data.csv')
    return df
```

**The flow is:**
1. Notebook reads raw CSVs from `data/`
2. Notebook processes and cleans the data
3. Notebook exports cleaned data to `outputs/cleaned_delivery_data.csv`
4. Dashboard reads from `outputs/cleaned_delivery_data.csv`

**Why this approach:**
- Separates data processing from visualization
- Dashboard loads faster (pre-processed data)
- Can update dashboard without re-running full pipeline

**Simple explanation:**
"The notebook does the heavy lifting of cleaning the data and saves it to a CSV. The dashboard simply reads that cleaned CSV and displays it with charts and filters."

---

## 8. What is your business recommendation?

**Answer:**
Based on my analysis, I recommend:

1. **Prioritize high-risk states:** Use the State Risk Score to identify regions where delivery problems are most damaging to customer satisfaction.

2. **Investigate root causes:** For states with high late delivery rates, investigate whether the issue is:
   - Warehouse locations
   - Carrier partnerships
   - Infrastructure problems
   - Route optimization

3. **Set performance targets:** Establish delivery performance targets by state and track progress over time.

4. **Monitor continuously:** Set up regular monitoring of delivery metrics alongside customer review scores.

**Simple explanation:**
"I recommend the company focus on the worst-performing states first, figure out why deliveries are late there, and set targets to improve. The Risk Score helps them prioritize where to start."

---

## Common Follow-up Questions

### "How would you productionize this pipeline?"

**Answer:**
- Schedule the notebook to run daily/weekly using Airflow or Prefect
- Store data in a database (PostgreSQL, BigQuery) instead of CSV files
- Add data quality checks before exporting
- Deploy dashboard to cloud (Streamlit Cloud, AWS, GCP)

### "What would you do differently?"

**Answer:**
- Use SQL for joins instead of Pandas for better performance with larger datasets
- Add more detailed time analysis (day of week, hour of day effects)
- Include external factors like weather data
- Build automated alerts for states that exceed late delivery thresholds

### "How did you ensure data quality?"

**Answer:**
- Checked for missing values before processing
- Verified row counts after each join
- Validated that join keys matched correctly
- Tested the final dataset against expected results

---

## Key Metrics to Remember

| Metric | Value |
|--------|-------|
| Total orders analyzed | ~99,000 |
| Late delivery rate | ~18% |
| Super Late rate | ~6% |
| On-time review score | ~4.0 |
| Late review score | ~3.5 |

---

## Tips for the Interview

1. **Speak confidently** — You built this project; you know it well
2. **Use the dashboard** — Show it running during the interview
3. **Reference the notebook** — Point to specific code cells if asked
4. **Keep answers concise** — Use the simple explanations above
5. **Be honest** — If you don't know something, say so and explain how you'd find out
