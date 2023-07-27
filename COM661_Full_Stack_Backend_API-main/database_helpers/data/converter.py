# This script is used to convert xml documents into json.

import csv 
import json 

def csv_to_json(csvFilePath, jsonFilePath):
    jsonArray = []
      
    #read csv file
    with open(csvFilePath, encoding='utf-8') as csvf: 
        #load csv file data using csv library's dictionary reader
        csvReader = csv.DictReader(csvf) 

        #convert each csv row into python dict
        for idx, row in enumerate(csvReader): 
            print(idx)
            #add this python dict to json array
            jsonArray.append(row)
  
    #convert python jsonArray to JSON String and write to file
    with open(jsonFilePath, 'w', encoding='utf-8') as jsonf: 
        jsonString = json.dumps(jsonArray, indent=4)
        jsonf.write(jsonString)

        
# csvFilePath = r'./Raw DataSets/credits.csv'
# jsonFilePath = r'data.json'

# csv_to_json(csvFilePath, jsonFilePath)


files = [r'./Raw DataSets/credits.csv', r'./Raw DataSets/keywords.csv', r'./Raw DataSets/movies_metadata.csv']
output_files = [r'./Processed/credits.json', r'./Processed/keywords.json', r'./Processed/movies_metadata.json']

for idx, file in enumerate(files):
    csv_to_json(file, output_files[idx])

print("-------------------------- Done --------------------------")