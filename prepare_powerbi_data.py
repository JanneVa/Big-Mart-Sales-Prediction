"""
Script para preparar datos para Power BI Dashboard
Este script genera los archivos CSV necesarios para crear el dashboard en Power BI
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.cluster import KMeans
import warnings
warnings.filterwarnings('ignore')

print("="*80)
print("PREPARACIÓN DE DATOS PARA POWER BI")
print("="*80)

# Cargar datos originales
print("\n1. Cargando datos originales...")
df = pd.read_csv('train_v9rqX0R.csv')
print(f"   ✓ Dataset cargado: {df.shape[0]:,} registros")

# Limpiar datos
df_clean = df.copy()
df_clean['Item_Fat_Content'] = df_clean['Item_Fat_Content'].replace({
    'low fat': 'Low Fat',
    'LF': 'Low Fat',
    'reg': 'Regular'
})

# Construir dataset a nivel producto
print("\n2. Construyendo dataset a nivel producto...")
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

# Clustering
print("\n3. Aplicando clustering de productos...")
clustering_features = [
    'Total_Sales', 'Avg_Sales_Per_Store', 'Num_Stores', 'Avg_MRP',
    'Avg_Weight', 'Avg_Visibility', 'Item_Type_Encoded',
    'Item_Fat_Content_Encoded', 'Sales_Stability', 'Price_Per_Unit_Weight'
]

X_clustering = product_metrics[clustering_features].copy()
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_clustering)

# Determinar número óptimo de clusters
from sklearn.metrics import silhouette_score
best_k = 2
best_score = -1
for k in range(2, 11):
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    labels = kmeans.fit_predict(X_scaled)
    score = silhouette_score(X_scaled, labels)
    if score > best_score:
        best_score = score
        best_k = k

print(f"   ✓ Número óptimo de clusters: {best_k} (Silhouette Score: {best_score:.4f})")

# Aplicar clustering final
kmeans_final = KMeans(n_clusters=best_k, random_state=42, n_init=10)
product_metrics['cluster_producto'] = kmeans_final.fit_predict(X_scaled)
print(f"   ✓ Clustering completado")

# Incorporar clusters al dataset original
print("\n4. Incorporando clusters al dataset original...")
df_with_clusters = df_clean.merge(
    product_metrics[['Item_Identifier', 'cluster_producto']],
    on='Item_Identifier',
    how='left'
)
print(f"   ✓ Dataset original con clusters: {df_with_clusters.shape}")

# Análisis por tienda y cluster
print("\n5. Calculando métricas por tienda y cluster...")
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
print(f"   ✓ Análisis tienda-cluster completado")

# Dataset a nivel tienda
print("\n6. Creando dataset a nivel tienda...")
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

cluster_pct_by_store = store_cluster_analysis.pivot_table(
    index='Outlet_Identifier',
    columns='cluster_producto',
    values='Pct_Sales_From_Cluster',
    fill_value=0
)
cluster_pct_by_store.columns = [f'Pct_Cluster_{int(col)}' for col in cluster_pct_by_store.columns]
store_analysis = store_analysis.merge(cluster_pct_by_store, left_on='Outlet_Identifier', right_index=True)
print(f"   ✓ Dataset a nivel tienda creado")

# Guardar archivos
print("\n7. Guardando archivos CSV para Power BI...")
product_metrics.to_csv('product_metrics_with_clusters.csv', index=False)
store_analysis.to_csv('store_analysis_with_clusters.csv', index=False)
store_cluster_analysis.to_csv('store_cluster_analysis.csv', index=False)
df_with_clusters.to_csv('original_data_with_clusters.csv', index=False)

print("\n" + "="*80)
print("ARCHIVOS GENERADOS PARA POWER BI:")
print("="*80)
print("1. product_metrics_with_clusters.csv")
print("   - Dataset a nivel producto con clusters asignados")
print("   - Usar para: Vista de Clusters de Productos")
print(f"   - Registros: {len(product_metrics):,}")
print()
print("2. store_analysis_with_clusters.csv")
print("   - Dataset a nivel tienda con mezcla de clusters")
print("   - Usar para: Vista de Mezcla de Clusters por Tienda")
print(f"   - Registros: {len(store_analysis)}")
print()
print("3. store_cluster_analysis.csv")
print("   - Análisis detallado tienda-cluster")
print("   - Usar para: Análisis cruzado tienda-cluster")
print(f"   - Registros: {len(store_cluster_analysis)}")
print()
print("4. original_data_with_clusters.csv")
print("   - Dataset original con clusters asignados")
print("   - Usar para: Análisis detallado y drill-down")
print(f"   - Registros: {len(df_with_clusters):,}")
print()
print("="*80)
print("INSTRUCCIONES PARA POWER BI:")
print("="*80)
print("1. Abrir Power BI Desktop")
print("2. Importar los 4 archivos CSV como fuentes de datos")
print("3. Crear relaciones:")
print("   - product_metrics_with_clusters[Item_Identifier] <-> original_data_with_clusters[Item_Identifier]")
print("   - store_analysis_with_clusters[Outlet_Identifier] <-> original_data_with_clusters[Outlet_Identifier]")
print("   - store_cluster_analysis[Outlet_Identifier] <-> store_analysis_with_clusters[Outlet_Identifier]")
print("4. Crear medidas DAX según sea necesario")
print("5. Diseñar las dos vistas del dashboard:")
print("   - Vista 1: Clusters de Productos")
print("   - Vista 2: Mezcla de Clusters por Tienda")
print("="*80)

