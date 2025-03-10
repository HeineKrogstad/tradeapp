import sqlite3

# Данные для добавления
stocks_data = [
    {"ticker": "AAPL", "name": "Apple Inc.", "last_price": 150.0},
    {"ticker": "GOOGL", "name": "Alphabet Inc.", "last_price": 2800.0},
    {"ticker": "MSFT", "name": "Microsoft Corporation", "last_price": 300.0},
    {"ticker": "AMZN", "name": "Amazon.com Inc.", "last_price": 3400.0},
    {"ticker": "TSLA", "name": "Tesla Inc.", "last_price": 700.0},
    {"ticker": "FB", "name": "Meta Platforms Inc.", "last_price": 350.0},
    {"ticker": "NVDA", "name": "NVIDIA Corporation", "last_price": 800.0},
    {"ticker": "BRK.B", "name": "Berkshire Hathaway Inc.", "last_price": 300.0},
    {"ticker": "JNJ", "name": "Johnson & Johnson", "last_price": 170.0},
    {"ticker": "V", "name": "Visa Inc.", "last_price": 250.0},
    {"ticker": "WMT", "name": "Walmart Inc.", "last_price": 140.0},
    {"ticker": "PG", "name": "Procter & Gamble Co.", "last_price": 150.0},
    {"ticker": "MA", "name": "Mastercard Inc.", "last_price": 380.0},
    {"ticker": "DIS", "name": "The Walt Disney Company", "last_price": 180.0},
    {"ticker": "PYPL", "name": "PayPal Holdings Inc.", "last_price": 250.0},
    {"ticker": "NFLX", "name": "Netflix Inc.", "last_price": 600.0},
    {"ticker": "INTC", "name": "Intel Corporation", "last_price": 50.0},
    {"ticker": "CSCO", "name": "Cisco Systems Inc.", "last_price": 55.0},
    {"ticker": "ADBE", "name": "Adobe Inc.", "last_price": 650.0},
    {"ticker": "CRM", "name": "Salesforce.com Inc.", "last_price": 270.0},
]

# Подключение к базе данных
conn = sqlite3.connect("stocks.db")
cursor = conn.cursor()

# Добавление акций в таблицу stocks
for stock in stocks_data:
    cursor.execute("""
        INSERT INTO stocks (ticker, name, last_price)
        VALUES (?, ?, ?)
    """, (stock["ticker"], stock["name"], stock["last_price"]))

# Сохранение изменений и закрытие соединения
conn.commit()
conn.close()

print("Акции успешно добавлены в базу данных.")