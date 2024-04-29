import psycopg2
from config import load_config

def delete_data():
    conn = None

    try:
        config = load_config()
        conn = psycopg2.connect(**config)
        cursor = conn.cursor()

        # Пример: Удаление данных для заданного пользователя
        username_to_delete = input("Enter username to delete: ")
        cursor.execute("DELETE FROM PhoneBook WHERE username = %s", (username_to_delete,))
        conn.commit()
        print("Data deleted successfully.")

    except (psycopg2.DatabaseError, Exception) as error:
        print(error)

    finally:
        if conn:
            cursor.close()
            conn.close()
            print("Database connection closed.")

if __name__ == '__main__':
    delete_data()