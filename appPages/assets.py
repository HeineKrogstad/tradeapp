import streamlit as st
from chart_component import tradingview_widget
import pandas as pd
from db_utils import get_portfolio_by_ticker, buy_stock, sell_stock, get_all_stocks, get_deals_by_ticker

def assets_page():
    st.header("Торговля")
    stocks = get_all_stocks()
    if stocks:
        stock_options = {stock["ticker"]: stock for stock in stocks}
        selected_ticker = st.selectbox("Выберите акцию", list(stock_options.keys()))
        selected_stock = stock_options[selected_ticker]
        tradingview_widget(symbol=selected_ticker)

        st.write(f"**Тикер:** {selected_stock['ticker']}")
        st.write(f"**Название:** {selected_stock['name']}")
        st.write(f"**Последняя цена:** {selected_stock['last_price']:.2f} $")

        quantity = st.number_input("Количество", min_value=1, step=1)

        col1, col2 = st.columns(2)
        with col1:
            if st.button("Купить"):
                success, message = buy_stock(
                    st.session_state.user["id"],
                    selected_stock["id"],
                    quantity,
                    selected_stock["last_price"]
                )
                if success:
                    st.success(message)
                else:
                    st.error(message)
                st.rerun()

        with col2:
            if st.button("Продать"):
                success, message = sell_stock(
                    st.session_state.user["id"],
                    selected_stock["id"],
                    quantity,
                    selected_stock["last_price"]
                )
                if success:
                    st.success(message)
                else:
                    st.error(message)
                st.rerun()
    else:
        st.write("Нет доступных акций для торговли.")
    
    asset_position = get_portfolio_by_ticker(st.session_state.user["id"], selected_stock['ticker'])
    st.subheader(f"Позиция по {selected_stock['ticker']}:")
    st.write(f"Количество: {asset_position['quantity']}")
    st.write(f"Средняя цена: {asset_position['avg_price']:.2f} $")

    st.subheader(f"Сделки по {selected_stock['ticker']}:")
    deals = get_deals_by_ticker(st.session_state.user["id"], selected_stock['ticker'])
    if deals:
        data = []
        for deal in deals:
            total_amount = deal[3] * deal[4]  # Цена * Количество
            data.append({
                "ID сделки": deal[0],
                "Тикер": deal[1],
                "Название": deal[2],
                "Цена ($)": f"{deal[3]:.2f}",
                "Количество": deal[4],
                "Сумма сделки ($)": f"{total_amount:.2f}",
                "Тип сделки": "Покупка" if deal[5] == "BUY" else "Продажа",
                "Время сделки": deal[6]
            })
        df_deals = pd.DataFrame(data)
        st.dataframe(df_deals)
    else:
        st.write("Сделки по этому инструменту не найдены.")