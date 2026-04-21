import os
import psycopg2
from dotenv import load_dotenv
from groq import Groq

load_dotenv(r"c:/Users/NoutSpace/VS Code/Spring2026/bank_analysis/.env")

api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise ValueError("❌ GROQ_API_KEY не найден!")

print(f"✅ Ключ загружен: {api_key[:10]}...")

client = Groq(api_key=api_key)


def get_db_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )


def get_tables():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT table_name FROM information_schema.tables
        WHERE table_schema = 'raw'
    """)
    tables = [row[0] for row in cursor.fetchall()]
    conn.close()
    return tables


def fetch_table_data(table_name: str, limit: int = 50) -> str:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM raw.{table_name} LIMIT %s", (limit,))
    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    conn.close()
    if not rows:
        return f"Таблица '{table_name}' пуста."
    result = f"Таблица: {table_name}\nКолонки: {', '.join(columns)}\n\nДанные:\n"
    for row in rows:
        result += str(row) + "\n"
    return result


def get_all_data() -> str:
    tables = get_tables()
    if not tables:
        return "Таблицы не найдены."
    all_data = ""
    for table in tables:
        all_data += fetch_table_data(table) + "\n\n"
    return all_data


def chat():
    print("🤖 Подключаюсь к базе данных...")
    try:
        tables = get_tables()
        print(f"✅ Подключено! Найдены таблицы: {', '.join(tables)}")
    except Exception as e:
        print(f"❌ Ошибка подключения к БД: {e}")
        return

    print("\nЗадавай вопросы по своим данным. Введи 'выход' для завершения.\n")

    while True:
        user_input = input("Ты: ").strip()
        if user_input.lower() in ["выход", "exit", "quit"]:
            print("До свидания!")
            break
        if not user_input:
            continue

        print("⏳ Думаю...")
        try:
            db_data = get_all_data()
        except Exception as e:
            print(f"❌ Ошибка БД: {e}")
            continue

        prompt = f"""
Ты — умный ассистент. Отвечай ТОЛЬКО на основе данных ниже.
Если ответа нет в данных — скажи честно.
Отвечай на том же языке, на котором задан вопрос.

=== ДАННЫЕ ИЗ БАЗЫ ===
{db_data}
======================

Вопрос: {user_input}
"""
        try:
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=1000
            )
            print(f"\n🤖 Бот: {response.choices[0].message.content}\n")
        except Exception as e:
            print(f"❌ Ошибка Groq: {e}\n")


if __name__ == "__main__":
    chat()