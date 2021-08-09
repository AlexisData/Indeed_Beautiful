import mysql.connector as mysql
from config import HOST, USER, PASSWD, COMPANIES_TABLE_CREATION, \
    COMPANIES_TABLE_CONFIRMATION, LOCATION_TABLE_CREATION, LOCATION_TABLE_CONFIRMATION, \
    JOBS_DESCRIPTION_TABLE_CREATION, JOBS_DESCRIPTION_TABLE_CONFIRMATION, \
    JOBS_TABLE_CREATION, JOBS_TABLE_CONFIRMATION

db = mysql.connect(
    host=HOST,
    user=USER,
    passwd=PASSWD,
    database="indeed")

mycursor = db.cursor()

def create_companies_table():
    mycursor.execute(COMPANIES_TABLE_CREATION)

    print(COMPANIES_TABLE_CONFIRMATION)

def create_localisation_table():
    mycursor.execute(LOCATION_TABLE_CREATION)

    print(LOCATION_TABLE_CONFIRMATION)

def create_job_description_table():
    mycursor.execute(JOBS_DESCRIPTION_TABLE_CREATION)

    print(JOBS_DESCRIPTION_TABLE_CONFIRMATION)

def create_jobs_table():
    mycursor.execute(JOBS_TABLE_CREATION)

    print(JOBS_TABLE_CONFIRMATION)


print("Creating Indeed Database Tables...")
create_companies_table()
create_localisation_table()
create_job_description_table()
create_jobs_table()
print("...Indeed Database Tables Created")
