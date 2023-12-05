import mysql.connector

mydb = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="NeforMAL_1488",
    auth_plugin='mysql_native_password',
)

my_cursor = mydb.cursor()
my_cursor.execute("CREATE DATABASE IF NOT EXISTS flask_db;")

my_cursor.execute("SHOW DATABASES;")
for db in my_cursor:
    print(db)