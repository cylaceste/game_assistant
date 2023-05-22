# Game Assistant
Our AI Game Jam project to automate game-lore generation. Features a front-end webpage that is rendered via Flask to prompt users for information about their game so we can create the description, some characters and images.

## Running Game Assistant
1. Set your openai key:
```
export OPENAI_KEY=<your_openai_key>
```
or if you're on Windows use:
```
set OPENAI_KEY=<your_openai_key>
```
2. Run all commands below.
```
git clone https://github.com/cylaceste/game_assistant.git game-assistant2
cd game-assistant
pip install -r requirements.txt
python game_assistant/flask_implementation/server.py
```
3. Go to [localhost](http://localhost:80).








# DEPRECATED

Deprecated because we could no longer access AWS acc.

game-assistant/backend is the lambda backend. First run 
zip -r my-deployment-package.zip game-assistant/backend/. 

Package as per https://docs.aws.amazon.com/lambda/latest/dg/python-package.html


game-assistant/frontend is the TBD frontend
