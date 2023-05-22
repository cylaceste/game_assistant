import json
import os
from typing import List, Dict

PROMPTS_PATH = os.path.join(os.path.dirname(__file__), 'prompts.json')


def get_descriptor_factory(game_descriptors: Dict[str, str]) -> callable:
    f = open(PROMPTS_PATH)
    prompts_map = json.load(f)

    def enrich_prompts(key: str, value: str) -> str:
        return prompts_map.get(key, {}).get(value, value)

    def get_descriptor(key: str) -> str:
        descriptor_value = game_descriptors.get(key, '')
        if isinstance(descriptor_value, list):
            descriptor_value = ', '.join([enrich_prompts(key, val) for val in descriptor_value])
        else:
            descriptor_value = enrich_prompts(key, descriptor_value)
        return str(descriptor_value)

    return get_descriptor


def generate_game_lore_query(game_descriptors: Dict[str, str]) -> str:
    get = get_descriptor_factory(game_descriptors)
    lore_query = f"The game is called {get('game_name')}, it's a {get('theme')} {get('genre')} about " \
                 f"{get('game_about')}. This game is tagged as {get('game_types')}." \
                 f"Generate 5 characters. In the game description, focus on the theme and genre but do not mention it" \
                 f"explicitly, and write about 4-5 lines describing the game.  Vaguely" \
                 f"mention some of the 5 characters. Generate color themes that match this game, with hexcodes for" \
                 f"the text and the background. Return your response in the following shape, with the response being " \
                 f"json.load-able but without any additional space or new line formatting:\n"

    response_shape = '''
        {
        "game_description": str,

        "characters":
        [
            "char_type": str (enumerate: Protagonist, Antagonist, Team Member, Important World Character),
            "char_name": str,
            "char_personality": str,
            "char_story": str,
            "char_appearance": str,
            "char_image_url": str


        ],
        "image_logo_url": str,
        "game_banner_url": str,
        "background_color": str,
        "text_color": str
        }
    '''

    lore_query += response_shape
    return lore_query
