# Inicio Rápido - Dashboard Streamlit

## Ejecutar el Dashboard (3 pasos)

### Paso 1: Abrir terminal en la carpeta del proyecto
```bash
cd "/Users/janeth/2025Q3 Business Intelligence/Tienda-producto"
```

### Paso 2: Ejecutar el script
```bash
./run_dashboard.sh
```

O manualmente:
```bash
source venv/bin/activate
streamlit run streamlit_app.py
```

### Paso 3: Abrir en el navegador
El dashboard se abrirá automáticamente en: **http://localhost:8501**

---

## Características del Dashboard

### ✨ Visualizaciones 3D Interactivas
- **Rotar**: Click y arrastrar en el gráfico 3D
- **Zoom**: Scroll del mouse o pellizcar en trackpad
- **Explorar**: Hover sobre los puntos para ver detalles

### Vistas Disponibles

1. **Vista 1: Clusters de Productos**
   - Visualización 3D de clusters (rotable)
   - Estadísticas por cluster
   - Distribución de tipos de producto
   - Gráficos 2D complementarios

2. **Vista 2: Mezcla por Tienda**
   - Visualización 3D de tiendas
   - Stacked bar charts
   - Heatmaps interactivos
   - Análisis detallado por tienda

3. **Análisis Detallado**
   - Resumen general
   - Filtros avanzados
   - Descarga de datos

### Controles Interactivos

- **Slider de Clusters**: Ajusta el número de clusters (2-10)
- **Selectores de Ejes**: Elige qué variables ver en 3D
- **Filtros**: Por tipo de producto, cluster, tienda
- **Zoom y Rotación**: En todas las visualizaciones 3D

---

## Solución de Problemas

### Error: "ModuleNotFoundError: No module named 'streamlit'"
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### Error: "command not found: streamlit"
Asegúrate de activar el entorno virtual:
```bash
source venv/bin/activate
```

### El dashboard no se abre automáticamente
Abre manualmente: http://localhost:8501

---

## Detener el Dashboard

Presiona `Ctrl+C` en la terminal donde está corriendo.

---

¡Disfruta explorando los clusters en 3D! 🎉

