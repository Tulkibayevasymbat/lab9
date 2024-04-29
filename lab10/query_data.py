import psycopg2
from config import load_config

def query_data():
    conn = None

    try:
        config = load_config()
        conn = psycopg2.connect(**config)
        cursor = conn.cursor()

        # Пример: Запрос данных для заданного пользователя
        username_filter = input("Enter username to filter: ")
        cursor.execute("SELECT * FROM PhoneBook WHERE username = %s", (username_filter,))
        rows = cursor.fetchall()

        # Вывод результатов запроса
        if rows:
            print("Results:")
            for row in rows:
                print("ID:", row[0])
                print("Username:", row[1])
                print("Phone Number:", row[2])
        else:
            print("No results found for the given username.")

    except (psycopg2.DatabaseError, Exception) as error:
        print(error)

    finally:
        if conn:
            cursor.close()
            conn.close()
            print("Database connection closed.")

if __name__ == '__main__':
    query_data()