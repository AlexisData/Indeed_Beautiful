import mysql.connector as mysql
import config

print("Creating Indeed Database Tables...")

HOST = config.HOST
USER = config.USER
PASSWD = config.PASSWD

db = mysql.connect(
    host = HOST,
    user = USER,
    passwd = PASSWD,
    database = "indeed")

mycursor = db.cursor()


mycursor.execute('CREATE TABLE jobs '
                 '(job_id INT(6) NOT NULL AUTO_INCREMENT PRIMARY KEY,'
                 'job_indeed_id VARCHAR(16), '
                 'contract_type VARCHAR(25), ' #Affiner
                 'job_posting_date DATETIME, '
                 'candidate_link VARCHAR(1000),' #Affiner
                 'salary VARCHAR(25),' # Affiner
                 'localisation_id INT(6),' #FK
                 'company_id INT(6),' #FK
                 'job_description_id INT(6));') # FK

print("Table jobs created")

mycursor.execute('CREATE TABLE companies '
                 '(company_id INT(6) NOT NULL AUTO_INCREMENT PRIMARY KEY,'
                 'name VARCHAR(100), ' #Vérifier
                 'rating_score FLOAT(2,1), '
                 'rating_count INT(7));')

print("Table companies created")

mycursor.execute('CREATE TABLE localisation '
                 '(localisation_id INT(6) NOT NULL AUTO_INCREMENT PRIMARY KEY,'
                 'localisation VARCHAR(50));') #Affiner

print("Table localisation created")

mycursor.execute('CREATE TABLE jobs_description '
                 '(job_description_id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,'
                 'job_description VARCHAR(10000));') #Affiner

print("Table jobs description created")

print("...Indeed Database Tables Created")
