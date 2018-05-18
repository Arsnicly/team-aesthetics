import json
from pprint import pprint


with open('titlepage.json') as json_data:
    d = json.load(json_data)
    pprint(d)


