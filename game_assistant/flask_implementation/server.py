from flask import Flask, render_template, jsonify, request
import openai
import json
import concurrent.futures
import os
from query_generation import generate_game_lore_query
TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), 'templates')
app = Flask(__name__, template_folder = TEMPLATE_DIR)

openai.api_key = YOUR KEY HERE

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/get-started', methods=['GET'])
def get_started():
    return render_template('get_started.html')


def generate_lore(prompt):
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


def generate_lore_images(lore):
    # Create a dictionary to store the results
    banner_args = (f"{lore['game_description']} Exciting, Fun, High Quality.", '1024x1024', lore, 'banner_image_url')
    logo_args = (f"{lore['game_description']} Simple, Clean, Minimalist, Abstract.", '256x256', lore, 'logo_image_url')
    image_args = []
    image_args += [banner_args, logo_args]
    for character in lore['characters']:
        character_args = (f"{character['char_appearance']} Attractive, Cool, Action Shot.", '512x512', character, 'char_image_url')
        image_args += [character_args]

    # Create a ThreadPoolExecutor
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Submit tasks to the executor
        futures = [executor.submit(generate_image, *args) for args in image_args]

        # Wait for all the tasks to complete
        concurrent.futures.wait(futures)

    return lore

def generate_image(description, size, result_dict, url_key):
    print('starting image gen')
    response = openai.Image.create(
        prompt=description,
        n=1,
        size=size
    )
    # Handle the response here, such as extracting the generated image URL
    # or saving the image to a file

    # Assign the result to the corresponding URL key in the shared dictionary
    print(response)
    result_dict[url_key] = response['data'][0]['url']

def call_openai(prompt):
    lore = generate_lore(prompt)
    lore_with_images = generate_lore_images(lore)
    return lore_with_images


def mock_response():

    IMAGE_ADDRESS = 'data:image/jpeg;base64,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'
    return \
    {
        "game_description": "Welcome to Battle Quest Arena, a dark RPG that takes you on an immersive journey into the mysterious world of Lily the Circus Clown. Prepare for an intense PvP experience combined with elements of a MOBA and strategic gameplay.",
        "characters": [
            {
                "char_type": "protagonist",
                "char_name": "Lily",
                "char_personality": "Lively and mischievous",
                "char_story": "Once a cheerful circus clown, Lily was consumed by darkness after a tragic incident. Now, she seeks redemption and revenge, wielding her razor-sharp juggling knives as her weapon of choice.",
                "char_appearance": "Dressed in tattered circus attire with a painted porcelain mask, Lily exudes an eerie aura, hiding her true emotions behind a sinister smile.",
                "char_image_url": IMAGE_ADDRESS
            },
            {
                "char_type": "antagonist",
                "char_name": "Dreadmaster",
                "char_personality": "Cunning and power-hungry",
                "char_story": "Once a renowned magician, Dreadmaster delved into forbidden arts, becoming a malevolent sorcerer. He seeks to harness the dark forces within the circus realm and bend them to his will.",
                "char_appearance": "Cloaked in shadowy robes and wielding a twisted staff, Dreadmaster's eyes glow with an unholy fire, reflecting his insatiable hunger for power.",
                "char_image_url": IMAGE_ADDRESS
            },
            {
                "char_type": "team_members",
                "char_name": "Spike",
                "char_personality": "Brave and loyal",
                "char_story": "Spike, a fearless acrobat, joined Lily's cause after witnessing her tragic transformation. With his acrobatic skills and unwavering determination, he becomes her trusted ally in the battle against darkness.",
                "char_appearance": "Adorned in a sleek black outfit with intricate patterns, Spike's agile movements and daring stunts make him a formidable presence in the arena.",
                "char_image_url": IMAGE_ADDRESS
            },
            {
                "char_type": "team_members",
                "char_name": "Mystica",
                "char_personality": "Mysterious and enigmatic",
                "char_story": "Mystica, a mysterious fortune teller, possesses ancient knowledge of the circus's hidden secrets. She joins Lily's quest, driven by her own hidden motives and a desire to unravel the truth.",
                "char_appearance": "Clad in flowing robes adorned with mystical symbols, Mystica's piercing gaze and cryptic aura make her an intriguing presence, always keeping her true intentions veiled.",
                "char_image_url": IMAGE_ADDRESS
            },
            {
                "char_type": "important_world_characters",
                "char_name": "Ringmaster",
                "char_personality": "Charismatic and manipulative",
                "char_story": "The Ringmaster, a charismatic leader, holds sway over the circus and its inhabitants. Beneath his charming facade lies a manipulative nature, orchestrating events for his own hidden agenda.",
                "char_appearance": "Dressed in an extravagant suit adorned with vibrant colors and adorned with glistening jewelry, the Ringmaster exudes an air of grandeur and control.",
                "char_image_url": IMAGE_ADDRESS
            }
        ],
        "image_logo_url": IMAGE_ADDRESS,
        "game_banner_url": IMAGE_ADDRESS,
        "background_color": "#1E1E1E",
        "text_color": "#FFFFFF"
    }



@app.route('/lore', methods=['GET', 'POST'])
def lore():
    if request.method == 'POST':
        payload = request.get_json()

        lore_prompt = generate_game_lore_query(payload)
        lore = call_openai(lore_prompt)
        print(lore)
        return render_template('lore.html', response=lore)
    else:
        # Handle GET request
        return render_template('lore.html', response=mock_response())

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)