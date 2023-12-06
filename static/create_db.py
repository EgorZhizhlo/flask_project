import mysql.connector


# admin_key: 7dY5syEJUMWUA6zT8e9BLYCwtirEYNfdJob1kxDThmJ4Tg6hwe880mM9Yi39KrYY57XezpsCRIv5Wb6zSFBiHAcSnEcVPmj5d1LL

def sql_database():
    config = {
        'user': 'root',
        'password': 'NeforMAL_1488',
        'host': 'db',
        'port': '3306',
        'database': 'flask_db',
    }
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    my_cursor = mydb.cursor()
    my_cursor.execute("CREATE DATABASE IF NOT EXISTS flask_db;")
    my_cursor.execute("USE flask_db;")
    return 0