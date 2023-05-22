# Game Assistant
Our AI Game Jam project to automate game-lore generation. Features a front-end webpage that is rendered via Flask to prompt users for information about their game so we can create the description, some characters and images.
![image](https://github.com/cylaceste/game_assistant/assets/120675172/5bc3029d-0153-4233-8d39-c5524e05987b)

## Demonstration

https://www.youtube.com/watch?v=P48h3K0MxD4

## Running Game Assistant
1. Set your openai key:
```
export OPENAI_KEY=<your_openai_key>
```
or if you're on Windows use:
```
set OPENAI_KEY=<your_openai_key>
```
2. Run all commands below by pasting into your terminal and hitting enter.
```
git clone https://github.com/cylaceste/game_assistant.git game-assistant
cd game-assistant
pip install -r requirements.txt
python game_assistant/flask_implementation/server.py
```
3. Go to [localhost](http://localhost:80).

## Future On-Demand Content Automation

Future work could include packages which are able to generate protos that can be consumed by a generic application to communicate back and forth with LLMs. This would allow any game engine to create content on-demand, such as new characters, items and quests.

![346098265_215142528043604_6187173156412883659_n](https://github.com/cylaceste/game_assistant/assets/120675172/bd546d3d-7190-4516-84b7-474cfdb45661)

## Resources Used
https://www.interactiveartsalberta.org/ai-game-jam-resources

![image](https://github.com/cylaceste/game_assistant/assets/120675172/02119548-e293-4c48-8487-9c6b093c2f3b)

https://chat.openai.com/

![image](https://github.com/cylaceste/game_assistant/assets/120675172/d14b2c1f-2cd2-4f61-9745-52d78c080db9)

# DEPRECATED

Deprecated because we could no longer access AWS acc.

game-assistant/backend is the lambda backend. First run 
zip -r my-deployment-package.zip game-assistant/backend/. 

Package as per https://docs.aws.amazon.com/lambda/latest/dg/python-package.html


game-assistant/frontend is the TBD frontend
