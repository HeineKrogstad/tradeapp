import streamlit as st

def tradingview_widget(symbol="AAPL", interval="D", theme="dark", height=610):
    """
    Функция для отображения виджета TradingView.

    Параметры:
    - interval: Интервал графика (например, "D" для дневного).
    - theme: Тема графика ("light" или "dark").
    - height: Высота виджета.
    """
    tradingview_html = f"""
    <!-- TradingView Widget BEGIN -->
    <div class="tradingview-widget-container">
      <div id="tradingview_chart"></div>
      <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
      <script type="text/javascript">
        new TradingView.widget({{
          "width": "100%",
          "height": {height},
          "symbol": "{symbol}",
          "interval": "{interval}",
          "timezone": "Etc/UTC",
          "theme": "{theme}",
          "style": "1",
          "locale": "ru",
          "toolbar_bg": "#f1f3f6",
          "enable_publishing": false,
          "allow_symbol_change": true,
          "container_id": "tradingview_chart"
        }});
      </script>
    </div>
    <!-- TradingView Widget END -->
    """
    st.components.v1.html(tradingview_html, height=height)