import json
import re

#Country data
countries = json.load(open("countries.json"))

#Treaty data
treaties = json.load(open("treaty.json"))

total = 0

#Iterate over treaties
for i in range(0, len(treaties)):
    
    title = treaties[i]["Title"]

    # Match all words after "with"
    match = re.search('with(.*)$', title)

    #If a match is found
    if match and match.group(1):

        #Split the string into an array of words to handle multiple word countries
        country = match.group(1).split(' ')

        #Current country name
        current = country[1]

        #Until a country match is found, add words to the search string
        i = 1
        while (current not in countries) and i < len(country) - 1:
            i += 1
            current += " "
            current += country[i]
        
        #If a country match is found
        if(current in countries):
            treaties[i]["with"] = current
            print(title + " -> " + current + "\n")
            total += 1

print(total)

#Write the modified json to file
with open('treaties_with_country.json', 'w') as out:  
    json.dump(treaties, out)