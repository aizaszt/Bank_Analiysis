import os
import psycopg2
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), "../../.env")
load_dotenv(dotenv_path=dotenv_path, encoding="utf-8")


def get_db_connection():

    try:
        connection = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
        )
        print("Успешно: Подключение к СУБД установлено.")
        return connection
    except Exception as e:
        print(f"Ошибка: Не удалось подключиться к СУБД. \nДетали: {e}")
        return None


if __name__ == "__main__":
    conn = get_db_connection()

    if conn:
        conn.close()


        