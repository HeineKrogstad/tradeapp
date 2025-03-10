import streamlit as st
from auth import auth_page
from main import main_page
from price_updater import start_price_update_thread

start_price_update_thread()

# Инициализация состояния сессии
if "user" not in st.session_state:
    st.session_state.user = None
if "page" not in st.session_state:
    st.session_state.page = "auth"

# Логика переключения страниц
if st.session_state.user:
    main_page()
else:
    auth_page()