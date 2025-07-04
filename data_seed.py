import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from faker import Faker
import random
from datetime import datetime, timedelta

DB_URI = "mysql+mysqlconnector://dbuser:dbpassword@localhost/bettertire"

TRANSACTIONS_PER_MONTH_RANGE = (20, 45)
TRANSACTION_PERIOD_MONTHS = 12
LINE_ITEMS_PER_TRANSACTION_RANGE = (1, 12)


def get_existing_data(engine):
    """Fetches existing IDs and data from core tables to ensure relational integrity."""
    try:
        with engine.connect() as connection:
            customers = pd.read_sql(
                "SELECT CustomerID FROM Customers", connection)
            users = pd.read_sql("SELECT UserID FROM Users", connection)
            products = pd.read_sql(
                "SELECT ProductID, UnitPrice FROM Products", connection)

            print(
                "Successfully fetched existing data from Customers, Users, and Products tables.")
            return {
                "customer_ids": customers['CustomerID'].tolist(),
                "user_ids": users['UserID'].tolist(),
                "products": products.to_dict('records')
            }
    except SQLAlchemyError as e:
        print(f"Error fetching existing data: {e}")
        return None


def generate_and_insert_data(engine, existing_data):
    """Generates and inserts a year's worth of transaction data."""
    if not all(existing_data.values()) or not all(len(v) > 0 for v in existing_data.values()):
        print("Cannot generate data. Missing essential IDs from database. Ensure Customers, Users, and Products are populated.")
        return

    fake = Faker()
    transactions_to_insert = []
    details_to_insert = []

    used_ref_numbers = set()

    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)

    current_date = start_date
    while current_date < end_date:
        num_transactions = random.randint(*TRANSACTIONS_PER_MONTH_RANGE)

        for _ in range(num_transactions):
            transaction_datetime = fake.date_time_between(
                start_date=current_date, end_date=current_date + timedelta(days=30))
            if transaction_datetime > end_date:
                continue

            while True:
                ref_num = f"INV-{random.randint(20240000, 20259999)}"
                if ref_num not in used_ref_numbers:
                    used_ref_numbers.add(ref_num)
                    break

            transaction = {
                "TransactionDateTime": transaction_datetime,
                "TransactionType": 'INVC',
                "ReferenceNumber": ref_num,
                "CustomerID": random.choice(existing_data['customer_ids']),
                "ReceivingPONumber": f"PO-{random.randint(10000, 50000)}",
                "CreatedByUserID": random.choice(existing_data['user_ids']),
                "CreatedDateTime": transaction_datetime - timedelta(minutes=random.randint(5, 60)),
                "LastChangedByUserID": random.choice(existing_data['user_ids']),
                "LastChangedDateTime": transaction_datetime,
            }
            transactions_to_insert.append(transaction)

        current_date += timedelta(days=30)

    print(f"Generated {len(transactions_to_insert)} transactions.")

    if not transactions_to_insert:
        print("No transactions were generated.")
        return

    try:
        with engine.connect() as connection:
            with connection.begin():
                max_id_before_insert_result = connection.execute(
                    text("SELECT MAX(TransactionID) FROM Transactions"))
                max_id_before_insert = max_id_before_insert_result.scalar_one_or_none() or 0

                trans_df = pd.DataFrame(transactions_to_insert)
                trans_df.to_sql('Transactions', con=connection,
                                if_exists='append', index=False)

                new_ids_query = text(
                    "SELECT TransactionID FROM Transactions WHERE TransactionID > :max_id")
                new_transactions_result = connection.execute(
                    new_ids_query, {"max_id": max_id_before_insert})
                new_transaction_ids = [row[0]
                                       for row in new_transactions_result]

                print(
                    f"Successfully inserted transactions. Found {len(new_transaction_ids)} new transaction IDs.")

                for trans_id in new_transaction_ids:
                    num_line_items = random.randint(
                        *LINE_ITEMS_PER_TRANSACTION_RANGE)
                    for _ in range(num_line_items):
                        product = random.choice(existing_data['products'])
                        quantity = random.choice([2, 4, 6, 8, 12])

                        price = float(product['UnitPrice']) * \
                            random.uniform(0.98, 1.05)
                        cost = price * random.uniform(0.80, 0.90)

                        detail = {
                            "TransactionID": trans_id,
                            "ProductID": product['ProductID'],
                            "Quantity": quantity,
                            "Price": round(price, 2),
                            "Cost": round(cost, 2)
                        }
                        details_to_insert.append(detail)

                if details_to_insert:
                    details_df = pd.DataFrame(details_to_insert)
                    details_df.to_sql(
                        'Transaction_Details', con=connection, if_exists='append', index=False)
                    print(
                        f"Successfully inserted {len(details_to_insert)} transaction detail line items.")

    except SQLAlchemyError as e:
        print(f"Database error during insertion: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    try:
        engine = create_engine(DB_URI)
        print("Database engine created successfully.")

        existing_data = get_existing_data(engine)

        if existing_data:
            generate_and_insert_data(engine, existing_data)
            print("\nData seeding process completed.")

    except Exception as e:
        print(f"Failed to initialize database engine: {e}")
