import os
import sqlite3
import pandas as pd

def generar_reporte_excel():
    print("🚀 Iniciando generación del reporte ejecutivo en Excel...")

    # 1. Rutas de la base de datos y del archivo de salida
    db_path = "churn.db"
    
    # Asegurar que la carpeta data/processed exista
    os.makedirs("data/processed", exist_ok=True)
    excel_path = "data/processed/reporte_ejecutivo_churn.xlsx"

    # 2. Conectar al Data Warehouse SQLite
    if not os.path.exists(db_path):
        print(f"❌ Error: No se encontró la base de datos en {db_path}. Ejecuta primero carga_dw.py")
        return
        
    conn = sqlite3.connect(db_path)

    # 3. Definir un diccionario con el nombre de cada pestaña y su respectiva consulta SQL
    consultas = {
        "Churn General": """
            SELECT 
                Churn,
                COUNT(*) AS total_clientes,
                ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM clientes_churn), 2) AS porcentaje
            FROM clientes_churn
            GROUP BY Churn;
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
        """
    }

    # 4. ExcelWriter para escribir cada DataFrame en una solapa distinta del mismo archivo
    with pd.ExcelWriter(excel_path, engine='openpyxl') as writer:
        for nombre_pestana, query_sql in consultas.items():
            print(f"📊 Ejecutando query para la pestaña: '{nombre_pestana}'...")
            df = pd.read_sql_query(query_sql, conn)
            
            # Guardar cada tabla en su solapa correspondiente sin incluir el índice de filas
            df.to_excel(writer, sheet_name=nombre_pestana, index=False)
            print(f"📑 Pestaña '{nombre_pestana}' agregada exitosamente.")

    # 5. Cerrar la conexión
    conn.close()
    print(f"\n🎉 ¡Reporte ejecutivo multipestaña generado con éxito en: {excel_path}!")

if __name__ == "__main__":
    generar_reporte_excel()