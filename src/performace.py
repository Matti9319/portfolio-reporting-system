import pandas as pd
from datetime import datetime, timedelta


prices = pd.read_csv(
    "data/prices.csv",
    parse_dates=["Date"]
)


def calculate_return(series, days):
    
    end = series.iloc[-1]

    start_date = series.index[-1] - timedelta(days=days)

    past = series[series.index <= start_date]

    if len(past) == 0:
        return None

    start = past.iloc[-1]

    return (end / start) - 1



results = []


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


    results.append({

        "Strumento": name,

        "1 settimana":
            calculate_return(close,7),

        "MTD":
            calculate_return(close,30),

        "YTD":
            calculate_return(close,365),

        "1 anno":
            calculate_return(close,365)

    })


report = pd.DataFrame(results)


report.to_csv(
    "data/performance.csv",
    index=False
)


print(report)
print("\nCreato: data/performance.csv")
