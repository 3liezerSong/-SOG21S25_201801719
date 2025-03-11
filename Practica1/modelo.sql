CREATE DATABASE IF NOT EXISTS ecommerce_data;
USE ecommerce_data;

CREATE TABLE IF NOT EXISTS gender (
    gender_id INT PRIMARY KEY AUTOINCREMENTAL,
    gender_name VARCHAR(20)
);

CREATE TABLE IF NOT EXISTS customer (
    customer_id INT PRIMARY KEY,
    gender_id INT,
    customer_age INT,
    FOREIGN KEY (gender_id) REFERENCES gender(gender_id)
);

CREATE TABLE IF NOT EXISTS product (
    product_name VARCHAR(150) PRIMARY KEY,
    product_category VARCHAR(50),
    product_price DECIMAL(10, 2)
);

CREATE TABLE IF NOT EXISTS order (
    order_id INT PRIMARY KEY,
    purchase_date DATE,
    customer_id INT,
    order_total DECIMAL(10, 2),
    payment_method VARCHAR(50),
    shipping_region VARCHAR(100),
    FOREIGN KEY (customer_id) REFERENCES customer(customer_id)
);

CREATE TABLE IF NOT EXISTS order_detail (
    order_id INT,
    product_name VARCHAR(255),
    quantity INT,
    PRIMARY KEY (order_id, product_name),
    FOREIGN KEY (order_id) REFERENCES order(order_id),
    FOREIGN KEY (product_name) REFERENCES product(product_name)
);


-- SQL SERVER

query2 = '''
    use practica1;

    CREATE TABLE gender (
        gender_id INT PRIMARY KEY IDENTITY(1,1),
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
        product_price DECIMAL(10, 2)
    );

    CREATE TABLE [order] (
        order_id INT PRIMARY KEY,
        purchase_date DATE,
        customer_id INT,
        order_total DECIMAL(10, 2),
        payment_method VARCHAR(50),
        shipping_region VARCHAR(100),
        FOREIGN KEY (customer_id) REFERENCES customer(customer_id)
    );

    CREATE TABLE order_detail (
        order_id INT,
        product_name VARCHAR(255),
        quantity INT NOT NULL,
        PRIMARY KEY (order_id, product_name),
        FOREIGN KEY (order_id) REFERENCES [order](order_id),
        FOREIGN KEY (product_name) REFERENCES product(product_name)
    );
'''
