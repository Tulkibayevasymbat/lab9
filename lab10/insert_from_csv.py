import csv
import psycopg2
from config import load_config

def insert_from_csv():
    conn = None

    try:
        config = load_config()
        conn = psycopg2.connect(**config)
        cursor = conn.cursor()

        with open('phonebook.csv', 'r') as file:
            reader = csv.reader(file)
            next(reader)  # Пропускаем заголовок
            for row in reader:
                if len(row) != 2:
                    print("Ошибка: неверный формат строки в CSV файле:", row)
                    continue
                username, phone_number = row
                cursor.execute("INSERT INTO PhoneBook (username, phone_number) VALUES (%s, %s)", (username, phone_number))
                print(f"Добавлен пользователь: {username}, номер телефона: {phone_number}")

        conn.commit()
        print("Данные успешно добавлены из CSV файла.")

    except (psycopg2.DatabaseError, Exception) as error:
        print("Ошибка при вставке данных из CSV файла:", error)

    finally:
        if conn:
            cursor.close()
            conn.close()
            print("Соединение с базой данных закрыто.")

if __name__ == '__main__':
    insert_from_csv()