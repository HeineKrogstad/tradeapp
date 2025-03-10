import streamlit as st
import sqlite3

# Функция для подключения к базе данных
def get_db_connection():
    conn = sqlite3.connect("stocks.db")
    conn.row_factory = sqlite3.Row  # Для доступа к данным по имени столбца
    return conn

# Функция для регистрации нового пользователя
def register_user(login, password, name, surname, passport, passport_issue, address):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO accounts (login, password, name, surname, passport, passport_issue, address)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (login, password, name, surname, passport, passport_issue, address))
        conn.commit()
        st.success("Регистрация прошла успешно! Теперь вы можете войти.")
    except sqlite3.IntegrityError:
        st.error("Пользователь с таким логином уже существует.")
    finally:
        conn.close()

# Функция для авторизации пользователя
def login_user(login, password):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM accounts WHERE login = ? AND password = ?", (login, password))
    user = cursor.fetchone()
    conn.close()
    return user

# Страница авторизации/регистрации
def auth_page():
    st.title("Авторизация/Регистрация")

    # Переключение между авторизацией и регистрацией
    tab1, tab2 = st.tabs(["Вход", "Регистрация"])

    with tab1:
        st.header("Вход")
        login = st.text_input("Логин", key="login")
        password = st.text_input("Пароль", type="password", key="password")
        if st.button("Войти"):
            user = login_user(login, password)
            if user:
                st.session_state.user = user
                st.success("Авторизация прошла успешно!")
                st.session_state.page = "main"  # Переход на главную страницу
                st.rerun()  # Перезагрузить страницу
            else:
                st.error("Неверный логин или пароль.")

    with tab2:
        st.header("Регистрация")
        new_login = st.text_input("Логин", key="new_login")
        new_password = st.text_input("Пароль", type="password", key="new_password")
        new_name = st.text_input("Имя", key="new_name")
        new_surname = st.text_input("Фамилия", key="new_surname")
        new_passport = st.text_input("Серия и номер паспорта", key="new_passport")
        new_passport_issue = st.text_input("Адрес выдачи паспорта", key="new_passport_issue")
        new_address = st.text_input("Адрес регистрации", key="new_address")
        if st.button("Зарегистрироваться"):
            if new_login and new_password and new_name and new_surname and new_passport and new_passport_issue and new_address:
                register_user(new_login, new_password, new_name, new_surname, new_passport, new_passport_issue, new_address)
            else:
                st.error("Заполните все поля.")