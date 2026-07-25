import yaml


# Carica configurazione portafoglio
with open("config/portfolio.yml", "r") as file:
    portfolio = yaml.safe_load(file)


funds = portfolio["funds"]

total_value = sum(
    fund["value"] for fund in funds
)


print("\n===== PORTAFOGLIO =====\n")

print(
    f"Valore totale: {total_value:,.2f} EUR"
)

print("\nDettaglio fondi:\n")


for fund in funds:

    weight = (
        fund["value"] / total_value * 100
    )

    print(
        f"{fund['name']}"
    )

    print(
        f"ISIN: {fund['isin']}"
    )

    print(
        f"Valore: {fund['value']:,.2f} EUR"
    )

    print(
        f"Peso: {weight:.2f}%"
    )

    print("----------------------")
