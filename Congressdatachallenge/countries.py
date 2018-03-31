import json
from itertools import chain
import pycountry
from urllib.request import Request, urlopen
import re

#Add names
country_list = [country.name for country in list(pycountry.countries)]

#Add official names
country_official_names = []
for country in list(pycountry.countries):
    if hasattr(country, "official_name"):
        country_official_names.append(country.official_name)

country_list.extend(country_official_names)

#Add historical names
historic_names = [country.name for country in list(pycountry.historic_countries)]
country_list.extend(historic_names)

#Add missing names
missing_countries = ['Republic of Kosovo', 'Federated States of Micronesia', 'ST. VINCENT AND THE GRENADINES']
country_list.extend(missing_countries)
alternate_names_of_countries = {'Russian Federation': ('Russia',)}

#Remove redundant names
country_list.remove('United States')

#print(len(country_list))

with open('treaty.json') as json_data:
    treaties = json.load(json_data)
    
    count = 0
    for i in range(280, 285):
        
        treaty = treaties[i]

        print("\nREADING TREATY: " + treaty["Title"])

        #Get URL
        url = treaty["URL"] + "/document-text?"
        print("\trequest sent to:", url)
        req = Request(url)
        req.add_header("User-Agent", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36")
        try:
            resp = urlopen(req)
        except:
            print("COULDN'T FIND TEXT")

        content = resp.read().decode("utf-8")

        #Text document stored inbetween <pre></pre> tags
        output = re.compile('<pre>(.*?)</pre>', re.DOTALL | re.IGNORECASE).findall(content)

        #If match found
        if output:
            print("\ttreaty text found")
            treaty_text = output[0]

            countries = []
            for country_name in country_list:
                country_lc = country_name.lower()
                if country_lc in treaty_text.lower():
                    count += 1
                    countries.append(country_name)
                    print("\t\t...match found: " + country_name)  
        else:
            print("\t cound't find text")
            #treaty['countries'] = countries     
#print(count) 

#with open('treaties_with_countries.json', 'w') as json_output_data:
#    json.dump(treaties, json_output_data)
