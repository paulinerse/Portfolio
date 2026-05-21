import pandas as pd

# 1) Charger le CSV
df = pd.read_csv(r"C:\Users\pauli\Documents\code\kaggle\ALDI PROJECT\data_aldi.csv")

# 2) Nettoyer les colonnes en pourcentage
# Exemples: "22%" -> 22.0
percent_cols = ["Margin_Rate_%", "PDM_Value", "DN_%"]

for col in percent_cols:
    df[col] = (
        df[col]
        .astype(str)
        .str.replace("%", "", regex=False)
        .str.replace(",", ".", regex=False)  # au cas où décimales avec virgule
        .str.strip()
    )
    df[col] = pd.to_numeric(df[col], errors="coerce")

# 3) Convertir la date
# Ton fichier est au format "03/2026" => mois/année
df["Date"] = pd.to_datetime(df["Date"], format="%m/%Y", errors="coerce")

# 4) Vérifications rapides
print("=== Aperçu nettoyé ===")
print(df.head())
print("\n=== Types des colonnes ===")
print(df.dtypes)

# 5) Analyse 1: ventes totales par catégorie
sales_by_category = (
    df.groupby("Category", as_index=False)["Sales_Value"]
    .sum()
    .sort_values("Sales_Value", ascending=False)
)

# 6) Analyse 2: marge moyenne (%)
avg_margin = df["Margin_Rate_%"].mean()

# 7) Analyse 3: top produits (par ventes)
top_products = (
    df.groupby("SKU_Name", as_index=False)["Sales_Value"]
    .sum()
    .sort_values("Sales_Value", ascending=False)
    .head(10)
)

# 8) Affichage des résultats
print("\n=== Ventes par catégorie ===")
print(sales_by_category)

print("\n=== Marge moyenne (%) ===")
print(round(avg_margin, 2))

print("\n=== Top produits (Top 10 par Sales_Value) ===")
print(top_products)