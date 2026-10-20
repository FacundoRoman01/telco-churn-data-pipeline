import os
import pandas as pd

def limpiar_datos_churn():
    # 1. Definir rutas
    RAW_PATH = "data/raw/telco_churn_raw.csv"
    PROCESSED_DIR = "data/processed"
    PROCESSED_PATH = os.path.join(PROCESSED_DIR, "telco_churn_clean.csv")

    # 2. Verificar si el archivo crudo existe
    if not os.path.exists(RAW_PATH):
        print(f"❌ Error: No se encontró el archivo en {RAW_PATH}. Asegurate de haberlo descargado primero.")
        return

    print("📥 Leyendo el archivo CSV crudo...")
    # 3. Leer el archivo csv
    df = pd.read_csv(RAW_PATH)

    # 4. Transformar y limpiar datos clave para el negocio
    print("🧹 Transformando tipos de datos y limpiando anomalías...")
    
    # Limpiar 'TotalCharges': convertir a numérico (forzando errores a NaN) y rellenar con 0
    df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')
    df['TotalCharges'] = df['TotalCharges'].fillna(0)

    # Opcional: limpiar espacios en blanco en IDs si existieran
    df['customerID'] = df['customerID'].str.strip()

    # 5. Crear carpeta procesada si no existe y guardar el nuevo DataFrame limpio
    os.makedirs(PROCESSED_DIR, exist_ok=True)
    
    df.to_csv(PROCESSED_PATH, index=False)
    print(f"✅ ¡Datos limpios guardados exitosamente en: {PROCESSED_PATH}!")
    print(f"📊 Total de registros procesados: {df.shape[0]}, Columnas: {df.shape[1]}")

# Ejecutar la función
if __name__ == "__main__":
    limpiar_datos_churn()