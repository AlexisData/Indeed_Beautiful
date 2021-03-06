from bs4 import BeautifulSoup
import requests
from datetime import datetime, timedelta
import re
from config import NUMBER_OF_LINK, BASE_JOB_POST_URL, \
    PROXY, COMPANY_NAME_TAG, COMPANY_RATING_TAG, COMPANY_FOOTER, JOB_DESCRIPTION_SECTION, \
    CANDIDATE_LINK_LOCATOR, FIRST_COMPANY, LAST_COMPANY

class ResultPageScraper:
    """
    Result Page scraper
    """

    def __init__(self, link):
        self.link = link
        proxies = {"https": PROXY, }
        self.source = requests.get(link, proxies=proxies)
        self.jobs_key_list = self.extract_jobkeys()

    def extract_jobkeys(self):
        """
        Extract the IDs of the job offers on Indeed website

        :return: a list of jobkeys
        """

        solution = re.findall("jobKeysWithInfo.*?true;", self.source.text)
        self.jobs_key_list = []
        for i in range(NUMBER_OF_LINK):
            self.jobs_key_list.append(solution[i][FIRST_COMPANY:LAST_COMPANY])
        return self.jobs_key_list

    def __iter__(self):
        return self

    def __next__(self):
        pass

    def __str__(self):
        return str(self.jobs_key_list)


class JobPageScraper:
    """
    Job page Scraper
    """

    def __init__(self, job_post_id):
        self.job_post_id = job_post_id
        self.job_informations = JobPageScraper.get_job_informations(self)

    def get_soup_job(self):
        """
        Given a job_post_id, this function returns the HTML content
        for a specific job page.

        :return: soup (BS4 object)
        """
        job_post_url = BASE_JOB_POST_URL + str(self.job_post_id)
        proxies = {"https": PROXY, }
        req = requests.get(job_post_url, proxies=proxies)
        soup = BeautifulSoup(req.text, "html.parser")
        return soup

    def extract_job_title(self):
        """
        This function extract job title from given soup.

        :return: a string, job_title
        """
        soup = JobPageScraper.get_soup_job(self)

        if soup:
            job_title = soup.h1.text
            return job_title
        else:
            return None

    def extract_company_name(self):
        """
        This function extract company name from given soup.

        :return: a string, company name
        """
        soup = JobPageScraper.get_soup_job(self)

        if soup:
            company_name = soup.find(
                class_=COMPANY_NAME_TAG).text
            return company_name
        else:
            return None

    def extract_company_location(self):
        """
        This function extract company location from given soup.

        :return: a string, company location
        """
        soup = JobPageScraper.get_soup_job(self)

        if soup:
            company_location = soup.find(
                class_=COMPANY_RATING_TAG).next_sibling.text
            return company_location
        else:
            return None

    def extract_contract_type(self):
        """
        This function extract job type from given soup.

        :return: a string, job type
        """
        soup = JobPageScraper.get_soup_job(self)

        if soup:
            contract_type = soup.find_all(
                class_=JOB_DESCRIPTION_SECTION)

            for div in contract_type:
                if str(div.text).startswith("Job Type"):
                    contract_type = (str(div.text)[
                                     8:])
                    return contract_type  # 8 to remove "Job Type" from beginning of the string
                else:
                    return None
        else:
            return None

    def extract_job_description(self):
        """
        this function returns job description from given soup

        :return: a string, job description
        """
        soup = JobPageScraper.get_soup_job(self)

        if soup:
            job_description = soup.find(id="jobDescriptionText").text
            return job_description
        else:
            return None

    def extract_candidate_link(self):
        """
        This function returns link to candidate from given soup.

        :return: a string, url link
        """
        soup = JobPageScraper.get_soup_job(self)

        if soup:
            candidate_link = soup.find(
                class_=CANDIDATE_LINK_LOCATOR)
            if candidate_link:
                return candidate_link["href"]
            else:
                return None
        else:
            return None

    def extract_salary(self):
        """
        This function returns salary from given soup.

        :return: a string, salary
        """
        soup = JobPageScraper.get_soup_job(self)

        if soup:
            salary = soup.find_all(
                class_=JOB_DESCRIPTION_SECTION)
            for div in salary:
                if str(div.text).startswith("Salary"):
                    return (str(div.text)[
                            6:])  # 6 to remove "Salary" from beginning of the string
                else:
                    return None
        else:
            return None

    def extract_company_rating_score(self):
        """
        This function returns company rating score from given soup.

        :return: a string, company rating score /5
        """
        soup = JobPageScraper.get_soup_job(self)

        if soup:
            company_rating_score = soup.find(itemprop="ratingValue")
            if company_rating_score:
                return company_rating_score["content"]
            else:
                return None
        else:
            return None

    def extract_number_of_ratings(self):
        """
        This function returns company number of ratings from given soup.

        :return: a string, count of votes
        """
        soup = JobPageScraper.get_soup_job(self)

        if soup:
            number_of_ratings = soup.find(itemprop="ratingCount")
            if number_of_ratings:
                return number_of_ratings.get("content")
            else:
                return None
        else:
            return None

    def get_number_of_days(self, string):
        """
        Given a string, deduct the number of days to extract from it

        :param string: a string
        :return: int, number of days
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

    def posting_date_calculator(self, days_to_subtract):
        """
        Given a number of days to substract, this function subtract them to current
        date. The target is to be able to calculate posting date of job post.

        :param days_to_subtract: an integer
        :return: a date
        """
        now = datetime.now()
        posting_date = now - timedelta(days=days_to_subtract)
        return posting_date

    def extract_job_posting_date(self):
        """
        This function returns job posting date from given soup

        :return: a string, job posting date
        """
        soup = JobPageScraper.get_soup_job(self)
        if soup:
            job_posting_date = soup.find(class_=COMPANY_FOOTER)
            number_of_days = JobPageScraper.get_number_of_days(self,
                                                               job_posting_date.text)
            posting_date = JobPageScraper.posting_date_calculator(self,
                                                                  number_of_days).date()
            return posting_date
        else:
            return None

    def get_job_informations(self):
        """
        Given a job id from Indeed, this function returns informations about
        job post : company name, company location etc. in a dictionary.

        :return: a dictionary, with job post informations
        """
        self.job_informations = {
            "id_post": self.job_post_id,
            "company_name": JobPageScraper.extract_company_name(self),
            "company_location": JobPageScraper.extract_company_location(self),
            "contract_type": JobPageScraper.extract_contract_type(self),
            "company_rating_score": JobPageScraper.extract_company_rating_score(
                self),
            "number_of_ratings": JobPageScraper.extract_number_of_ratings(
                self),
            "job_posting_date": JobPageScraper.extract_job_posting_date(self),
            "job_description": JobPageScraper.extract_job_description(self),
            "candidate_link": JobPageScraper.extract_candidate_link(self),
            "salary": JobPageScraper.extract_salary(self)
        }

        return self.job_informations

    def __str__(self):
        return str(JobPageScraper.get_job_informations(self))

    def __getitem__(self, item):
        return self.job_informations[item]
