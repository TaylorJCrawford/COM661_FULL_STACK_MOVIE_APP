import requests
import json

# https://rapidapi.com/standingapi-standingapi-default/api/moviesdb5/

url = "https://moviesdb5.p.rapidapi.com/om"

querystring = {"t":"Game of Thrones"}

headers = {
	"X-RapidAPI-Key": "PLACEHOLDER",
	"X-RapidAPI-Host": "moviesdb5.p.rapidapi.com"
}

url = "https://movie-database-alternative.p.rapidapi.com/"

querystring = {"s":"Game of Thrones","r":"json","page":"1"}
headers = {
            "X-RapidAPI-Key": "PLACEHOLDER",
            "X-RapidAPI-Host": "movie-database-alternative.p.rapidapi.com"
        }

response = requests.request("GET", url, headers=headers, params=querystring)

# print(response.text['Search'])

json_value = json.loads(response.text)
print(json_value['Search'][0]['Poster'])