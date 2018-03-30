import json
from itertools import chain
import pycountry

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
    #print treaties[0]
    count = 0
    for treaty in treaties:
        #print treaty['Title']
        #if any(country_name in treaty['Title'] for country_name in country_list):
        countries = []
        for country_name in country_list:
            country_lc = country_name.lower()
            if country_lc in treaty['Title'].lower():
                count+=1
                countries.append(country_name)
                #print country_name
                #treaty.update({'countries', })
            if country_name in alternate_names_of_countries:
                for alternate_name in alternate_names_of_countries[country_name]:
                    if alternate_name.lower() in treaty['Title'].lower():
                        if country_name not in countries:
                            countries.append(country_name)
                            #print treaty['Title']
                #if any(alternate_name.lower() in treaty['Title'].lower() for alternate_name in alternate_names_of_countries[country_name]):
                #    print [alternate_name.lower() in treaty['Title'].lower() for alternate_name in alternate_names_of_countries[country_name] ]
                #    print country_name
        #print treaty['Title']        
        #print countries  
        if len(countries) == 0:
            #print treaty['Title']  
            pass  

        treaty['countries'] = countries     
print(count) 
#with open('treaties_with_countries.json', 'w') as json_output_data:
#    json.dump(treaties, json_output_data)
