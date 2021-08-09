import mysql.connector as mysql
from config import HOST, USER, PASSWD
from API_requests import get_coordinates, get_company_rating, localisation_formatting

db = mysql.connect(
    host=HOST,
    user=USER,
    passwd=PASSWD,
    auth_plugin='mysql_native_password',
    database="indeed")

def query_empty_coordinates():
    """
    This function query localisation from company localisation
    """
    mycursor = db.cursor()
    mycursor.execute(
        "SELECT localisation, localisation_id FROM localisation WHERE latitude is NULL")
    record = mycursor.fetchall()
    return record


def insert_coordinates(coordinates, localisation_id):
    """
    This function insert coordinates in db
    """
    mycursor = db.cursor()
    mycursor.execute(
        "UPDATE localisation SET latitude = " + str(coordinates[1]) +
        ", longitude = " + str(coordinates[0]) +
        " WHERE localisation_id = " + str(localisation_id))
    db.commit()
    print("{} inserted".format(coordinates))


def get_and_insert_coordinates():
    """
    This function get coordinate from API and insert them in db.
    """
    record = query_empty_coordinates()
    for r in record:
        coordinates = (get_coordinates(localisation_formatting(r[0])))
        print(coordinates)
        if coordinates[0] is not None and coordinates[1] is not None:
            insert_coordinates(coordinates, r[1])
        else:
            pass


def query_empty_google_rating():
    """
    This function returns  company with empty rating score
    """
    mycursor = db.cursor()
    mycursor.execute(
        "SELECT name, company_id FROM companies WHERE google_rating_score is NULL")
    record = mycursor.fetchall()
    return record


def insert_google_rating_score(google_rating, company_id):
    """
    From id, this function insert google rating score in db.
    """
    mycursor = db.cursor()
    mycursor.execute(
        "UPDATE companies SET google_rating_score = " + str(google_rating) +
        " WHERE company_id = " + str(company_id))
    db.commit()
    print("score for company id : {} inserted".format(company_id))


def get_and_insert_google_rating_score():
    """
    This function get and insert google rating score in db.
    """
    record = query_empty_google_rating()
    for r in record:
        google_rating = get_company_rating(r[0])
        print(google_rating)
        if google_rating is not None:
            insert_google_rating_score(google_rating, r[1])
        else:
            pass
