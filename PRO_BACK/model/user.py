# Replace the placeholders with your MySQL database credentials
import mysql

import mysql.connector
db_connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="marty1234",
    database="pro"
)
