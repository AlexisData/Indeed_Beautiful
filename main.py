from scraper import JobPageScraper, ResultPageScraper
from database_construction import *
import argparse
from config import BASE_JOB_RESULTS_URL, KEYWORD_HELPER, PLACE_HELPER, \
    NUMBER_PAGE_HELPER
from API_db_management import get_and_insert_google_rating_score, get_and_insert_coordinates

def get_user_informations():
    """
    This function get parameters givens by user in CLI.

    :return: values given, in dictionary
    """

    parser = argparse.ArgumentParser()

    parser.add_argument('keyword', help=KEYWORD_HELPER, type=str,
                        default="Python", nargs="?")
    parser.add_argument('place', help=PLACE_HELPER, type=str,
                        default="Boston", nargs="?")
    parser.add_argument("number_of_pages", help=NUMBER_PAGE_HELPER,
                        default=15, type=int, nargs="?")

    args = parser.parse_args()

    args_dict = vars(args)

    return args_dict


def parse_user_informations(args_dict):
    """
    Create link to request from values in dictionary

    :param args_dict: a dict
    :return: a list of links
    """
    keyword = args_dict["keyword"]
    place = args_dict["place"]
    number_of_pages = args_dict["number_of_pages"]

    links = []

    for i in range(number_of_pages):
        link = BASE_JOB_RESULTS_URL + keyword + "&l=" + place \
               + "&sort=date" + "&start=" + str(10 * int(i))
        links.append(link)

    return links


def main():
    args_dict = get_user_informations()
    results_page_links = parse_user_informations(args_dict)

    print ("Starting Scrapping...")

    for link in results_page_links:
        jobs_key = ResultPageScraper(link)

        for job_key in jobs_key.jobs_key_list:
            print("Go on job {}".format(job_key))
            job = JobPageScraper(job_key)

            insert_post_informations(job["id_post"],
                                     job["contract_type"],
                                     job["job_posting_date"],
                                     job["candidate_link"],
                                     job["salary"],
                                     job["company_name"],
                                     job["company_rating_score"],
                                     job["number_of_ratings"],
                                     job["company_location"],
                                     job["job_description"])

            print("Job post {} inserted".format(job_key))

    print("Scrapping over... updating database...")
    get_and_insert_coordinates()
    get_and_insert_google_rating_score()

if __name__ == '__main__':
    main()
