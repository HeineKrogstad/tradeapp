import sqlite3

DB_PATH = "stocks.db"

# Подключение к базе данных
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Создание таблицы portfolio_history
cursor.execute("""
CREATE TABLE IF NOT EXISTS portfolio_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    account_id INTEGER NOT NULL,
    total_value REAL NOT NULL,
    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (account_id) REFERENCES accounts(id)
)
""")

# Сохранение изменений и закрытие соединения
conn.commit()
conn.close()

print("Таблица portfolio_history создана.")
