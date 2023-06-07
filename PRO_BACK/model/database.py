import mysql.connector
connection = mysql.connector.connect(
    host="localhost",
    port="3306",
    user="root",
    password="marty1234",
    database="pro"
)
cursor = connection.cursor()
# # Select all rows from a table
# cursor.execute("SELECT * FROM pro.admin")
# rows = cursor.fetchall()
#
# for row in rows:
#     print(row)
# cursor.close()
# connection.close()
