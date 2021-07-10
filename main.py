from scraper import JobPageScraper, ResultPageScraper
from database_construction import *
from random import randint
from time import sleep
import argparse
import logging


def get_user_informations():
    """
    This function get parameters givens by user in CLI.

    :return: values given, in dictionary
    """

    parser = argparse.ArgumentParser()

    parser.add_argument('keyword', help='keyword of the job you are '
                                        'looking for', type=str,
                        default="Data+Science", nargs="?")
    parser.add_argument('place', help='where do you want to work', type=str,
                        default="United+States", nargs="?")
    parser.add_argument("number_of_pages", help="number of pages to scrape",
                        default=4, type=int, nargs="?")

    try:
        args = parser.parse_args()
    except:
        raise ValueError("Your input must be of the form: keyword(string) "
                         "place(string) number_of_pages(integer) with spaces "
                         "inside an argument replaced by + (Ex: New+York)")

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
        link = "https://www.indeed.com/jobs?q=" + keyword + "&l=" + place \
               + "&sort=date" + "&start=" + str(10 * int(i))
        links.append(link)

    return links


def main():
    logging.basicConfig(level=logging.INFO, filename='indeed.log',
                        filemode='w',
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    args_dict = get_user_informations()
    results_page_links = parse_user_informations(args_dict)

    for link in results_page_links:
        try:
            jobs_key = ResultPageScraper(link)
        except IndexError:
            logging.error("Exception occurred",
                          exc_info=True)

        sleep(randint(1, 10))

        for job_key in jobs_key.jobs_key_list:
            try:
                job = JobPageScraper(job_key)
                sleep(randint(1, 10))

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

                logging.info(job["id_post"] + " OK")

            except Exception:
                logging.error("Exception occurred with " + str(job_key),
                              exc_info=True)
                pass


if __name__ == '__main__':
    main()
