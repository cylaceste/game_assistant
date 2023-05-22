from flask import Flask, render_template, jsonify, request
import openai
import json
import concurrent.futures
import os
from query_generation import generate_game_lore_query

TEMPLATE_DIR: str = os.path.join(os.path.dirname(__file__), 'templates')
app: Flask = Flask(__name__, template_folder=TEMPLATE_DIR)

openai.api_key = os.getenv("OPENAI_KEY")

@app.route('/', methods=['GET'])
def index() -> str:
    return render_template('index.html')

@app.route('/get-started', methods=['GET'])
def get_started() -> str:
    return render_template('get_started.html')

def generate_lore(prompt: str) -> dict:
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a story writer that writes stories for video games. "
                                          "Your writing is captivating and leaves "
                                          "readers wanting for more."},
            {"role": "user", "content": prompt},
        ]
    )
    lore = response.choices[0].message.content
    lore = json.loads(lore)
    return lore

def generate_lore_images(lore: dict) -> dict:
    banner_args = (f"{lore['game_description']} Exciting, Fun, High Quality.", '1024x1024', lore, 'banner_image_url')
    logo_args = (f"{lore['game_description']} Simple, Clean, Minimalist, Abstract.", '256x256', lore, 'logo_image_url')
    image_args = [banner_args, logo_args]
    for character in lore['characters']:
        character_args = (f"{character['char_appearance']} Attractive, Cool, Action Shot.", '512x512', character, 'char_image_url')
        image_args.append(character_args)

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(generate_image, *args) for args in image_args]
        concurrent.futures.wait(futures)

    return lore

def generate_image(description: str, size: str, result_dict: dict, url_key: str) -> None:
    print('starting image gen')
    response = openai.Image.create(
        prompt=description,
        n=1,
        size=size
    )
    print(response)
    result_dict[url_key] = response['data'][0]['url']

def call_openai(prompt: str) -> dict:
    lore = generate_lore(prompt)
    lore_with_images = generate_lore_images(lore)
    return lore_with_images

@app.route('/lore', methods=['POST'])
def lore() -> str:
    payload = request.get_json()
    lore_prompt = generate_game_lore_query(payload)
    lore = call_openai(lore_prompt)
    print(lore)
    return render_template('lore.html', response=lore)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)
