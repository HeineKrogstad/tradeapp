import streamlit as st
from docsGenerators.reg_doc_generator import generate_financial_report
from docsGenerators.depo_doc_generator import generate_broker_report
from db_utils import get_user_by_id, get_user_assets, get_user_balance, get_deals_by_account

def forms_page():
    st.header("Отчёты")
    
    accounts = [
    {"number": "RUB30601810800002151879", "currency": "RUB"},
    {"number": "USD30601840900002151901", "currency": "USD"},
    {"number": "EUR30601978800002151902", "currency": "EUR"}
    ]

    user_data = get_user_by_id(st.session_state.user["id"])

    deposit_accounts = [
        {"type": "Счет депо владельца", "number": "3JRT3", "section": "-"},
        {"type": "Торговый счет депо", "number": "3JRT4", "section": "MEX"},
        {"type": "Торговый счет депо", "number": "3JRT5", "section": "DVP"},
        {"type": "Торговый счет депо", "number": "3JRT6", "section": "BEB"}
    ]

    # Кнопка для генерации отчёта
    if st.button("Создать документ об открытии счета"):
        output_file = "document.pdf"
        generate_financial_report(
            name=user_data["name"],
            address=user_data["address"],
            passport=user_data["passport"],
            passport_issue=user_data["passport_issue"],
            contract_number="2021413493",
            contract_date="11.03.2020",
            accounts=accounts,
            deposit_contract="D021413493",
            deposit_accounts=deposit_accounts,
            output_file=output_file
        )

        # Чистое скачивание PDF
        with open(output_file, "rb") as file:
            pdf_bytes = file.read()  # Считываем в бинарном формате
        
        st.download_button(
            label="Скачать документ",
            data=pdf_bytes,
            file_name="Брокерский_отчет.pdf",
            mime="application/pdf"
        )

    deals = get_deals_by_account(st.session_state.user["id"])
    balance = get_user_balance(st.session_state.user["id"])
    assets = get_user_assets(st.session_state.user["id"])

    if st.button("Создать справку о сделках и активах"):
        output_file2 = "broker_report.pdf"
        generate_broker_report(
            user_name=user_data["name"],
            account_number="2021413493",
            deals=deals,
            assets=assets,
            balance=balance,
            output_file=output_file2
        )                  
        # Чистое скачивание PDF
        with open(output_file2, "rb") as file:
            pdf_bytes = file.read()  # Считываем в бинарном формате
        
        st.download_button(
            label="Скачать документ",
            data=pdf_bytes,
            file_name="Брокерский_отчет.pdf",
            mime="application/pdf"
        )