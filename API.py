import requests
import ast
from config import HOST, USER, PASSWD
import mysql.connector as mysql


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
     param: company localisation (A city)
     return: formatted company localisation (A city)
     """
    localisation = localisation.replace(' ', '+')
    return localisation

def get_coordinates(localisation_formatted):
    """
     This function takes the formatted localisation and use google API to return the coordinates of the city.
     param: formatted city name
     return: coordinates of the city
     """
    r1 = requests.get("https://maps.googleapis.com/maps/api/geocode/json?address=" + localisation_formatted + "&key=AIzaSyDEZfkZJhJvk6tf4cm3kFHwHtrkKZGWFP0")
    r1 = r1.content.decode("UTF-8")
    dic_coordinates = ast.literal_eval(r1)
    lat = dic_coordinates['results'][0]['geometry']['bounds']['northeast']['lat']
    long = dic_coordinates['results'][0]['geometry']['bounds']['northeast']['lng']
    return [lat, long]

def get_company_info(company_name, lat, long):
    """
     This function takes a formatted company name and the longitude and latitude of the city the company is located
     and use it with google API to return a dictionary with the address, name and google rating of the company.
     param: formatted company name, latitude and longitude
     return: dictionary with the address, name and google rating of the company.
     """
    r2 = requests.get("https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input=" + company_name + "&inputtype=textquery&fields=formatted_address,name,rating&locationbias=circle:200000@" + str(lat) + "," + str(long) + "&key=AIzaSyDEZfkZJhJvk6tf4cm3kFHwHtrkKZGWFP0")
    dic_company = r2.content
    dic_company = dic_company.decode("UTF-8")
    dic_company = ast.literal_eval(dic_company)
    address = dic_company['candidates'][0]['formatted_address']
    name = dic_company['candidates'][0]['name']
    rating = dic_company['candidates'][0]['rating']
    return({"address": address, "name" : name, "rating": rating, })

def create_dic_company(company_name, localisation):
    """main function"""
    # company_name = 'liberty mutual insurance'
    # localisation = 'New York'
    company_name_formatted = company_name_formatting(company_name)
    localisation_formatted = localisation_formatting(localisation)
    lat = get_coordinates(localisation_formatted)[0]
    long = get_coordinates(localisation_formatted)[1]
    print(get_company_info(company_name_formatted, lat, long))
    return get_company_info(company_name_formatted, lat, long)

create_dic_company()

def insert_coord(lat, lon, id):
    """
    Update location db by id with latitude and longitude value
    """
    db = mysql.connect(
        host=HOST,
        user=USER,
        passwd=PASSWD,
        auth_plugin='mysql_native_password',
        database="indeed")

    my_cursor = db.cursor()
    my_cursor.execute("UPDATE localisation SET lat =" + lat +
                      ", lon = " + lon + "WHERE id = " + id)

    db.commit()
    print("Insert Localisation OK")
