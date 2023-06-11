import psycopg2
import os

from dotenv import load_dotenv
from choices import df

load_dotenv()

if __name__ == '__main__':
    conn = psycopg2.connect(
        host="localhost",
        database=os.getenv('DB_NAME'),
        user=os.getenv('DB_USERNAME'),
        password=os.getenv('DB_PASSWORD')
    )
    print("Connected to the database!")

    with conn.cursor() as cur:
        # Run users.sql
        with open('users.sql') as db_file:
            cur.execute(db_file.read())
        # Run drug.sql
        with open('drug.sql') as db_file:
            cur.execute(db_file.read())

        # Import all drugs from the dataset
        all_drug = list(
            map(lambda x: tuple(x), 

                df[['id', 'name', 'brand', 'price', 'city']].to_records(index=False))
        )
        args_str = ','.join(cur.mogrify("(%s, %s, %s, %s, %s)", tuple(str(val) for val in i)).decode('utf-8') for i in all_drug)
        cur.execute("INSERT INTO Drug (id,name,brand,price,city) VALUES " + args_str)

        # Dummy pharmacist 1 sells all drug
        dummy_sales = [(1, i) for i in range(1, len(all_drug) + 1)]
        args_str = ','.join(cur.mogrify("(%s, %s)", i).decode('utf-8') for i in dummy_sales)
        cur.execute("INSERT INTO Sell (pharmacist_pk, drug_pk) VALUES " + args_str)

        conn.commit()

    conn.close()
