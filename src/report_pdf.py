import pandas as pd
import yaml
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from datetime import datetime
import os


# Cartella report
os.makedirs("reports", exist_ok=True)


# Lettura configurazione portafoglio
with open("config/portfolio.yml", "r") as file:
    portfolio = yaml.safe_load(file)


# Lettura performance
performance = pd.read_csv(
    "data/performance.csv"
)


# Creazione PDF
today = datetime.today().strftime("%Y-%m-%d")

filename = f"reports/Portfolio_Report_{today}.pdf"


doc = SimpleDocTemplate(
    filename,
    pagesize=A4
)


styles = getSampleStyleSheet()

content = []


# Titolo
content.append(
    Paragraph(
        "Portfolio Report - Michele",
        styles["Title"]
    )
)

content.append(
    Spacer(1, 20)
)


# Data
content.append(
    Paragraph(
        f"Data report: {today}",
        styles["Normal"]
    )
)

content.append(
    Spacer(1, 20)
)


# Valore totale
total_value = sum(
    fund["value"]
    for fund in portfolio["funds"]
)


content.append(
    Paragraph(
        f"Valore totale portafoglio: {total_value:,.2f} EUR",
        styles["Heading2"]
    )
)

content.append(
    Spacer(1, 20)
)


# Tabella fondi

table_data = [
    [
        "Fondo",
        "Valore (€)",
        "Peso (%)"
    ]
]


for fund in portfolio["funds"]:

    weight = (
        fund["value"] /
        total_value *
        100
    )

    table_data.append(
        [
            fund["name"],
            f"{fund['value']:,.2f}",
            f"{weight:.2f}"
        ]
    )


table = Table(table_data)


table.setStyle(
    TableStyle(
        [
            ("GRID",(0,0),(-1,-1),0.5,None),
            ("ALIGN",(1,1),(-1,-1),"RIGHT")
        ]
    )
)


content.append(table)

content.append(
    Spacer(1,30)
)


# Performance

content.append(
    Paragraph(
        "Performance",
        styles["Heading2"]
    )
)


perf_table = [
    list(performance.columns)
]


for _, row in performance.iterrows():

    perf_table.append(
        [
            str(x)
            for x in row.values
        ]
    )


table2 = Table(perf_table)


table2.setStyle(
    TableStyle(
        [
            ("GRID",(0,0),(-1,-1),0.5,None)
        ]
    )
)


content.append(table2)


doc.build(content)


print(
    f"Report creato: {filename}"
)
