import pandas as pd
import os

# Verifica che il file prezzi esista
if not os.path.exists("data/prices.csv"):
    print("Nessun file data/prices.csv trovato.")
    exit()

prices = pd.read_csv("data/prices.csv", parse_dates=["Date"])

def calculate_return(series, days):
    """Calcola il rendimento a X giorni gestendo i dati mancanti."""
    if len(series) < 2:
        return None
    end = series.iloc[-1]
    # Prende il valore di N giorni fa o il più vecchio disponibile
    start_idx = max(0, len(series) - days)
    start = series.iloc[start_idx]
    if start == 0 or pd.isna(start):
        return None
    return ((end - start) / start) * 100

print("\n===== CALCOLO PERFORMANCE =====\n")

for name, group in prices.groupby("name"):
    group = group.sort_values("Date").dropna(subset=["Close"])
    close = group["Close"]
    
    print(f"--- {name} ---")
    if len(close) == 0:
        print("Dati storici non disponibili (gestito via NAV manuale)\n")
        continue

    val_1w = calculate_return(close, 7)
    val_1m = calculate_return(close, 30)
    val_1y = calculate_return(close, 365)

    print(f"Ultimo Prezzo: {close.iloc[-1]:.2f}")
    print(f"1 Settimana:   {f'{val_1w:.2f}%' if val_1w is not None else 'N/A'}")
    print(f"1 Mese:        {f'{val_1m:.2f}%' if val_1m is not None else 'N/A'}")
    print(f"12 Mesi:       {f'{val_1y:.2f}%' if val_1y is not None else 'N/A'}\n")
