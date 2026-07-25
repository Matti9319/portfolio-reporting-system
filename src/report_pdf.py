import pandas as pd
import os
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

# 1. Verifica che i dati esistano
if not os.path.exists("data/performance.csv"):
    print("❌ Errore: File data/performance.csv non trovato. Esegui prima performance.py!")
    exit()

df = pd.read_csv("data/performance.csv")

# Assicurati che la cartella reports esista
os.makedirs("reports", exist_ok=True)

# Nome del file PDF di output con la data di oggi
today_str = datetime.now().strftime("%Y-%m-%d")
pdf_path = f"reports/Portfolio_Report_{today_str}.pdf"

doc = SimpleDocTemplate(
    pdf_path,
    pagesize=letter,
    rightMargin=40, leftMargin=40,
    topMargin=40, bottomMargin=40
)

styles = getSampleStyleSheet()
story = []

# Titolo del Report
title_style = ParagraphStyle(
    "ReportTitle",
    parent=styles["Heading1"],
    fontSize=20,
    leading=24,
    textColor=colors.HexColor("#1A365D"),
    spaceAfter=12
)
story.append(Paragraph("Report Performance Portafoglio", title_style))
story.append(Paragraph(f"<b>Data Report:</b> {today_str}", styles["Normal"]))
story.append(Spacer(1, 20))

# Intestazione Tabella
table_data = [["Strumento", "Prezzo (€)", "1 Sett (%)", "1 Mese (%)", "12 Mesi (%)"]]

# Popolamento dati
for _, row in df.iterrows():
    name = str(row["name"])
    price = f"{row['price']:.2f}" if pd.notna(row['price']) else "N/A"
    r_1w = f"{row['return_1w']:.2f}%" if pd.notna(row['return_1w']) else "N/A"
    r_1m = f"{row['return_1m']:.2f}%" if pd.notna(row['return_1m']) else "N/A"
    r_1y = f"{row['return_1y']:.2f}%" if pd.notna(row['return_1y']) else "N/A"
    
    table_data.append([name, price, r_1w, r_1m, r_1y])

# Stile Tabella
t = Table(table_data, colWidths=[200, 80, 80, 80, 80])
t.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1A365D")),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('ALIGN', (0, 0), (0, -1), 'LEFT'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, -1), 10),
    ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
    ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor("#F7FAFC")),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E0")),
]))

story.append(t)

# Generazione PDF
doc.build(story)
print(f"✅ PDF generato con successo: {pdf_path}")
