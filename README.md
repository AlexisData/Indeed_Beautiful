
# Indeed is Beautiful

A scrapper to retrieve information about jobs available on Indeed.
## Description

The script presented is a scrapper which, from a keyword, 
a location (in the USA) and a number of pages, retrieves 
information associated with job offers posted on the Indeed.com 
website: company, position, salary, description...
## Installation 

First, install the packages from requirements.txt
    
## Usage/Examples

### How to use this script ?

The Indeed_Beautiful.py script admits 3 arguments:
- the searched keyword (for example: Python, Gardener, Librarian...), of type string: by default: Data+Science
- the desired work location (for example: Washington, Dallas, Texas...), of type string: default: United+States
- the number of pages to be scanned, of type integer; default: 4.

When strings consist of compound words, for example New York, replace the space with a "+": New+York

For example, to search for a PHP developer job in Las Vegas, and get only the first 2 pages of results:

Indeed_Beautiful.py Developer+PHP Las+Vegas 2

### What do I got ?

The script returns the following information for each offer:
job_id, company_name, company_location, contract_type, company_rating_score, 
number_of_ratings, job_posting_date, job_description, candidate_link,
salary.

All this information is inserted into a dictionary 
(in preparation for its importation into the database - see Roadmap)

  
## Tech Stack

Full Python !

  
## Roadmap

In the future, this script will be improved, by :
- importing and storing the retrieved data in a database;
- automating the execution of the script
  
## Authors

- @alexisdata
- @garyrouch

  
## License

MIT License

Copyright (c) 2021 Alex&Gary

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
