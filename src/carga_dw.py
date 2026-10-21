import logging
import os
import pandas as pd
import sqlite3

# Configurar el sistema de logs para el proceso de carga al Data Warehouse
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()],
)


def cargar_datos_a_sqlite():
  logging.info("🚀 Iniciando la carga de datos hacia SQLite...")

  # 1. Definimos la ruta de nuestra base de datos SQLite (ubicada en la carpeta database/)
  db_path = "database/churn.db"
  os.path.dirname(db_path) and os.makedirs(
      os.path.dirname(db_path), exist_ok=True
  )

  conexion = None
  try:
    conexion = sqlite3.connect(db_path)
    logging.info(f"📦 Base de datos conectada/creada en: {db_path}")

    # 2. Diccionario de tablas y sus rutas procesadas
    archivos_a_cargar = {"clientes_churn": "data/processed/telco_churn_clean.csv"}

    # 3. Recorremos el diccionario, leemos el CSV y lo cargamos a la tabla
    for nombre_tabla, ruta_csv in archivos_a_cargar.items():
      if not os.path.exists(ruta_csv):
        logging.error(f"No se encontró el archivo procesado en: {ruta_csv}")
        continue

      logging.info(f"📄 Leyendo {ruta_csv} para carga en Data Warehouse...")
      df = pd.read_csv(ruta_csv)

      # Cargar a SQLite
      df.to_sql(nombre_tabla, conexion, if_exists="replace", index=False)
      logging.info(
          f"✅ Tabla '{nombre_tabla}' cargada exitosamente con {df.shape[0]}"
          " registros."
      )

  except Exception as e:
    logging.critical(f"Error crítico durante la carga en el Data Warehouse: {e}")
    raise

  finally:
    # 4. Asegurar el cierre de la conexión pase lo que pase
    if conexion:
      conexion.close()
      logging.info("🔒 Conexión a la base de datos cerrada correctamente.")


if __name__ == "__main__":
  cargar_datos_a_sqlite()