import glob
from bs4 import BeautifulSoup
import pandas as pd

file_name_list = glob.glob("html/*.html")

final_data = []

for file_name in file_name_list:    
    with open(file_name, 'r', encoding='utf-8') as f:
        print(file_name)
        
        file_data=f.read()

        soup = BeautifulSoup(file_data, 'html.parser')
        data = soup.select("a[href*=en-data/dataset]")

        dataset_items = soup.findAll("div", {"class": "dataset-item"})

        for item in dataset_items:
            header = item.select_one('a')
            name = header.contents[0]
            print(name)
            link = 'https://data.gov.hk' + header['href']

            org = item.findAll('a', {'class': 'media-view'})[0]
            org_name = org.contents[0]
            org_link = 'https://data.gov.hk' + org['href']

            notes = item.findAll('a', {'class': 'notes'})
            if len(notes) > 0:
                notes_desc = notes[0].contents[0]
            else:
                notes_desc = ''

            category = item.findAll('ul', {'class': 'group list-unstyled'})[0]
            category_a = category.select_one('a')
            category_name = category_a.contents[0]
            category_link = 'https://data.gov.hk' + category_a['href']
            # Can category be multiple?

            format_str = ''
            format_list = item.findAll('ul', {'class': 'dataset-resources'})[0]
            for format_item in format_list.select('li'):
                format_a = format_item.select_one('a')
                format_str += format_a.contents[0] + ','

            final_data.append([name, link, org_name, org_link, notes_desc, format_str])

data_header= ['Name', 'link', 'Org Name', 'Org Link', 'Notes', 'Formats']
df = pd.DataFrame(final_data, columns=data_header)
df.to_csv('csv/dump.csv', index=False)
