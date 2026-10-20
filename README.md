# 📊 Telco Churn Analysis & Data Pipeline

Pipeline de datos de punta a punta, modelado de Data Warehouse local, análisis SQL avanzado y generación de reportes ejecutivos automatizados para la retención de clientes en la industria de telecomunicaciones.

---

## 🚀 Resumen del Proyecto
Este proyecto simula un caso de negocio real de análisis de abandono de clientes (*Churn*) en una empresa de telecomunicaciones. El objetivo principal es identificar patrones de comportamiento, cuantificar el impacto financiero de las cancelaciones y automatizar la entrega de insights accionables para la toma de decisiones gerenciales.

El desarrollo abarca desde la ingesta de datos crudos hasta la implementación de una base de datos relacional local, consultas analíticas de negocio, un reporte multipestaña automatizado en Excel y un Dashboard interactivo de Business Intelligence.

---

## 🛠️ Stack Tecnológico & Herramientas
* **Lenguaje:** Python 
* **Manipulación y Procesamiento:** Pandas, OpenPyXL
* **Data Warehouse / Base de Datos:** SQLite3 (Arquitectura relacional local)
* **Automatización:** Scripts ETL personalizados
* **Control de Versiones:** Git & GitHub

---

## ⚙️ Arquitectura del Pipeline de Datos (ETL)
1. **Extract (Extracción):** Ingesta del dataset crudo de clientes de telecomunicaciones.
2. **Transform (Transformación & Limpieza):** 
   * Auditoría y tratamiento de valores nulos y anómalos (ej. normalización de la columna `TotalCharges` en clientes nuevos con `tenure = 0`).
   * Limpieza de tipos de datos y estandarización de variables categóricas.
3. **Load (Carga / Data Warehouse):** Inserción de los datos limpios en una base de datos relacional estructurada en SQLite (`churn.db`).
4. **Analyze & Deliver (Análisis y Reporte):** Ejecución de consultas SQL analíticas orientadas al negocio y exportación automatizada a un reporte ejecutivo multipestaña en Excel (`reporte_ejecutivo_churn.xlsx`).

---

## 📈 Hallazgos Clave & Métricas de Negocio (*Insights*)

* **Churn Rate Global:** La tasa general de abandono de la compañía se ubica en el **26.54%** sobre un total de **7.043 clientes** analizados.
* **Vulnerabilidad Crítica por Contrato:** Los clientes con modalidad **Month-to-month (mes a mes)** presentan una tasa de abandono catastrófica del **42.71%**, concentrando la abrumadora mayoría de las bajas frente a los contratos anuales o bianuales.
* **Impacto Financiero (Revenue Loss):** La compañía pierde más de **$139,000 dólares mensuales** en ingresos recurrentes debido a las cancelaciones, siendo el segmento mensual el principal detonante de la sangría financiera (**~$120,840 USD** mensuales perdidos en ese segmento).

---

## 📂 Estructura del Repositorio

```text
proyect-churn-data/
│
├── data/
│   ├── processed/
│   │   └── reporte_ejecutivo_churn.xlsx   # Reporte ejecutivo automatizado (Multipestaña)
│   └── telco_churn_raw.csv                # Dataset crudo original
│
├── churn.db                               # Data Warehouse local en SQLite
├── analisis_churn.py                      # Script de consultas analíticas y exportación Excel
└── README.md                              # Documentación del proyecto



