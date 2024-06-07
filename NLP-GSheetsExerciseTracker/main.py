import requests
import datetime as dt
import os

SHEETY_BASE_URL = "https://api.sheety.co/"
NUTX_BASE_URL = "https://trackapi.nutritionix.com"
SHEETY_ENDPOINT = "1b6f51f3794b7b79146a57cbb1564de2/workoutTracking/workouts"
NUTX_EXEC_NLP_ENDPOINT = "/v2/natural/exercise"
SHEETY_URL = SHEETY_BASE_URL + SHEETY_ENDPOINT
NUTX_URL = NUTX_BASE_URL + NUTX_EXEC_NLP_ENDPOINT

NUTX_APP_ID = os.environ.get("NUTX_APP_ID")
NUTX_API_KEY = os.environ.get("NUTX_API_KEY")
SHEETY_AUTH_TOKEN = os.environ.get("SHEETY_AUTH_TOKEN")

NUTX_AUTH_HEADER = {
    "x-app-id": NUTX_APP_ID,
    "x-app-key": NUTX_API_KEY,
    "x-remote-user-id": "0"
}
SHEETY_AUTH_HEADER = {
    "Authorization": f"Bearer {SHEETY_AUTH_TOKEN}"
}

def get_user_input():
    return input("What did you do for exercise today?\n")

def get_current_time():
    return {
        "date": dt.date.today().strftime("%d/%m/%Y"),
        "time": dt.datetime.now().strftime("%H:%M:%S")
    }

def convert_user_input_to_query(user_input):
    return {"query": user_input}

def make_nutx_query(url, header, user_input_query):
    response = requests.post(url=url, json=user_input_query, headers=header)
    response.raise_for_status()
    return response.json()

def extract_exercise_duration_calories(json_output, t_info):
    new_entries = []
    for exercise in json_output["exercises"]:
        name = exercise["name"]
        duration = exercise["duration_min"]
        calories = exercise["nf_calories"]
        new_entry = {
            "date": t_info["date"],
            "time": t_info["time"],
            "exercise": str.capitalize(name),
            "duration": duration,
            "calories": calories,
        }
        new_entries.append(new_entry)
    return new_entries

def update_sheets(url, header, post_body):
    response = requests.post(url=url, json=post_body, headers=header)
    response.raise_for_status()

def run():
    nutx_data = make_nutx_query(url=NUTX_URL,
                                header=NUTX_AUTH_HEADER,
                                user_input_query=convert_user_input_to_query(get_user_input()))
    print(nutx_data)
    entries = extract_exercise_duration_calories(json_output=nutx_data, t_info=get_current_time())
    for entry in entries:
        json_payload = {
            "workout": entry
        }
        update_sheets(url=SHEETY_URL, header=SHEETY_AUTH_HEADER, post_body=json_payload)

run()