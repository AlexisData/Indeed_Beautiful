import requests
import ast
from config import GOOGLE_API_ADRESS, GOOGLE_API_KEY, \
    GOOGLE_API_COMPANY

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
    try:
        lat = dic_coordinates['results'][0]['geometry']['bounds']['northeast'][
            'lat']
        long = dic_coordinates['results'][0]['geometry']['bounds']['northeast'][
            'lng']
        lat = round(lat, 7)
        long = round(long, 7)
    except IndexError:
        lat = None
        long = None
    except KeyError:
        lat = None
        long = None

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

    try:
        rating = dic_company['candidates'][0]['rating']
    except IndexError:
        rating = None
    except KeyError:
        rating = None

    return rating
