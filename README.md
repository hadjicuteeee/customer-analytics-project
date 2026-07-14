# Customer Analytics ETL Pipeline

An end-to-end ETL pipeline built with **Python, PostgreSQL, Docker, and SQL**. This project loads customer sales data from CSV files into PostgreSQL, creates analytics views, performs RFM (Recency, Frequency, Monetary) customer segmentation, and prepares data for Power BI dashboards.

---

## Tech Stack

- Python
- Pandas
- PostgreSQL
- SQLAlchemy
- Docker
- Docker Compose
- SQL
- Power BI

---

## Project Structure

```text
customer-analytics-etl/
│
├── data/
│   ├── customer.csv
│   ├── information.csv
│   └── product.csv
│
├── output/
│   └── rfm_analysis.csv
│
├── sql/
│   └── views.sql
│
├── load.py
├── rfm.py
├── main.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env.example
└── README.md
```

---

## ETL Workflow

1. Read CSV files using Pandas.
2. Load data into PostgreSQL.
3. Create analytics schema and SQL views.
4. Perform RFM customer segmentation.
5. Export RFM results.
6. Connect Power BI to analytics views.

---

## SQL Views

The project creates an analytics schema with the following views:

- vw_sales
- vw_category_sales
- vw_customer_ranking
- vw_yearly_revenue
- vw_monthly_revenue
- vw_gender_segmentation
- vw_age_segmentation
- vw_location_revenue
- vw_agent_performance
- vw_product_sales

---

## RFM Analysis

The RFM model calculates:

- Recency
- Frequency
- Monetary

Customer segments include:

- Champion
- Loyal Customer
- Potential Loyalist
- At Risk
- Lost Customer

---

## Docker

Build the project

```bash
docker compose up --build
```

Stop containers

```bash
docker compose down
```
---
## Environment Variables
Create a `.env` file.
```env
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
DB_NAME=analysis
```
---
## Future Improvements
- Star Schema
- GitHub Actions
- Automated Testing
- Incremental ETL
- Airflow Pipeline
- Power BI Dashboard
---
## Author
Jihad Dion Apues
GitHub:
https://github.com/analyst-jihad