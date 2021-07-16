import mysql.connector as mysql
import config

HOST = config.HOST
USER = config.USER
PASSWD = config.PASSWD

db = mysql.connect(
    host=HOST,
    user=USER,
    passwd=PASSWD,
    database="indeed")

mycursor = db.cursor()

def create_companies_table():
    mycursor.execute('CREATE TABLE companies '
                     '(company_id INT(6) NOT NULL AUTO_INCREMENT PRIMARY KEY,'
                     'name VARCHAR(100), '
                     'rating_score FLOAT(2,1), '
                     'rating_count INT(7));')

    print("Table companies created")

def create_localisation_table():
    mycursor.execute('CREATE TABLE localisation '
                     '(localisation_id INT(6) NOT NULL AUTO_INCREMENT PRIMARY KEY,'
                     'localisation VARCHAR(50));')

    print("Table localisation created")

def create_job_description_table():
    mycursor.execute('CREATE TABLE jobs_description '
                     '(job_description_id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,'
                     'job_description VARCHAR(10000));')

    print("Table jobs description created")

def create_jobs_table():
    mycursor.execute('CREATE TABLE jobs '
                     '(job_id INT(6) NOT NULL AUTO_INCREMENT PRIMARY KEY,'
                     'job_indeed_id VARCHAR(16), '
                     'contract_type VARCHAR(25), '
                     'job_posting_date DATETIME, '
                     'candidate_link VARCHAR(1000),'
                     'salary VARCHAR(25),'
                     'localisation_id INT(6), FOREIGN KEY (localisation_id) REFERENCES localisation(localisation_id),'
                     'company_id INT(6), FOREIGN KEY (company_id) REFERENCES companies(company_id),'
                     'job_description_id INT(6), FOREIGN KEY (job_description_id) REFERENCES jobs_description(job_description_id));')

    print("Table jobs created")


print("Creating Indeed Database Tables...")
create_companies_table()
create_localisation_table()
create_job_description_table()
create_jobs_table()
print("...Indeed Database Tables Created")
