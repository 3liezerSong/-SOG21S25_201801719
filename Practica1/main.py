from conexion import conectar_bd
import pandas as pd
import pyodbc

import matplotlib.pyplot as plt
import seaborn as sns

df_global = None
dimensiones_global = None

def borrar_db():
    query = '''use master;
               ALTER DATABASE practica1 SET SINGLE_USER WITH ROLLBACK IMMEDIATE;
               DROP DATABASE practica1;'''

    conn = conectar_bd() 
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute(query)
            print("\033[32mBase de datos borrada con éxito.\033[0m")
        except Exception as error:
            print("\033[31mERROR AL BORRAR LA BASE DE DATOS: {}\033[0m".format(error))
        finally:
            conn.close()
    else:
        print("\033[31mNo se pudo conectar a la base de datos.\033[0m")


def crear_modelo():
    query = ''' use master;
                IF NOT EXISTS (SELECT name FROM sys.databases WHERE name = 'practica1')
                BEGIN
                    CREATE DATABASE practica1;
	            END; 
            '''
    query2 =''' use practica1;

                CREATE TABLE gender (
                    gender_id INT IDENTITY(1,1) PRIMARY KEY,
                    gender_name VARCHAR(20) NOT NULL
                );

                CREATE TABLE customer (
                    customer_id INT PRIMARY KEY,
                    gender_id INT NOT NULL, 
                    customer_age INT NOT NULL,
                    FOREIGN KEY (gender_id) REFERENCES gender(gender_id)
                );

                CREATE TABLE product (
                    product_name VARCHAR(150) PRIMARY KEY,
                    product_category VARCHAR(50),
                    product_price DECIMAL(10, 4) DEFAULT 0
                );

                CREATE TABLE [order] (
                    order_id INT PRIMARY KEY,
                    purchase_date DATE,
                    customer_id INT,
                    order_total DECIMAL(10, 4) DEFAULT 0,
                    payment_method VARCHAR(50),
                    shipping_region VARCHAR(100),
                    FOREIGN KEY (customer_id) REFERENCES customer(customer_id)
                );

                CREATE TABLE order_detail (
                    order_id INT,
                    product_name VARCHAR(150),
                    quantity INT NOT NULL,
                    PRIMARY KEY (order_id, product_name),
                    FOREIGN KEY (order_id) REFERENCES [order](order_id),
                    FOREIGN KEY (product_name) REFERENCES product(product_name)
                );    
            ''' 
    try:
        conn = conectar_bd()
        if conn is None:
            print("\033[31mNo se pudo conectar a la base de datos.\033[0m")
            return

        cursor = conn.cursor()

        cursor.execute("SELECT name FROM sys.databases WHERE name = 'practica1'")
        db_exists = cursor.fetchone()
        if db_exists:
            print("\033[33mLa base de datos 'practica1' ya existe.\033[0m")
        else:
            cursor.execute(query)
            print("\033[32mBase de datos 'practica1' creada exitosamente.\033[0m")

        cursor.execute(query2)  
        print("\033[32mTablas creadas exitosamente.\033[0m")

    except pyodbc.Error as error:
        print("\033[31mERROR AL CREAR BASE DE DATOS O TABLAS: {}\033[0m".format(error))

    finally:
        if conn:
            conn.close()

##Creación de funciones para la visualización de datos

def visualizar_datos(df):
    plt.figure(figsize=(12, 6))
    sns.barplot(x=df['product_category'], y=df['order_total'], estimator=sum, ci=None)
    plt.title("Distribución de Ventas por Categoría de Producto")
    plt.xlabel("Categoría del Producto")
    plt.ylabel("Total de Ventas")
    plt.xticks(rotation=45)
    plt.show()
    
    plt.figure(figsize=(12, 6))
    sns.barplot(x=df['shipping_region'], y=df['order_total'], estimator=sum, ci=None)
    plt.title("Distribución de Ventas por Región")
    plt.xlabel("Región de Envío")
    plt.ylabel("Total de Ventas")
    plt.xticks(rotation=45)
    plt.show()

def calcular_estadisticas(df):
    print("\nEstadísticas para variables numéricas:")
    columnas_numericas = df.select_dtypes(include=['number'])
    estadisticas = columnas_numericas.agg(['mean', 'median', lambda x: x.mode().iloc[0] if not x.mode().empty else None])
    estadisticas.rename(index={'<lambda>': 'mode'}, inplace=True)
    print(estadisticas)
    return estadisticas

def analizar_tendencias(df):
    df['month'] = df['purchase_date'].dt.month_name()
    ventas_por_mes = df.groupby('month')['order_total'].sum().sort_values()
    
    print("\nMeses con menores ventas:")
    print(ventas_por_mes.head(3))
    print("\nMeses con mayores ventas:")
    print(ventas_por_mes.tail(3))
    
    plt.figure(figsize=(12, 6))
    sns.barplot(x=ventas_por_mes.index, y=ventas_por_mes.values)
    plt.title("Ventas Totales por Mes")
    plt.xlabel("Mes")
    plt.ylabel("Total de Ventas")
    plt.xticks(rotation=45)
    plt.show()
    
    productos_vendidos = df.groupby('product_name')['quantity'].sum().sort_values()
    
    print("\nProductos menos vendidos:")
    print(productos_vendidos.head(5))
    print("\nProductos más vendidos:")
    print(productos_vendidos.tail(5))
    
    plt.figure(figsize=(12, 6))
    sns.barplot(y=productos_vendidos.index[-10:], x=productos_vendidos.values[-10:])
    plt.title("Top 10 Productos Más Vendidos")
    plt.xlabel("Cantidad Vendida")
    plt.ylabel("Producto")
    plt.show()


def segmentar_clientes(df):
    # Agrupar por rangos de edad
    bins = [0, 18, 25, 35, 45, 55, 65, 100]
    labels = ['0-18', '19-25', '26-35', '36-45', '46-55', '56-65', '65+']
    df['age_group'] = pd.cut(df['customer_age'], bins=bins, labels=labels, right=False)
    
    # Análisis de patrones de compra por edad
    ventas_por_edad = df.groupby('age_group')['order_total'].sum()
    print("\nVentas totales por grupo de edad:")
    print(ventas_por_edad)
    
    plt.figure(figsize=(12, 6))
    sns.barplot(x=ventas_por_edad.index, y=ventas_por_edad.values)
    plt.title("Ventas por Grupo de Edad")
    plt.xlabel("Grupo de Edad")
    plt.ylabel("Total de Ventas")
    plt.show()
    
    # Comparar comportamiento de compra entre géneros
    ventas_por_genero = df.groupby('customer_gender')['order_total'].sum()
    print("\nVentas totales por género:")
    print(ventas_por_genero)
    
    plt.figure(figsize=(8, 6))
    sns.barplot(x=ventas_por_genero.index, y=ventas_por_genero.values, palette="coolwarm")
    plt.title("Ventas Totales por Género")
    plt.xlabel("Género")
    plt.ylabel("Total de Ventas")
    plt.show()
    
    
def analizar_correlaciones(df):
    # Correlación entre total de la orden y edad del cliente
    correlacion = df[['customer_age', 'order_total']].corr()
    print("\nCorrelación entre la edad del cliente y el total de la orden:")
    print(correlacion)
    
    plt.figure(figsize=(8, 6))
    sns.scatterplot(x=df['customer_age'], y=df['order_total'], alpha=0.5)
    plt.title("Relación entre Edad del Cliente y Total de la Orden")
    plt.xlabel("Edad del Cliente")
    plt.ylabel("Total de la Orden")
    plt.show()
    
    # Relación entre categoría del producto y método de pago
    plt.figure(figsize=(12, 6))
    sns.countplot(x=df['product_category'], hue=df['payment_method'])
    plt.title("Método de Pago Preferido por Categoría de Producto")
    plt.xlabel("Categoría del Producto")
    plt.ylabel("Frecuencia")
    plt.xticks(rotation=45)
    plt.legend(title="Método de Pago")
    plt.show()
    
def generar_graficos(df):
    plt.figure(figsize=(12, 6))
    sns.barplot(x=df['product_category'], y=df['order_total'], estimator=sum, ci=None)
    plt.title("Distribución de Ventas por Categoría de Producto")
    plt.xlabel("Categoría del Producto")
    plt.ylabel("Total de Ventas")
    plt.xticks(rotation=45)
    plt.show()
    
    plt.figure(figsize=(12, 6))
    sns.barplot(x=df['shipping_region'], y=df['order_total'], estimator=sum, ci=None)
    plt.title("Distribución de Ventas por Región")
    plt.xlabel("Región de Envío")
    plt.ylabel("Total de Ventas")
    plt.xticks(rotation=45)
    plt.show()
    
    df['month'] = df['purchase_date'].dt.month_name()
    ventas_por_mes = df.groupby('month')['order_total'].sum().sort_values()
    plt.figure(figsize=(12, 6))
    sns.lineplot(x=ventas_por_mes.index, y=ventas_por_mes.values, marker='o')
    plt.title("Tendencia de Ventas por Mes")
    plt.xlabel("Mes")
    plt.ylabel("Total de Ventas")
    plt.xticks(rotation=45)
    plt.show()
    
    plt.figure(figsize=(8, 6))
    sns.scatterplot(x=df['customer_age'], y=df['order_total'], alpha=0.5)
    plt.title("Relación entre Edad del Cliente y Total de la Orden")
    plt.xlabel("Edad del Cliente")
    plt.ylabel("Total de la Orden")
    plt.show()
    
    ventas_por_genero = df.groupby('customer_gender')['order_total'].sum()
    plt.figure(figsize=(8, 6))
    sns.barplot(x=ventas_por_genero.index, y=ventas_por_genero.values, palette="coolwarm")
    plt.title("Ventas Totales por Género")
    plt.xlabel("Género")
    plt.ylabel("Total de Ventas")
    plt.show()
    
    productos_vendidos = df.groupby('product_name')['quantity'].sum().sort_values()
    plt.figure(figsize=(12, 6))
    sns.barplot(y=productos_vendidos.index[-10:], x=productos_vendidos.values[-10:])
    plt.title("Top 10 Productos Más Vendidos")
    plt.xlabel("Cantidad Vendida")
    plt.ylabel("Producto")
    plt.show()
    
    plt.figure(figsize=(12, 6))
    sns.countplot(x=df['product_category'], hue=df['payment_method'])
    plt.title("Método de Pago Preferido por Categoría de Producto")
    plt.xlabel("Categoría del Producto")
    plt.ylabel("Frecuencia")
    plt.xticks(rotation=45)
    plt.legend(title="Método de Pago")
    plt.show()
    


def extraer():
    print("\033[H\033[J")
    path = "ventas_tienda_online.csv"
    try:
        df = pd.read_csv(path, delimiter=",", on_bad_lines="skip", engine="python")
        print("\nColumnas leídas desde el archivo CSV:")
        print(df.columns.tolist())  
        print("Número total de registros:", len(df))

        filas_a_mostrar = int(input("¿Cuántas filas te gustaría ver? Ingresa un número: "))

        print("\nPrimeras", filas_a_mostrar, "filas del archivo:")
        print(df.head(filas_a_mostrar))
        input("Presione Enter para continuar...")

        print("\nÚltimas", filas_a_mostrar, "filas del archivo:")
        print(df.tail(filas_a_mostrar))
        input("Presione Enter para continuar...")
        
        ##Visualización de datos
        calcular_estadisticas(df)
        visualizar_datos(df)
        analizar_tendencias(df)
        segmentar_clientes(df)   
        analizar_correlaciones(df)  
        generar_graficos(df)  
        
        
        return df

    except Exception as e:
        print(f"Error al leer el archivo: {e}")
        input("Presione Enter para continuar...")
        return None


def transformar(df):
    print("\033[H\033[J")
    # Asegúrate de que las fechas estén en formato datetime
    df['purchase_date'] = pd.to_datetime(df['purchase_date'], errors='coerce')  # Convierte a datetime, valores no válidos serán NaT
    # Reemplazar valores vacíos o no numéricos en product_price y order_total
    df['product_price'] = pd.to_numeric(df['product_price'], errors='coerce').fillna(0).round(4)
    df['order_total'] = pd.to_numeric(df['order_total'], errors='coerce').fillna(0).round(4)


    df['customer_gender'] = df['customer_gender'].replace(["0", "-", "", pd.NA, None], "Sin definir")
    dim_gender = df[['customer_gender']].drop_duplicates().copy()
    dim_gender['gender_id'] = range(1, len(dim_gender) + 1)
    #dim_gender.rename(columns={'customer_gender': 'gender_name'}, inplace=True)


    df['customer_age'] = df['customer_age'].replace(["0", "-", "", pd.NA, None], 0)
    dim_customer = df[['customer_id', 'customer_gender', 'customer_age', 'purchase_date']].drop_duplicates().copy()
    #dim_customer = df[['customer_id', 'customer_gender', 'customer_age']].drop_duplicates().copy()
    dim_customer = dim_customer.loc[dim_customer.groupby('customer_id')['purchase_date'].idxmax()]
    dim_customer['gender_id'] = dim_customer['customer_gender'].map(dim_gender.set_index('customer_gender')['gender_id'])


    df['product_name'] = df['product_name'].replace(["0", "-", "", pd.NA, None], "Sin definir")
    df['product_category'] = df['product_category'].replace(["0", "-", "", pd.NA, None], "Sin definir")
    dim_product = df[['product_name', 'product_category', 'product_price']].drop_duplicates().copy()
    dim_product = dim_product.drop_duplicates(subset=['product_name'])


    df['payment_method'] = df['payment_method'].replace(["", pd.NA, None], "Sin definir")
    dim_order = df[['order_id', 'purchase_date', 'customer_id', 'order_total', 'payment_method', 'shipping_region']].drop_duplicates().copy()


    df['quantity'] = df['quantity'].replace(["0", "-", "", pd.NA, None], 0)
    dim_order_detail = df[['order_id', 'product_name', 'quantity']].drop_duplicates().copy()


    print("\033[32mDatos transformados exitosamente.\033[0m")
    return dim_gender, dim_customer, dim_product, dim_order, dim_order_detail

def cargar(dimensiones):

    if dimensiones is None:
        print("\033[1;31mError: No hay datos transformados. Primero ejecuta la transformación.\033[0m")
        return

    dim_gender, dim_customer, dim_product, dim_order, dim_order_detail = dimensiones

    try:
        conn = conectar_bd()
        if conn is None:
            print("\033[31mNo se pudo conectar a la base de datos.\033[0m")
            return

        cursor = conn.cursor()
        cursor.fast_executemany = True 
        cursor.execute("USE practica1;")
        conn.autocommit = False
        # Tabla gender
        data_to_insert_gender = [(row['customer_gender'],) for _, row in dim_gender.iterrows()]
        cursor.executemany("""
            INSERT INTO gender (gender_name)
            VALUES (?)
        """, data_to_insert_gender)
        print("cargando gender")
        

        # Tabla customer
        data_to_insert_customer = [(row['customer_id'], row['gender_id'], row['customer_age']) for _, row in dim_customer.iterrows()]
        cursor.executemany("""
            INSERT INTO customer (customer_id, gender_id, customer_age)
            VALUES (?, ?, ?)
        """, data_to_insert_customer)
        print("cargando customer")
        

        # Tabla product
        data_to_insert_product = [(row['product_name'], row['product_category'], row['product_price']) for _, row in dim_product.iterrows()]
        cursor.executemany("""
            INSERT INTO product (product_name, product_category, product_price)
            VALUES (?, ?, ?)
        """, data_to_insert_product)
        print("cargando product")

        # Tabla order
        data_to_insert_order = [(row['order_id'], row['purchase_date'], row['customer_id'], row['order_total'], row['payment_method'], row['shipping_region']) for _, row in dim_order.iterrows()]
        cursor.executemany("""
            INSERT INTO [order] (order_id, purchase_date, customer_id, order_total, payment_method, shipping_region)
            VALUES (?, ?, ?, ?, ?, ?)
        """, data_to_insert_order)
        print("cargando order")

        # Tabla order_detail
        data_to_insert_order_detail = [(row['order_id'], row['product_name'], row['quantity']) for _, row in dim_order_detail.iterrows()]
        cursor.executemany("""
            INSERT INTO order_detail (order_id, product_name, quantity)
            VALUES (?, ?, ?)
        """, data_to_insert_order_detail)
        print("cargando order_detail")

        conn.commit()
        print("\033[32mDatos cargados exitosamente.\033[0m")

    except pyodbc.Error as error:
        print(f"\033[31mError al insertar datos: {error}\033[0m")
        conn.rollback()

    finally:
        if conn:
            conn.close()



def obtener_datos():
    try:
        conn = conectar_bd()
        if conn is None:
            return None

        cursor = conn.cursor()
        cursor.execute("USE practica1;")  # Asegurarse de que estamos usando la base de datos correcta

        query = '''
        SELECT o.order_id, o.purchase_date, o.order_total, p.product_category, o.shipping_region
        FROM [order] o
        JOIN order_detail od ON o.order_id = od.order_id
        JOIN product p ON od.product_name = p.product_name
        '''
        df = pd.read_sql(query, conn)
        conn.close()
        return df

    except pyodbc.Error as e:
        print(f"Error al obtener los datos: {e}")
        return None





if __name__ == "__main__":
    borrar_db()
    crear_modelo()
    df_global = extraer()
    dimensiones_global = transformar(df_global)
    cargar(dimensiones_global)