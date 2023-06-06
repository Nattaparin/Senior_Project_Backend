import mysql.connector
connection = mysql.connector.connect(
    host="your_host",
    port="your_port",
    user="root",
    password="marty1234",
    database="your_database"
)
cursor = connection.cursor()
# Select all rows from a table
#cursor.execute("SELECT * FROM your_table")
#rows = cursor.fetchall()

# for row in rows:
#     print(row)
# cursor.close()
# connection.close()
