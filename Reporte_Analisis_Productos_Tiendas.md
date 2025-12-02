# Reporte de Análisis: Segmentación de Productos y Análisis por Tienda
## Big Mart Sales Prediction - Business Intelligence

**Fecha del Análisis:** Noviembre 2024  
**Dataset:** Big Mart Sales Prediction (8,523 registros, 1,559 productos únicos, 10 tiendas)  
**Método de Clustering:** K-Means (2 clusters óptimos, Silhouette Score: 0.198)

---

## Resumen Ejecutivo

Este reporte presenta los resultados del análisis de segmentación de productos mediante técnicas de clustering y el análisis de su distribución por tienda. El análisis identifica **2 segmentos principales de productos** basados en su comportamiento de ventas, características y distribución, y analiza cómo cada tienda se posiciona respecto a estos segmentos.

**Hallazgos Clave:**
- Se identificaron 2 clusters de productos con perfiles claramente diferenciados
- Cluster 0: Productos de volumen medio-bajo con mayor diversidad de tipos
- Cluster 1: Productos de alto volumen con enfoque en Snack Foods
- Las tiendas muestran una distribución consistente: ~33-40% Cluster 0, ~60-67% Cluster 1
- La tienda OUT027 lidera en ventas absolutas de ambos clusters

---

## 1. ¿Qué tipos de productos existen en nuestro portafolio?

### Respuesta: Identificación de 2 Segmentos Principales

Mediante el análisis de clustering basado en variables de ventas, precio, distribución y características del producto, se identificaron **2 segmentos principales** en el portafolio:

### **Cluster 0: Productos de Volumen Medio-Bajo (Diversificados)**

**Características Principales:**
- **Ventas Totales Promedio:** $7,351.43 por producto
- **Ventas Totales Acumuladas:** $6,358,991.22 (34.2% del total)
- **Número de Productos:** 865 productos (55.5% del portafolio)
- **Precio Promedio (MRP):** Moderado
- **Distribución:** Presente en múltiples tiendas
- **Tipo de Producto Más Común:** Fruits and Vegetables (116 productos)

**Perfil del Segmento:**
Este cluster representa productos con un perfil de ventas más moderado pero con mayor diversidad en el portafolio. Incluye una amplia gama de categorías de productos, siendo especialmente fuerte en:
- Fruits and Vegetables (116 productos)
- Snack Foods (115 productos)
- Frozen Foods (92 productos)
- Household (86 productos)
- Baking Goods (76 productos)
- Dairy (70 productos)

**Características de Negocio:**
- Mayor diversificación de categorías
- Ventas más estables y distribuidas
- Menor dependencia de productos específicos
- Perfil más balanceado entre diferentes tipos de productos

### **Cluster 1: Productos de Alto Volumen (Enfocados)**

**Características Principales:**
- **Ventas Totales Promedio:** $17,625.55 por producto (2.4x mayor que Cluster 0)
- **Ventas Totales Acumuladas:** $12,232,134.19 (65.8% del total)
- **Número de Productos:** 694 productos (44.5% del portafolio)
- **Precio Promedio (MRP):** Similar al Cluster 0
- **Distribución:** Amplia presencia en tiendas
- **Tipo de Producto Más Común:** Snack Foods (105 productos)

**Perfil del Segmento:**
Este cluster representa los productos de mayor rendimiento en ventas. Aunque tiene menos productos que el Cluster 0, genera significativamente más ingresos. Las categorías principales incluyen:
- Snack Foods (105 productos)
- Fruits and Vegetables (104 productos)
- Household (84 productos)
- Frozen Foods (63 productos)
- Dairy (55 productos)
- Canned (52 productos)

**Características de Negocio:**
- Alto volumen de ventas por producto
- Enfoque en categorías de alto rendimiento
- Mayor contribución a los ingresos totales
- Productos con mejor performance individual

### Comparación de Clusters

| Métrica | Cluster 0 | Cluster 1 | Diferencia |
|---------|-----------|-----------|------------|
| **Productos** | 865 (55.5%) | 694 (44.5%) | +171 productos |
| **Ventas Totales** | $6.36M (34.2%) | $12.23M (65.8%) | Cluster 1: 1.9x más |
| **Ventas Promedio/Producto** | $7,351 | $17,626 | Cluster 1: 2.4x más |
| **Tipo Principal** | Fruits & Vegetables | Snack Foods | Diferente enfoque |

### Conclusiones sobre Tipos de Productos

El portafolio se divide en dos segmentos claramente diferenciados:

1. **Segmento Diversificado (Cluster 0):** Representa más de la mitad de los productos pero genera aproximadamente un tercio de las ventas. Caracterizado por mayor diversidad y estabilidad.

2. **Segmento de Alto Rendimiento (Cluster 1):** Aunque representa menos productos, genera casi dos tercios de las ventas totales. Caracterizado por productos de alto volumen y enfoque en categorías premium.

---

## 2. ¿Qué tiendas venden más de cada tipo de producto?

### Respuesta: Análisis de Distribución por Tienda

### Distribución General por Tienda

Todas las tiendas muestran un patrón similar de distribución entre clusters, con el **Cluster 1 dominando las ventas** (60-67% de las ventas de cada tienda) y el **Cluster 0 representando 33-40%**.

### Top 5 Tiendas por Cluster

#### **Cluster 0 - Productos de Volumen Medio-Bajo:**

| Ranking | Tienda | Ventas Cluster 0 | % de Ventas de la Tienda | Tipo de Tienda | Ubicación |
|---------|--------|------------------|-------------------------|----------------|-----------|
| 1 | **OUT027** | $1,144,607.41 | 33.1% | Supermarket Type3 | Tier 3 |
| 2 | **OUT049** | $772,750.12 | 35.4% | Supermarket Type1 | Tier 1 |
| 3 | **OUT017** | $763,823.07 | 35.2% | Supermarket Type1 | Tier 2 |
| 4 | **OUT035** | $762,624.63 | 33.6% | Supermarket Type1 | Tier 2 |
| 5 | **OUT046** | $744,996.24 | 35.2% | Supermarket Type1 | Tier 1 |

**Observaciones:**
- OUT027 lidera en ventas absolutas del Cluster 0
- Las tiendas Supermarket Type1 dominan el top 5
- El porcentaje de ventas del Cluster 0 varía entre 33-35% en estas tiendas
- Las tiendas Tier 1 y Tier 2 están bien representadas

#### **Cluster 1 - Productos de Alto Volumen:**

| Ranking | Tienda | Ventas Cluster 1 | % de Ventas de la Tienda | Tipo de Tienda | Ubicación |
|---------|--------|------------------|-------------------------|----------------|-----------|
| 1 | **OUT027** | $2,309,318.64 | 66.9% | Supermarket Type3 | Tier 3 |
| 2 | **OUT035** | $1,505,498.30 | 66.4% | Supermarket Type1 | Tier 2 |
| 3 | **OUT013** | $1,435,336.97 | 67.0% | Supermarket Type1 | Tier 3 |
| 4 | **OUT049** | $1,411,219.69 | 64.6% | Supermarket Type1 | Tier 1 |
| 5 | **OUT017** | $1,403,642.22 | 64.8% | Supermarket Type1 | Tier 2 |

**Observaciones:**
- OUT027 también lidera en ventas del Cluster 1, consolidándose como la tienda líder
- El Cluster 1 representa 64-67% de las ventas en estas tiendas
- Supermarket Type1 domina el ranking
- Mezcla de ubicaciones Tier 1, 2 y 3

### Análisis Detallado por Tienda

#### **OUT027 - Supermarket Type3, Tier 3 (Líder Absoluto)**
- **Ventas Totales:** $3,453,926.05
- **Distribución:** 33.1% Cluster 0 | 66.9% Cluster 1
- **Productos:** 485 productos Cluster 0 | 450 productos Cluster 1
- **Características:** La tienda más grande en ventas totales, lidera ambos clusters

#### **OUT035 - Supermarket Type1, Tier 2**
- **Ventas Totales:** $2,268,122.94
- **Distribución:** 33.6% Cluster 0 | 66.4% Cluster 1
- **Productos:** 486 productos Cluster 0 | 444 productos Cluster 1
- **Características:** Segundo lugar en ventas del Cluster 1

#### **OUT013 - Supermarket Type1, Tier 3**
- **Ventas Totales:** $2,142,663.58
- **Distribución:** 33.0% Cluster 0 | 67.0% Cluster 1
- **Productos:** 496 productos Cluster 0 | 436 productos Cluster 1
- **Características:** Mayor porcentaje de Cluster 1 (67%)

#### **OUT049 - Supermarket Type1, Tier 1**
- **Ventas Totales:** $2,183,969.81
- **Distribución:** 35.4% Cluster 0 | 64.6% Cluster 1
- **Productos:** 508 productos Cluster 0 | 422 productos Cluster 1
- **Características:** Mayor porcentaje de Cluster 0 entre las tiendas grandes

#### **OUT017 - Supermarket Type1, Tier 2**
- **Ventas Totales:** $2,167,465.29
- **Distribución:** 35.2% Cluster 0 | 64.8% Cluster 1
- **Productos:** 503 productos Cluster 0 | 423 productos Cluster 1
- **Características:** Balance similar a OUT049

#### **Tiendas Pequeñas (Grocery Stores)**

**OUT010 - Grocery Store, Tier 3:**
- **Ventas Totales:** $188,340.17
- **Distribución:** 37.8% Cluster 0 | 62.2% Cluster 1
- **Características:** Mayor porcentaje de Cluster 0, pero menor volumen total

**OUT019 - Grocery Store, Tier 1:**
- **Ventas Totales:** $179,694.09
- **Distribución:** 40.0% Cluster 0 | 60.0% Cluster 1
- **Características:** Mayor porcentaje de Cluster 0 entre todas las tiendas

### Patrones Identificados

1. **Consistencia en Distribución:** Todas las tiendas muestran una distribución similar (~33-40% Cluster 0, ~60-67% Cluster 1)

2. **Tiendas Líderes:** OUT027 domina en ambos clusters, seguida por tiendas Supermarket Type1

3. **Grocery Stores:** Las tiendas pequeñas (OUT010, OUT019) tienen mayor porcentaje de Cluster 0 pero menor volumen absoluto

4. **Tipo de Tienda:** Supermarket Type1 y Type3 muestran mejor performance que Grocery Stores

5. **Ubicación:** No hay un patrón claro por Tier, las tiendas líderes están distribuidas en diferentes niveles

---

## 3. ¿Qué oportunidades de negocio se observan por tienda/segmento de producto?

### Respuesta: Oportunidades Estratégicas Identificadas

### Oportunidades por Segmento de Producto

#### **Oportunidades para Cluster 0 (Productos Diversificados)**

**1. Optimización de Mix de Productos**
- **Situación:** El Cluster 0 representa 55.5% de los productos pero solo 34.2% de las ventas
- **Oportunidad:** Revisar el portafolio para identificar productos de bajo rendimiento y considerar:
  - Descontinuar productos con ventas marginales
  - Reasignar espacio a productos del Cluster 1
  - Optimizar inventario para reducir costos de almacenamiento

**2. Estrategia de Precios y Promociones**
- **Situación:** Productos con ventas promedio más bajas
- **Oportunidad:** 
  - Implementar estrategias de pricing dinámico
  - Crear paquetes promocionales para impulsar ventas
  - Desarrollar campañas de marketing específicas para categorías como Fruits and Vegetables

**3. Expansión de Categorías Fuertes**
- **Situación:** Fruits and Vegetables y Snack Foods son categorías importantes en ambos clusters
- **Oportunidad:** 
  - Expandir líneas de productos en estas categorías
  - Desarrollar productos premium en estas categorías para migrarlos al Cluster 1

#### **Oportunidades para Cluster 1 (Productos de Alto Rendimiento)**

**1. Protección y Expansión**
- **Situación:** Cluster 1 genera 65.8% de las ventas con solo 44.5% de los productos
- **Oportunidad:**
  - Proteger estos productos asegurando disponibilidad constante
  - Expandir líneas de productos similares
  - Desarrollar nuevos productos siguiendo el perfil del Cluster 1

**2. Optimización de Distribución**
- **Situación:** Productos de alto volumen requieren gestión eficiente
- **Oportunidad:**
  - Optimizar cadena de suministro para estos productos
  - Asegurar presencia en todas las tiendas
  - Negociar mejores términos con proveedores

**3. Desarrollo de Productos Premium**
- **Situación:** Snack Foods es la categoría líder
- **Oportunidad:**
  - Desarrollar variantes premium de productos existentes
  - Explorar nuevas categorías de snacks
  - Crear exclusivas de marca propia

### Oportunidades por Tienda

#### **OUT027 - Oportunidad de Replicación de Modelo**

**Situación:** Líder absoluto en ambos clusters con $3.45M en ventas

**Oportunidades:**
1. **Análisis de Mejores Prácticas:**
   - Documentar estrategias de merchandising
   - Analizar mix de productos óptimo
   - Replicar modelo en otras tiendas

2. **Expansión del Modelo:**
   - Aplicar lecciones aprendidas a tiendas similares
   - Desarrollar playbook de operaciones

3. **Optimización Continua:**
   - Aumentar porcentaje de Cluster 1 si es posible
   - Optimizar espacio para productos de alto rendimiento

#### **Tiendas Supermarket Type1 - Oportunidad de Estandarización**

**Situación:** 6 de las 10 tiendas son Supermarket Type1 y muestran buen rendimiento

**Oportunidades:**
1. **Estandarización de Operaciones:**
   - Crear estándares de mix de productos
   - Desarrollar guías de merchandising
   - Implementar procesos comunes

2. **Optimización Colectiva:**
   - Negociación de compras centralizada
   - Compartir mejores prácticas
   - Análisis comparativo de performance

#### **Grocery Stores (OUT010, OUT019) - Oportunidad de Transformación**

**Situación:** Menor volumen de ventas y mayor dependencia del Cluster 0

**Oportunidades:**
1. **Reformulación de Mix:**
   - Aumentar presencia de productos Cluster 1
   - Reducir SKUs de bajo rendimiento
   - Enfocarse en productos de alto volumen

2. **Estrategia de Ubicación:**
   - Evaluar si la ubicación justifica el formato actual
   - Considerar conversión a Supermarket Type1 si es viable
   - Optimizar espacio disponible

3. **Enfoque en Eficiencia:**
   - Reducir costos operativos
   - Optimizar inventario
   - Mejorar rotación de productos

#### **OUT018 y OUT045 - Oportunidad de Crecimiento**

**Situación:** Tiendas con buen rendimiento pero con potencial de mejora

**Oportunidades:**
1. **Alineación con Líderes:**
   - Analizar diferencias con OUT027
   - Implementar estrategias probadas
   - Ajustar mix de productos

2. **Optimización de Espacio:**
   - Reasignar espacio a productos Cluster 1
   - Mejorar presentación de productos premium
   - Optimizar layout de tienda

### Oportunidades Transversales

#### **1. Estrategia de Diversificación vs. Concentración**

**Análisis:**
- Cluster 0: Mayor diversidad pero menor rendimiento
- Cluster 1: Menor diversidad pero mayor rendimiento

**Recomendación:**
- **Estrategia Híbrida:** Mantener diversidad en Cluster 0 para estabilidad, pero aumentar peso de Cluster 1 para crecimiento
- **Target:** Llegar a 50-50% en ventas entre clusters optimizando el portafolio

#### **2. Desarrollo de Nuevos Productos**

**Oportunidad:**
- Desarrollar productos que combinen características de ambos clusters
- Crear productos premium en categorías del Cluster 0
- Expandir categorías exitosas del Cluster 1

#### **3. Optimización de Cadena de Suministro**

**Oportunidad:**
- Diferentes estrategias de inventario por cluster
- Cluster 1: Inventario justo a tiempo, alta rotación
- Cluster 0: Inventario optimizado, menor rotación aceptable

#### **4. Estrategia de Marketing Diferenciada**

**Oportunidad:**
- **Cluster 1:** Marketing de volumen, promociones agresivas
- **Cluster 0:** Marketing de nicho, educación del consumidor
- Campañas específicas por tipo de producto y tienda

#### **5. Análisis de Rentabilidad por Cluster**

**Oportunidad Crítica:**
- Analizar márgenes de ganancia por cluster (no solo ventas)
- Identificar si Cluster 1 tiene mejores márgenes
- Optimizar mix considerando rentabilidad, no solo volumen

### Plan de Acción Recomendado

#### **Corto Plazo (1-3 meses):**
1. Analizar rentabilidad por cluster y producto
2. Identificar productos de bajo rendimiento en Cluster 0
3. Optimizar mix en Grocery Stores
4. Documentar mejores prácticas de OUT027

#### **Mediano Plazo (3-6 meses):**
1. Implementar estrategias de pricing diferenciadas
2. Reasignar espacio en tiendas según clusters
3. Desarrollar campañas de marketing específicas
4. Optimizar cadena de suministro por cluster

#### **Largo Plazo (6-12 meses):**
1. Desarrollar nuevos productos basados en perfiles de clusters
2. Expandir categorías exitosas
3. Replicar modelo de OUT027 en otras tiendas
4. Transformar Grocery Stores o considerar cierre/relocalización

---

## Conclusiones Finales

### Resumen de Respuestas a las Preguntas de Negocio

**1. ¿Qué tipos de productos existen en nuestro portafolio?**
- **Respuesta:** Dos segmentos principales identificados:
  - **Cluster 0:** Productos diversificados de volumen medio-bajo (55.5% productos, 34.2% ventas)
  - **Cluster 1:** Productos de alto volumen y rendimiento (44.5% productos, 65.8% ventas)

**2. ¿Qué tiendas venden más de cada tipo de producto?**
- **Respuesta:** 
  - **Cluster 0:** OUT027 lidera ($1.14M), seguida por OUT049, OUT017, OUT035, OUT046
  - **Cluster 1:** OUT027 también lidera ($2.31M), seguida por OUT035, OUT013, OUT049, OUT017
  - Todas las tiendas muestran distribución similar: ~33-40% Cluster 0, ~60-67% Cluster 1

**3. ¿Qué oportunidades de negocio se observan por tienda/segmento de producto?**
- **Respuesta:** Múltiples oportunidades identificadas:
  - Optimización de portafolio (reducir Cluster 0, expandir Cluster 1)
  - Replicación del modelo de OUT027
  - Transformación de Grocery Stores
  - Estrategias diferenciadas de pricing y marketing
  - Desarrollo de nuevos productos basados en perfiles exitosos

### Recomendación Estratégica Principal

**Enfoque Dual:**
1. **Proteger y expandir Cluster 1** (generador de 65.8% de ventas)
2. **Optimizar Cluster 0** (reducir productos de bajo rendimiento, mantener diversidad estratégica)

**Meta:** Lograr un balance 50-50% en ventas entre clusters mediante optimización del portafolio, manteniendo la diversidad necesaria para estabilidad del negocio.

---

**Reporte generado por:** Sistema de Business Intelligence  
**Metodología:** Clustering K-Means con análisis de segmentación  
**Próximos pasos:** Implementación de recomendaciones y seguimiento de KPIs

