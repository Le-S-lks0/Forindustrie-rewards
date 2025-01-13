import requests
import time

classId = 0000
authToken = "Bearer ......"

crystalnumber = 1

url = f"http://univers.forindustrie.fr/plateforme/api/v1/class/{classId}/completed-content"

headers = {
  "accept": "*/*",
  "accept-language": "fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7",
  "authorization": authToken,
  "content-type": "application/json",
  "sec-ch-ua": "\"Chromium\";v=\"130\", \"Google Chrome\";v=\"130\", \"Not?A_Brand\";v=\"99\"",
  "sec-ch-ua-mobile": "?0",
  "sec-ch-ua-platform": "\"Windows\"",
  "sec-fetch-dest": "empty",
  "sec-fetch-mode": "cors",
  "sec-fetch-site": "same-origin"
}

while True:
    crystalnumber = crystalnumber + 1
    data = {
        "type": "item", #video, ...
        "content_id": f"FIDF RejoindraiIndustrie-Fragment Prefab ({crystalnumber})", # crystal number = id crystal
        "world_id": 9,
        "region_id": 25,
        "score": 100,
        "multiplier": 0,
        "allianceActive": 0,
        #"itemId": ""
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        print("C'est bon! Reponse:", response.text)
    else:
        print("Erreur:", response.status_code, response.text)
        
    print(f"Crystal: {crystalnumber}")
    time.sleep(3)