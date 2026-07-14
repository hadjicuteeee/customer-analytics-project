import os
import logging
import pandas as pd

from sqlalchemy import create_engine, text
from dotenv import load_dotenv

if os.path.exists(".env"):
    load_dotenv(override=False)

logging.basicConfig(
    filename="data.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


engine = create_engine(
    f"postgresql+psycopg2://"
    f"{os.getenv('DB_USER')}:"
    f"{os.getenv('DB_PASSWORD')}@"
    f"{os.getenv('DB_HOST')}:"
    f"{os.getenv('DB_PORT')}/"
    f"{os.getenv('DB_NAME')}"
)


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
SQL_DIR = os.path.join(BASE_DIR, "sql")

customer_df = pd.read_csv(os.path.join(DATA_DIR, "customer.csv"))
information_df = pd.read_csv(os.path.join(DATA_DIR, "information.csv"))
product_df = pd.read_csv(os.path.join(DATA_DIR, "product.csv"))


def load_db():

    tables = [
        ("customer", customer_df),
        ("information", information_df),
        ("product", product_df)
    ]

    for table_name, dataframe in tables:

        if dataframe.empty:
            logging.error(f"{table_name} is empty.")
            continue

        dataframe.to_sql(
            table_name,
            engine,
            if_exists="replace",
            index=False
        )

        logging.info(f"{table_name} loaded successfully.")


def create_views():

    sql_file = os.path.join(SQL_DIR, "views.sql")

    with open(sql_file, "r", encoding="utf-8") as file:
        sql = file.read()

    statements = [
        stmt.strip()
        for stmt in sql.split(";")
        if stmt.strip()
    ]

    with engine.begin() as connection:

        for statement in statements:
            connection.execute(text(statement))

    logging.info("Analytics views created successfully.")