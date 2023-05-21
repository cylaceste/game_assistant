
# The game’s name is PowerQuest, the theme is Dark, the genre is Fantasy, the audience is Gen X and game is a single player game. Please fill out the response below. Generate 5 characters and create a narrative for the game_description around some of them. Be somewhat vague in the description.

def get_descriptor_factory(game_descriptors):
    def get_descriptor(key):
        descriptor_value = game_descriptors.get(key, '')
        if isinstance(descriptor_value, list):
            descriptor_value = ', '.join(descriptor_value)
        return str(descriptor_value)
    return get_descriptor

def generate_game_lore_query(game_descriptors):
    get = get_descriptor_factory(game_descriptors)
    lore_query = f"The game is called {get('game_name')}, it's a {get('theme')} {get('genre')} about " \
                 f"{get('game_about')}. This game is tagged as {get('game_types')}." \
                 f"Generate 5 characters. In the game description, focus on the theme and genre and vaguely" \
                 f"mention some of the 5 characters. Generate color themes that match this game, with hexcodes for" \
                 f"the text and the background. For the image urls, find some Return your response in the following shape:\n"

    response_shape = \
    '''
        {
        game_description: str,
    
        characters:
        [
            char_type: string enumerate(Protagonist, Antagonist, Team Member, Important World Character),
            char_name: str,
            char_personality: str,
            char_story: str,
            char_appearance: str,
            char_image_url: str
        
    
        ],
        image_logo_url: str,
        game_banner_url: str,
        background_color: str,
        text_color: str,
        
    [
            {
    '''

    lore_query += response_shape
    return lore_query
