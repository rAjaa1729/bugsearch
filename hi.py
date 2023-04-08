from newapp import User
import mysql.connector
def get_db_connection():
    mydb = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password= "sql@Prism1920",
        database = "BugSearch"
    )
    return mydb
my_db=get_db_connection()
email_id="rajaprismsagar001@gmail.com"
cursor = my_db.cursor(dictionary=True)
query = "SELECT * FROM Users WHERE email_id = %s"
cursor.execute(query, (email_id,))
row = cursor.fetchone()
cursor.close()
user=User(**row)
print(user.username)