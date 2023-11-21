import mysql.connector

conn = mysql.connector.connect(
    host = "localhost",
    database = "bajanproject",
    user = "root",
    password = "root"
)

cursor = conn.cursor()