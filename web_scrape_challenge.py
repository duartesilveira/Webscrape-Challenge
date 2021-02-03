##########DATA SCIENCE ASSIGNMENT########
#EXERCICE 1 - Replace empty string value with null.
import json

#IMPORT DATA
#DEAL WITH NULL VALUES IN PYTHON
null = None
data = [{
"firstname": "Elian",
"email": '',
"mobilephone": "0653560813",
"website": '',
"owner_url": "/studentenhuisprofiel/2801/displayroomAdvert", "lastname": "Wassink",
"company": "Particulier, Eigenaar",
"kvk": '',
"note": '',
"activein": '',
"plaats": "Arnhem"
}, {
"firstname": "Alan",
"email": '',
"mobilephone": "0653560813", 
"website": '',
"owner_url": '/studentenhuisprofiel/2283/displayroomAdvert', "lastname": "Biker",
"company": "Euronetich",
"kvk": null,
"note": null, 
"activein": null, 
"plaats": "Utrecht"
    }] 

#REPLACE 
data_null = json.dumps(data).replace('""', 'null')
#SEE THE RESULTS
#print(data_null)

#EXERCICE 2 - Delete duplicate rows base on url column (leaving only row with lower ID left), and update its column “count” to have the value of its highest duplicate row ID
import pandas as pd 
import numpy as np

#CREATE THE DATAFRAME
data = pd.DataFrame(np.array([['A', 10,'www.A.com'], ['B', 21,'www.B.com'], ['C', 12,'www.C.com'],['D', 31,'www.D.com'],['A', 13,'www.A.com'],['D', 18,'www.D.com'],['A', 5,'www.A.com']]),
                   columns=['First name', 'Count', 'Url']).rename_axis('ID', axis=1) 
data.index = np.arange(1, len(data)+1)
#GROUP DUPLICATES TOGETHER AND KEEP THE LAST ONES IN THIS PARTICULAR CASE WORKS, HOWEVER TO GENERALIZE I WOULD TAKE ANOTHER APPROACH 
data_unique = data.sort_values('First name',ascending=True).drop_duplicates(subset=['Url'],keep='last')
#UPDATES THE INDEXES
data_unique.index = np.arange(1, len(data_unique)+1)
#SEE THE RESULTS
#print(data_unique)

# EXERCICE 3 - Using the table from question number 2, convert the result of the query “Select * from table_from_question_2” to csv and json format. You may have more than 1 answer.
#TO CSV
data_csv = data.to_csv()
#VIEW RESULTS
#print(data_csv)
#TO JSON
data_json = data.to_json(orient="index")
#VIEW RESULTS
#print(data_json)

# EXERCICE 4
#Output: 
#3
#2
#1
#setTimeout() method calls a function after the code runs
#The method then() returns a Promise, in this case none so it's returned in second

# EXERCICE 5 -SCRAPE ROOM INFORMATION
import time
from selenium import webdriver
from requests_html import HTMLSession
from bs4 import BeautifulSoup 

#FUNCTION TO CREATE AN HTML SESSION FOR JAVASCRIPT RENDERED WEBSITES
def create_HTML_session(URL):
    # create an HTML Session object
    session = HTMLSession()
    URL = URL
    resp = session.get(URL)
    details = BeautifulSoup(resp.html.html, "lxml")
    return details

def site_login(PATH,URL):
    ##SILENIUM 
    driver = webdriver.Chrome(PATH)  
    driver.get(URL)
    #CLICK LOGIN BUTTON
    driver.find_element_by_xpath('//*[@id="header"]/nav/div/div/ul[2]/li[2]').click()
    time.sleep(2)
    #PASS USERNAME
    username = driver.find_element_by_xpath('//*[@id="UserEmail"]')
    username.clear()
    username.send_keys("duarte@gmail.com")
    time.sleep(2)
    #PASS PASSWORD
    password = driver.find_element_by_xpath('//*[@id="LoginPassword"]')
    password.clear()
    password.send_keys("123456789")
    time.sleep(2)
    #CLICK LOGIN
    driver.find_element_by_xpath('//*[@id="login-page"]/div[2]/div[6]/div[3]/div[2]/button').click()
    time.sleep(5)
    driver.quit()

#LOGIN TO SCRAPE CONTACT INFO
def get_contact_info(URL):
    site_login(PATH,URL)
    details = create_HTML_session(URL)
    contact = [x.get_text(separator='\n') for x in details.find_all('tr')] 
    return contact

#SCRAPE INFO AND ORGANIZE IT INTO A JSON FILE
def get_page_info(URL):
    #GET THE SOUP
    details = create_HTML_session(URL)
    ##TITLE
    title = details.find('h1',{'class','title roomdetails'}).get_text(separator='\n')
    ##GENERAL INFOS
    surface = [x.get_text(separator='') for x in details.find_all('div',{'class','flex-wrapper'})]
    type = details.find('div',{'class','furnishing'}).get_text(separator='\n')
    availability = details.find('div',{'class','availability'}).get_text(separator='\n')
    viewing = details.find('div',{'class','viewing-night'}).get_text(separator='\n')
    woning_details = [x.get_text(separator=',') for x in details.find_all('div',{'class','col s6 l3 no-padding-left info-col'})]
    contact = get_contact_info(URL)
    data = json.dumps({'name': title[1], 'surface': surface, 'type': type, 'availability': availability, 'viewing': viewing, 'woning_details': woning_details, 'contact': contact}, indent=2)
    return data 
#GLOBAL VARIABLES 
URL = 'https://kamernet.nl/huren/kamer-amsterdam/lomanstraat/kamer-1876337'
#YOU NEED SILENIUM CHROMEDRIVER AND PASTE HERE THE PATH 
PATH = '/Users/duartesilveira/Downloads/chromedriver'
#RUN THE SCRIPT
create_HTML_session(URL)
data = get_page_info(URL)
#SEE THE RESULTS 
print(data)
#I did it for one instead of all but the logic is the same (sorry short deadline - at least for me!! :) )
##HOPE TO HEAR FROM YOU