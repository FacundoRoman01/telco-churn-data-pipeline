# 📊 Telco Churn Analysis & Data Pipeline

Pipeline de datos de punta a punta, modelado de Data Warehouse local, análisis SQL avanzado y generación de reportes ejecutivos automatizados para la retención de clientes en la industria de telecomunicaciones.

---

## 🚀 Resumen del Proyecto
Este proyecto simula un caso de negocio real de análisis de abandono de clientes (*Churn*) en una empresa de telecomunicaciones. El objetivo principal es identificar patrones de comportamiento, cuantificar el impacto financiero de las cancelaciones y automatizar la entrega de insights accionables para la toma de decisiones gerenciales.

El desarrollo abarca desde la ingesta de datos crudos hasta la implementación de una base de datos relacional local, consultas analíticas de negocio, un reporte multipestaña automatizado en Excel y un Dashboard interactivo de Business Intelligence.

---

## 🛠️ Stack Tecnológico & Herramientas
- **Lenguaje:** Python 
- **Manipulación y Procesamiento:** Pandas, OpenPyXL
- **Data Warehouse / Base de Datos:** SQLite3 (Arquitectura relacional local)
- **Automatización:** Scripts ETL personalizados
- **Control de Versiones:** Git & GitHub

---

## ⚙️ Arquitectura del Pipeline de Datos (ETL)
1. **Extract (Extracción):** Ingesta del dataset crudo de clientes de telecomunicaciones.
2. **Transform (Transformación & Limpieza):** 
   * Auditoría y tratamiento de valores nulos y anómalos (ej. normalización de la columna `TotalCharges` en clientes nuevos con `tenure = 0`).
   * Limpieza de tipos de datos y estandarización de variables categóricas.
3. **Load (Carga / Data Warehouse):** Inserción de los datos limpios en una base de datos relacional estructurada en SQLite (`churn.db`).
4. **Analyze & Deliver (Análisis y Reporte):** Ejecución de consultas SQL analíticas orientadas al negocio y exportación automatizada a un reporte ejecutivo multipestaña en Excel (`reporte_ejecutivo_churn.xlsx`).

---

## 🔍 Gobierno y Calidad de Datos (*Data Quality*)
Con el fin de garantizar la confiabilidad analítica y evitar sesgos en el Business Intelligence, se implementaron procesos rigurosos de auditoría y control de calidad en la etapa de transformación:
* **Detección y Tratamiento de Nulos:** Auditoría automatizada mediante scripts de Python (`src/auditoria.py`) para identificar inconsistencias estructurales y valores vacíos ocultos en formato de cadenas de texto.
* **Coherencia Financiera (`TotalCharges` vs `tenure`):** Identificación y normalización de registros en clientes con antigüedad de 0 meses (`tenure = 0`), cuyos cargos totales presentaban espacios en blanco, asegurando que no alteren las métricas financieras globales.
* **Tipado Estricto de Datos:** Conversión de campos numéricos mal tipados (como cargos mensuales y totales almacenados como texto) a tipos de datos flotantes (*float*), garantizando la precisión matemática en las consultas SQL y Looker Studio.
* **Integridad Referencial:** Validación de unicidad en la clave primaria de clientes y consistencia en los valores de variables categóricas clave (como `Contract` y `Churn`).

---

## 📈 Hallazgos Clave & Métricas de Negocio (*Insights*)

- **Churn Rate Global:** La tasa general de abandono de la compañía se ubica en el **26.54%** sobre un total de **7.043 clientes** analizados.
- **Vulnerabilidad Crítica por Contrato:** Los clientes con modalidad **Month-to-month (mes a mes)** presentan una tasa de abandono catastrófica del **42.71%**, concentrando la abrumadora mayoría de las bajas frente a los contratos anuales o bianuales.
- **Impacto Financiero (Revenue Loss):** La compañía pierde más de **$139,000 dólares mensuales** en ingresos recurrentes debido a las cancelaciones, siendo el segmento mensual el principal detonante de la sangría financiera (**~$120,840 USD** mensuales perdidos en ese segmento).

---

## 📂 Estructura del Repositorio

```text
proyect-churn-data/
│
├── data/
│   ├── raw/
│   │   └── telco_churn_raw.csv          # Dataset crudo original e inmutable
│   └── processed/
│       ├── telco_churn_clean.csv        # Dataset limpio y transformado
│       └── reporte_ejecutivo_churn.xlsx # Reporte ejecutivo automatizado (Multipestaña)
│
├── database/
│   └── churn.db                         # Data Warehouse local en SQLite
│
├── src/                                 # Código fuente del pipeline y scripts analíticos
│   ├── auditoria.py
│   ├── auditoria_churn.py
│   ├── carga_dw.py                      # Script de carga al Data Warehouse
│   ├── consultas_analiticas.py          # Consultas SQL y generación de reporte Excel
│   └── limpieza.py                      # Script de limpieza y transformación de datos
│
├── .gitignore                           # Configuración de archivos ignorados por Git
└── README.md                            # Documentación del proyecto

```

📊 Dashboard de Business Intelligence (BI)
El Data Warehouse fue conectado a Looker Studio para la construcción de un panel de control interactivo (Executive Dashboard) que incluye:

Tarjeta de KPIs ejecutivos principales (Clientes Totales, Clientes Perdidos, Tasa de Abandono Global y Pérdida Mensual Total).

Gráfico de barras de Pérdida Mensual de Ingresos por Tipo de Contrato.

Gráfico circular de Distribución de Clientes Perdidos por Tipo de Contrato (destacando el 88.6% en contratos mensuales).

Gráfico de barras horizontales de Gasto Mensual Promedio por Cliente Perdido (Ticket).

Desarrollado con un enfoque riguroso en ingeniería de datos, modelado relacional y visualización analítica.

<img width="1920" height="1668" alt="screencapture-datastudio-google-u-0-reporting-34647a65-37ea-47d4-9b44-61a4314daeda-page-yfiBG-2026-10-20-13_19_22" src="https://github.com/user-attachments/assets/1dda0d74-7065-4a8e-ab6f-16906a813a01" />



