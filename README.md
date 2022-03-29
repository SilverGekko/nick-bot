# nick-bot
Controling a VM using a discord bot.

## Setup
#### virtual environment
```
python3.8 -m venv venv
source venv/bin/activate
```

#### Python Dependencies
```
pip install -r requirements.txt
```

#### System Dependencies
```
apt-get install ffmpeg
```
or whatever package manager you use.

#### Tokens & Keys
```
# .env
DISCORD_TOKEN='...'
DISCORD_GUILD='...'
```
`DISCORD_TOKEN`
- create new bot in Discord web console
- Reset/Reveal token

`DISCORD_GUILD`
- open Discord
- enabled Developer Mode in Settings -> Advanced
- right click server name (top left) -> Copy ID

## Running
locally,
```
python main.py
```
