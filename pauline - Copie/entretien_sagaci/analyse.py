import pandas as pd
import numpy as np
import sys

# Ensure UTF-8 printing on all terminal environments
sys.stdout.reconfigure(encoding='utf-8')

def clean_malaria_data(filepath):
    print("[INFO] Initializing Malaria Data Cleaning Pipeline...")
    df = pd.read_csv(filepath)
    print(f"[DATA] Raw Dataset Shape: {df.shape[0]} rows, {df.shape[1]} columns")
    
    # 1. Analyze missing value rates
    missing_rates = df.isnull().mean() * 100
    print("\n[DIAGNOSTIC] Missing Value Rates per Column:")
    for col, rate in missing_rates.items():
        if rate > 0:
            print(f"  - {col}: {rate:.2f}% missing")
            
    # 2. Prune columns exceeding 50% missingness threshold
    threshold = 50.0
    cols_to_keep = missing_rates[missing_rates <= threshold].index
    cols_to_drop = missing_rates[missing_rates > threshold].index
    
    print(f"\n[PRUNING] Filtering columns with > {threshold}% missing values:")
    for col in cols_to_drop:
        print(f"  - Dropped: '{col}' ({missing_rates[col]:.2f}% missing)")
        
    df_pruned = df[cols_to_keep].copy()
    print(f"[DATA] Pruned Dataset Shape: {df_pruned.shape[0]} rows, {df_pruned.shape[1]} columns")
    
    # 3. Handle specific missing data in key columns
    malaria_col = 'Incidence of malaria (per 1,000 population at risk)'
    water_col = 'People using at least basic drinking water services (% of population)'
    sanitation_col = 'People using at least basic sanitation services (% of population)'
    
    # Check nulls in key columns
    print("\n[IMPUTATION] Handling missing values in key analytical columns:")
    for col in [malaria_col, water_col, sanitation_col]:
        if col in df_pruned.columns:
            null_count = df_pruned[col].isnull().sum()
            print(f"  - '{col}': {null_count} nulls found.")
            if null_count > 0:
                # Group by country and fill missing values with country-specific average,
                # if still null (whole country missing), fill with global average.
                df_pruned[col] = df_pruned.groupby('Country Name')[col].transform(lambda x: x.fillna(x.mean()))
                # Secondary fallback for countries with zero data
                global_mean = df_pruned[col].mean()
                df_pruned[col] = df_pruned[col].fillna(global_mean)
                print(f"    -> Imputed {null_count} values using Country-specific Mean + Global fallback.")
                
    # 4. Export clean file
    output_path = filepath.replace(".csv", "_cleaned.csv")
    df_pruned.to_csv(output_path, index=False)
    print(f"\n[EXPORT] Cleaned dataset successfully saved to: {output_path}")
    return df_pruned, list(cols_to_drop)

if __name__ == "__main__":
    import os
    filepath = r"c:\Users\User\Documents\code\pauline\entretien_sagaci\DatasetAfricaMalaria.csv"
    if os.path.exists(filepath):
        clean_malaria_data(filepath)
    else:
        print(f"[ERROR] File not found at {filepath}")
