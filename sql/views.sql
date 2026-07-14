
CREATE SCHEMA IF NOT EXISTS analytics;

CREATE OR REPLACE VIEW analytics.vw_sales AS
SELECT
    i.transaction_id,
    i.date,
    i.sales_agent,
    i.quantity,
    i.total_amount,

    c.customer_id,
    c.name,
    c.email,
    c.gender,
    c.age,
    c.location,

    p.product_id,
    p.product_name,
    p.category,
    p.price

FROM information i
INNER JOIN customer c
    ON i.customer_id = c.customer_id
INNER JOIN product p
    ON i.product_id = p.product_id;


CREATE OR REPLACE VIEW analytics.vw_category_sales AS
SELECT
    category,
    ROUND(SUM(total_amount::DECIMAL),2) AS total_revenue,

    ROW_NUMBER() OVER(
        ORDER BY SUM(total_amount) DESC
    ) AS ranking,

    CONCAT(
        ROUND(
            SUM(total_amount::DECIMAL) * 100 /
            SUM(SUM(total_amount::DECIMAL)) OVER(),
            2
        ),
        '%'
    ) AS percentage
FROM analytics.vw_sales
GROUP BY category;

CREATE OR REPLACE VIEW analytics.vw_customer_ranking AS
SELECT
    name,

    SUM(total_amount::DECIMAL) AS total_spent,
    ROW_NUMBER() OVER(
        ORDER BY SUM(total_amount) DESC
    ) AS ranking
FROM analytics.vw_sales
GROUP BY name;

CREATE OR REPLACE VIEW analytics.vw_yearly_revenue AS
SELECT
    EXTRACT(YEAR FROM date::DATE) AS year,
    ROUND(
        SUM(total_amount::DECIMAL),
        2
    ) AS revenue
FROM analytics.vw_sales
GROUP BY 1
ORDER BY 1;

CREATE OR REPLACE VIEW analytics.vw_monthly_revenue AS
SELECT
    EXTRACT(YEAR FROM date::DATE) AS year,
    EXTRACT(MONTH FROM date::DATE) AS month,
    ROUND(
        SUM(total_amount::DECIMAL),
        2
    ) AS revenue
FROM analytics.vw_sales
GROUP BY 1,2
ORDER BY 1,2;


CREATE OR REPLACE VIEW analytics.vw_gender_segmentation AS
SELECT
    gender,
    COUNT(customer_id) AS total_customers,
    ROUND(
        SUM(total_amount::DECIMAL),
        2
    ) AS revenue,
    ROUND(
        AVG(total_amount::DECIMAL),
        2
    ) AS average_order_value
FROM analytics.vw_sales
GROUP BY gender;

CREATE OR REPLACE VIEW analytics.vw_age_segmentation AS
SELECT
    CASE
        WHEN age BETWEEN 18 AND 24 THEN '18-24'
        WHEN age BETWEEN 25 AND 34 THEN '25-34'
        WHEN age BETWEEN 35 AND 44 THEN '35-44'
        ELSE '45+'
    END AS age_group,

    COUNT(customer_id) AS total_customers,
    ROUND(
        SUM(total_amount::DECIMAL),
        2
    ) AS revenue,
    ROUND(
        AVG(total_amount::DECIMAL),
        2
    ) AS average_order_value
FROM analytics.vw_sales
GROUP BY age_group
ORDER BY age_group;


CREATE OR REPLACE VIEW analytics.vw_agent_performance AS
SELECT
    sales_agent,
    COUNT(transaction_id) AS total_transactions,
    ROUND(
        SUM(total_amount::DECIMAL),
        2
    ) AS total_revenue,
    ROUND(
        AVG(total_amount::DECIMAL),
        2
    ) AS average_transaction_value
FROM analytics.vw_sales
GROUP BY sales_agent
ORDER BY total_revenue DESC;


CREATE OR REPLACE VIEW analytics.vw_location_revenue AS
SELECT
    location,
    ROUND(
        SUM(total_amount::DECIMAL),
        2
    ) AS revenue
FROM analytics.vw_sales
GROUP BY location
ORDER BY revenue DESC;


CREATE OR REPLACE VIEW analytics.vw_product_sales AS
SELECT
    product_name,
    category,
    SUM(quantity) AS total_sold,
    ROUND(
        SUM(total_amount::DECIMAL),
        2
    ) AS revenue
FROM analytics.vw_sales
GROUP BY product_name, category
ORDER BY revenue DESC;