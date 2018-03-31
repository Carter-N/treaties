import operator
import json
from itertools import chain
import pycountry
from urllib.request import Request, urlopen
import re
from datetime import datetime

#Country name list
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
missing_countries = ['Republic of Kosovo', 'Federated States of Micronesia', 'ST. VINCENT AND THE GRENADINES', 'Union of Soviet Socialist Republics']

country_list.extend(missing_countries)

#Remove redundant names
country_list.remove('United States')
country_list.remove('United States of America')

with open('treaty.json') as json_data:
    
    #Treaty list
    treaties = json.load(json_data)
    
    count = 0

    for i in range(0, len(treaties)):
        
        treaty = treaties[i]

        print("\nreading treaty: " + treaty["Title"])

        #Attempt to find text if date after 1995 
        year = int(treaty["Date Received From President"].split("/")[2])

        #Country match
        match = "n/a"
        
        if year > 1995:

            #Fetch url and request treaty text
            url = treaty["URL"] + "/document-text?"
            req = Request(url)
            req.add_header("User-Agent", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36")

            #Attempt GET request
            try:
                resp = urlopen(req)
            except:
                print("\tcould not find treaty text")

            content = resp.read().decode("utf-8")

            #If content found extract text between <pre></pre> tags
            output = re.compile('<pre>(.*?)</pre>', re.DOTALL | re.IGNORECASE).findall(content)

            if output:
                treaty_text = output[0]

                #Frequency list of country matches
                countries = {}

                for country_name in country_list:
                    
                    country_lc = country_name.lower()
                    
                    #Find number of matches of substring
                    #TODO
                    match_count = treaty_text.lower().count(country_lc)
                    
                    if match_count > 0:
                        countries[country_name] = match_count

                #Print frequency results
                if len(countries) > 0:
                    match = max(countries.items(), key = operator.itemgetter(1))[0]
                    print("\ttext matched with " + match)
                    count += 1
        
                else:
                    print("\tno text match found")
            else:
                print("\tcound't find treaty text")

        #Search title if text matches not found
        #TODO prioritize title matches over text
        if match == "n/a":

            #Matches
            countries = []

            for country_name in country_list:
                    country_lc = country_name.lower()
                    if country_lc in treaty["Title"].lower():
                        
                        countries.append(country_name)

            #Return longest match
            if len(countries) > 0:
                match = max(countries, key = len)
                print("\ttitle matched with " + match)
                count += 1
            else:
                print("\tno title match found")

        treaties[i]["countries"] = [match]

    print("\n\ntotal " + str(count) + " treaties matched\n\n")

with open('treaties_with_countries.json', 'w') as json_output_data:
    json.dump(treaties, json_output_data)
