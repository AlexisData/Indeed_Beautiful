from scraper import JobPageScraper, ResultPageScraper
from random import randint
from time import sleep
import argparse


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
    args_dict = get_user_informations()
    results_page_links = parse_user_informations(args_dict)

    for link in results_page_links:
        jobs_key = ResultPageScraper(link)
        sleep(randint(1, 10))

        print(jobs_key.jobs_key_list)

        for job_key in jobs_key.jobs_key_list:
            job = JobPageScraper(job_key)
            print(job)
            sleep(randint(1, 10))


if __name__ == '__main__':
    main()
