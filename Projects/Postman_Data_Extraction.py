import requests

url = "https://api.higherme.com/classic/jobs?page=1&includes=location,location.company,location.externalServiceReferences&limit=24&filters\\[brand.id\\]=58bd9e7f472bd&filters\\[lat\\]=43.645466&filters\\[lng\\]=-79.374916&filters\\[distance\\]=12.5&sort\\[distance\\]=asc"

payload = ""
headers = {
  'accept': 'application/json, text/plain, */*',
  'accept-language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
  'higherme-client-version': '2024.06.12_22.0a',
  'origin': 'https://app.higherme.com',
  'priority': 'u=1, i',
  'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
  'sec-ch-ua-mobile': '?0',
  'sec-ch-ua-platform': '"macOS"',
  'sec-fetch-dest': 'empty',
  'sec-fetch-mode': 'cors',
  'sec-fetch-site': 'same-site',
  'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
}

response = requests.request("GET", url, headers=headers, data=payload)

response_data = response.json()

print(type(response_data))
print(response_data.get('data')[0])