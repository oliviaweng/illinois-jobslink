import sys
import os
import os.path
import requests
import json
import sqlite3

from bs4 import BeautifulSoup
from selenium import webdriver

from settings import *


# session needs to be global to maintain same session
session = requests.Session()

# Init Database
if(os.path.exists(DB)):
    os.remove(DB)
conn = sqlite3.connect(DB)
c = conn.cursor()
c.execute('''CREATE TABLE listings
                (name text, id text, url text, apply text, zipcode text, wages text, description text, education text)''')


def scrape():
    # Goes through all 40 pages of job listings, scrapes job url, name, and id
    # number
    # There are 40 pages of results, with 250 listings per page. There should
    # be more, but it's capped here.
    for n in range(1, 41):
        # Changes the page= number
        page = PAGE_URL[:87] + str(n) + PAGE_URL[88:]
        # r = session.get(page)
        soup = BeautifulSoup(r.content, "html.parser")
        listings = soup.find_all("dt")  # Finds all dt tags
        for l in listings:
            # Finds the a tag, which will have the name and the url
            urls = l.find_all('a')
            for u in urls:
                # The href part of the tag will have the url
                job_url = u['href']
                name = u.string     # The name will be in the string part of the a tag
                id_num = u.string[u.string.find('(') + 1:u.string.find(')')]

                # print(r.content)

                # Insert the job listing into the database (only the name and url
                # have been implemented at this point)
                c.execute(
                    "INSERT INTO listings VALUES (?, ?, ?, 'TODO', 'TODO', 'TODO', 'TODO', 'TODO');", (name, id_num, job_url))
            # Need to scrape for description, zipcode, wages, education, etc and
            # put them into the DB. ---> Use above code as a model as well as what
            # we did in the scraping workshop.
    conn.commit()


def login():
    # get html data for login page
    soup = BeautifulSoup(session.get(LOGIN_URL).content, "html.parser")
    # pulls login url from page, could change per session
    login = soup.find_all('form')[0]['action']

    login data = dict(v_username=USER_NAME,
                      v_password=PASSWORD,
                      FormName='Form0',
                      fromlogin=1,
                      button='Log in')

    # logs in
    r = session.post(BASE_URL + login, data=login_data)


if __name__ == '__main__':
    login()
    scrape()
    c.close()
