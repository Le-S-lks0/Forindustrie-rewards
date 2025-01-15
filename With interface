import requests
import random
import time
from colorama import init, Fore
import os
import json

init(autoreset=True)

SESSION_FILE = "session_data.json"
REQUEST_INTERVAL = 1


def load_session():
    if os.path.exists(SESSION_FILE):
        with open(SESSION_FILE, "r") as file:
            data = json.load(file)
            return data.get("session_code"), data.get("crystal_numbers", {})
    return None, {}


def save_session(session_code, crystal_numbers):
    with open(SESSION_FILE, "w") as file:
        json.dump(
            {
                "session_code": session_code,
                "crystal_numbers": crystal_numbers
            }, file)


def authenticate(session_code=None):
    url = "https://univers.forindustrie.fr/plateforme/api/v1/authenticate"
    headers = {
        "accept": "application/json",
        "accept-language": "fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7",
        "content-type": "application/x-www-form-urlencoded",
        "sec-ch-ua":
        "\"Google Chrome\";v=\"131\", \"Chromium\";v=\"131\", \"Not_A Brand\";v=\"24\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
    }

    if not session_code:
        session_code = input("Entrez votre code de session : ")
        save_session(session_code,
                     {})

    data = {"code": session_code}

    response = requests.post(url, headers=headers, data=data)

    if response.status_code == 200:
        print(Fore.GREEN + "Authentification réussie.")
        token = response.json().get("token")
        print(Fore.CYAN + "Token :", token + "\n")
        return token
    elif response.status_code == 404:
        print(Fore.RED + "Classe non trouvée.")
        return None
    else:
        print(
            Fore.RED +
            f"Erreur d'authentification : {response.status_code}, {response.text}"
        )
        return None


def fetch_user_data(token, session_code):
    url = f"https://univers.forindustrie.fr/plateforme/api/v1/get/{session_code}"
    headers = {
        "accept": "*/*",
        "accept-language": "fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7",
        "authorization": f"Bearer {token}",
        "sec-ch-ua":
        "\"Google Chrome\";v=\"131\", \"Chromium\";v=\"131\", \"Not_A Brand\";v=\"24\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        user_data = response.json()

        class_data = user_data.get("schoolClass", {})
        class_name = class_data.get("name", "Inconnu")
        class_id = class_data.get("id", "Inconnu")
        class_score = class_data.get("score_total", "Non disponible")

        print(Fore.GREEN + f"Bienvenue {class_name} (ID: {class_id}) !")
        print(Fore.YELLOW + f"Votre score actuel : {class_score}\n")

        return user_data
    else:
        print(
            Fore.RED +
            f"Erreur lors de la récupération des données utilisateur : {response.status_code}, {response.text}"
        )
        return None


def perform_action(token, user_data, crystal_numbers):
    content_data = user_data.get("contents", {})

    # PRINT POINT JUST FOR DEBUGGING
    print(Fore.YELLOW + f"Quiz: {crystal_numbers.get('quiz', 0)}")
    print(Fore.YELLOW + f"Vidéo: {crystal_numbers.get('video', 0)}")
    print(Fore.YELLOW + f"Item: {crystal_numbers.get('item', 0)}")

    while True:
        print("\nChoisissez une action :")
        print("1. Quiz")
        print("2. Vidéo")
        print("3. Item")
        print("4. Quitter")
        choice = input("Votre choix : ")

        if choice == "4":
            print(Fore.GREEN + "Bye.")
            break

        action_type = "quiz" if choice == "1" else "video" if choice == "2" else "item"
        crystal_numbers = load_session()[1]
        crystal_numbers[action_type] += 1

        save_session(session_code, crystal_numbers)
        content_id = crystal_numbers.get(action_type)

        url = f"http://univers.forindustrie.fr/plateforme/api/v1/class/{user_data.get('schoolClass', {}).get('id')}/completed-content"
        headers = {
            "accept": "*/*",
            "accept-language": "fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7",
            "authorization": f"Bearer {token}",
            "content-type": "application/json",
            "sec-ch-ua":
            "\"Chromium\";v=\"130\", \"Google Chrome\";v=\"130\", \"Not?A_Brand\";v=\"99\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
        }

        data = {
            "type": action_type,
            "content_id": f"{content_id}",
            "world_id": 9,
            "region_id": 25,
            "score": 500,
            "multiplier": 2,
            "allianceActive": 0,
            "itemId": "",
        }

        if action_type == "quiz":
            data[
                "goodResponses"] = f"{random.randint(4, 5)}"  # Spécifique au quiz

        if action_type == "item":
            data[
                "content_id"] = f'FIDF RejoindraiIndustrie-Fragment Prefab ({crystal_numbers.get("item")})'

        retry_attempts = 0
        max_retries = 2
        while True:
            crystal_numbers = load_session()[1]
            crystal_numbers[action_type] += 1
            try:
                response = requests.post(url, headers=headers, json=data)
                if response.status_code == 200:
                    print(Fore.GREEN + "Requête réussie ! Réponse :",
                          response.text)
                    retry_attempts = 0 
                    crystal_numbers = load_session()[1]
                    with open('data.json', 'w') as f:
                        json.dump(response.json(), f)
                elif response.status_code == 400 and "Progress Item already added" in response.text:
                    print(Fore.RED + "Item déjà ajouté, tentative suivante...")
                    retry_attempts += 1
                    if retry_attempts > max_retries:
                        print(Fore.RED + "Deux tentatives échouées. ")
                        retry_attempts = 0
                        crystal_numbers = load_session()[
                            1]
                        break
                else:
                    print(Fore.RED +
                          f"Erreur : {response.status_code}, {response.text}")
                    retry_attempts = 0
                print(crystal_numbers[action_type])
            except Exception as e:
                print(Fore.RED + f"Erreur lors de la requête : {str(e)}")
                retry_attempts = 0

            time.sleep(REQUEST_INTERVAL)


if __name__ == "__main__":
    session_code, crystal_numbers = load_session()

    if not session_code:
        print(Fore.YELLOW +
              "Aucun code de session trouvé, veuillez entrer votre code.")
        session_code = input("Code de session : ")
        save_session(session_code, crystal_numbers
                     )

    token = authenticate(session_code)

    if token:
        user_data = fetch_user_data(token, session_code)
        if user_data:
            # Exécuter les actions demandées
            perform_action(token, user_data, crystal_numbers)
