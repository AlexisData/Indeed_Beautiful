import mysql.connector as mysql
from config import HOST, USER, PASSWD

db = mysql.connect(
    host=HOST,
    user=USER,
    passwd=PASSWD,
    auth_plugin='mysql_native_password',
    database="indeed")


def insert_job_informations(job_indeed_id, contract_type, job_posting_date,
                            candidate_link, salary, company_id,
                            localisation_id, job_description_id):
    """
    This function insert provided data in database
    """
    mycursor = db.cursor()
    mycursor.execute(
        'INSERT INTO jobs (job_indeed_id, contract_type, job_posting_date, candidate_link, salary, company_id, localisation_id, job_description_id) values (%s, %s, %s, %s, %s, %s, %s, %s)',
        (job_indeed_id, contract_type, job_posting_date, candidate_link,
         salary, company_id, localisation_id, job_description_id))
    db.commit()
    print("Insert job information about " + job_indeed_id + " OK !")


def insert_company_informations(name, rating_score, rating_count):
    """
    This function insert provided data in database
    """
    mycursor = db.cursor()
    mycursor.execute(
        'INSERT INTO companies (name, rating_score, rating_count) values (%s,%s,%s)',
        (name, rating_score, rating_count))
    db.commit()
    print("Insert company information about " + name + " OK !")
    return mycursor.lastrowid


def insert_localisation(localisation):
    """
    This function insert provided data in database
    """
    mycursor = db.cursor()
    mycursor.execute("INSERT INTO localisation (localisation) values (%s)",
                     (localisation,))
    db.commit()
    print("Insert localisation " + localisation + " OK !")
    return mycursor.lastrowid


def insert_job_description(job_description):
    """
    This function insert provided data in database
    """
    mycursor = db.cursor()
    mycursor.execute(
        "INSERT INTO jobs_description (job_description) values (%s)",
        (job_description,))
    db.commit()
    print("Insert Job description OK")
    return mycursor.lastrowid

def query_job_id(job_indeed_id):
    """
    This function query job_id from db
    """
    mycursor = db.cursor()
    mycursor.execute(
        "SELECT job_id FROM jobs WHERE job_indeed_id = '" + job_indeed_id + "'")
    record = mycursor.fetchone()
    return record

def query_company_name(name):
    """
    This function query company name from db
    """
    mycursor = db.cursor()
    mycursor.execute(
        "SELECT company_id FROM companies WHERE name = '" + name + "'")
    record = mycursor.fetchone()
    return record

def query_company_localisation(localisation):
    """
    This function query localisation from company localisation
    """
    mycursor = db.cursor()
    mycursor.execute(
        "SELECT localisation_id FROM localisation WHERE localisation = '" + localisation + "'")
    record = mycursor.fetchone()
    return record


def insert_post_informations(job_indeed_id, contract_type, job_posting_date,
                             candidate_link, salary, name, rating_score,
                             rating_count, localisation, job_description):
    """
    This function insert provided data in database
    """

    record = query_job_id(job_indeed_id)

    if record:
        print(
            "The job_indeed_id number : " + job_indeed_id + " already exists in the table")

    else:
        record = query_company_name(name)

        if record:
            company_id = record[0]
        else:
            company_id = insert_company_informations(name, rating_score,
                                                     rating_count)

        record = query_company_localisation(localisation)

        if record:
            localisation_id = record[0]
        else:
            localisation_id = insert_localisation(localisation)

        job_description_id = insert_job_description(job_description)

        insert_job_informations(job_indeed_id, contract_type, job_posting_date,
                                candidate_link, salary, company_id,
                                localisation_id, job_description_id)
