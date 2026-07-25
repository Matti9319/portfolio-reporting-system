import pandas as pd
import os

# Verifica che il file prezzi esista
if not os.path.exists("data/prices.csv"):
    print("Nessun file data/prices.csv trovato.")
    exit()

prices = pd.read_csv("data/prices.csv", parse_dates=["Date"])
prices["Close"] = pd.to_numeric(prices["Close"], errors="coerce")

def calculate_return(series, days):
    """Calcola il rendimento a X giorni gestendo i dati mancanti."""
    if len(series) < 2:
        return None
    end = series.iloc[-1]
    start_idx = max(0, len(series) - days)
    start = series.iloc[start_idx]
    if pd.isna(start) or start == 0 or pd.isna(end):
        return None
    return ((end - start) / start) * 100

print("\n===== CALCOLO PERFORMANCE =====\n")

results = []

for name, group in prices.groupby("name"):
    group = group.sort_values("Date").dropna(subset=["Close"])
    close = group["Close"]
    
    if len(close) == 0:
        continue

    val_1w = calculate_return(close, 7)
    val_1m = calculate_return(close, 30)
    val_1y = calculate_return(close, 365)

    results.append({
        "name": name,
        "price": round(close.iloc[-1], 2),
        "return_1w": round(val_1w, 2) if val_1w is not None else None,
        "return_1m": round(val_1m, 2) if val_1m is not None else None,
        "return_1y": round(val_1y, 2) if val_1y is not None else None
    })

# Salva i risultati nel file data/performance.csv
df_perf = pd.DataFrame(results)
df_perf.to_csv("data/performance.csv", index=False)

print(df_perf)
print("\n✅ File data/performance.csv creato con successo!")
