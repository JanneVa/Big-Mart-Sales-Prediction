"""
Dashboard Streamlit para Segmentación de Productos y Análisis por Tienda
Big Mart Sales Prediction - Business Intelligence con Clustering
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.cluster import KMeans, AgglomerativeClustering
from sklearn.metrics import silhouette_score
from sklearn.decomposition import PCA
import warnings
warnings.filterwarnings('ignore')

# Configuración de la página
st.set_page_config(
    page_title="Product Segmentation & Store Analysis",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Título principal
st.title("Product Segmentation and Store Analysis Dashboard")
st.markdown("### Big Mart Sales Prediction - Business Intelligence with Clustering")

# Cache para cargar y procesar datos
@st.cache_data
def load_and_process_data():
    """Cargar y procesar los datos"""
    # Cargar datos originales
    df = pd.read_csv('train_v9rqX0R.csv')
    
    # Limpiar datos
    df_clean = df.copy()
    df_clean['Item_Fat_Content'] = df_clean['Item_Fat_Content'].replace({
        'low fat': 'Low Fat',
        'LF': 'Low Fat',
        'reg': 'Regular'
    })
    
    # Construir dataset a nivel producto
    product_metrics = df_clean.groupby('Item_Identifier').agg({
        'Item_Outlet_Sales': ['sum', 'mean', 'std', 'count'],
        'Item_MRP': 'mean',
        'Item_Weight': 'mean',
        'Item_Visibility': 'mean',
        'Outlet_Identifier': 'nunique',
        'Item_Type': 'first',
        'Item_Fat_Content': 'first'
    }).reset_index()
    
    product_metrics.columns = [
        'Item_Identifier',
        'Total_Sales',
        'Avg_Sales_Per_Store',
        'Std_Sales',
        'Num_Store_Records',
        'Avg_MRP',
        'Avg_Weight',
        'Avg_Visibility',
        'Num_Stores',
        'Item_Type',
        'Item_Fat_Content'
    ]
    
    # Tratar valores faltantes
    product_metrics['Avg_Weight'] = product_metrics.groupby('Item_Type')['Avg_Weight'].transform(
        lambda x: x.fillna(x.median())
    )
    product_metrics['Avg_Weight'] = product_metrics['Avg_Weight'].fillna(product_metrics['Avg_Weight'].median())
    product_metrics['Std_Sales'] = product_metrics['Std_Sales'].fillna(0)
    
    # Codificar variables categóricas
    le_item_type = LabelEncoder()
    le_fat_content = LabelEncoder()
    product_metrics['Item_Type_Encoded'] = le_item_type.fit_transform(product_metrics['Item_Type'])
    product_metrics['Item_Fat_Content_Encoded'] = le_fat_content.fit_transform(product_metrics['Item_Fat_Content'])
    
    # Crear variables adicionales
    product_metrics['Sales_Stability'] = product_metrics['Std_Sales'] / (product_metrics['Avg_Sales_Per_Store'] + 1)
    product_metrics['Price_Per_Unit_Weight'] = product_metrics['Avg_MRP'] / (product_metrics['Avg_Weight'] + 1)
    
    return df_clean, product_metrics, le_item_type, le_fat_content

@st.cache_data
def perform_clustering(product_metrics, n_clusters=None):
    """Realizar clustering de productos"""
    clustering_features = [
        'Total_Sales', 'Avg_Sales_Per_Store', 'Num_Stores', 'Avg_MRP',
        'Avg_Weight', 'Avg_Visibility', 'Item_Type_Encoded',
        'Item_Fat_Content_Encoded', 'Sales_Stability', 'Price_Per_Unit_Weight'
    ]
    
    X_clustering = product_metrics[clustering_features].copy()
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X_clustering)
    
    # Determinar número óptimo si no se especifica
    if n_clusters is None:
        best_k = 2
        best_score = -1
        for k in range(2, 11):
            kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
            labels = kmeans.fit_predict(X_scaled)
            score = silhouette_score(X_scaled, labels)
            if score > best_score:
                best_score = score
                best_k = k
        n_clusters = best_k
    
    # Aplicar clustering
    kmeans_final = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    product_metrics['cluster_producto'] = kmeans_final.fit_predict(X_scaled)
    
    # PCA para visualización 3D
    pca = PCA(n_components=3)
    X_pca = pca.fit_transform(X_scaled)
    product_metrics['PC1'] = X_pca[:, 0]
    product_metrics['PC2'] = X_pca[:, 1]
    product_metrics['PC3'] = X_pca[:, 2]
    
    return product_metrics, X_scaled, scaler, pca, n_clusters

@st.cache_data
def prepare_store_analysis(df_clean, product_metrics):
    """Preparar análisis por tienda"""
    # Incorporar clusters al dataset original
    df_with_clusters = df_clean.merge(
        product_metrics[['Item_Identifier', 'cluster_producto']],
        on='Item_Identifier',
        how='left'
    )
    
    # Análisis por tienda y cluster
    store_cluster_analysis = df_with_clusters.groupby(['Outlet_Identifier', 'cluster_producto']).agg({
        'Item_Outlet_Sales': ['sum', 'mean', 'count'],
        'Item_Identifier': 'nunique',
        'Item_MRP': 'mean'
    }).reset_index()
    
    store_cluster_analysis.columns = [
        'Outlet_Identifier',
        'cluster_producto',
        'Total_Sales_Cluster',
        'Avg_Sales_Per_Product',
        'Num_Records',
        'Num_Unique_Products',
        'Avg_MRP'
    ]
    
    store_total_sales = df_with_clusters.groupby('Outlet_Identifier')['Item_Outlet_Sales'].sum().reset_index()
    store_total_sales.columns = ['Outlet_Identifier', 'Store_Total_Sales']
    
    store_cluster_analysis = store_cluster_analysis.merge(store_total_sales, on='Outlet_Identifier')
    store_cluster_analysis['Pct_Sales_From_Cluster'] = (
        store_cluster_analysis['Total_Sales_Cluster'] / 
        store_cluster_analysis['Store_Total_Sales'] * 100
    )
    
    # Dataset a nivel tienda
    store_analysis = df_with_clusters.groupby('Outlet_Identifier').agg({
        'Item_Outlet_Sales': 'sum',
        'Outlet_Type': 'first',
        'Outlet_Size': 'first',
        'Outlet_Location_Type': 'first',
        'Outlet_Establishment_Year': 'first',
        'Item_Identifier': 'nunique'
    }).reset_index()
    
    store_analysis.columns = [
        'Outlet_Identifier',
        'Total_Sales',
        'Outlet_Type',
        'Outlet_Size',
        'Outlet_Location_Type',
        'Outlet_Establishment_Year',
        'Num_Unique_Products'
    ]
    
    return df_with_clusters, store_cluster_analysis, store_analysis

# Cargar datos
with st.spinner("Cargando y procesando datos..."):
    df_clean, product_metrics, le_item_type, le_fat_content = load_and_process_data()

# Sidebar para controles
st.sidebar.header("⚙️ Controles del Dashboard")

# Selector de número de clusters
n_clusters = st.sidebar.slider(
    "Número de Clusters",
    min_value=2,
    max_value=10,
    value=4,
    help="Ajusta el número de clusters para el análisis"
)

# Realizar clustering
with st.spinner("Realizando clustering..."):
    product_metrics, X_scaled, scaler, pca, optimal_k = perform_clustering(product_metrics, n_clusters)

# Preparar análisis por tienda
df_with_clusters, store_cluster_analysis, store_analysis = prepare_store_analysis(df_clean, product_metrics)

# Mostrar información en sidebar
st.sidebar.markdown("---")
st.sidebar.metric("Productos Únicos", f"{len(product_metrics):,}")
st.sidebar.metric("Tiendas", f"{df_clean['Outlet_Identifier'].nunique()}")
st.sidebar.metric("Clusters", n_clusters)

# Tabs para las diferentes vistas
tab1, tab2, tab3 = st.tabs(["🎯 Vista 1: Clusters de Productos", "🏪 Vista 2: Mezcla por Tienda", "📈 Análisis Detallado"])

with tab1:
    st.header("Vista 1: Clusters de Productos")
    
    # Visualización 3D interactiva de clusters
    st.subheader("Visualización 3D Interactiva de Clusters")
    st.markdown("**Rotar, hacer zoom y explorar los clusters en 3D usando los controles del gráfico**")
    
    # Selector de variables para los ejes
    col1, col2, col3 = st.columns(3)
    
    with col1:
        x_axis = st.selectbox(
            "Eje X",
            options=['PC1', 'Total_Sales', 'Avg_MRP', 'Avg_Sales_Per_Store', 'Num_Stores'],
            index=0
        )
    
    with col2:
        y_axis = st.selectbox(
            "Eje Y",
            options=['PC2', 'Total_Sales', 'Avg_MRP', 'Avg_Sales_Per_Store', 'Num_Stores'],
            index=1 if 'Total_Sales' in ['PC2', 'Total_Sales', 'Avg_MRP', 'Avg_Sales_Per_Store', 'Num_Stores'] else 0
        )
    
    with col3:
        z_axis = st.selectbox(
            "Eje Z",
            options=['PC3', 'Total_Sales', 'Avg_MRP', 'Avg_Sales_Per_Store', 'Num_Stores'],
            index=2 if 'PC3' in ['PC3', 'Total_Sales', 'Avg_MRP', 'Avg_Sales_Per_Store', 'Num_Stores'] else 0
        )
    
    # Filtro por tipo de producto
    item_types = ['Todos'] + list(product_metrics['Item_Type'].unique())
    selected_type = st.selectbox("Filtrar por Tipo de Producto", item_types)
    
    # Preparar datos para visualización
    plot_data = product_metrics.copy()
    if selected_type != 'Todos':
        plot_data = plot_data[plot_data['Item_Type'] == selected_type]
    
    # Crear gráfico 3D interactivo
    fig_3d = px.scatter_3d(
        plot_data,
        x=x_axis,
        y=y_axis,
        z=z_axis,
        color='cluster_producto',
        size='Total_Sales',
        hover_data=['Item_Identifier', 'Item_Type', 'Total_Sales', 'Avg_MRP', 'Num_Stores'],
        color_continuous_scale='viridis',
        title=f'Clusters de Productos en 3D ({x_axis} vs {y_axis} vs {z_axis})',
        labels={
            x_axis: x_axis,
            y_axis: y_axis,
            z_axis: z_axis,
            'cluster_producto': 'Cluster'
        }
    )
    
    fig_3d.update_layout(
        scene=dict(
            xaxis_title=x_axis,
            yaxis_title=y_axis,
            zaxis_title=z_axis,
            camera=dict(
                eye=dict(x=1.5, y=1.5, z=1.5)
            )
        ),
        height=700,
        width=1000
    )
    
    st.plotly_chart(fig_3d, use_container_width=True)
    
    # Estadísticas por cluster
    st.subheader("Estadísticas por Cluster")
    
    col1, col2 = st.columns(2)
    
    with col1:
        cluster_stats = product_metrics.groupby('cluster_producto').agg({
            'Total_Sales': ['mean', 'sum', 'count'],
            'Avg_MRP': 'mean',
            'Num_Stores': 'mean',
            'Item_Type': lambda x: x.mode()[0] if len(x.mode()) > 0 else 'N/A'
        }).round(2)
        cluster_stats.columns = ['Avg_Total_Sales', 'Sum_Total_Sales', 'Num_Products', 
                                'Avg_MRP', 'Avg_Num_Stores', 'Most_Common_Type']
        st.dataframe(cluster_stats, use_container_width=True)
    
    with col2:
        # Distribución de productos por cluster
        cluster_counts = product_metrics['cluster_producto'].value_counts().sort_index()
        fig_bar = px.bar(
            x=cluster_counts.index,
            y=cluster_counts.values,
            labels={'x': 'Cluster', 'y': 'Número de Productos'},
            title='Distribución de Productos por Cluster',
            color=cluster_counts.values,
            color_continuous_scale='viridis'
        )
        st.plotly_chart(fig_bar, use_container_width=True)
    
    # Visualización 2D adicional
    st.subheader("Visualizaciones 2D Complementarias")
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig_scatter = px.scatter(
            plot_data,
            x='Total_Sales',
            y='Avg_MRP',
            color='cluster_producto',
            size='Num_Stores',
            hover_data=['Item_Identifier', 'Item_Type'],
            title='Total Sales vs Average MRP por Cluster',
            color_continuous_scale='viridis'
        )
        st.plotly_chart(fig_scatter, use_container_width=True)
    
    with col2:
        fig_scatter2 = px.scatter(
            plot_data,
            x='Avg_Sales_Per_Store',
            y='Num_Stores',
            color='cluster_producto',
            size='Total_Sales',
            hover_data=['Item_Identifier', 'Item_Type'],
            title='Avg Sales Per Store vs Number of Stores',
            color_continuous_scale='viridis'
        )
        st.plotly_chart(fig_scatter2, use_container_width=True)
    
    # Distribución de tipos de producto por cluster
    st.subheader("Distribución de Tipos de Producto por Cluster")
    item_type_by_cluster = product_metrics.groupby(['cluster_producto', 'Item_Type']).size().reset_index(name='Count')
    item_type_pct = item_type_by_cluster.groupby('cluster_producto').apply(
        lambda x: x.assign(Pct=x['Count'] / x['Count'].sum() * 100)
    ).reset_index(drop=True)
    
    fig_sunburst = px.sunburst(
        item_type_pct,
        path=['cluster_producto', 'Item_Type'],
        values='Count',
        title='Distribución de Tipos de Producto por Cluster (Sunburst)',
        color='Pct',
        color_continuous_scale='viridis'
    )
    st.plotly_chart(fig_sunburst, use_container_width=True)

with tab2:
    st.header("Vista 2: Mezcla de Clusters por Tienda")
    
    # Visualización 3D de tiendas y clusters
    st.subheader("Visualización 3D: Tiendas y Clusters")
    
    # Preparar datos para visualización 3D de tiendas
    store_cluster_pivot = store_cluster_analysis.pivot_table(
        index='Outlet_Identifier',
        columns='cluster_producto',
        values='Pct_Sales_From_Cluster',
        fill_value=0
    ).reset_index()
    
    # Agregar información de tienda
    store_cluster_pivot = store_cluster_pivot.merge(
        store_analysis[['Outlet_Identifier', 'Total_Sales', 'Outlet_Type', 'Outlet_Location_Type']],
        on='Outlet_Identifier'
    )
    
    # Obtener columnas de clusters (excluyendo Outlet_Identifier)
    cluster_cols = [col for col in store_cluster_pivot.columns 
                   if col != 'Outlet_Identifier' and col not in ['Total_Sales', 'Outlet_Type', 'Outlet_Location_Type']
                   and isinstance(col, (int, float))]
    
    # Seleccionar ejes para visualización 3D
    if len(cluster_cols) >= 3:
        x_col, y_col, z_col = cluster_cols[0], cluster_cols[1], cluster_cols[2]
        x_label = f'Cluster {int(x_col)} %'
        y_label = f'Cluster {int(y_col)} %'
        z_label = f'Cluster {int(z_col)} %'
    elif len(cluster_cols) == 2:
        x_col, y_col, z_col = cluster_cols[0], cluster_cols[1], 'Total_Sales'
        x_label = f'Cluster {int(x_col)} %'
        y_label = f'Cluster {int(y_col)} %'
        z_label = 'Total Sales ($)'
    elif len(cluster_cols) == 1:
        x_col, y_col, z_col = cluster_cols[0], 'Total_Sales', 'Total_Sales'
        x_label = f'Cluster {int(x_col)} %'
        y_label = 'Total Sales ($)'
        z_label = 'Total Sales ($)'
    else:
        x_col, y_col, z_col = 'Total_Sales', 'Total_Sales', 'Total_Sales'
        x_label = y_label = z_label = 'Total Sales ($)'
    
    # Visualización 3D de tiendas
    fig_store_3d = px.scatter_3d(
        store_cluster_pivot,
        x=x_col,
        y=y_col,
        z=z_col,
        color='Outlet_Type',
        size='Total_Sales',
        hover_data=['Outlet_Identifier', 'Outlet_Location_Type'] + cluster_cols[:3],
        title='Distribución de Tiendas por Mezcla de Clusters (3D)',
        labels={
            x_col: x_label,
            y_col: y_label,
            z_col: z_label
        }
    )
    
    fig_store_3d.update_layout(
        scene=dict(
            camera=dict(eye=dict(x=1.5, y=1.5, z=1.5))
        ),
        height=700
    )
    
    st.plotly_chart(fig_store_3d, use_container_width=True)
    
    # Stacked bar chart de porcentajes por tienda
    st.subheader("Distribución de Ventas por Cluster en cada Tienda")
    
    cluster_cols_pct = [col for col in store_analysis.columns if col.startswith('Pct_Cluster_')]
    if cluster_cols_pct:
        store_cluster_data = store_analysis.set_index('Outlet_Identifier')[cluster_cols_pct]
        
        fig_stacked = go.Figure()
        colors = px.colors.qualitative.Set3
        
        for i, col in enumerate(cluster_cols_pct):
            fig_stacked.add_trace(go.Bar(
                name=f'Cluster {col.split("_")[-1]}',
                x=store_cluster_data.index,
                y=store_cluster_data[col],
                marker_color=colors[i % len(colors)]
            ))
        
        fig_stacked.update_layout(
            barmode='stack',
            title='Porcentaje de Ventas por Cluster en cada Tienda',
            xaxis_title='Tienda',
            yaxis_title='Porcentaje de Ventas (%)',
            height=500
        )
        
        st.plotly_chart(fig_stacked, use_container_width=True)
    
    # Heatmap interactivo
    st.subheader("Heatmap: Porcentaje de Ventas por Cluster y Tienda")
    
    if cluster_cols_pct:
        heatmap_data = store_analysis.set_index('Outlet_Identifier')[cluster_cols_pct].T
        
        fig_heatmap = px.imshow(
            heatmap_data.values,
            labels=dict(x="Tienda", y="Cluster", color="Porcentaje (%)"),
            x=heatmap_data.columns,
            y=[f'Cluster {col.split("_")[-1]}' for col in cluster_cols_pct],
            color_continuous_scale='YlOrRd',
            aspect="auto",
            title='Heatmap: Porcentaje de Ventas por Cluster y Tienda'
        )
        
        fig_heatmap.update_layout(height=400)
        st.plotly_chart(fig_heatmap, use_container_width=True)
    
    # Ventas totales por tienda
    st.subheader("Ventas Totales por Tienda")
    
    store_sales_sorted = store_analysis.sort_values('Total_Sales', ascending=False)
    
    fig_sales = px.bar(
        store_sales_sorted,
        x='Outlet_Identifier',
        y='Total_Sales',
        color='Outlet_Type',
        title='Ventas Totales por Tienda',
        labels={'Total_Sales': 'Ventas Totales ($)', 'Outlet_Identifier': 'Tienda'}
    )
    fig_sales.update_layout(height=500, xaxis_tickangle=-45)
    st.plotly_chart(fig_sales, use_container_width=True)
    
    # Tabla de análisis por tienda
    st.subheader("Análisis Detallado por Tienda")
    
    selected_store = st.selectbox(
        "Seleccionar Tienda para Análisis Detallado",
        options=store_analysis['Outlet_Identifier'].unique()
    )
    
    if selected_store:
        store_detail = store_cluster_analysis[store_cluster_analysis['Outlet_Identifier'] == selected_store]
        store_info = store_analysis[store_analysis['Outlet_Identifier'] == selected_store].iloc[0]
        
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Ventas Totales", f"${store_info['Total_Sales']:,.2f}")
        col2.metric("Tipo de Tienda", store_info['Outlet_Type'])
        col3.metric("Ubicación", store_info['Outlet_Location_Type'])
        col4.metric("Productos Únicos", f"{store_info['Num_Unique_Products']}")
        
        # Gráfico de distribución por cluster para la tienda seleccionada
        fig_store_cluster = px.pie(
            store_detail,
            values='Pct_Sales_From_Cluster',
            names='cluster_producto',
            title=f'Distribución de Ventas por Cluster - {selected_store}',
            hole=0.4
        )
        st.plotly_chart(fig_store_cluster, use_container_width=True)
        
        st.dataframe(store_detail[['cluster_producto', 'Total_Sales_Cluster', 'Pct_Sales_From_Cluster', 
                                   'Num_Unique_Products', 'Avg_MRP']], use_container_width=True)

with tab3:
    st.header("Análisis Detallado")
    
    # Resumen general
    st.subheader("Resumen General del Dataset")
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total de Registros", f"{len(df_clean):,}")
    col2.metric("Productos Únicos", f"{len(product_metrics):,}")
    col3.metric("Tiendas", f"{df_clean['Outlet_Identifier'].nunique()}")
    col4.metric("Ventas Totales", f"${df_clean['Item_Outlet_Sales'].sum():,.2f}")
    
    # Análisis por tipo de tienda
    st.subheader("Análisis por Tipo de Tienda")
    
    store_type_cluster = df_with_clusters.groupby(['Outlet_Type', 'cluster_producto']).agg({
        'Item_Outlet_Sales': 'sum',
        'Item_Identifier': 'nunique'
    }).reset_index()
    
    store_type_total = df_with_clusters.groupby('Outlet_Type')['Item_Outlet_Sales'].sum().reset_index()
    store_type_total.columns = ['Outlet_Type', 'Type_Total_Sales']
    
    store_type_cluster = store_type_cluster.merge(store_type_total, on='Outlet_Type')
    store_type_cluster['Pct_Sales'] = (
        store_type_cluster['Item_Outlet_Sales'] / 
        store_type_cluster['Type_Total_Sales'] * 100
    )
    
    fig_type = px.bar(
        store_type_cluster,
        x='Outlet_Type',
        y='Pct_Sales',
        color='cluster_producto',
        title='Distribución de Ventas por Cluster y Tipo de Tienda',
        labels={'Pct_Sales': 'Porcentaje de Ventas (%)', 'Outlet_Type': 'Tipo de Tienda'},
        barmode='stack'
    )
    st.plotly_chart(fig_type, use_container_width=True)
    
    # Tabla de datos
    st.subheader("Datos de Productos con Clusters")
    
    # Filtros
    col1, col2 = st.columns(2)
    with col1:
        selected_clusters = st.multiselect(
            "Filtrar por Clusters",
            options=sorted(product_metrics['cluster_producto'].unique()),
            default=sorted(product_metrics['cluster_producto'].unique())
        )
    
    with col2:
        selected_item_types = st.multiselect(
            "Filtrar por Tipo de Producto",
            options=product_metrics['Item_Type'].unique().tolist(),
            default=product_metrics['Item_Type'].unique().tolist()
        )
    
    filtered_data = product_metrics[
        (product_metrics['cluster_producto'].isin(selected_clusters)) &
        (product_metrics['Item_Type'].isin(selected_item_types))
    ]
    
    st.dataframe(
        filtered_data[['Item_Identifier', 'Item_Type', 'cluster_producto', 
                      'Total_Sales', 'Avg_MRP', 'Num_Stores', 'Avg_Sales_Per_Store']],
        use_container_width=True,
        height=400
    )
    
    # Descargar datos
    csv = filtered_data.to_csv(index=False)
    st.download_button(
        label=" Descargar Datos Filtrados (CSV)",
        data=csv,
        file_name=f"productos_clusters_{pd.Timestamp.now().strftime('%Y%m%d')}.csv",
        mime="text/csv"
    )

# Footer
st.markdown("---")
st.markdown("**Dashboard creado para análisis de segmentación de productos y análisis por tienda**")
st.markdown("*Big Mart Sales Prediction - Business Intelligence con Clustering*")

