from openai import OpenAI
from API import get_api_key, get_prompt

# Set your API key
API_KEY = get_api_key()  # Replace with your actual API key

client = OpenAI(
    api_key=API_KEY
)

# Function to generate a script for a given topic
def generate_script():
    # Construct the prompt
    # prompt = f"Write a concise 60-second script explaining {topic} in simple terms."
    prompt = get_prompt()

    # Make the API call using GPT-4
    response = client.chat.completions.create(
        model="gpt-4o",  # Using GPT-4 model
        messages=[
            {"role": "user", "content": prompt},
        ]
    )

    # Extract the generated text
    script = response.choices[0].message.content
    print(script)
    return script.split('\n')[0],script.split('\n')[2]

# Example usage
# script = generate_script()