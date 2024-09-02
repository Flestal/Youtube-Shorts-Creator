from openai import OpenAI
from API import get_api_key, get_prompt

API_KEY = get_api_key()

client = OpenAI(
    api_key=API_KEY
)

def generate_script():
    prompt = get_prompt()

    response = client.chat.completions.create(
        model="gpt-4o",  
        messages=[
            {"role": "user", "content": prompt},
        ]
    )

    script = response.choices[0].message.content
    print(script)
    return script.split('\n')[0],script.split('\n')[2]