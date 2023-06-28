# Introduction

Rumbo is a discord bot written in Python that is mainly built around serving as a matchmaking utility for the video game Crash Team Rumble™. It has various social and game-related commands.

# Libraries

Rumbo is built on [Pycord](https://pycord.dev/) and uses [Tortoise ORM](https://tortoise.github.io/) to interact with its SQLite3 database.

# Intents

Before setting up Rumbo, make sure you have enabled all intents in your discord application. Rumbo needs access to members, messages and so on due to the capability to interact with the bot by reacting to messages or clicking on buttons.

# Setup

To set up Rumbo, first create a virtual environment in Python:

~~~
$ cd /path/to/rumbo
$ python3 -m venv venv
~~~

Next, install the packages from the `requirements.txt`.

~~~
$ pip install --upgrade -r requirements.txt
~~~

Next, copy the `settings.example.json` file to a `settings.json` file and fill out all the required properties:

```json
{
  "bot_user_id": "",
  "enable_debug": true,
  "owner": "",
  "guild": "",
  "bot_secret": "",
  "default_embed_color": 0
}
```

Here is an explanation of all available properties:

* `bot_user_id` is the discord user id of your bot
* `enable_debug` enabled various debug functions and debug logging (don't use this in production)
* `owner` is the user id of the one who "owns" the bot (this does not have to be the server owner, but can be)
* `guild` is the discord server id where the bot will run
* `bot_secret` is the secret token that you got from your discord application administration
* `default_embed_color` is an octal number which is used for embeds which do not use an otherwise defined color

After that, you can execute the `start_bot.sh` script to run the bot.

~~~
$ chmod +x ./start_bot.sh
$ ./start_bot.sh
~~~
