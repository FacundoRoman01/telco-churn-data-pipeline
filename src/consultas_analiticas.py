import logging
import os
import pandas as pd
import sqlite3

# Configurar el sistema de logs para el generador de reportes
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()],
)


def generar_reporte_excel():
  logging.info(" Iniciando generación del reporte ejecutivo en Excel...")

  # 1. Rutas de la base de datos (apuntando a database/churn.db) y del archivo de salida
  db_path = "database/churn.db"
  excel_path = "data/processed/reporte_ejecutivo_churn.xlsx"

  # Asegurar que la carpeta data/processed exista
  os.makedirs(os.path.dirname(excel_path), exist_ok=True)

  # 2. Conectar al Data Warehouse SQLite con validación
  if not os.path.exists(db_path):
    logging.error(
        f"No se encontró la base de datos en {db_path}. Ejecuta primero"
        " carga_dw.py"
    )
    return

  conn = None
  try:
    conn = sqlite3.connect(db_path)
    logging.info(f"📦 Conexión establecida exitosamente con el Data Warehouse.")

    # 3. Definir un diccionario con el nombre de cada pestaña y su respectiva consulta SQL
    consultas = {
        "Churn General": """
                SELECT 
                    (SELECT COUNT(*) FROM clientes_churn) AS total_clientes,
                    SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) AS clientes_perdidos,
                    ROUND(SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS churn_rate_global
                FROM clientes_churn;
            """,
        "Por Contrato": """
                SELECT 
                    Contract,
                    SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) AS clientes_perdidos,
                    COUNT(*) AS total_clientes_contrato,
                    ROUND(SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS tasa_churn_porcentaje
                FROM clientes_churn
                GROUP BY Contract
                ORDER BY tasa_churn_porcentaje DESC;
            """,
        "Impacto Financiero": """
                SELECT 
                    Contract,
                    COUNT(*) AS clientes_perdidos,
                    ROUND(SUM(MonthlyCharges), 2) AS perdida_mensual_total,
                    ROUND(AVG(MonthlyCharges), 2) AS ticket_promedio_perdido
                FROM clientes_churn
                WHERE Churn = 'Yes'
                GROUP BY Contract
                ORDER BY perdida_mensual_total DESC;
            """,
    }

    # 4. ExcelWriter para escribir cada DataFrame en una solapa distinta del mismo archivo
    with pd.ExcelWriter(excel_path, engine="openpyxl") as writer:
      for nombre_pestana, query_sql in consultas.items():
        logging.info(f"📊 Ejecutando query para la pestaña: '{nombre_pestana}'...")
        df = pd.read_sql_query(query_sql, conn)

        # Guardar cada tabla en su solapa correspondiente sin incluir el índice de filas
        df.to_excel(writer, sheet_name=nombre_pestana, index=False)
        logging.info(f"📑 Pestaña '{nombre_pestana}' agregada exitosamente.")

    logging.info(
        f"🎉 ¡Reporte ejecutivo multipestaña generado con éxito en:"
        f" {excel_path}!"
    )

  except Exception as e:
    logging.critical(
        f"Error crítico durante la generación del reporte en Excel: {e}"
    )
    raise

  finally:
    # 5. Asegurar el cierre de la conexión pase lo que pase
    if conn:
      conn.close()
      logging.info(
          "🔒 Conexión al Data Warehouse cerrada correctamente tras generar el"
          " reporte."
      )


if __name__ == "__main__":
  generar_reporte_excel()