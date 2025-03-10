import os
from datetime import datetime
from fpdf import FPDF

def generate_broker_report(user_name, account_number, deals, assets, balance, output_file):
    report_date = datetime.now().strftime("%d.%m.%Y")
    font_path = os.path.join(os.path.dirname(__file__), "fonts", "DejaVuSans.ttf")
    
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    
    pdf.add_font("DejaVu", "", font_path, uni=True)
    pdf.set_font("DejaVu", size=12)
    
    pdf.cell(200, 10, "Брокерский отчет", ln=True, align='C')
    pdf.cell(200, 10, f"Дата: {report_date}", ln=True, align='C')

    pdf.cell(200, 10, "АО «Трейдинг Системс»", ln=True, align='C')
    pdf.cell(200, 10, "Хуторская 2-я, 38а, стр. 26, Москва, 127287, Россия", ln=True, align='C')
    pdf.cell(200, 10, "tradingsystems.ru", ln=True, align='C')
    pdf.ln(10)

    pdf.ln(10)
    
    pdf.cell(200, 10, f"Клиент: {user_name}", ln=True)
    pdf.cell(200, 10, f"Номер счета: {account_number}", ln=True)
    pdf.ln(10)
    
    pdf.multi_cell(0, 10, "АО «Трейдинг Системс», лицензия профессионального участника рынка ценных бумаг на осуществление "
                         "брокерской деятельности № 045-14050-100000 от 06.03.2018, выданная Банком России, "
                         "в ответ на Ваше обращение сообщает следующее.")
    pdf.ln(5)

    pdf.cell(200, 10, "Сделки по счету:", ln=True)
    pdf.ln(5)
    
    pdf.cell(50, 10, "Дата", border=1)
    pdf.cell(40, 10, "Актив", border=1)
    pdf.cell(20, 10, "Кол-во", border=1)
    pdf.cell(30, 10, "Цена ($)", border=1)
    pdf.cell(40, 10, "Тип", border=1, ln=True)
    
    for deal in deals:
        pdf.cell(50, 10, deal['deal_time'], border=1)
        pdf.cell(40, 10, deal['name'], border=1)
        pdf.cell(20, 10, str(deal['quantity']), border=1)
        pdf.cell(30, 10, f"{deal['price']:.2f}", border=1)
        pdf.cell(40, 10, "Покупка" if deal['action_type'] == "BUY" else "Продажа", border=1, ln=True)
    
    pdf.ln(10)
    pdf.cell(200, 10, "Текущие активы:", ln=True)
    pdf.ln(5)
    
    pdf.cell(40, 10, "Актив", border=1)
    pdf.cell(30, 10, "Количество", border=1)
    pdf.cell(40, 10, "Текущая цена ($)", border=1)
    pdf.cell(40, 10, "Стоимость ($)", border=1, ln=True)
    
    for asset in assets:
        total_value = asset['quantity'] * asset['last_price']
        pdf.cell(40, 10, asset['ticker'], border=1)
        pdf.cell(30, 10, str(asset['quantity']), border=1)
        pdf.cell(40, 10, f"{asset['last_price']:.2f}", border=1)
        pdf.cell(40, 10, f"{total_value:.2f}", border=1, ln=True)
    
    pdf.ln(10)
    pdf.cell(200, 10, "Остаток на балансе:", ln=True)
    pdf.ln(5)
    
    pdf.cell(40, 10, "Валюта", border=1)
    pdf.cell(60, 10, "Остаток", border=1, ln=True)
    
    pdf.cell(40, 10, "Доллар США", border=1)
    pdf.cell(60, 10, f"{balance:.2f}", border=1, ln=True)
    
    pdf.multi_cell(0, 10, "Руководитель отдела поддержки инвестиций,\nЕ. И. Савельева")
    pdf.ln(10)
    pdf.multi_cell(0, 10, "АО «Трейдинг Системс»\nк/с 30101810145250000974 в ГУ Банка России по ЦФО БИК 044525974\nИНН 7710140679 КПП 771301001\nhttps://www.tbank.ru")

    pdf.output(output_file)