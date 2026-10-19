import pandas as pd
import kagglehub

# Cargar dataset
path = kagglehub.dataset_download("blastchar/telco-customer-churn")
df = pd.read_csv(f"{path}/WA_Fn-UseC_-Telco-Customer-Churn.csv")

# Filtrar solo las filas donde TotalCharges tiene espacios en blanco o no es un número válido
filas_raras = df[pd.to_numeric(df['TotalCharges'], errors='coerce').isna()]

print(f"Cantidad de filas detectadas: {len(filas_raras)}")
print("\nMostrando las columnas clave de esas filas:")
print(filas_raras[['customerID', 'tenure', 'MonthlyCharges', 'TotalCharges', 'Churn']])