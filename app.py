import os
import time
from flask import Flask, request, jsonify
from datetime import datetime, timedelta
from dotenv import load_dotenv
from groq import Groq

# Load environment variables
load_dotenv()

app = Flask(__name__)
last_request_time = datetime.now()
request_interval = timedelta(seconds=2)  # To respect the retry-after rate limit

@app.route('/api/entrepreneur', methods=['POST'])
def main():
    global last_request_time

    user_responses = request.get_json()

    if not user_responses:
        return jsonify({'error': 'Invalid input'}), 400

    # Generate the pitch deck using the responses
    pitch_deck = {}
    context = ""

    sections = {
        "Cover Slide": [
            "Business name",
            "Tagline",
            "Presenter's name and title",
            "Date"
        ],
        "Introduction": [
            "Overview of the business",
            "Mission statement"
        ],
        "Problem Statement": [
            "The problem your company is solving",
            "Pain points of your target customers"
        ],
        "Solution": [
            "Description of your products or services",
            "Your unique selling proposition"
        ],
        "Market Opportunity": [
            "Industry overview",
            "Target customers"
        ],
        "Business Model": [
            "Revenue streams",
            "Primary revenue source"
        ],
        "Go-To-Market Strategy": [
            "Marketing strategies",
            "Customer acquisition methods"
        ],
        "Business Goals": [
            "Short-term and long-term goals",
            "Key performance indicators (KPIs)"
        ],
        "Competitive Analysis": [
            "Main competitors",
            "Strengths and weaknesses compared to them"
        ],
        "Challenges and Risks": [
            "Challenges your business faces",
            "Mitigation strategies"
        ],
        "Closing": [
            "Summary of the business opportunity",
            "Call to action"
        ]
    }

    for section, prompts in sections.items():
        if (datetime.now() - last_request_time) < request_interval:
            time.sleep((request_interval - (datetime.now() - last_request_time)).total_seconds())

        section_content = generate_section(section, prompts, user_responses, context)
        pitch_deck[section] = section_content
        context += f"{section}: {section_content}\n"
        last_request_time = datetime.now()

    return jsonify({'message': 'Pitch deck created', 'pitch_deck': pitch_deck})

def generate_section(section, prompts, responses, context):
    # Retrieve the API key from environment variables
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY environment variable is not set")

    # Initialize the Groq client with the API key
    client = Groq(api_key=api_key)

    prompt = f"""Based on the following information, generate the {section} section of a pitch deck:

Context:
{context}

User Input:
{str(responses)}

Please provide concise answers to the following prompts for the {section} section:

"""
    for prompt_item in prompts:
        prompt += f"- {prompt_item}\n"

    prompt += "\nEnsure your responses are relevant to the given user input and maintain consistency with previous sections."

    completion_params = {
        "model": "llama3-8b-8192",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7,
        "max_tokens": 500,
        "top_p": 1,
        "stream": True,
        "stop": None,
    }

    try:
        completion = client.chat.completions.create(**completion_params)
        section_content = []
        for chunk in completion:
            content = chunk.choices[0].delta.content
            if content:
                section_content.append(content)
                print(content, end="")  # Print the content as it's received
        return ''.join(section_content)
    except Exception as e:
        return f"An error occurred: {e}"

if __name__ == "__main__":
    app.run(debug=True, port=5001)