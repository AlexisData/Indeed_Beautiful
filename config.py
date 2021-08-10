# MySql Database User Settings

HOST = "localhost"
USER = "root"
PASSWD = ""

# Proxy Configuration

PROXY = 'https://51.210.105.57:24000'

# Constant values

FIRST_ELEMENT = 0
BASE_JOB_RESULTS_URL = "https://www.indeed.com/jobs?q="
BASE_JOB_POST_URL = "https://www.indeed.com/viewjob?jk="
NUMBER_OF_LINK = 15

# Argparse helpers

KEYWORD_HELPER = "Keyword of the job you are looking for"
PLACE_HELPER = "Where do you want to work"
NUMBER_PAGE_HELPER = "Number of pages to scrape"

# Indeed tags

COMPANY_NAME_TAG = "icl-u-lg-mr--sm icl-u-xs-mr--xs"
COMPANY_RATING_TAG = "jobsearch-InlineCompanyRating icl-u-xs-mt--xs jobsearch-DesktopStickyContainer-companyrating"
COMPANY_FOOTER = "jobsearch-JobMetadataFooter"
JOB_DESCRIPTION_SECTION = "jobsearch-JobDescriptionSection-sectionItem"
CANDIDATE_LINK_LOCATOR = "icl-Button icl-Button--primary icl-Button--md icl-Button--block"

FIRST_COMPANY = 17
LAST_COMPANY = -10

# Google API informations

GOOGLE_API_ADRESS = "https://maps.googleapis.com/maps/api/geocode/json?address="
GOOGLE_API_COMPANY = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input="
GOOGLE_API_KEY = ""

# SQL queries - Tables creation

COMPANIES_TABLE_CREATION = """CREATE TABLE companies 
                 (company_id INT(6) NOT NULL AUTO_INCREMENT PRIMARY KEY, 
                 name VARCHAR(100), 
                 rating_score FLOAT(2,1), 
                 rating_count INT(7), 
                 google_rating_score FLOAT(2,1));"""

COMPANIES_TABLE_CONFIRMATION = "Table companies created"

LOCATION_TABLE_CREATION = """CREATE TABLE localisation 
                     (localisation_id INT(6) NOT NULL AUTO_INCREMENT PRIMARY KEY, 
                     localisation VARCHAR(50), longitude FLOAT(10,7), latitude FLOAT(10,7));"""

LOCATION_TABLE_CONFIRMATION = "Table localisation created"

JOBS_DESCRIPTION_TABLE_CREATION = """CREATE TABLE jobs_description 
                     (job_description_id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY, 
                     job_description VARCHAR(10000));"""

JOBS_DESCRIPTION_TABLE_CONFIRMATION = "Table jobs description created"

JOBS_TABLE_CREATION = """CREATE TABLE jobs 
                     (job_id INT(6) NOT NULL AUTO_INCREMENT PRIMARY KEY, 
                     job_indeed_id VARCHAR(16), 
                     contract_type VARCHAR(25), 
                     job_posting_date DATETIME,  
                     candidate_link VARCHAR(1000), 
                     salary VARCHAR(25), 
                     localisation_id INT(6), FOREIGN KEY (localisation_id) REFERENCES localisation(localisation_id), 
                     company_id INT(6), FOREIGN KEY (company_id) REFERENCES companies(company_id), 
                     job_description_id INT(6), FOREIGN KEY (job_description_id) REFERENCES jobs_description(job_description_id));"""

JOBS_TABLE_CONFIRMATION = "Table Jobs created"