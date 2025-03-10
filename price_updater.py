import sqlite3
import time
import yfinance as yf
import threading
from datetime import datetime

DB_PATH = "stocks.db"

def get_stock_price(ticker):
    """Получает текущую цену акции через yfinance, с обработкой ошибок и задержкой."""
    attempts = 3  # Количество попыток перед тем, как сдаться
    for attempt in range(attempts):
        try:
            stock = yf.Ticker(ticker)
            price = stock.fast_info["last_price"]
            if price:
                return round(price, 2)
            else:
                print(f"⚠️ Нет данных по цене для {ticker}")
                return None
        except Exception as e:
            print(f"❌ Ошибка при получении данных для {ticker}: {e}")
            if "Too Many Requests" in str(e):
                wait_time = (attempt + 1) * 5  # Увеличиваем задержку при повторных попытках
                print(f"🔄 Повтор запроса через {wait_time} секунд...")
                time.sleep(wait_time)
            else:
                return None  # Если ошибка не связана с лимитами, выходим

def update_prices_in_db():
    """Обновляет цены акций в базе данных SQLite с задержкой между запросами."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT id, ticker FROM stocks")
    stocks = cursor.fetchall()

    for stock_id, ticker in stocks:
        new_price = get_stock_price(ticker)
        if new_price is not None:
            cursor.execute("""
                UPDATE stocks 
                SET last_price = ?, updated_at = ? 
                WHERE id = ?
            """, (new_price, datetime.now(), stock_id))
            conn.commit()
        
        time.sleep(2)  # Задержка между запросами для избежания блокировки

    conn.close()

def update_stock_prices():
    """Фоновый процесс обновления курсов акций каждые 10 секунд."""
    while True:
        update_prices_in_db()
        time.sleep(10)  # Увеличиваем интервал между полными обновлениями

def start_price_update_thread():
    """Запускает поток обновления курсов."""
    thread = threading.Thread(target=update_stock_prices, daemon=True)
    thread.start()