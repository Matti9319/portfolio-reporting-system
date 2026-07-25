import yaml
import yfinance as yf
import pandas as pd
import os


# Lettura configurazione
with open("config/portfolio.yml", "r") as file:
    portfolio = yaml.safe_load(file)


os.makedirs("data", exist_ok=True)


results = []


for fund in portfolio["funds"]:

    ticker = fund.get("ticker")

    if ticker:

        print(f"Scarico dati: {fund['name']} - {ticker}")

        data = yf.download(
            ticker,
            period="5y",
            auto_adjust=True
        )

        if not data.empty:

            temp = data[["Close"]].copy()

            temp["name"] = fund["name"]
            temp["isin"] = fund["isin"]

            temp.reset_index(inplace=True)

            results.append(temp)

        else:
            print(f"Nessun dato trovato per {ticker}")

    else:
        print(
            f"{fund['name']} senza ticker Yahoo - verrà gestito con NAV"
        )


if results:

    prices = pd.concat(results)

    prices.to_csv(
        "data/prices.csv",
        index=False
    )

    print("\nDownload completato")
    print("File creato: data/prices.csv")

else:

    print("Nessun dato scaricato")
