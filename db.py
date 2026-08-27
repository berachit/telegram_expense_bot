import os 
import psycopg2
from dotenv import load_dotenv

load_dotenv()

DB_HOST=os.getenv("DB_HOST")
DB_PORT=os.getenv("DB_PORT")
DB_NAME=os.getenv("DB_NAME")
DB_USER=os.getenv("DB_USER")
DB_PASSWORD=os.getenv("DB_PASSWORD")

def get_connection():
    connection = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )

    return connection

def add_user(telegram_id, username):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO users (telegram_id, username)
        VALUES(%s,%s)
        ON CONFLICT (telegram_id) DO NOTHING
        """,
        (telegram_id, username)
    )

    connection.commit()

    cursor.close()
    connection.close()


if __name__ == "__main__":
    connection = get_connection()

    print("Database connected successfully")

    connection.close()