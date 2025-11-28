# Segmentación de Productos y Análisis por Tienda
## Big Mart Sales Prediction - Business Intelligence con Clustering

Este proyecto implementa un flujo completo de Business Intelligence para segmentar productos y analizar su comportamiento por tienda usando técnicas de clustering.

## Estructura del Proyecto

```
Tienda-producto/
├── train_v9rqX0R.csv                    # Dataset original
├── Product_Segmentation_Analysis.ipynb  # Notebook principal con todas las fases
├── streamlit_app.py                     # Dashboard interactivo en Streamlit
├── prepare_powerbi_data.py             # Script para preparar datos para Power BI
├── Executive_Summary.tex               # Resumen ejecutivo en formato LaTeX
├── requirements.txt                    # Dependencias Python
├── run_dashboard.sh                    # Script para ejecutar el dashboard
├── requerimientos.md                   # Especificaciones del proyecto
└── README.md                           # Este archivo
```

## Requisitos

### Librerías Python necesarias:
```bash
pip install -r requirements.txt
```

O instalar manualmente:
```bash
pip install streamlit pandas numpy plotly scikit-learn scipy
```

## Uso del Proyecto

### 1. 🚀 Ejecutar Dashboard Interactivo en Streamlit (RECOMENDADO)

El dashboard incluye visualizaciones 3D interactivas que se pueden rotar y explorar:

**Opción A: Usando el script (Linux/Mac)**
```bash
./run_dashboard.sh
```

**Opción B: Ejecutar manualmente con entorno virtual**
```bash
# Crear entorno virtual (solo la primera vez)
python3 -m venv venv

# Activar entorno virtual
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias (solo la primera vez)
pip install -r requirements.txt

# Ejecutar dashboard
streamlit run streamlit_app.py
```

El dashboard se abrirá automáticamente en tu navegador en `http://localhost:8501`

**Nota:** El script `run_dashboard.sh` crea y gestiona automáticamente el entorno virtual.

**Características del Dashboard:**
- ✅ **Visualizaciones 3D interactivas** con rotación y zoom
- ✅ **Vista 1: Clusters de Productos** - Explora los clusters en 3D usando PCA o variables originales
- ✅ **Vista 2: Mezcla por Tienda** - Analiza la distribución de clusters por tienda
- ✅ **Análisis Detallado** - Filtros y tablas interactivas
- ✅ **Controles dinámicos** - Ajusta el número de clusters y filtra por tipo de producto
- ✅ **Gráficos interactivos** - Scatter plots, heatmaps, sunburst charts, y más

### 2. Ejecutar el Notebook Principal

Abrir y ejecutar `Product_Segmentation_Analysis.ipynb` que contiene todas las fases:

- **Fase A**: Exploración inicial del dataset
- **Fase B**: Construcción del dataset a nivel producto
- **Fase C**: Clustering de productos (K-Means y Jerárquico)
- **Fase D**: Análisis por tienda usando clusters de producto
- **Fase E**: Dashboard de BI con visualizaciones

### 3. Preparar Datos para Power BI

Ejecutar el script de preparación:
```bash
python prepare_powerbi_data.py
```

Este script generará los siguientes archivos CSV:
- `product_metrics_with_clusters.csv` - Dataset a nivel producto con clusters
- `store_analysis_with_clusters.csv` - Dataset a nivel tienda con mezcla de clusters
- `store_cluster_analysis.csv` - Análisis detallado tienda-cluster
- `original_data_with_clusters.csv` - Dataset original con clusters asignados

### 4. Crear Dashboard en Power BI (Opcional)

1. Abrir Power BI Desktop
2. Importar los 4 archivos CSV generados como fuentes de datos
3. Crear relaciones:
   - `product_metrics_with_clusters[Item_Identifier]` ↔ `original_data_with_clusters[Item_Identifier]`
   - `store_analysis_with_clusters[Outlet_Identifier]` ↔ `original_data_with_clusters[Outlet_Identifier]`
   - `store_cluster_analysis[Outlet_Identifier]` ↔ `store_analysis_with_clusters[Outlet_Identifier]`
4. Crear medidas DAX según sea necesario
5. Diseñar las dos vistas del dashboard:
   - **Vista 1**: Clusters de Productos
   - **Vista 2**: Mezcla de Clusters por Tienda

### 5. Generar Resumen Ejecutivo

Compilar el archivo LaTeX `Executive_Summary.tex` usando un compilador LaTeX (Overleaf, TeXstudio, etc.):

```bash
pdflatex Executive_Summary.tex
```

O usar Overleaf:
1. Subir `Executive_Summary.tex` a Overleaf
2. Compilar el documento
3. Descargar el PDF generado

## Entregables

1. ✅ **Dashboard Streamlit** (`streamlit_app.py`) con visualizaciones 3D interactivas
2. ✅ **Notebook** (`Product_Segmentation_Analysis.ipynb`) con cada una de las fases
3. ✅ **Script de preparación** (`prepare_powerbi_data.py`) para generar datos para Power BI
4. ✅ **Resumen ejecutivo** (`Executive_Summary.tex`) en formato LaTeX (3 páginas en inglés)

## Preguntas de Negocio Respondidas

El dashboard permite responder:

- **¿Qué tipos de productos existen en nuestro portafolio?**
  - Respuesta: Los clusters identificados representan diferentes perfiles de productos basados en ventas, precio, distribución y características.

- **¿Qué tiendas venden más de cada tipo de producto?**
  - Respuesta: El análisis por tienda muestra la mezcla de clusters que vende cada tienda, identificando patrones y oportunidades.

- **¿Qué oportunidades de negocio se observan por tienda/segmento de producto?**
  - Respuesta: El análisis revela tiendas con sobre-dependencia de clusters, oportunidades de diversificación, y mejores prácticas replicables.

## Notas Técnicas

- El clustering utiliza K-Means con número óptimo determinado por Silhouette Score
- También se implementa clustering jerárquico para comparación
- Las variables se escalan usando StandardScaler antes del clustering
- Los valores faltantes se imputan usando la mediana por tipo de producto

## Contacto y Soporte

Para preguntas sobre el proyecto, consultar el archivo `requerimientos.md` para las especificaciones completas.

