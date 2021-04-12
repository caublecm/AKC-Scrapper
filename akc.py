
# Import libraries

import json as json
import regex as re
from bs4 import BeautifulSoup
import pandas as pd
import requests

# Call AKC Marketplace for breeders advertising new or upcoming litters within 50mile radius of zipcode 98053
r = requests.get('https://marketplace.akc.org/puppies?location=98053&radius=50')
html = r.text
parser = BeautifulSoup(html, 'html.parser')

# Isolates the breeder, breed and litter information from the html which is a nested dictionary between <script>
d = parser.find(id="react-root")
s = parser.find_all('script')
scripts = s[12]
# Isolates the nested dictionary
jsonStr = re.search(r'\{.*\}', str(scripts)).group()

# Reformat the dictionary to a python friendly list of dictionary entries
dct = json.loads(jsonStr)
entries = dct['app']['search_results']['pages']['data']

list_entries = []
for e in entries:
    list_entries.append(e)

# Converts the list into a Pandas Dataframe
akc = pd.DataFrame(data=list_entries)
print(akc)

# Explores the number of rows and columns and prints the column titles
akc.shape
print(akc.columns)

# Export File to CSV
akc.to_csv('akc.csv')

#
#
# #
# # # Press the green button in the gutter to run the script.
# # if __name__ == '__main__':
# #     print_hi('PyCharm')
#
# # See PyCharm help at https://www.jetbrains.com/help/pycharm/
