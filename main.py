import logging
import sys

# Importamos las funciones principales desde la carpeta src/
from src.carga_dw import cargar_datos_a_sqlite
from src.consultas_analiticas import generar_reporte_excel
from src.limpieza import limpiar_datos_churn

# Configurar el sistema de logs global para el orquestador
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()],
)


def ejecutar_pipeline_completo():
  logging.info("==================================================")
  logging.info("🚀 INICIANDO ORQUESTADOR GENERAL DEL PIPELINE DE CHURN")
  logging.info("==================================================")

  try:
    # Paso 1: Limpieza y Transformación (Data Quality)
    logging.info("\n--- [FASE 1/3]: Limpieza y Transformación ---")
    limpiar_datos_churn()

    # Paso 2: Carga al Data Warehouse (SQLite)
    logging.info("\n--- [FASE 2/3]: Carga al Data Warehouse ---")
    cargar_datos_a_sqlite()

    # Paso 3: Generación de Reporte Ejecutivo (Excel Multipestaña)
    logging.info("\n--- [FAse 3/3]: Generación de Reporte Analítico ---")
    generar_reporte_excel()

    logging.info("==================================================")
    logging.info("🎉 ¡PIPELINE COMPLETO EJECUTADO CON ÉXITO DE PUNTA A PUNTA!")
    logging.info("==================================================")

  except Exception as e:
    logging.critical(
        f"❌ El orquestador detectó un error crítico y detuvo el pipeline: {e}"
    )
    sys.exit(1)


if __name__ == "__main__":
  ejecutar_pipeline_completo()