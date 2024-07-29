import os

# Set the environment variable in the notebook
os.environ['GROQ_API_KEY'] = 'YOUR API KEY RIGHT HERE!'

from groq import Groq

def main():
    # Retrieve the API key from environment variables
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY environment variable is not set")

    # Initialize the Groq client with the API key
    client = Groq(api_key=api_key)
    
    # Define the chat completion parameters
    completion_params = {
        "model": "llama3-8b-8192",
        "messages": [
            {
                "role": "user",
                "content": "Hi there, how are you doing?"  # Add your user message content here
            }
        ],
        "temperature": 1,
        "max_tokens": 1024,
        "top_p": 1,
        "stream": True,
        "stop": None,
    }

    try:
        # Create a chat completion
        completion = client.chat.completions.create(**completion_params)
        
        # Process and print the streamed completion
        for chunk in completion:
            print(chunk.choices[0].delta.content or "", end="")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
