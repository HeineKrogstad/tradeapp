import sqlite3

# Функция для подключения к базе данных
def get_db_connection():
    conn = sqlite3.connect("stocks.db")
    conn.row_factory = sqlite3.Row  # Для доступа к данным по имени столбца
    return conn

# Функция для получения баланса пользователя
def get_user_balance(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT balance FROM accounts WHERE id = ?", (user_id,))
    balance = cursor.fetchone()["balance"]
    conn.close()
    return balance

def save_portfolio_history(user_id, conn):
    conn = conn
    cursor = conn.cursor()

    # Получаем текущий баланс пользователя
    cursor.execute("SELECT balance FROM accounts WHERE id = ?", (user_id,))
    balance_row = cursor.fetchone()
    balance = balance_row["balance"] if balance_row else 0.0  # Если balance_row None, используем 0.0

    query = """
        SELECT SUM(p.quantity * s.last_price)
        FROM portfolio p
        JOIN stocks s ON p.stock_id = s.id
        WHERE p.account_id = ?
    """
    
    cursor.execute(query, (user_id,))
    portfolio_row = cursor.fetchone()
    portfolio_value = portfolio_row[0] if portfolio_row and portfolio_row[0] is not None else 0.0 

    # Общая стоимость портфеля (баланс + стоимость акций)
    total_value = balance + portfolio_value

    # Сохраняем в историю
    cursor.execute("""
        INSERT INTO portfolio_history (account_id, total_value)
        VALUES (?, ?)
    """, (user_id, total_value))

# Функция для получения массива активов пользователя
def get_user_assets(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT stocks.ticker, stocks.name, stocks.last_price, portfolio.quantity, portfolio.avg_price
        FROM portfolio
        JOIN stocks ON portfolio.stock_id = stocks.id
        WHERE portfolio.account_id = ?
    """, (user_id,))
    assets = cursor.fetchall()
    conn.close()
    return assets

# Функция для пополнения счёта
def deposit_funds(user_id, amount):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE accounts SET balance = balance + ? WHERE id = ?", (amount, user_id))
    save_portfolio_history(user_id, conn)
    conn.commit()
    conn.close()

# Функция для вывода средств
def withdraw_funds(user_id, amount):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE accounts SET balance = balance - ? WHERE id = ?", (amount, user_id))
    save_portfolio_history(user_id, conn)
    conn.commit()
    conn.close()

# Функция для получения списка всех акций
def get_all_stocks():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM stocks")
    stocks = cursor.fetchall()
    conn.close()
    return stocks

# Функция для покупки акций
def buy_stock(user_id, stock_id, quantity, price):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # Проверка баланса
        cursor.execute("SELECT balance FROM accounts WHERE id = ?", (user_id,))
        balance = cursor.fetchone()["balance"]
        total_cost = quantity * price
        if balance < total_cost:
            return False, "Недостаточно средств на счёте."

        # Добавление сделки
        cursor.execute("""
            INSERT INTO deals (account_id, stock_id, price, quantity, action_type)
            VALUES (?, ?, ?, ?, 'BUY')
        """, (user_id, stock_id, price, quantity))

        # Обновление портфеля
        cursor.execute("""
            INSERT INTO portfolio (account_id, stock_id, quantity, avg_price)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(account_id, stock_id) DO UPDATE SET
                quantity = quantity + excluded.quantity,
                avg_price = ((portfolio.quantity * portfolio.avg_price) + (excluded.quantity * excluded.avg_price)) / (portfolio.quantity + excluded.quantity)
        """, (user_id, stock_id, quantity, price))

        # Обновление баланса
        cursor.execute("UPDATE accounts SET balance = balance - ? WHERE id = ?", (total_cost, user_id))
        save_portfolio_history(user_id, conn)
        conn.commit()
        return True, "Покупка успешно завершена."
    except Exception as e:
        conn.rollback()
        return False, str(e)
    finally:
        conn.close()

# Функция для продажи акций
def sell_stock(user_id, stock_id, quantity, price):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # Проверка наличия акций
        cursor.execute("SELECT quantity FROM portfolio WHERE account_id = ? AND stock_id = ?", (user_id, stock_id))
        portfolio_quantity = cursor.fetchone()["quantity"]
        if portfolio_quantity < quantity:
            return False, "Недостаточно акций для продажи."

        # Добавление сделки
        cursor.execute("""
            INSERT INTO deals (account_id, stock_id, price, quantity, action_type)
            VALUES (?, ?, ?, ?, 'SELL')
        """, (user_id, stock_id, price, quantity))

        # Обновление портфеля
        cursor.execute("""
            UPDATE portfolio
            SET quantity = quantity - ?
            WHERE account_id = ? AND stock_id = ?
        """, (quantity, user_id, stock_id))

        # Обновление баланса
        total_income = quantity * price
        cursor.execute("UPDATE accounts SET balance = balance + ? WHERE id = ?", (total_income, user_id))
        
        # Сохранение истории стоимости портфеля
        save_portfolio_history(user_id, conn)

        conn.commit()
        return True, "Продажа успешно завершена."
    except Exception as e:
        conn.rollback()
        return False, str(e)
    finally:
        conn.close()

def get_deals_by_ticker(user_id, ticker):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = """
        SELECT d.id, s.ticker, s.name, d.price, d.quantity, d.action_type, d.deal_time
        FROM deals d
        JOIN stocks s ON d.stock_id = s.id
        WHERE d.account_id = ? AND s.ticker = ?
        ORDER BY d.deal_time DESC
    """
    cursor.execute(query, (user_id, ticker))
    deals = cursor.fetchall()
    conn.close()
    return deals

def get_portfolio_by_ticker(user_id, ticker):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = """
        SELECT p.quantity, p.avg_price
        FROM portfolio p
        JOIN stocks s ON p.stock_id = s.id
        WHERE p.account_id = ? AND s.ticker = ?
    """
    cursor.execute(query, (user_id, ticker))
    position = cursor.fetchone()
    conn.close()
    
    if position:
        return {"quantity": position[0], "avg_price": position[1]}
    else:
        return {"quantity": 0, "avg_price": 0.0}

def get_portfolio_value(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = """
        SELECT SUM(p.quantity * s.last_price)
        FROM portfolio p
        JOIN stocks s ON p.stock_id = s.id
        WHERE p.account_id = ?
    """
    
    cursor.execute(query, (user_id,))
    total_value = cursor.fetchone()[0]
    conn.close()
    
    return total_value if total_value else 0.0

def get_portfolio_history(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Получаем историю
    cursor.execute("""
        SELECT recorded_at, total_value
        FROM portfolio_history
        WHERE account_id = ?
        ORDER BY recorded_at
    """, (user_id,))
    history = cursor.fetchall()

    conn.close()
    return history

def get_deals_by_account(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = """
        SELECT d.id, s.ticker, s.name, d.price, d.quantity, d.action_type, d.deal_time
        FROM deals d
        JOIN stocks s ON d.stock_id = s.id
        WHERE d.account_id = ?
        ORDER BY d.deal_time DESC
    """
    cursor.execute(query, (user_id,))
    deals = cursor.fetchall()
    conn.close()
    return deals

def get_user_by_id(user_id):
    conn = get_db_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT * FROM accounts WHERE id = ?", (user_id,))
        row = cursor.fetchone()

        if row:
            return dict(row)
        else:
            return None
    except sqlite3.Error as e:
        print(f"Ошибка при выполнении запроса: {e}")
        return None
    finally:
        conn.close()