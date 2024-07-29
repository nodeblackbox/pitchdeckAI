import os
import requests
import json

def populate_template(template_path, data):
    with open(template_path, 'r') as file:
        template = json.load(file)

    # Populate the template with data
    for key, value in data.items():
        for section in template['pitchDeck'].values():
            if isinstance(section, dict) and key in section:
                section[key] = value

    return template

def generate_pitch_deck(data, api_key):
    completion_params = {
        "model": "llama3-8b-8192",
        "messages": [
            {
                "role": "user",
                "content": f"Generate a pitch deck based on the following information: {data}"
            }
        ],
        "temperature": 1,
        "max_tokens": 1024,
        "top_p": 1,
        "stream": True,
        "stop": None,
    }

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    response = requests.post("https://api.groq.com/v1/endpoint", json=completion_params, headers=headers)

    if response.status_code != 200:
        raise Exception(f"API request failed with status {response.status_code}: {response.text}")

    pitch_deck = response.json()

    template_path = 'templates/pitch_deck_template.json'
    populated_pitch_deck = populate_template(template_path, pitch_deck)

    return populated_pitch_deck
