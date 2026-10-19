import os
import pandas as pd
import sqlite3

def cargar_datos_a_sqlite(): 
    print("🚀 Iniciando la carga de datos hacia SQLite...")

    # 1. Definimos la ruta de nuestra base de datos SQLite
    db_path = "churn.db"

    conexion = sqlite3.connect(db_path)
    print(f"📦 Base de datos conectada/creada en: {db_path}")

    # 2. Diccionario de tablas y sus rutas procesadas
    archivos_a_cargar = {
       "clientes_churn": "data/processed/telco_churn_clean.csv"
    }

    # 3. Recorremos el diccionario, leemos el CSV y lo cargamos a la tabla
    for nombre_tabla, ruta_csv in archivos_a_cargar.items():
        if not os.path.exists(ruta_csv):
            print(f"❌ No se encontró el archivo en: {ruta_csv}")
            continue
            
        print(f"📄 Leyendo {ruta_csv}...")
        df = pd.read_csv(ruta_csv)
        
        # Cargar a SQLite
        df.to_sql(nombre_tabla, conexion, if_exists="replace", index=False)
        print(f"✅ Tabla '{nombre_tabla}' cargada exitosamente con {df.shape[0]} registros.")

    # 4. Cerrar la conexión
    conexion.close()
    print("🔒 Conexión a la base de datos cerrada correctamente.")

if __name__ == "__main__":
    cargar_datos_a_sqlite()