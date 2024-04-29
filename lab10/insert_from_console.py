import psycopg2
from config import load_config

def insert_from_console():
    conn = None

    try:
        config = load_config()
        conn = psycopg2.connect(**config)
        cursor = conn.cursor()

        username = input("Enter username: ")
        phone_number = input("Enter phone number: ")

        cursor.execute("INSERT INTO PhoneBook (username, phone_number) VALUES (%s, %s)", (username, phone_number))
        conn.commit()
        print("Data inserted from console successfully.")

    except (psycopg2.DatabaseError, Exception) as error:
        print(error)

    finally:
        if conn:
            cursor.close()
            conn.close()
            print("Database connection closed.")

if __name__ == '__main__':
    insert_from_console()