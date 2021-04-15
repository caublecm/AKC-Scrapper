
#Import libraries

import json as json
import re
from bs4 import BeautifulSoup
import pandas as pd
import requests

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36'}
# Extract: Call AKC Marketplace for breeders advertising new or upcoming litters within 50mile radius of zipcode 98053
def extract(pnum):
    r = requests.get(f'https://marketplace.akc.org/puppies?location=98053&page={pnum}&radius=50', headers)
    html = r.content
    parser = BeautifulSoup(html, 'html.parser')
    return parser

# Transform: Parses the data for the information needed
def transform(parser):
    # Isolates the breeder, breed and litter information from the html which is a nested dictionary between <script>
    s = parser.find_all('script')
    # Selects the 12th script element
    scripts = s[12]
    # Isolates the nested dictionary
    jsonStr = re.search(r'\{.*\}', str(scripts)).group()

    # Reformat the dictionary to a python friendly list of dictionary entries
    dct = json.loads(jsonStr)
    entries = dct['app']['search_results']['pages']['data']

    for e in entries:
        list_entries.append(e)
    return

"""Calls the transform function to get the parsed information, loads it into a dataframe and saves it as a .csv"""

list_entries = []
#gets pages 1 to 10
for i in range(1, 10):
    print(f'Getting page, {i}')
    c = extract(i)
    t = transform(c)

akc = pd.DataFrame(data=list_entries)

# Extract the breeds from the 'website' column and put them in a separate column

breed_list = []
urls = akc['website'].to_list()
for url in urls:
    try:
        breed = url.split('/')[3]
    except:
        breed = url.split('=')[-1]
    breed_list.append(breed)

akc['breed'] = breed_list

# Export File to CSV
akc.to_csv('akc.csv')
print(akc.head(10))
print(akc['breed'])

# remove useless columns
useless_cols = ['id','title', 'organization_id', 'organization_name', 'contact_name',
                'has_photo', 'cover_photo',
                'cover_draw', 'cover_image', 'lat', 'lon', 'state_name',
                'zip', 'bom', 'breeds', 'breed_name_plural', 'order', 'expected_breed',
                'count_of_listings_indexed', 'distance', 'display_zip']
akc.drop(columns = useless_cols, axis = 1, inplace = True)

# Export File to CSV
akc.to_csv('akc.csv')
print(akc.head(10))
print(akc.columns)