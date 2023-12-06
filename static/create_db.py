import mysql.connector

# admin_key: 7dY5syEJUMWUA6zT8e9BLYCwtirEYNfdJob1kxDThmJ4Tg6hwe880mM9Yi39KrYY57XezpsCRIv5Wb6zSFBiHAcSnEcVPmj5d1LL

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