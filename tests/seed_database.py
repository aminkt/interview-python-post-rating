import os

import psycopg2
import random
from datetime import datetime

# Database connection parameters
db_params = {
    'dbname': os.environ['POSTGRES_DB'],
    'user': os.environ['POSTGRES_USER'],
    'password': os.environ['POSTGRES_PASSWORD'],
    'host': 'db',
    'port': '5432'
}

# Connect to the PostgreSQL database
conn = psycopg2.connect(**db_params)
cursor = conn.cursor()

# Function to generate random data for the rate table
def generate_rate_data():
    is_applied = False
    old_score = random.choice([None, random.randint(0, 5)])
    score = random.randint(0, 5)
    created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f') + ' +00:00'
    post_id = random.randint(1, 3)  # Assuming you have 10 posts for example
    user_id = random.randint(1, 1)  # Assuming you have 100 users for example
    return (old_score, score, is_applied, created_at, post_id, user_id)

# Insert 400 rows into the rate table
insert_query = """
INSERT INTO rates (old_score, score, is_applied, created_at, post_id, user_id)
VALUES (%s, %s, %s, %s, %s, %s)
"""

# Disable foreign key checks
cursor.execute("ALTER TABLE rates DISABLE TRIGGER ALL;")
for _ in range(400):
    try:
        rate_data = generate_rate_data()
        cursor.execute(insert_query, rate_data)
        conn.commit()
    except Exception as e:
        # Ignore duplicate
        print(f"duplicate:{e}")


# Commit the transaction and close the connection
cursor.close()
conn.close()

print("Inserted 400 rows into the rate table.")
