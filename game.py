"""
file name: game.py
description: movie wordle discord bot
language: python3
author: Samson Zhang | sz7651@rit.edu, Celina Chen
"""

import os
import discord
from imdb_search import *
from discord.ext import commands
from dotenv import load_dotenv
import random

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
bot = commands.Bot(command_prefix='!')
secret_name = get_rand_movie()
word_blanks = []


@bot.event
async def on_ready():
    """
    prints a message on bot startup
    """
    for guild in bot.guilds:
        if guild.name == GUILD:
            break

    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching,
                                                        name='my roommate sleep'))

    print(
        f'{bot.user} has descended upon:\n'
        f'{guild.name}(id: {guild.id})\n'
        'Leggo, bot started\n'
        '.-.-.-..-.-.-.-.-.'
    )

@bot.command()
async def start(ctx):
    init_word_reveal()
    init_hint = 'Initial hints: ' + str(secret_name['year'])
    await ctx.send(init_hint)
    await ctx.send(display_word())


@bot.command(help='use "!guess <movie name>"')
async def guess(ctx, *args):
    """
    command, takes the user input and checks whether it matches the secret name
    the secret name will be reset once the user gives up or gets the correct answer
    :param ctx: context
    :param args: user input
    """
    global secret_name

    if len(args) == 0:
        await ctx.send("You did not enter a guess. Enter a movie name after the command.")
        return
        
    elif check_movie(' '.join(args), secret_name):
        await ctx.send('Correct! You Win!')
        await ctx.send('use !start to start the next game')
        secret_name = get_rand_movie()
        init_word_reveal()
        
    else:
        await ctx.send("You guessed: " + get_user_movie(' '.join(args)))
        await ctx.send('Incorrect, try asking again')

@bot.command(help = 'use !giveup to give up')
async def giveup(ctx):
    global secret_name
    await ctx.send("Here's the correct answer: " + secret_name['title'])
    await ctx.send('use !start to start the next game')
    secret_name = get_rand_movie()
    init_word_reveal()
    
@bot.command(help='use "!hint to reveal a letter"')
async def hint(ctx):
    if not check_reveals():
        reveal_word()
        await ctx.send("Here's a hint:" + display_word())
    else:
        await ctx.send("Max hint limit reached!")

def check_reveals():
    """
    checks if the number of characters revealed has reached the limit of half the word

    :return: true if the number of revealed chars is more than or equal to half of the movie name
    """
    global word_blanks

    length = len(word_blanks)
    count = 0

    for i in word_blanks:
        if i != "_" or i.isalpha():
            count += 1
        if count >= length/2:
            return True

    return False


def init_word_reveal():
    """
    initializes the word blanks based on the secret movie
    """
    global word_blanks

    word_blanks = []

    for i in secret_name['title']:
        if i.isalpha():
            word_blanks.append("_")
        else:
            word_blanks.append(i)

def display_word():
    """
    takes the list of chars from word blanks and creates a complete string

    :return: the complete string of the word blank list
    """
    word = "```"

    for i in word_blanks:
        word += i

    word += "```"
    return word 

def reveal_word():
    """
    reveals a random character in the secret movie name
    """
    global word_blanks

    random_reveal = random.randrange(len(secret_name['title']) - 1)

    while word_blanks[random_reveal].isalpha():
        random_reveal = random.randrange(len(secret_name['title']) - 1)
    
    word_blanks[random_reveal] = secret_name['title'][random_reveal]

if __name__ == "__main__":
    bot.run(TOKEN)
