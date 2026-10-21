import logging
import os
import kagglehub
import pandas as pd

# Configurar el sistema de logs para la auditoría
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()],
)


def ejecutar_auditoria():
  try:
    logging.info("Descargando/verificando el dataset con kagglehub...")
    path = kagglehub.dataset_download("blastchar/telco-customer-churn")
    logging.info(f"Ruta de los archivos descargados: {path}")

    # Buscar automáticamente el archivo .csv dentro de la carpeta descargada
    archivos_csv = [f for f in os.listdir(path) if f.endswith(".csv")]

    if not archivos_csv:
      logging.error("No se encontró ningún archivo CSV en la ruta descargada.")
      return

    CSV_PATH = os.path.join(path, archivos_csv[0])
    logging.info(f"Archivo detectado: {archivos_csv[0]}")

    # Leer el dataset con Pandas
    df = pd.read_csv(CSV_PATH)
    logging.info(
        "Dataset leído con éxito. Total de registros:"
        f" {df.shape[0]}, Columnas: {df.shape[1]}"
    )

    # 2. Auditoría de Calidad de Datos (Data Quality Check)
    logging.info("=" * 50)
    logging.info("📊 REPORTE DE CALIDAD DE DATOS (DATA QUALITY)")
    logging.info("=" * 50)

    # A. Tipos de datos por columna
    logging.info("--- 1. Tipos de datos por columna ---")
    print(df.dtypes)

    # B. Conteo de valores nulos
    logging.info("--- 2. Valores Nulos por Columna ---")
    nulos = df.isnull().sum()
    if nulos.sum() > 0:
      logging.warning(
          "Se encontraron valores nulos:\n"
          f"{nulos[nulos > 0]}"
      )
    else:
      logging.info("¡No hay valores nulos explícitos (NaN)!")

    # C. Detección de espacios en blanco ocultos en 'TotalCharges'
    if "TotalCharges" in df.columns:
      espacios_blanco = (
          df["TotalCharges"].astype(str).str.strip().eq("").sum()
      )
      logging.info(
          "--- 3. Auditoría de anomalías en 'TotalCharges' ---"
      )
      logging.info(
          "Registros con espacios en blanco vacíos en 'TotalCharges':"
          f" {espacios_blanco}"
      )

    # D. Duplicados
    duplicados = df.duplicated().sum()
    logging.info("--- 4. Registros Duplicados ---")
    logging.info(f"Filas totalmente duplicadas: {duplicados}")

    # E. Distribución de la variable objetivo (Churn)
    if "Churn" in df.columns:
      logging.info(
          "--- 5. Distribución de la Variable Objetivo (Churn) ---"
      )
      print(df["Churn"].value_counts(dropna=False))
      print("\nPorcentajes:")
      print(df["Churn"].value_counts(normalize=True) * 100)

    logging.info("=" * 50)
    logging.info("🏁 Auditoría finalizada exitosamente.")
    logging.info("=" * 50)

  except Exception as e:
    logging.critical(
        f"Ocurrió un error crítico durante la auditoría de datos: {e}"
    )
    raise


if __name__ == "__main__":
  ejecutar_auditoria()