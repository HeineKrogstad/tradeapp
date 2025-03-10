import os
from datetime import datetime
from fpdf import FPDF

# Получаем путь к шрифту в папке проекта
FONT_PATH = os.path.join(os.path.dirname(__file__), "fonts", "DejaVuSans.ttf")

def generate_financial_report(name, address, passport, passport_issue, contract_number,
                              contract_date, accounts, deposit_contract, deposit_accounts, output_file):
    report_date = datetime.now().strftime("%d.%m.%Y")

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Подключаем локальный шрифт
    pdf.add_font("DejaVu", "", FONT_PATH, uni=True)
    pdf.set_font("DejaVu", size=12)

    pdf.cell(200, 10, "АО «Трейдинг Системс»", ln=True, align='C')
    pdf.cell(200, 10, "Хуторская 2-я, 38а, стр. 26, Москва, 127287, Россия", ln=True, align='C')
    pdf.cell(200, 10, "tradingsystems.ru", ln=True, align='C')
    pdf.ln(10)

    pdf.cell(200, 10, f"Исх. №{contract_number}_{report_date.replace('.', '')}", ln=True)
    pdf.cell(200, 10, f"От {report_date} г.", ln=True)
    pdf.ln(10)

    pdf.multi_cell(0, 10, f"{name}\n{address}\n\nПаспорт №{passport}\nВыдан: {passport_issue}\n")
    pdf.ln(5)

    pdf.multi_cell(0, 10, "АО «Трейдинг Системс», лицензия профессионального участника рынка ценных бумаг на осуществление "
                         "брокерской деятельности № 045-14050-100000 от 06.03.2018, выданная Банком России, "
                         "в ответ на Ваше обращение сообщает следующее.")
    pdf.ln(5)

    pdf.cell(200, 10, f"1. Договор об оказании услуг на финансовом рынке №{contract_number} от {contract_date}г.", ln=True)
    pdf.cell(200, 10, "   В рамках договора Вам были открыты лицевые счета:", ln=True)
    pdf.ln(5)

    pdf.cell(90, 10, "Номер", border=1)
    pdf.cell(90, 10, "Валюта", border=1, ln=True)

    for account in accounts:
        pdf.cell(90, 10, account['number'], border=1)
        pdf.cell(90, 10, account['currency'], border=1, ln=True)

    pdf.ln(10)
    pdf.cell(200, 10, f"2. Депозитарный договор № {deposit_contract} от {contract_date}г.", ln=True)
    pdf.cell(200, 10, "   Открытые счета депо:", ln=True)
    pdf.ln(5)

    pdf.cell(70, 10, "Тип", border=1)
    pdf.cell(60, 10, "Номер", border=1)
    pdf.cell(60, 10, "Раздел", border=1, ln=True)

    for dep_acc in deposit_accounts:
        pdf.cell(70, 10, dep_acc['type'], border=1)
        pdf.cell(60, 10, dep_acc['number'], border=1)
        pdf.cell(60, 10, dep_acc['section'], border=1, ln=True)

    pdf.ln(10)
    pdf.multi_cell(0, 10, "По Депозитарному договору доходы и выплаты по ценным бумагам выплачиваются на указанные выше лицевые счета.")
    pdf.ln(5)

    pdf.multi_cell(0, 10, "Руководитель отдела поддержки инвестиций,\nЕ. И. Савельева")
    pdf.ln(10)
    pdf.multi_cell(0, 10, "АО «Трейдинг Системс»\nк/с 30101810145250000974 в ГУ Банка России по ЦФО БИК 044525974\nИНН 7710140679 КПП 771301001\nhttps://www.tbank.ru")

    pdf.output(output_file)
