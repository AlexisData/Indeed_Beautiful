"""
Script to create MySQL db Indeed
"""
import mysql.connector as mysql
import config

def create_database():
    """
    Create Indeed db
    """
    print("Creating Indeed Database...")

    HOST = config.HOST
    USER = config.USER
    PASSWD = config.PASSWD

    db = mysql.connect(
        host = HOST,
        user = USER,
        passwd = PASSWD)

    mycursor = db.cursor()
    mycursor.execute("DROP DATABASE indeed")
    mycursor.execute("CREATE DATABASE indeed")

    print("...Indeed Database creation OK !")

create_database()
