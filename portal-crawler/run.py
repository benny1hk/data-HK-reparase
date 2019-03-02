import csv
import requests
import lxml
from bs4 import BeautifulSoup

import codecs

page_limit = 1000

categories = [
    "city-management","climate-and-weather","commerce-and-industry","development","education",
    "employment-and-labour","environment","finance","food","health","housing",
    "information-technology-and-broadcasting","law-and-security","miscellaneous","population",
    "recreation-and-culture","social-welfare","transport"
    ]

full_url = "https://data.gov.hk/en-datasets/category/city-management,climate-and-weather,commerce-and-industry,development,education,employment-and-labour,environment,finance,food,health,housing,information-technology-and-broadcasting,law-and-security,miscellaneous,population,recreation-and-culture,social-welfare,transport"
url = "https://data.gov.hk/en-datasets/category/"
params = {
    "order": "name",
    "file-content": "no",
    "page": 1
}

def crawbycategory(in_category,page):
    cate_url = url + in_category
    params['page'] = page
    recp = requests.get(url=cate_url,params=params)

    soup = BeautifulSoup(recp.text, 'lxml') 
    datasetitems = soup.select(".dataset-item")
    page_len = len(datasetitems)
    # print(page_len)

    if page_len>0:
        page_rows = []
        for item in (datasetitems):
            page_rows.append(item)
        return page_rows
    else:
        return None

def crawportalhtml():
    rows = []
    total_items = 0
    with codecs.open('dataset_list.html', 'w', "utf-8") as myfile:
        for page_num in range(page_limit):
            page_rows = []
            recp = requests.get(url=url,params=params)
            
            soup = BeautifulSoup(recp.text, 'lxml') 
            datasetitems = soup.select(".dataset-item")
            page_len = len(datasetitems)
            total_items += page_len
            print("Print Length of page %d / %d" % (page_len, total_items))

            if page_len>0:
                for item in (datasetitems):
                    page_rows.append(item)
                for row in page_rows:
                    myfile.write("%s\n" % row)
                params['page'] +=1
            else:
                break



def appendhtml_file(category,data):
    with codecs.open("./html/" + category + ".html", 'w+', "utf-8") as myfile:
        for row in data:
            myfile.write("%s\n" % row)
    return

if __name__ == "__main__":
    # crawportalhtml()
    # recp = crawbycategory(categories[0],1)
    for category in categories:
        # category = categories[3]
        total_page_len = 0
        page = 1
        datasetitems = []
        while True:
            recp = crawbycategory(category,page)

            if recp is not None:
                page_len = len(recp)
                total_page_len += page_len
                print("Category:", category, "Page:", page, "Found:", page_len, "Total:", total_page_len)
                datasetitems.extend(recp)
                appendhtml_file(category,datasetitems)
                page += 1
            else:
                break
            
        # break #for the testing
