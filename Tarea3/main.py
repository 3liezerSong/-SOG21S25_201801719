import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib
import numpy as np

matplotlib.use('Agg')

# Cargar los datos
file_path = "winequality-red.csv" 
df = pd.read_csv(file_path, delimiter=";")

# Limpieza y preparación de datos
print("\nIniciando limpieza de datos...")

# Verificar valores nulos
missing_values = df.isnull().sum()
if missing_values.any():
    print("Valores nulos encontrados. Rellenando con la mediana...")
    df.fillna(df.median(), inplace=True)
else:
    print("No hay valores nulos.")

# 🛠️ Eliminar duplicados
num_duplicados = df.duplicated().sum()
if num_duplicados > 0:
    print(f"Se encontraron {num_duplicados} filas duplicadas. Eliminándolas...")
    df.drop_duplicates(inplace=True)
else:
    print("No hay filas duplicadas.")

# Identificar valores fuera de rango (outliers) usando el método IQR
Q1 = df.quantile(0.25)
Q3 = df.quantile(0.75)
IQR = Q3 - Q1

# Definir umbrales para los valores normales
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

# Contar valores atípicos
outliers = ((df < lower_bound) | (df > upper_bound)).sum()
total_outliers = outliers.sum()

if total_outliers > 0:
    print(f"Se encontraron {total_outliers} valores atípicos. Eliminándolos...")
    df = df[~((df < lower_bound) | (df > upper_bound)).any(axis=1)]
else:
    print("No se encontraron valores atípicos significativos.")

# Verificar tipos de datos y convertir si es necesario
print("\nVerificando tipos de datos...")
print(df.dtypes)

# Asegurar que la columna 'quality' sea tipo e
if df["quality"].dtype != "int64":
    print("Convirtiendo 'quality' a entero...")
    df["quality"] = df["quality"].astype(int)

print("Tipos de datos verificados.")


summary_stats = df.describe()
corr_matrix = df.corr()


# Gráfico 1: Distribución de la calidad del vino
quality_counts = df["quality"].value_counts()
plt.figure(figsize=(8, 5))
sns.countplot(x="quality", data=df, palette="viridis", edgecolor="black")
plt.title("Distribución de la Calidad del Vino", fontsize=14)
plt.xlabel("Calidad del Vino", fontsize=12)
plt.ylabel("Frecuencia", fontsize=12)
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.savefig("quality_distribution.png")
plt.close()

# Gráfico 2: Relación entre alcohol y calidad
alcohol_quality_corr = df[["quality", "alcohol"]].corr().iloc[0, 1]
plt.figure(figsize=(8, 5))
sns.boxplot(x="quality", y="alcohol", data=df, palette="coolwarm", notch=True)
plt.title("Relación entre Alcohol y Calidad del Vino", fontsize=14)
plt.xlabel("Calidad del Vino", fontsize=12)
plt.ylabel("Porcentaje de Alcohol", fontsize=12)
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.savefig("alcohol_quality.png")
plt.close()

# Gráfico 3: Relación entre acidez volátil y calidad
volatile_acidity_quality_corr = df[["quality", "volatile acidity"]].corr().iloc[0, 1]
plt.figure(figsize=(8, 5))
sns.boxplot(x="quality", y="volatile acidity", data=df, palette="magma", notch=True)
plt.title("Relación entre Acidez Volátil y Calidad del Vino", fontsize=14)
plt.xlabel("Calidad del Vino", fontsize=12)
plt.ylabel("Acidez Volátil", fontsize=12)
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.savefig("volatile_acidity_quality.png")
plt.close()

# Gráfico 4: Relación entre el pH y la calidad del vino
pH_quality_corr = df[["quality", "pH"]].corr().iloc[0, 1]
plt.figure(figsize=(8, 5))
sns.boxplot(x="quality", y="pH", data=df, palette="Blues", notch=True)
plt.title("Relación entre pH y Calidad del Vino", fontsize=14)
plt.xlabel("Calidad del Vino", fontsize=12)
plt.ylabel("pH", fontsize=12)
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.savefig("pH_quality.png")
plt.close()

# Gráfico 5: Relación entre ácido cítrico y calidad
citric_acid_quality_corr = df[["quality", "citric acid"]].corr().iloc[0, 1]
plt.figure(figsize=(8, 5))
sns.boxplot(x="quality", y="citric acid", data=df, palette="crest", notch=True)
plt.title("Relación entre Ácido Cítrico y Calidad del Vino", fontsize=14)
plt.xlabel("Calidad del Vino", fontsize=12)
plt.ylabel("Ácido Cítrico", fontsize=12)
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.savefig("citric_acid_quality.png")
plt.close()

# Gráfico 6: Densidad vs Calidad del vino
density_quality_corr = df[["quality", "density"]].corr().iloc[0, 1]
plt.figure(figsize=(8, 5))
sns.boxplot(x="quality", y="density", data=df, palette="PuRd", notch=True)
plt.title("Relación entre Densidad y Calidad del Vino", fontsize=14)
plt.xlabel("Calidad del Vino", fontsize=12)
plt.ylabel("Densidad", fontsize=12)
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.savefig("density_quality.png")
plt.close()
