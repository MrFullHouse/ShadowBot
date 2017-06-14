import asyncio
import subprocess
import sys
import discord
import json
from bs4 import BeautifulSoup
import re
import os
import datetime

client = discord.Client()
with open('config.json') as config_data:
    config_json = json.load(config_data)
    api_key = config_json['api_key']
    simcraft_path = config_json['path']
    token = config_json['discord_token']
character = str(sys.argv[1])
server = str(sys.argv[2])
channel = str(sys.argv[3])
author = sys.argv[4]
region = str(sys.argv[5])

def damagestrip(character, server, region):
    with open('%s%s-%s-%s-dps.html' % (simcraft_path, character, server, region), encoding='utf8') as infile:
        soup = BeautifulSoup(infile, "html.parser")
        return soup.find(text=re.compile(' dps'))

def mod_date(filename):
    t = os.path.getmtime(filename)
    return datetime.datetime.fromtimestamp(t)

@client.event
@asyncio.coroutine
def on_ready():
        for x in config_json['servers']:
            client.accept_invite(x)
        yield from client.send_message(client.get_channel(channel), '%s: Симуляция для %s завершена' % (author, character))
        yield from client.send_message(client.get_channel(channel), '%s: %s' % (author, damagestrip(character, server, region)))
        yield from client.send_message(client.get_channel(channel), 'Ссылка: http://52.88.164.238/output/%s-%s-%s-dps.html' % (character, server, region))
        yield from client.logout()

print('%s./simc armory=%s,%s,%s calculate_scale_factors=0 iterations=10000 html=%s-%s-%s-dps.html output=%s-%s.txt fight_style=PatchWerk' % (simcraft_path, region, server, character, character, server, region, character, region))
subprocess.call('%s./simc armory=%s,%s,%s calculate_scale_factors=0 iterations=10000 html=%s-%s-%s-dps.html output=%s-%s.txt fight_style=PatchWerk' % (simcraft_path, region, server, character, character, server, region, character, region), cwd=simcraft_path, shell=True)
client.run(token)
