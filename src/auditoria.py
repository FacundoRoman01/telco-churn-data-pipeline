import logging
import kagglehub
import pandas as pd

# Configurar el sistema de logs para la auditoría de anomalías
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()],
)


def auditar_filas_anomalas():
  try:
    logging.info("Descargando/verificando el dataset con kagglehub...")
    path = kagglehub.dataset_download("blastchar/telco-customer-churn")

    # Ruta estándar del archivo CSV en el dataset de Kaggle
    csv_path = f"{path}/WA_Fn-UseC_-Telco-Customer-Churn.csv"

    logging.info(f"Leyendo el dataset desde: {csv_path}")
    df = pd.read_csv(csv_path)

    # Filtrar solo las filas donde TotalCharges tiene espacios en blanco o no es un número válido
    filas_raras = df[pd.to_numeric(df["TotalCharges"], errors="coerce").isna()]

    cantidad_raras = len(filas_raras)
    logging.info(
        f"Auditoría completada. Cantidad de filas anómalas detectadas:"
        f" {cantidad_raras}"
    )

    if cantidad_raras > 0:
      logging.warning(
          "Se encontraron registros con inconsistencias en 'TotalCharges'."
      )
      print("\nMostrando las columnas clave de esas filas:")
      print(
          filas_raras[[
              "customerID",
              "tenure",
              "MonthlyCharges",
              "TotalCharges",
              "Churn",
          ]]
      )
    else:
      logging.info("¡No se encontraron anomalías en 'TotalCharges'!")

  except Exception as e:
    logging.critical(
        f"Ocurrió un error crítico al auditar las filas anómalas: {e}"
    )
    raise


if __name__ == "__main__":
  auditar_filas_anomalas()