import psycopg2
import os
from dotenv import load_dotenv

conn = None
cur = None
load_dotenv()

try:
    conn = psycopg2.connect(
        users = os.getenv('POSTGRES_USER'),
        password = os.getenv('POSTGRES_PASSWORD'),
        host = os.getenv('POSTGRES_HOST'),
        port = os.getenv('POSTGRES_PORT'),
        database = os.getenv('POSTGRES_DB')
    )
    cur = conn.cursor()


    create_table = '''
    CREATE TABLE tasks
        id SERIAL PRIMARY KEY,
        name VARCHAR(100),
        date DATE
    );
    '''

    cur.execute(create_table)
    conn.commit()
    print("Table tasks created successfully")

except Exception as error:
    print("Error table creation", error)

finally:
    cur.close()
    conn.close()
    print("Connection closed")


