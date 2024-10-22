
CREATE TABLE customers (
CustomerID SERIAL PRIMARY KEY, 
CustomerName varchar(100) DEFAULT NULL, 
ContactName varchar(100) DEFAULT NULL, 
City varchar(100) DEFAULT NULL, 
Address varchar(100) DEFAULT NULL, 
PostalCode varchar(10) DEFAULT NULL, 
Country varchar(100) DEFAULT NULL);
COPY public.customers FROM '/tmp/customers.csv' DELIMITER ';' CSV HEADER;

CREATE TABLE categories( 
CategoryID SERIAL PRIMARY KEY, 
CategoryName varchar(100) DEFAULT NULL, 
Description text DEFAULT NULL);
COPY public.categories FROM '/tmp/categories.csv' DELIMITER ';' CSV HEADER;

CREATE TABLE employees( 
EmployeeID SERIAL PRIMARY KEY, 
LastName varchar(100) DEFAULT NULL, 
FirstName varchar(100) DEFAULT NULL, 
Date varchar(25) DEFAULT NULL, 
Photo bytea DEFAULT NULL, 
Notes text DEFAULT NULL);
COPY public.employees FROM '/tmp/employees.csv' DELIMITER ';' CSV HEADER;

CREATE TABLE shippers( 
ShipperID SERIAL PRIMARY KEY, 
ShipperName varchar(100) DEFAULT NULL, 
Phone varchar(20) DEFAULT NULL);
COPY public.shippers FROM '/tmp/shippers.csv' DELIMITER ';' CSV HEADER;

CREATE TABLE orders( 
OrderID SERIAL PRIMARY KEY, 
CustomerID  int REFERENCES customers(CustomerID), 
EmployeeID int REFERENCES employees(EmployeeID), 
OrderDate varchar(25) DEFAULT NULL, 
ShipperID int REFERENCES shippers(ShipperID));
COPY public.orders FROM '/tmp/orders.csv' DELIMITER ';' CSV HEADER;

CREATE TABLE suppliers( 
SupplierID SERIAL PRIMARY KEY, 
SupplierName varchar(100) DEFAULT NULL, 
ContactName varchar(100) DEFAULT NULL, 
Address varchar(100) DEFAULT NULL, 
City varchar(100) DEFAULT NULL, 
PostalCode varchar(10) DEFAULT NULL, 
Country varchar(100) DEFAULT NULL, 
Phone varchar(20) DEFAULT NULL);
COPY public.suppliers FROM '/tmp/suppliers.csv' DELIMITER ';' CSV HEADER;

CREATE TABLE products( 
ProductID SERIAL PRIMARY KEY, 
ProductName varchar(100) DEFAULT NULL, 
SupplierID int REFERENCES suppliers(SupplierID), 
CategoryID int REFERENCES categories(CategoryID), 
Unit varchar(50) DEFAULT NULL, 
Price decimal(10, 2) DEFAULT NULL);
COPY public.products FROM '/tmp/products.csv' DELIMITER ';' CSV HEADER;

CREATE TABLE orderDetails( 
OrderDetailID SERIAL PRIMARY KEY, 
OrderID int REFERENCES orders(OrderID), 
ProductID int REFERENCES products(ProductID), 
Quantity int DEFAULT NULL);
COPY public.orderDetails FROM '/tmp/orderDetails.csv' DELIMITER ';' CSV HEADER;