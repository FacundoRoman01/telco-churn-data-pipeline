import os
import pandas as pd
import kagglehub

print("📥 Descargando/verificando el dataset con kagglehub...")
# Descarga la última versión del dataset de Telco Churn
path = kagglehub.dataset_download("blastchar/telco-customer-churn")
print(f"📁 Ruta de los archivos descargados: {path}")

# Buscar automáticamente el archivo .csv dentro de la carpeta descargada
archivos_csv = [f for f in os.listdir(path) if f.endswith('.csv')]

if not archivos_csv:
    print("❌ No se encontró ningún archivo CSV en la ruta descargada.")
    exit()

CSV_PATH = os.path.join(path, archivos_csv[0])
print(f"✅ Archivo detectado: {archivos_csv[0]}\n")

# Leer el dataset con Pandas
try:
    df = pd.read_csv(CSV_PATH)
    print(f"✅ Dataset leído con éxito. Total de registros: {df.shape[0]}, Columnas: {df.shape[1]}\n")

except Exception as e:
    print(f"❌ Error al leer el archivo CSV: {e}")
    exit()

# 2. Auditoría de Calidad de Datos (Data Quality Check)
print("="*50)
print("📊 REPORTE DE CALIDAD DE DATOS (DATA QUALITY)")
print("="*50)

# A. Tipos de datos por columna
print("\n--- 1. Tipos de datos por columna ---")
print(df.dtypes)

# B. Conteo de valores nulos
print("\n--- 2. Valores Nulos por Columna ---")
nulos = df.isnull().sum()
print(nulos[nulos > 0] if nulos.sum() > 0 else "¡No hay valores nulos explícitos (NaN)!")

# C. Detección de espacios en blanco ocultos en 'TotalCharges'
print("\n--- 3. Auditoría de anomalías en 'TotalCharges' ---")
if 'TotalCharges' in df.columns:
    espacios_blanco = df['TotalCharges'].astype(str).str.strip().eq('').sum()
    print(f"Registros con espacios en blanco vacíos en 'TotalCharges': {espacios_blanco}")

# D. Duplicados
print("\n--- 4. Registros Duplicados ---")
duplicados = df.duplicated().sum()
print(f"Filas totalmente duplicadas: {duplicados}")

# E. Distribución de la variable objetivo (Churn)
print("\n--- 5. Distribución de la Variable Objetivo (Churn) ---")
if 'Churn' in df.columns:
    print(df['Churn'].value_counts(dropna=False))
    print("\nPorcentajes:")
    print(df['Churn'].value_counts(normalize=True) * 100)

print("\n" + "="*50)
print("🏁 Auditoría finalizada.")
print("="*50)