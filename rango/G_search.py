
# not used because G gives cut-and-paste script to run
# later, with better json parsing, could update this & views function to
# ... be more like in the book (or do server-side data tracking)
from googleapiclient.discovery import build

import json
import os
import pprint
import urllib

"""
cwd=os.getcwd()
print("the cwd is"+cwd)
# for some reson, after adding this, I didn't need the full path to API key ...
"""

def read_GsearchAPI_key():
    try:
        with open(r'GoogleSearchAPI.key', 'r') as f:
            GsearchAPI_key = f.readline()
    except:
        raise IOError('GoogleSearchAPI.key file not found')
    
    return GsearchAPI_key

    # remember to exclude .key from git
    # for reasons I will never understand, I needed the full path here.
    # and then it was also fine after I deleted it.  magic. 

def read_CSE_key():
    try:
        with open(r'GoogleSearchCSE.key', 'r') as f:
            CSE_key = f.readline()
    except:
        raise IOError('GoogleSearchCSE.key file not found')
    
    return CSE_key

    # remember to exclude .key from git


def run_query(search_terms):
    GsearchAPI_key = read_GsearchAPI_key()
    CSE_key = read_CSE_key()
    
    service = build("customsearch", "v1", developerKey=GsearchAPI_key)
    results = service.cse().list(q = search_terms, cx = CSE_key, num=10).execute()
    return results



# test line, search function is working, should probably add a limit # for results
results = run_query("coffee")

with open('data.json', 'w') as f:
    json.dump(results, f)
"""

json_results = json.loads(results)

for result in json_results['d']['results']:
    print("the result is:"+result)
    results.append({'title': result['title'],
                   'link': result['link'],
                   'summary': result['snippet']})
    
    pprint.pprint(result)

"""

#next shit no worky


"""
    
    res = json.decoder(result)
    print('snippet')
"""

    
    