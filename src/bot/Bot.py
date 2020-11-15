#!/usr/bin/env python3

import discord
import os
import random

import mysql_helper

BOT_TOKEN = os.environ['BOT_TOKEN']

RANDOM_PARROT_CHATTER = ["SQUAWK!!!", "Squawky wants a cookie!!!", "Squawky is a good bird!",
                         "Let's make discord great again!", "SQUAWK!", "Cookie!", "The cake is a lie!",
                         "I'm Squawky!", "I'm a star"]

HELP_TEXT = """`!parrot read` to read messages on this channel
%s"""

channels = []
users = []


def users_to_text():
    users_as_text = ""
    for u in users:
        if users_as_text != "":
            users_as_text += " and "
        users_as_text += str(u.name) + "#" + str(u.discriminator) + " "

    return users_as_text


def pick_random_chatter():
    return RANDOM_PARROT_CHATTER[random.randint(0, len(RANDOM_PARROT_CHATTER) - 1)]


class MyClient(discord.Client):
    async def on_ready(self):
        print("I've logged in. Squawk!")

    async def on_message(self, message):
        if message.author == client.user:
            return

        if message.content.startswith("!parrot"):
            message_content = message.content.split(" ")

            if len(message_content) == 1:
                await message.channel.send(pick_random_chatter())

            elif message_content[1] == "help":
                await message.channel.send(pick_random_chatter())
                await self.show_help(message)

            elif message_content[1] == "read":
                await self.read_channel(message.channel)
                await message.channel.send("I've read messages from " + users_to_text())

            else:
                await message.channel.send("SQUAWK! I don't understand!")
                await self.show_help(message)

    async def show_help(self, message):
        await message.channel.send(HELP_TEXT % pick_random_chatter())

    async def read_channel(self, channel):
        messages = await channel.history(limit=20000).flatten()
        for m in messages:
            if not m.author.bot:
                if m.author not in users:
                    users.append(m.author)
                if not m.content.startswith("!"):
                    print(str(m.author) + " wrote " + m.content)
                    mysql_helper.write_message(str(m.author), m.content)
        print(users)


client = MyClient(max_messages=20000)
client.run(BOT_TOKEN)


