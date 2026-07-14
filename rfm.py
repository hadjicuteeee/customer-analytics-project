import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

engine = create_engine(
    f"postgresql+psycopg2://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@"
    f"{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)


def get_data():

    query = """
        SELECT
            c.customer_id,
            c.name,
            i.transaction_id,
            i.date,
            p.price
        FROM customer c
        INNER JOIN information i
            ON c.customer_id = i.customer_id
        INNER JOIN product p
            ON i.product_id = p.product_id
    """

    df = pd.read_sql(query, engine)

    return df


def rfm():

    df = get_data()

    df["date"] = pd.to_datetime(df["date"])
    df["price"] = df["price"].astype(float)

    # date, transactionid, price
    snap_date = df["date"].max() + pd.Timedelta(days=1)

    rfm = df.groupby(["customer_id", "name"]).agg({
        "date": lambda x: (snap_date - x.max()).days,
        "transaction_id": "count",
        "price": "sum"
    })

    rfm.columns = ["Recency", "Frequency", "Monetary"]

    return rfm


def scoring(rfm):

    rfm['R_Score'] = pd.qcut(rfm['Recency'], 5, labels=[5,4,3,2,1])
    rfm['F_Score'] = pd.qcut(rfm['Frequency'].rank(method='first'), 5, labels=[1,2,3,4,5])
    rfm['M_Score'] = pd.qcut(rfm['Monetary'], 5, labels=[1,2,3,4,5])


    rfm["R_Score"] = rfm["R_Score"].astype(int)
    rfm["F_Score"] = rfm["F_Score"].astype(int)
    rfm["M_Score"] = rfm["M_Score"].astype(int)

    rfm["RFM_SCORE"] = (
        rfm["R_Score"].astype(str) +
        rfm["F_Score"].astype(str) +
        rfm["M_Score"].astype(str)
    )

    return rfm

def segment_customer(rfm):

    def segment(customer):

        r = customer["R_Score"]
        f = customer["F_Score"]
        m = customer["M_Score"]

        if r >= 4 and f >= 4 and m >= 4:
            return "Champion"

        elif r >= 3 and f >= 3:
            return "Loyal Customer"

        elif r >= 4 and f <= 2:
            return "Potential Loyalist"

        elif r <= 2 and f >= 3:
            return "At Risk"

        elif r <= 2 and f <= 2:
            return "Lost Customer"

        else:
            return "Regular"

    rfm["Segment"] = rfm.apply(segment, axis=1)

    return rfm


def main():

    rfm_table = rfm()
    rfm_table = scoring(rfm_table)
    rfm_table = segment_customer(rfm_table)
    print(rfm_table)

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    OUTPUT_DIR = os.path.join(BASE_DIR, "output")

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    rfm_table.reset_index().to_csv(
        os.path.join(OUTPUT_DIR, "rfm_analysis.csv"),
        index=False
    )

if __name__ == "__main__":
    main()