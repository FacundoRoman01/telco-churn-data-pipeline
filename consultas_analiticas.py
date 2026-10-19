import sqlite3
import pandas as pd

def analizar_churn_general():
    # 1. Conectarnos a nuestro Data Warehouse SQLite
    db_path = "churn.db"
    conn = sqlite3.connect(db_path)

    # 2. Escribir nuestra consulta SQL
    # Queremos agrupar por el estado de Churn, contar cuántos clientes hay y calcular el porcentaje
    query = """
    SELECT 
        Churn,
        COUNT(*) AS total_clientes,
        ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM clientes_churn), 2) AS porcentaje
    FROM clientes_churn
    GROUP BY Churn;
    """



    query = """
    SELECT 
        Contract,
        SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) AS clientes_perdidos,
        COUNT(*) AS total_clientes_contrato,
        ROUND(SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS tasa_churn_porcentaje
    FROM clientes_churn
    GROUP BY Contract
    ORDER BY tasa_churn_porcentaje DESC;
    """


    query = """
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


    print("📊 Ejecutando consulta SQL: Churn Rate General...\n")
    
    # 3. Ejecutar la query y cargar el resultado en un DataFrame de Pandas
    df_resultado = pd.read_sql(query, conn)

    # 4. Mostrar el resultado por consola
    print(df_resultado)

    # Cerrar conexión
    conn.close()

if __name__ == "__main__":
    analizar_churn_general()