from conexion import conectar_bd
import pandas as pd
import pyodbc

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


def extraer():
    print("\033[H\033[J")
    path = "C:\\Users\\50255\\Documents\\-SOG21S25_201801719\\Practica1\\ventas_tienda_online.csv"
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
        cursor.execute("USE practica1;")

        # Tabla gender
        data_to_insert_gender = [(row['customer_gender'],) for _, row in dim_gender.iterrows()]
        cursor.executemany("""
            INSERT INTO gender (gender_name)
            VALUES (?)
        """, data_to_insert_gender)
        

        # Tabla customer
        data_to_insert_customer = [(row['customer_id'], row['gender_id'], row['customer_age']) for _, row in dim_customer.iterrows()]
        cursor.executemany("""
            INSERT INTO customer (customer_id, gender_id, customer_age)
            VALUES (?, ?, ?)
        """, data_to_insert_customer)


        # Tabla product
        data_to_insert_product = [(row['product_name'], row['product_category'], row['product_price']) for _, row in dim_product.iterrows()]
        cursor.executemany("""
            INSERT INTO product (product_name, product_category, product_price)
            VALUES (?, ?, ?)
        """, data_to_insert_product)


        # Tabla order
        data_to_insert_order = [(row['order_id'], row['purchase_date'], row['customer_id'], row['order_total'], row['payment_method'], row['shipping_region']) for _, row in dim_order.iterrows()]
        cursor.executemany("""
            INSERT INTO [order] (order_id, purchase_date, customer_id, order_total, payment_method, shipping_region)
            VALUES (?, ?, ?, ?, ?, ?)
        """, data_to_insert_order)


        # Tabla order_detail
        data_to_insert_order_detail = [(row['order_id'], row['product_name'], row['quantity']) for _, row in dim_order_detail.iterrows()]
        cursor.executemany("""
            INSERT INTO order_detail (order_id, product_name, quantity)
            VALUES (?, ?, ?)
        """, data_to_insert_order_detail)

        conn.commit()
        print("\033[32mDatos cargados exitosamente.\033[0m")

    except pyodbc.Error as error:
        print(f"\033[31mError al insertar datos: {error}\033[0m")
        conn.rollback()

    finally:
        if conn:
            conn.close()


if __name__ == "__main__":
    borrar_db()
    crear_modelo()
    df_global = extraer()
    dimensiones_global = transformar(df_global)
    cargar(dimensiones_global)