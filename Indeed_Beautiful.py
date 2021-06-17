from bs4 import BeautifulSoup
import requests
from datetime import datetime, timedelta
from random import randint
from time import sleep
import re


FIRST_ELEMENT = 0
BASE_JOB_POST_URL = "https://www.indeed.com/viewjob?jk="

def make_a_request(link):
    """returns the content of a website using the link of the website"""
    source = requests.get(link)
    return source

def extract_jobkeys(content):
    """extract the IDs of the job offers on Indeed website"""
    solution = re.findall("jobKeysWithInfo.*?true;", content)
    final_list = []
    NUMBER_OF_LINK = 15
    for i in range(NUMBER_OF_LINK):
        final_list.append(solution[i][17:-10])
    return final_list


def get_soup(job_post_id):
    """
    Given a job_post_id, this function returns the HTML content
    for a specific job page.

    :param job_post_id: str
    :return: soup (BS4 object)
    """
    job_post_url = BASE_JOB_POST_URL + job_post_id
    req = requests.get(job_post_url)
    soup = BeautifulSoup(req.text, "html.parser")
    return soup


def extract_job_title(soup):
    """
    This function extract job title from given soup.

    :param soup: soup (BS4 object)
    :return: a string, job_title
    """
    job_title = soup.h1.text
    return job_title


def extract_company_name(soup):
    """
    This function extract company name from given soup.

    :param soup: soup (BS4 object)
    :return: a string, company name
    """
    company_name = soup.find(class_="icl-u-lg-mr--sm icl-u-xs-mr--xs").text
    return company_name


def extract_company_location(soup):
    """
    This function extract company location from given soup.

    :param soup: soup (BS4 object)
    :return: a string, company location
    """
    company_location = soup.find(
        class_="jobsearch-InlineCompanyRating icl-u-xs-mt--xs "
               "jobsearch-DesktopStickyContainer-companyrating").next_sibling.text
    return company_location


def extract_contract_type(soup):
    """
    This function extract job type from given soup.

    :param soup: soup (BS4 Object)
    :return: a string, job type
    """
    contract_type = soup.find_all(
        class_="jobsearch-JobDescriptionSection-sectionItem")

    for div in contract_type:
        if str(div.text).startswith("Job Type"):
            return (str(div.text)[
                    8:])  # 8 to remove "Job Type" from beginning of the string


def extract_job_description(soup):
    """
    this function returns job description from given soup

    :param soup: soup (BS4 Object)
    :return: a string, job description
    """
    job_description = soup.find(id="jobDescriptionText").text
    return job_description


def extract_candidate_link(soup):
    """
    This function returns link to candidate from given soup.

    :param soup: soup (BS4 Object)
    :return: a string, url link
    """
    candidate_link = soup.find(
        class_="icl-Button icl-Button--primary icl-Button--md icl-Button--block")
    if candidate_link:
        return candidate_link["href"]


def extract_salary(soup):
    """
    This function returns salary from given soup.

    :param soup: soup (BS4 object)
    :return: a string, salary
    """
    salary = soup.find_all(
        class_="jobsearch-JobDescriptionSection-sectionItem")
    for div in salary:
        if str(div.text).startswith("Salary"):
            return (str(div.text)[
                    6:])  # 6 to remove "Salary" from beginning of the string


def extract_company_rating_score(soup):
    """
    This function returns company rating score from given soup.

    :param soup: soup (BS4 object)
    :return: a string, company rating score /5
    """

    company_rating_score = soup.find(itemprop="ratingValue")
    if company_rating_score:
        return company_rating_score["content"]


def extract_number_of_ratings(soup):
    """
    This function returns company number of ratings from given soup.

    :param soup: soup (BS4 object)
    :return: a string, count of votes
    """

    number_of_ratings = soup.find(itemprop="ratingCount")
    if number_of_ratings:
        return number_of_ratings.get("content")



def get_job_informations(job_post_id):
    """
    Given a job id from Indeed, this function returns informations about
    job post : company name, company location etc. in a dictionary.

    :param job_post_id: a string, id of job post
    :return: a dictionary, with job post informations
    """
    soup = get_soup(job_post_id)
    job_informations = {
        "id_post": job_post_id,
        "company_name": extract_company_name(soup),
        "company_location": extract_company_location(soup),
        "contract_type": extract_contract_type(soup),
        "company_rating_score": extract_company_rating_score(soup),
        "number_of_ratings": extract_number_of_ratings(soup),
        "job_posting_date": extract_job_posting_date(soup),
        "job_description": extract_job_description(soup),
        "candidate_link": extract_candidate_link(soup),
        "salary": extract_salary(soup)
    }

    return job_informations


def get_number_of_days(string):
    """

    :param string:
    :return:
    """
    if "Just posted" in string:
        return 0
    elif "Today" in string:
        return 0
    elif "ago" in string:
        days = re.findall(r'[0-9]+', string)
        return int(days[0])
    else:
        return None

def posting_date_calculator(days_to_subtract):
    """
    Given a number of days to substract, this function subtract them to current
    date. The target is to be able to calculate posting date of job post.

    :param days_to_subtract: an integer
    :return: a date
    """
    now = datetime.now()
    posting_date = now - timedelta(days=days_to_subtract)
    return posting_date

def extract_job_posting_date(soup):
    """
    This function returns job posting date from given soup

    :param soup: soup (BS4 Object)
    :return: a string, job posting date
    """
    job_posting_date = soup.find(class_="jobsearch-JobMetadataFooter")
    number_of_days = get_number_of_days(job_posting_date.text)
    posting_date = posting_date_calculator(number_of_days).date()
    return posting_date

def main(number_of_pages):
    """print the job Ids for a given number of pages in Indeed"""
    for i in range(number_of_pages):
        link = "https://www.indeed.com/jobs?q=data+science&l=United+States&sort=date" + "&start=" + 10 * str(i)
        content = make_a_request(link).text
        content_list = extract_jobkeys(content)
        for id_post in content_list:
            print(get_job_informations(id_post))
            sleep(randint(1, 10))

if __name__ == '__main__':
    main(1)