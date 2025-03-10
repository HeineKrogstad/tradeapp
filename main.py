import streamlit as st
from appPages.assets import assets_page
from appPages.analytics import analytics_page
from appPages.forms import forms_page
from db_utils import get_user_balance, deposit_funds, withdraw_funds


# Функция для отображения главной страницы
def main_page():
    st.title("Брокерский счёт")

    # Вкладки
    tab1, tab2, tab3, tab4 = st.tabs(["Обзор", "Активы", "Аналитика", "Отчёты"])

    with tab1:
        st.header("Обзор")
        # Получение баланса пользователя
        balance = get_user_balance(st.session_state.user["id"])
        st.write(f"Баланс: **{balance:.2f} $**")

        st.markdown("---")
        st.header("Действия")

        # Пополнение счёта
        deposit_amount = st.number_input("Сумма для пополнения", min_value=0.01, step=0.01, format="%.2f")
        if st.button("Пополнить счёт"):
            deposit_funds(st.session_state.user["id"], deposit_amount)
            st.success(f"Счёт успешно пополнен на {deposit_amount:.2f} $")
            st.rerun()

        # Вывод средств
        withdraw_amount = st.number_input("Сумма для вывода", min_value=0.01, step=0.01, format="%.2f")
        if st.button("Вывести средства"):
            if withdraw_amount > balance:
                st.error("Недостаточно средств на счёте.")
            else:
                withdraw_funds(st.session_state.user["id"], withdraw_amount)
                st.success(f"Средства успешно выведены: {withdraw_amount:.2f} ₽")
                st.rerun()

    with tab2:
        assets_page()

    with tab3:
        analytics_page()

    with tab4:
        forms_page()

    # Кнопка для выхода
    if st.button("Выйти"):
        st.session_state.user = None
        st.session_state.page = "auth"
        st.rerun()