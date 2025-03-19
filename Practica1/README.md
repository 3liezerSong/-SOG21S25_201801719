# Practica 1 Sistemas Organizacionales y Gerenciales 2


#### Integrantes

|Nombre                             |Carnet        |
|-----------------------------------|--------------|
|Luis David Garcia Alay             |201612511     |
|Eliezer Abraham Zapeta Alvarafo	|201801719     |


# Documentacion

## Planificación del Proyecto: Análisis de Ventas en Línea
- Inicio: 8 de marzo
- Finalización prevista: 20 de marzo
- Equipo: 2 miembros

### División de Tareas entre los Miembros del Equipo

![PLanificacion de tareas parctica 1](./img/Planificacion.png)


### Herramientas y Tecnologías Utilizadas
- **Lenguaje de programación: Python 🐍**
- **Base de datos: AWS RDS (MySQL) ☁**
- **Bibliotecas para análisis y visualización:**
- **Pandas 📊 (Manejo de datos)**
- **Matplotlib y Seaborn 📈 (Visualización)**
- **Scikit-learn 🤖 (Análisis de correlación)**
- **Entorno de desarrollo: Python / VS Code**
- **Control de versiones: GitHub**

**Razón de elección:**
- Python: Fácil manejo de datos y amplia compatibilidad con bibliotecas de análisis.
- AWS RDS: Permite escalabilidad y acceso remoto a la base de datos.
- Matplotlib y Seaborn: Facilitan la generación de gráficos detallados.

### Establecimiento de Plazos

🗓 Fases del Proyecto y Cronograma

📅 Semana 1 (8 - 12 de marzo):
✅ Preparación de datos (extracción, limpieza y carga en AWS).
✅ Exploración inicial de los datos.

📅 Semana 2 (13 - 17 de marzo):
✅ Análisis de tendencias y segmentación de clientes.
✅ Identificación de correlaciones y generación de gráficos.
✅ Generación de conclusiones y recomendaciones.

📅 Semana 3 (18 - 20 de marzo):
✅ Revisión y optimización del código.
✅ Preparación del informe final y presentación.
✅ Entrega del proyecto el 20 de marzo.

--------------------------------------------------------
## Proceso de Analisis
#### 📌 Manual de Análisis de Datos: Ventas en Línea

##### **1️⃣ Enfoque Paso a Paso para la Limpieza y Preparación de los Datos**

###### **📌 Paso 1: Extracción de Datos**  
**Fuente:** Archivo CSV `ventas_tienda_online.csv`  
**Acción:** Se cargaron los datos en un DataFrame de Pandas utilizando:

```python
import pandas as pd
df = pd.read_csv("ventas_tienda_online.csv")
```

---

###### **📌 Paso 2: Identificación de Problemas en los Datos**  
Se verificaron los siguientes aspectos:

```python
print(df.isnull().sum())  # Valores nulos
print(df.duplicated().sum())  # Datos duplicados
print(df.dtypes)  # Tipos de datos
```

---

###### **📌 Paso 3: Limpieza y Corrección de Datos**  

| Problema Detectado | Solución Implementada |
|--------------------|----------------------|
| **Valores nulos en `customer_gender`, `product_category`, `payment_method`** | Se llenaron con la moda (valor más frecuente). |
| **Valores nulos en `customer_age`** | Se llenaron con la mediana de la edad. |
| **Valores nulos en `product_price`** | Se reemplazaron con la media del precio. |
| **Datos duplicados** | Se eliminaron usando `df.drop_duplicates()`. |
| **Formato de fecha incorrecto (`purchase_date`)** | Se convirtió a `datetime` con `pd.to_datetime()`. |

✅ **Código de limpieza:**

```python
df.drop_duplicates(inplace=True)
df.fillna({
    'customer_gender': df['customer_gender'].mode()[0],
    'customer_age': df['customer_age'].median(),
    'product_category': df['product_category'].mode()[0],
    'product_price': df['product_price'].mean()
}, inplace=True)
df['purchase_date'] = pd.to_datetime(df['purchase_date'], dayfirst=True)
```

✅ **Resultado:** Datos limpios y listos para el análisis.  

---

##### **2️⃣ Decisiones Tomadas Durante el Análisis Exploratorio de Datos**  

###### **📌 Análisis Inicial**  
✅ Se calcularon **estadísticas básicas**:

```python
print(df.describe())
```

✅ Se realizaron **visualizaciones** para identificar patrones:

- **Ventas por categoría de producto** 📊
- **Ventas por región** 🌎
- **Tendencias de ventas por mes** 📅

✅ **Decisiones Claves:**
1. **Segmentación de clientes** por edad (`0-18`, `19-25`, `26-35`, etc.).
2. Identificación de **productos más vendidos**.
3. **Relación entre métodos de pago y categorías de productos**.
4. Determinación de **meses con mayores y menores ventas**.

---

##### **3️⃣ Desafíos Encontrados y Cómo Fueron Superados**  

###### **📌 1. Datos Incompletos o Nulos**  
🔴 **Problema:** Algunas columnas tenían valores faltantes.  
✅ **Solución:** Se rellenaron con valores estadísticos (moda, mediana, media).  

---

###### **📌 2. Formato de Fechas Incorrecto**  
🔴 **Problema:** `purchase_date` estaba en un formato no estándar.  
✅ **Solución:** Se convirtió a `datetime` con `dayfirst=True`.  

---

###### **📌 3. Volumen de Datos y Tiempo de Procesamiento**  
🔴 **Problema:** Algunas consultas demoraban demasiado al analizar tendencias.  
✅ **Solución:** Se optimizaron cálculos con `groupby()` y `sum()`.  

```python
df.groupby('month')['order_total'].sum()
```

---

###### **📌 4. Visualización de Datos con Categorías Mixtas**  
🔴 **Problema:** Algunas categorías tenían muchas subcategorías, dificultando la visualización.  
✅ **Solución:** Se agruparon y se usaron gráficos de **barras y dispersión**.

```python
import seaborn as sns
sns.barplot(x=df['product_category'], y=df['order_total'], estimator=sum)
```

---

###### **📌 5. Análisis de Correlación**  
🔴 **Problema:** No se podía calcular correlación directamente entre `product_category` y `payment_method`.  
✅ **Solución:** Se usaron gráficos de **conteo (`sns.countplot()`)**.

```python
sns.countplot(x=df['product_category'], hue=df['payment_method'])
```


--------------------------------------
## 📌 Metodología: Selección de Visualizaciones en el Análisis de Datos

### **1️⃣ Introducción**

En este documento se describe la metodología utilizada para seleccionar las visualizaciones más apropiadas en el análisis de los datos de ventas en línea. La selección de gráficos se basó en la naturaleza de los datos y el tipo de información que se quería comunicar.

### **2️⃣ Criterios para la Selección de Visualizaciones**

Para elegir las visualizaciones, consideramos los siguientes factores:

- **Tipo de variable**: Numérica o categórica.
- **Objetivo del análisis**: Comparación, distribución, tendencia o correlación.
- **Claridad y facilidad de interpretación**: La visualización debía ser comprensible para diferentes públicos.

### **3️⃣ Tipos de Visualizaciones y su Justificación**

| **Tipo de Gráfico** | **Uso en el Proyecto** | **Justificación** |
|--------------------|---------------------|------------------|
| **Gráfico de Barras** | Ventas por categoría de producto y región | Permite comparar valores categóricos de manera clara y rápida. |
| **Gráfico de Líneas** | Tendencia de ventas por mes | Muestra la evolución de las ventas en el tiempo, identificando picos y bajas. |
| **Gráfico de Dispersión** | Relación entre edad del cliente y total de la orden | Facilita la detección de patrones y correlaciones entre dos variables numéricas. |
| **Gráfico de Barras Apiladas** | Método de pago por categoría de producto | Permite ver la distribución de métodos de pago dentro de cada categoría. |
| **Gráfico de Pastel** | Distribución de ventas por género | Ayuda a visualizar proporciones de una variable categórica. |
| **Gráfico de Histogramas** | Distribución de edades de los clientes | Muestra la frecuencia de valores dentro de rangos específicos. |
| **Heatmap (Mapa de Calor)** | Matriz de correlación entre variables numéricas | Resalta relaciones entre múltiples variables de forma visualmente efectiva. |


### **4️⃣ Aplicación de Visualizaciones en el Análisis**

#### **📊 1. Comparación de Ventas por Categoría de Producto**
✅ **Visualización utilizada:** Gráfico de Barras  
✅ **Motivo:** Permite comparar rápidamente las ventas entre categorías.

```python
import seaborn as sns
import matplotlib.pyplot as plt

plt.figure(figsize=(12, 6))
sns.barplot(x=df['product_category'], y=df['order_total'], estimator=sum, ci=None)
plt.title("Ventas por Categoría de Producto")
plt.xlabel("Categoría")
plt.ylabel("Total de Ventas")
plt.xticks(rotation=45)
plt.show()
```

---

#### **📉 2. Tendencia de Ventas por Mes**
✅ **Visualización utilizada:** Gráfico de Líneas  
✅ **Motivo:** Muestra la evolución de las ventas en el tiempo.

```python
df['month'] = df['purchase_date'].dt.month_name()
ventas_por_mes = df.groupby('month')['order_total'].sum()

plt.figure(figsize=(12, 6))
plt.plot(ventas_por_mes.index, ventas_por_mes.values, marker='o', linestyle='-')
plt.title("Tendencia de Ventas por Mes")
plt.xlabel("Mes")
plt.ylabel("Total de Ventas")
plt.xticks(rotation=45)
plt.show()
```

#### **📌 3. Relación entre Edad del Cliente y Total de la Orden**
✅ **Visualización utilizada:** Gráfico de Dispersión  
✅ **Motivo:** Permite visualizar tendencias y correlaciones.

```python
plt.figure(figsize=(8, 6))
sns.scatterplot(x=df['customer_age'], y=df['order_total'], alpha=0.5)
plt.title("Relación entre Edad y Total de la Orden")
plt.xlabel("Edad del Cliente")
plt.ylabel("Total de la Orden")
plt.show()
```


#### **📌 4. Método de Pago Preferido por Categoría de Producto**
✅ **Visualización utilizada:** Gráfico de Barras Apiladas  
✅ **Motivo:** Muestra la distribución de métodos de pago en cada categoría.

```python
plt.figure(figsize=(12, 6))
sns.countplot(x=df['product_category'], hue=df['payment_method'])
plt.title("Método de Pago por Categoría de Producto")
plt.xlabel("Categoría")
plt.ylabel("Frecuencia")
plt.xticks(rotation=45)
plt.legend(title="Método de Pago")
plt.show()
```


### **5️⃣ Conclusión**

✔ **Cada tipo de gráfico se seleccionó en función del tipo de datos y el objetivo del análisis.**  
✔ **Se priorizó la claridad, la facilidad de interpretación y la efectividad en la comunicación de los hallazgos.**  
✔ **El uso de diferentes visualizaciones permitió entender mejor el comportamiento de los clientes y las ventas.**  

🚀 **Este enfoque optimizó el análisis y permitió extraer insights valiosos para la toma de decisiones.**
 

