from load import load_db, create_views
from rfm import main as run_rfm

def main():

    load_db()
    create_views()
    run_rfm()
    print("ETL Pipeline Finished Successfully!")


if __name__ == "__main__":
    main()