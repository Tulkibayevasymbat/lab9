import psycopg2
from config import load_config

def create_table():
    """ Create PhoneBook table in PostgreSQL """
    conn = None

    try:
        config = load_config()  # Загружаем конфигурацию подключения из файла
        conn = psycopg2.connect(**config)  # Подключаемся к базе данных
        cursor = conn.cursor()

        # Создаем таблицу PhoneBook
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS PhoneBook (
                id SERIAL PRIMARY KEY,
                username TEXT NOT NULL,
                phone_number TEXT NOT NULL
            )
            """)
        conn.commit()
        print("Table 'PhoneBook' created successfully.")

    except (psycopg2.DatabaseError, Exception) as error:
        print(error)

    finally:
        if conn:
            cursor.close()
            conn.close()
            print("Database connection closed.")

if __name__ == '__main__':
    create_table()  # Вызываем функцию create_table() при запуске скрипта