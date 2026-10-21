import logging
import os
import pandas as pd

# Configurar el sistema de logs para registrar marcas de tiempo y severidad
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()],
)


def limpiar_datos_churn():
  # 1. Definir rutas
  RAW_PATH = "data/raw/telco_churn_raw.csv"
  PROCESSED_DIR = "data/processed"
  PROCESSED_PATH = os.path.join(PROCESSED_DIR, "telco_churn_clean.csv")

  # 2. Verificar si el archivo crudo existe 
  if not os.path.exists(RAW_PATH):
    logging.error(
        f"No se encontró el archivo en {RAW_PATH}. Asegurate de haberlo"
        " descargado primero."
    )
    return

  try:
    logging.info("Leyendo el archivo CSV crudo...")
    # 3. Leer el archivo csv
    df = pd.read_csv(RAW_PATH)
    filas_iniciales = df.shape[0]

    # 4. Transformar y limpiar datos clave para el negocio
    logging.info("Transformando tipos de datos y limpiando anomalías...")

    # Limpiar 'TotalCharges': convertir a numérico (forzando errores a NaN) y rellenar con 0
    df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")
    nulos_totales = df["TotalCharges"].isna().sum()

    if nulos_totales > 0:
      logging.warning(
          f"Se detectaron {nulos_totales} valores nulos/anómalos en"
          " 'TotalCharges'. Rellenando con 0."
      )
    df["TotalCharges"] = df["TotalCharges"].fillna(0)

    # Limpiar espacios en blanco en IDs si existieran
    if "customerID" in df.columns:
      df["customerID"] = df["customerID"].str.strip()

    # 5. Crear carpeta procesada si no existe y guardar el nuevo DataFrame limpio
    os.makedirs(PROCESSED_DIR, exist_ok=True)
    df.to_csv(PROCESSED_PATH, index=False)

    filas_finales = df.shape[0]
    logging.info(
        f"¡Datos limpios guardados exitosamente en: {PROCESSED_PATH}!"
    )
    logging.info(
        f"Métricas de Auditoría -> Registros iniciales: {filas_iniciales} |"
        f" Registros finales: {filas_finales} | Columnas procesadas:"
        f" {df.shape[1]}"
    )

  except Exception as e:
    logging.critical(
        f"Ocurrió un error crítico durante el proceso de limpieza: {e}"
    )
    raise


# Ejecutamos la función
if __name__ == "__main__":
  limpiar_datos_churn()