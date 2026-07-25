import pandas as pd
import numpy as np
from datetime import datetime


# Caricamento dati
prices = pd.read_csv(
    "data/prices.csv",
    parse_dates=["Date"]
)


def calculate_return(series, start_date):
    """
    Calcola rendimento da una data iniziale
    """

    series = series.sort_index()

    end_value = series.iloc[-1]

    available = series[
        series.index <= start_date
    ]

    if len(available) == 0:
        return None

    start_value = available.iloc[-1]

    return (end_value / start_value) - 1



def annualized_return(total_return, days):
    """
    Annualizzazione rendimento
    """

    if total_return is None or days <= 0:
        return None

    return (1 + total_return) ** (365 / days) - 1



results = []


today = prices["Date"].max()


# Date di riferimento

start_week = today - pd.Timedelta(days=7)

start_month = today.replace(day=1)

start_year = today.replace(
    month=1,
    day=1
)

start_1y = today - pd.DateOffset(years=1)



for name in prices["name"].unique():

    data = prices[
        prices["name"] == name
    ].copy()


    data = data.sort_values(
        "Date"
    )


    data = data.set_index(
        "Date"
    )


    close = data["Close"]


    weekly = calculate_return(
        close,
        start_week
    )

    mtd = calculate_return(
        close,
        start_month
    )

    ytd = calculate_return(
        close,
        start_year
    )

    one_year = calculate_return(
        close,
        start_1y
    )


    # Volatilità

    daily_returns = close.pct_change().dropna()

    volatility = (
        daily_returns.std()
        *
        np.sqrt(252)
    )


    annualized = annualized_return(
        one_year,
        365
    )


    results.append({

        "Strumento": name,

        "Weekly":
            weekly,

        "MTD":
            mtd,

        "YTD":
            ytd,

        "1Y":
            one_year,

        "Annualizzato":
            annualized,

        "Volatilità":
            volatility

    })



report = pd.DataFrame(results)


# Salvataggio

report.to_csv(
    "data/performance.csv",
    index=False
)


print("\n===== PERFORMANCE REPORT =====\n")

print(report)


print(
    "\nCreato: data/performance.csv"
)
