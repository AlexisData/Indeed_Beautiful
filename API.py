import requests
import ast
import mysql.connector as mysql
from config import HOST, USER, PASSWD, GOOGLE_API_ADRESS, GOOGLE_API_KEY, \
    GOOGLE_API_COMPANY

db = mysql.connect(
    host=HOST,
    user=USER,
    passwd=PASSWD,
    auth_plugin='mysql_native_password',
    database="indeed")


def company_name_formatting(company_name):
    """
    This function takes a company name and format it to be used with google API.
    param: company name
    return: formatted company name
    """
    company_name = company_name.replace(' ', '%20')
    return company_name


def localisation_formatting(localisation):
    """
     This function takes a localisation and format it to be used with google API.
     param: company localisation
     return: formatted company localisation
     """
    localisation = localisation.replace(' ', '+')
    return localisation


def get_coordinates(localisation_formatted):
    """
     This function takes the formatted localisation and use google API to return the coordinates of the city.
     param: formatted city name
     return: coordinates of the city, tuple
     """
    r1 = requests.get(
        GOOGLE_API_ADRESS + localisation_formatted + "&key=" + GOOGLE_API_KEY)
    r1 = r1.content.decode("UTF-8")
    dic_coordinates = ast.literal_eval(r1)
    lat = dic_coordinates['results'][0]['geometry']['bounds']['northeast'][
        'lat']
    long = dic_coordinates['results'][0]['geometry']['bounds']['northeast'][
        'lng']
    lat = round(lat, 7)
    long = round(long, 7)
    return (lat, long)


def get_company_rating(company_name):
    """
     This function returns company rating from Google

     param: company name
     return: google rating of the company.
     """
    r2 = requests.get(
        GOOGLE_API_COMPANY + company_name + "&inputtype=textquery&fields=formatted_address,name,rating&key=" + GOOGLE_API_KEY)
    dic_company = r2.content
    dic_company = dic_company.decode("UTF-8")
    dic_company = ast.literal_eval(dic_company)

    rating = dic_company['candidates'][0]['rating']
    return rating


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
        "WHERE localisation_id = " + str(localisation_id))
    db.commit()
    print("{} inserted".format(coordinates))


def get_and_insert_coordinates():
    """
    This function get coordinate from API and insert them in db.
    """
    record = query_empty_coordinates()
    for r in record:
        coordinates = (get_coordinates(localisation_formatting(r[0])))
        if coordinates:
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
        if google_rating:
            insert_google_rating_score(google_rating, r[1])
        else:
            pass
