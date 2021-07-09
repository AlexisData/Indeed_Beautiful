import mysql.connector as mysql
import config
import datetime


HOST = config.HOST
USER = config.USER
PASSWD = config.PASSWD

db = mysql.connect(
    host = 'localhost',
    user = 'root',
    passwd = '12345678',
    auth_plugin='mysql_native_password',
    database = "indeed")

mycursor = db.cursor()

dic = {'id_post': 'd253a9f6eacc5408', 'company_name': 'JPMorgan Chase Bank, N.A.', 'company_location': 'Columbus, OH', 'contract_type': 'Full-time', 'company_rating_score': '3.9', 'number_of_ratings': '8616', 'job_posting_date': datetime.date(2021, 7, 6), 'job_description': "The Audit technology team, part of Corporate Technology, strive to build best in class ML and AI solutions for Internal Audit Department. The team is on a mission to provide first class user experience by automation of processes and data analysis using AL/ML techniques. The role is a unique opportunity for an experienced, well-rounded, and hands-on practitioner in analytics. The position offers an opportunity to work on multiple initiatives and apply data science skills to support the development of ML and AI solutions.\nResponsibilities:\nApply data science best practices, methods and tools for analytical work in Audit Technology DA opportunities\nDevelop, plan, and execute analytical work, individually and with the team, working with large-scale datasets\nPartner and work closely with product owners and other leads to ensure feasibility and progress of the product delivered\nWork side by side with modelers to ensure the best ML and AI solutions are being delivered to the business\nHave a clear view of success metrics, model and implementation feasibility and impact to customer\nArticulate analytical findings in clear and concise deliverables, including presentations, discussions, and visualizations\nAdhere to standards of excellence by demonstrating professional expertise, strong work ethic, integrity and professional behavior\n\nQualifications/Skills:\n\n5+ years of hands on industry experience in leveraging data science (including ML) and analytics to solve business problems\nBachelor's degree in relevant quantitative field required, advanced degree preferred in analytical field (e.g. Statistics, Economics, Applied Math, Operations Research, other Data Science fields)\nExpert knowledge in quantitative methods for business, advance data science methods and ML\nExperience across broad range of modern data science and analytics tools (e.g., SQL, Hive, Hadoop, Spark, Python)\nProficiency in SQL and Python required.\nAbility to work in large and medium sized project teams, as self-directed contributor with a proven track record of being detail orientated, innovative, creative, and strategic\nJPMorgan Chase & Co., one of the oldest financial institutions, offers innovative financial solutions to millions of consumers, small businesses and many of the world's most prominent corporate, institutional and government clients under the J.P. Morgan and Chase brands. Our history spans over 200 years and today we are a leader in investment banking, consumer and small business banking, commercial banking, financial transaction processing and asset management.\nWe recognize that our people are our strength and the diverse talents they bring to our global workforce are directly linked to our success. We are an equal opportunity employer and place a high value on diversity and inclusion at our company. We do not discriminate on the basis of any protected attribute, including race, religion, color, national origin, gender, sexual orientation, gender identity, gender expression, age, marital or veteran status, pregnancy or disability, or any other basis protected under applicable law. In accordance with applicable law, we make reasonable accommodations for applicants' and employees' religious practices and beliefs, as well as any mental health or physical disability needs.\nEqual Opportunity Employer/Disability/Veterans", 'candidate_link': 'https://www.indeed.com/rc/clk?jk=d253a9f6eacc5408&from=vj&pos=bottom&mvj=0&sjdu=YmZE5d5THV8u75cuc0H6Y26AwfY51UOGmh3Z9h4OvXiPnSpY5mJYAGE2AMnplIJDl8EZNoFLzyHkpvcd7-Y9bg&astse=11500090684e2278&assa=233', 'salary': None}

job_indeed_id = dic['id_post']
contract_type = dic['contract_type']
job_posting_date = dic['job_posting_date']
candidate_link = dic['candidate_link']
salary = dic['salary']
name = dic['company_name']
rating_score = dic['company_rating_score']
rating_count = dic['number_of_ratings']
localisation = dic['company_location']
job_description = dic['job_description']

mycursor.execute('INSERT INTO jobs (job_indeed_id, contract_type, job_posting_date, candidate_link, salary) values (%s, %s, %s, %s, %s)', (job_indeed_id, contract_type, job_posting_date, candidate_link, salary))

mycursor.execute('INSERT INTO companies (name, rating_score, rating_count) values (%s,%s,%s)', (name, rating_score, rating_count))

mycursor.execute("INSERT INTO localisation (localisation) values (%s)", (localisation,))

mycursor.execute("INSERT INTO jobs_description (job_description) values (%s)", (job_description,))

db.commit()

print("Table jobs created")

mycursor.execute("SELECT * FROM jobs_description")
record = mycursor.fetchall()
for r in record:
    print(r)