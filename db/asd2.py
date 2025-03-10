import sqlite3

def add_new_columns_to_accounts():
    # Подключаемся к базе данных
    conn = sqlite3.connect("stocks.db")
    cursor = conn.cursor()

    try:
        # Добавляем новые столбцы, если они еще не существуют
        cursor.execute("ALTER TABLE accounts ADD COLUMN passport TEXT;")
        cursor.execute("ALTER TABLE accounts ADD COLUMN passport_issue TEXT;")
        cursor.execute("ALTER TABLE accounts ADD COLUMN address TEXT;")
        
        # Сохраняем изменения
        conn.commit()
        print("Новые поля успешно добавлены в таблицу accounts.")
    except sqlite3.OperationalError as e:
        # Если столбцы уже существуют, игнорируем ошибку
        if "duplicate column name" in str(e):
            print("Новые поля уже существуют в таблице accounts.")
        else:
            print(f"Ошибка при добавлении новых полей: {e}")
    finally:
        # Закрываем соединение с базой данных
        conn.close()

# Вызов функции для добавления новых полей
add_new_columns_to_accounts()