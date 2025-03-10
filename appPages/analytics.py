import streamlit as st
import plotly.express as px
import pandas as pd

from db_utils import get_user_assets, get_portfolio_value, get_portfolio_history

def analytics_page():
    st.header("Аналитика")
    st.subheader(f"Суммарная стоимость портфеля: {get_portfolio_value(st.session_state.user['id']):.2f} $")

    # Получение активов пользователя
    assets = get_user_assets(st.session_state.user["id"])
    
    if assets:
        # Подготовка данных для диаграммы
        labels = [asset["ticker"] for asset in assets]  # Тикеры акций
        values = [asset["quantity"] * asset["last_price"] for asset in assets]  # Общая стоимость акций

        # Создание круговой диаграммы
        fig = px.pie(
            names=labels,
            values=values,
            title="Распределение активов",
            labels={"names": "Акции", "values": "Стоимость"},
        )

        # Отображение диаграммы
        st.plotly_chart(fig)

        if assets:
            data = []
            for asset in assets:
                if asset['quantity'] > 0:  # Исключаем активы с quantity = 0
                    total_value = asset['quantity'] * asset['last_price']
                    total_current_value = asset["last_price"] * asset["quantity"]
                    profit = total_current_value - total_value  # Прибыль
                    data.append({
                        "Тикер": asset['ticker'],
                        "Название": asset['name'],
                        "Количество": asset['quantity'],
                        "Текущая цена ($)": f"{asset['last_price']:.2f}",
                        "Средняя цена ($)": f"{asset['avg_price']:.2f}",
                        "Стоимость покупки ($)": f"{total_value:.2f}",
                        "Текущая стоимость": f"{total_current_value:.2f}",
                        "Прибыль ($)": f"{profit:.2f}"
                    })
            df = pd.DataFrame(data)
            st.dataframe(df)
        else:
            st.write("У вас пока нет активов.")

        # График истории стоимости портфеля
        portfolio_history = get_portfolio_history(st.session_state.user["id"])
        if portfolio_history:
            # Преобразуем данные в DataFrame
            df = pd.DataFrame(portfolio_history, columns=["recorded_at", "total_value"])
            df["recorded_at"] = pd.to_datetime(df["recorded_at"])

            # Строим график
            fig_line = px.line(
                df,
                x="recorded_at",
                y="total_value",
                title="История стоимости портфеля",
                labels={"recorded_at": "Дата", "total_value": "Стоимость портфеля ($)"},
            )
            st.plotly_chart(fig_line)
        else:
            st.write("Нет данных для построения графика истории стоимости портфеля.")


