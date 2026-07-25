import pandas as pd
import yaml
import os

# Carica la configurazione del portafoglio
with open("config/portfolio.yml", "r") as f:
    config = yaml.safe_load(f)

# Carica i prezzi storici se esistono
prices = pd.DataFrame()
if os.path.exists("data/prices.csv"):
    prices = pd.read_csv("data/prices.csv", parse_dates=["Date"])
    prices["Close"] = pd.to_numeric(prices["Close"], errors="coerce")

def calculate_return(series, days):
    if len(series) < 2:
        return None
    end = series.iloc[-1]
    start_idx = max(0, len(series) - days)
    start = series.iloc[start_idx]
    if pd.isna(start) or start == 0 or pd.isna(end):
        return None
    return ((end - start) / start) * 100

results = []

for fund in config.get("funds", []):
    name = fund.get("name")
    val_static = fund.get("value")
    
    # Cerca i dati del fondo nei prezzi scaricati
    fund_prices = prices[prices["name"] == name].sort_values("Date").dropna(subset=["Close"]) if not prices.empty and "name" in prices.columns else pd.DataFrame()
    
    if not fund_prices.empty:
        close = fund_prices["Close"]
        latest_price = close.iloc[-1]
        val_1w = calculate_return(close, 7)
        val_1m = calculate_return(close, 30)
        val_1y = calculate_return(close, 365)
    else:
        # Se non ci sono serie storiche scaricate, usa il valore da YML
        latest_price = val_static
        val_1w, val_1m, val_1y = None, None, None

    results.append({
        "name": name,
        "price": round(latest_price, 2) if latest_price is not None else None,
        "return_1w": round(val_1w, 2) if val_1w is not None else None,
        "return_1m": round(val_1m, 2) if val_1m is not None else None,
        "return_1y": round(val_1y, 2) if val_1y is not None else None
    })

os.makedirs("data", exist_ok=True)
df_perf = pd.DataFrame(results)
df_perf.to_csv("data/performance.csv", index=False)

print("\n===== CALCOLO PERFORMANCE COMPLETO =====\n")
print(df_perf)
print("\n✅ File data/performance.csv aggiornato per TUTTI i fondi!")
