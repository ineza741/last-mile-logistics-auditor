# Last Mile Logistics Auditor — Presentation Outline

## Slide 1: Project Title

### Title
**Last Mile Logistics Auditor**
*Delivery Performance & Customer Satisfaction Analysis*

### Bullet Points
- Portfolio project analyzing last-mile delivery performance
- Built with Python, Pandas, Plotly, and Streamlit
- Uses real-world Olist Brazilian E-Commerce dataset

### Speaker Notes
"Good morning/afternoon. My name is [Your Name], and today I'll be presenting my project called Last Mile Logistics Auditor. This is a data engineering and analytics project where I analyzed delivery performance for a fictional logistics company called Veridi Logistics. The goal was to understand whether delivery delays were happening in specific regions and whether those delays were causing negative customer reviews."

---

## Slide 2: Business Problem

### Title
**Business Problem**

### Bullet Points
- Veridi Logistics noticed increasing negative customer reviews
- Complaints focused on late deliveries
- Management needed to know:
  - Are delays happening in specific states?
  - Are late deliveries causing bad reviews?
- Objective: Identify problem regions and quantify impact

### Speaker Notes
"Veridi Logistics, a Brazilian e-commerce logistics company, was seeing an increase in negative customer reviews. The complaints were specifically about late deliveries. Management needed answers to two key questions: First, are these delivery delays happening in specific geographic regions, or is it a nationwide problem? Second, is there actually a correlation between late deliveries and lower customer review scores? My project was designed to answer both questions using data analysis."

---

## Slide 3: Dataset and Data Engineering Pipeline

### Title
**Dataset & Data Engineering Pipeline**

### Bullet Points
- Source: Olist Brazilian E-Commerce (Kaggle)
- 6 relational CSV datasets
- 99,000+ delivered orders analyzed

**Pipeline Steps:**
1. Loaded 6 CSV files
2. Joined tables using order_id, customer_id, product_id
3. Created master analytical dataset
4. Cleaned missing/canceled orders
5. Converted timestamps to datetime
6. Engineered delay_days and delivery_status features
7. Exported cleaned dataset

### Speaker Notes
"I used the Olist Brazilian E-Commerce dataset from Kaggle, which contains real transaction data from a Brazilian e-commerce platform. The dataset consists of 6 related CSV files containing orders, reviews, customers, products, and category translations. My data engineering pipeline started by loading all 6 files, then joining them using foreign keys like order_id and customer_id. After joining, I created a master dataset with one record per order. I then cleaned the data by removing canceled orders and orders without delivery dates. Finally, I engineered new features including delay_days and delivery_status to enable the analysis."

---

## Slide 4: Delay Calculation Logic

### Title
**Delay Calculation Logic**

### Bullet Points
- **delay_days** = Actual Delivery Date − Estimated Delivery Date
  - Positive value = Order arrived LATE
  - Negative value = Order arrived EARLY

- **delivery_status** categorization:
  - delay_days ≤ 0 → **On Time**
  - delay_days 1-5 → **Late**
  - delay_days > 5 → **Super Late**

- **is_late** = Binary flag (1 = Late or Super Late)

### Speaker Notes
"The core of my analysis depends on how I calculated delivery delays. I computed delay_days by subtracting the estimated delivery date from the actual delivery date. A positive value means the order arrived after the promised date, so it was late. A negative value means it arrived early. I then created a delivery_status category to group these into three buckets: On Time for orders delivered on or before the estimated date, Late for orders 1-5 days late, and Super Late for orders more than 5 days late. I also created a binary is_late flag for easier aggregation in the analysis."

---

## Slide 5: Regional Delivery Findings

### Title
**Regional Delivery Findings**

### Bullet Points
- Delivery performance varies significantly by state
- Some states show late delivery rates above 30%
- Other states maintain rates below 15%

**Key Findings:**
- Worst performing states identified
- Best performing states identified
- Clear geographic patterns in delivery issues

### Speaker Notes
"My geographic analysis revealed significant variation in delivery performance across Brazilian states. Some states, particularly in the North and Northeast regions, showed late delivery rates exceeding 30%, while states in the Southeast maintained rates below 15%. This confirms that delivery delays are not uniform across the country — they are concentrated in specific regions. This geographic insight is valuable for management because it means targeted logistics improvements in these problem states could significantly improve overall delivery performance."

---

## Slide 6: Late Delivery vs Customer Reviews

### Title
**Late Delivery Impact on Customer Reviews**

### Bullet Points
- Clear negative correlation between delays and reviews
- On-time deliveries average ~4.0 review score
- Late deliveries drop to ~3.5
- Super Late deliveries drop to ~2.8

**Conclusion:**
- Late deliveries directly reduce customer satisfaction
- Each day of delay correlates with lower review scores

### Speaker Notes
"The second key finding was the direct relationship between delivery delays and customer satisfaction. On-time deliveries received an average review score of approximately 4.0 out of 5. When deliveries were late, the average score dropped to around 3.5. For super late deliveries, the score fell further to approximately 2.8. This clearly demonstrates that late deliveries are causing negative customer reviews. The scatter plot shows a clear downward trend — as delay days increase, review scores decrease. This validates management's concern that delivery performance is impacting customer satisfaction."

---

## Slide 7: State Risk Score Feature

### Title
**State Risk Score — Custom Feature**

### Bullet Points
**Formula:**
```
Risk Score = Late Delivery % × (5 − Average Review Score)
```

**What it measures:**
- Combines operational performance (late %)
- With customer impact (review score)

**Business Value:**
- High Risk Score = Priority for improvement
- Helps allocate resources to problem regions
- Focuses on regions causing biggest customer experience problems

### Speaker Notes
"As my candidate choice feature, I created the State Risk Score. This metric combines two important dimensions: the percentage of late deliveries in a state and the average customer review score. The formula multiplies the late delivery percentage by the difference between a perfect score of 5 and the actual average review. A high risk score means a state has both many late deliveries AND unhappy customers. This helps management prioritize which regions to focus on first — not just where delays are happening, but where those delays are actually hurting the business through negative customer feedback."

---

## Slide 8: Final Recommendation

### Title
**Final Recommendation**

### Bullet Points
**For Veridi Logistics:**
1. Prioritize logistics improvements in high-risk states
2. Investigate root causes in North/Northeast regions
3. Set delivery performance targets by state
4. Monitor review scores alongside delivery metrics

**Technical Achievements:**
- Built end-to-end data pipeline
- Created interactive dashboard
- Developed custom Risk Score metric
- Delivered actionable business insights

### Speaker Notes
"Based on my analysis, I have three key recommendations for Veridi Logistics. First, prioritize logistics improvements in the high-risk states identified by the Risk Score metric. Second, investigate the root causes of delivery delays in the North and Northeast regions — it could be infrastructure, carrier partnerships, or warehouse locations. Third, establish delivery performance targets by state and monitor review scores alongside delivery metrics to track improvement. From a technical perspective, this project demonstrates my ability to build an end-to-end data pipeline, create interactive visualizations, develop custom analytical features, and deliver actionable business insights. Thank you for your attention, and I'm happy to answer any questions."

---

## Presentation Tips

1. **Keep it under 10 minutes** — Practice timing each slide
2. **Show the dashboard** — Have it running during the presentation
3. **Use the notebook** — Reference specific code cells if asked technical questions
4. **Be ready for questions** — Common questions:
   - "How did you handle missing data?"
   - "Why did you choose these specific visualizations?"
   - "How would you productionize this pipeline?"
   - "What would you do differently?"

5. **Demonstrate confidence** — You built this; you know it well
