#!/bin/bash
# Script para ejecutar el dashboard Streamlit

echo "=========================================="
echo "Iniciando Dashboard Streamlit"
echo "=========================================="
echo ""

# Verificar si existe el entorno virtual
if [ ! -d "venv" ]; then
    echo "Creando entorno virtual..."
    python3 -m venv venv
fi

# Activar entorno virtual
echo "Activando entorno virtual..."
source venv/bin/activate

# Instalar dependencias si es necesario
if ! python -c "import streamlit" 2>/dev/null; then
    echo "Instalando dependencias..."
    pip install -q -r requirements.txt
fi

echo ""
echo "Iniciando servidor Streamlit..."
echo "El dashboard estará disponible en: http://localhost:8501"
echo "Presiona Ctrl+C para detener el servidor"
echo ""
streamlit run streamlit_app.py

