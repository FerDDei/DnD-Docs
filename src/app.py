from flask import Flask, render_template, jsonify
from dotenv import load_dotenv
import os
from openai import OpenAI
import ast
import json

load_dotenv()

app = Flask(__name__)

client = OpenAI(
    # This is the default and can be omitted
    api_key=os.environ.get("OPENAI_API_KEY"),
)

def prompt_gpt(client, prompt):
    # Create chat completion
    print(f"Prompt: {prompt}")
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="gpt-4o",
        max_tokens=3000,
        temperature=0.9,
        n=1,
        stop=None
    )

    # Extract number of tokens from the completion

    chat_completion = chat_completion.choices[0].message.content

    return chat_completion

def extract_json_from_prompt(chat_completion):
    try:
        # Extract data between ```json\n and \n```
        json_data = chat_completion.split('```json\n')[1].split('\n```')[0]
        # Load the JSON string into a dictionary to ensure it's valid JSON
        json_data = json.loads(json_data)
    except Exception as e:
        print(f"Error extracting JSON: {e}")
        json_data = {}
    return json_data

def generate_char_info(user_input, instructions):
    prompt = (
        f"Here is added information about the character I would like you to know about: {user_input}\n"
        "Generate new values for each of the keys in this JSON structure:\n"
        f"Here is the new JSON with generated values:\n{instructions}\n\n"
    )
    file_name = os.path.join(app.root_path, 'content.json')
    while True:
        chat_completion = prompt_gpt(client=client, prompt=prompt)
        content_json = extract_json_from_prompt(chat_completion)
        if len(content_json) == len(instructions):
            print("Generated JSON has the correct number of keys.")
            with open(file_name, 'w') as f:
                json.dump(content_json, f, indent=4)
            break

@app.route('/')
def index():
    user_input = "Pufflen the Stoned has super long moustache, which is platted, long hair, he is asian, and a human wizard, who is a massive stoner and a big fan of the Woodland elves dank weed"
    instructions_path = os.path.join(app.root_path, 'instructions.json')
    try:
        with open(instructions_path, 'r') as f:
            instructions = json.load(f)
    except FileNotFoundError:
        return "Instructions file not found", 404
    
    generate_char_info(user_input, instructions)
    
    content_path = os.path.join(app.root_path, 'content.json')
    try:
        with open(content_path, 'r') as f:
            character_info = json.load(f)
    except FileNotFoundError:
        return "Content file not found", 404
    
    return render_template('index.html', json=character_info)

if __name__ == '__main__':
    app.run(debug=True)
