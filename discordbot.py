import asyncio
import discord
import json
import subprocess
import os
import datetime
import requests
import re
from string import punctuation
from bs4 import BeautifulSoup
import time

client = discord.Client()
with open('config.json') as config_data:
    config_json = json.load(config_data)
    api_key = config_json['api_key']
    simcraft_path = config_json['path']
    token = config_json['discord_token']

#Returns true if character exists on armory, false otherwise
def char_exists(character,server, region):    
    try:
        print('https://%s.api.battle.net/wow/character/%s/%s?locale=en_US&apikey=%s' % (region, server, character, api_key))
        requests.get('https://%s.api.battle.net/wow/character/%s/%s?locale=en_US&apikey=%s' % (region, server, character, api_key))
        return True
    except:
        return False

#Removes strip from message, and returns Charactername in a message formatted 'charactername-servername'
def charstrip(message, strip):
    character = message.replace("%s" % strip, "")
    head, sep, tail = character.partition('-')
    head = puncstrip(head)
    return head.capitalize()

#Returns Servername from '!command charactername-servername' input
def serverstrip(message):
    head, sep, tail = message.partition('-')
    head1, sep1, tail1 = tail.partition('-')
    if head1.strip().lower()=="рф":
     return "Ревущий-фьорд";
    if head1.strip().lower()=="пб":
     return "Пиратская-бухта";
    if head1.strip().lower()=="сд":
     return "Свежеватель-душ";
    if head1.strip().lower()=="чш":
     return "Черный-шрам";
    if head1.strip().lower()=="вп":
     return "Вечная-песня";
    if head1.strip().lower()=="кл":
     return "Король-лич";
    if head1.strip().lower()=="сс":
     return "Страж-смерти";
    if head1.strip().lower()=="бт":
     return "Борейская-тундра";
    if head1.strip().lower()=="ял":
     return "Ясеневый-лес";
    if head1.strip().lower()=="тс":
     return "Ткач-смерти";

    return head1.capitalize().strip().replace(" ", "-");

#Returns Regionname from '!command charactername-servername' input
def regionfind(message):
    head, sep, tail = message.partition('-')
    head1, sep1, tail1 = tail.partition('-')
    region = tail1.lower();
    if (tail1.lower() == "us" or tail1.lower() =="na"):
        region = "us";
    if (tail1.lower() == "eu" or tail1.lower() =="ru" or tail1.lower() =="еу" or tail1.lower() =="ру"):
        region = "eu";
    return region;

#Returns s stripped of all punctuation
def puncstrip(s):
    return ''.join(c for c in s if c not in punctuation)

#Returns a pawn string from simcraft output
def pawnstrip(character, server):
    with open('%s%s-%s.html' % (simcraft_path, character, server), encoding='utf8') as infile:
        soup = BeautifulSoup(infile, "html.parser")
        return soup.find(text=re.compile(' Pawn: v1: '))

#Returns modified date of a file in local time        
def mod_date(filename):
    t = os.path.getmtime(filename)
    return datetime.datetime.fromtimestamp(t)

#Returns armory update time
def armory_date(character, server, region):
    print('https://%s.api.battle.net/wow/character/%s/%s?fields=talents&locale=en_US&apikey=%s' % (region, server, character, api_key))
    armory_json = requests.get('https://%s.api.battle.net/wow/character/%s/%s?locale=en_US&apikey=%s' % (region, server, character, api_key))
    armory_json = armory_json.json()
    update_time = armory_json['lastModified']
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(update_time / 1000))

#Returns true if DPS role, false if any other role
def is_dps(character, server, region):
    armory_json = requests.get('https://%s.api.battle.net/wow/character/%s/%s?fields=talents&locale=en_US&apikey=%s' % (region, server, character, api_key))
    armory_json = armory_json.json()
    for i in range(0,7):
        try:
            armory_json['talents'][0]['talents'][i]['spec']['role'] == 'DPS'
            return armory_json['talents'][0]['talents'][i]['spec']['role'] == 'DPS'
        except:
            print('No role (isDPS check 1 ) identifier in tier %s.' % i)
    print('Can\'t find first try, going second')
    for i in range(0,7):
        try:
            selected = armory_json['talents'][i]['selected']
            if(selected):
                return armory_json['talents'][i]['talents'][i]['spec']['role']  == 'DPS'
        except:
            print('No role (isDPS check 2 ) identifier in tier %s.' % i)
    print('Making 3rd and final attempt to get isDPS')
    for i in range(0,7):
        try:
            selected = armory_json['talents'][i]['selected']
            if(selected):
                return armory_json['talents'][i]['spec']['name'] == 'DPS'      
        except:
            print('No role (isDPS check 3 ) identifier in tier %s.' % i)

#Returns role            
def get_role(character, server, region):
    armory_json = requests.get('https://%s.api.battle.net/wow/character/%s/%s?fields=talents&locale=en_US&apikey=%s' % (region, server, character, api_key))
    armory_json = armory_json.json()
    for i in range(0,7):
        try:
            x = armory_json['talents'][0]['talents'][i]['spec']['role']
            if(x):
                return x
        except:
            print('No role (getrole 1) identifier in tier %s.' % i)
    print('Can\'t find role (getRole check1), going second')
    for i in range(0,7):
        try:
            selected = armory_json['talents'][i]['selected']
            if(selected):
                return armory_json['talents'][i]['talents'][i]['spec']['role']
        except:
            print('No role (getrole 2) identifier in tier %s.' % i)
    print("3rd and final attempt to get Role")
    for i in range(0,7):
        try:
            x = armory_json['talents'][i]['spec']['role']  
            return x
        except:
            print('No role (getrole 3) identifier in tier %s.' % i)

#Returns spec    
def get_spec(character, server, region):
    armory_json = requests.get('https://%s.api.battle.net/wow/character/%s/%s?fields=talents&locale=en_US&apikey=%s' % (region, server, character, api_key))
    armory_json = armory_json.json()
    for i in range(0,7):
        try:
            x = armory_json['talents'][0]['talents'][i]['spec']['name']
            if(x):
                return x
        except:
            print('No spec (getspec 1) identifier in tier %s.' % i)
    print('Can\'t find spec (getSpec check1), going second')
    for i in range(0,3):
        try:
            selected = armory_json['talents'][i]['selected']
            if(selected):
                x = armory_json['talents'][i]['talents'][i]['spec']['name']        
                return x
        except:
            print('No spec (getspec 2) identifier in tier %s.' % i)
    print('3rd and final attempt to getSpec')
    for i in range(0,3):
        try:
            selected = armory_json['talents'][i]['selected']
            if(selected):
                x = armory_json['talents'][i]['spec']['name']        
                return x
        except:
            print('No spec3 identifier in tier %s.' % i)

@client.event
@asyncio.coroutine
def on_ready():
#On ready, joins all servers in JSON
    for x in config_json['servers']:
        client.accept_invite(x)
    print('Logged in as')
    print(client.user.name)
    print('---------')
    
@client.event
@asyncio.coroutine 
def on_message(message):
    author = message.author
    if message.content.startswith('!help'):
        yield from client.send_message(message.channel, 'Для того чтоб увидеть вес своих статов наберите: \'!sim имяперсонажа-название сервера-eu\'. Чтоб просто посчитать дпс наберите \'!dps имяперсонажа-название сервера-eu\' Всё маленькими буквами, с пробелом в названии реалма. Я оповещу вас об окончании симуляции.')    
        yield from client.send_message(message.channel, 'Данные вашего персонажа берутся из армори, так что обновите его перед симуляцией выйдя из игрового мира')
    if message.content.startswith('!nerd'):
        yield from client.send_message(message.channel, 'Я делаю 10k итераций боя с одной целью (patchwerk), используя статы и таланты из армори на момент сима. Кастомные симы недоступны.')
        yield from client.send_message(message.channel, 'SimulationCraft 725-01 for World of Warcraft 7.2.5 Live (wow build 24287, git build a7b6fa3)')
        yield from client.send_message(message.channel, 'Моё железо виртуальное, находится на Amazon. Даже бот находится в Amazon, а ты нет.')
    if message.content.startswith('!2sim ') or message.content.startswith('!3sim ') or message.content.startswith('!sim3 ') or message.content.startswith('!sim ') or message.content.startswith('!dps '):
        run2 = False
        run3 = False
        runAll3 = False
        runStandalone = False
        runDPS = False

        if(message.content.startswith('!2sim ')):
            character = charstrip(message.content, '!2sim ').strip()
            run2 = True
        elif(message.content.startswith('!3sim ')):
            character = charstrip(message.content, '!3sim ').strip()
            run3 = True
        elif(message.content.startswith('!sim3 ')):
            character = charstrip(message.content, '!sim3 ').strip()
            runAll3 = false
        elif(message.content.startswith('!sim ')):
            character = charstrip(message.content, '!sim ').strip()
            runStandalone = True
        elif(message.content.startswith('!dps ')):
            character = charstrip(message.content, '!dps ').strip()
            runDPS = True

        server = serverstrip(message.content).replace("'", "").strip()
        region = regionfind(message.content).strip()
        escapeAuthor = author.mention.replace(">", "\>").replace("<", "\<")        
        print('Ищем %s - %s - %s' % (character, server, region))
#        yield from client.send_message(message.channel, 'Считаем статы для %s - %s - %s. Если одновременно поступило несколько вопросов я могу подвиснуть. Будьте взаимовежливы ' % (character, server, region))                    
        if char_exists(character, server, region):
            print("Go Go Go")
            isDPS = is_dps(character, server, region)
            spec = get_spec(character, server, region)
            role = get_role(character, server, region)
            print('Looking at %s - %s - %s who exists and is a %s' % (character, server, region, spec ))
            if (isDPS or spec == 'Shadow'):
                if(spec == 'Shadow' or True):
#                    yield from client.send_message(message.channel, 'Мне требуется несколько минут чтоб обработать этот запрос. Я позову когда закончу рассчеты')
                    yield from client.send_message(message.channel, 'Текущий спек для %s-%s-%s: %s. Последнее обновление армори: %s' % (character, server, region, spec, armory_date(character, server, region)))                                      
                    if(run2):
                        print('Starting a 2 target standalone')
                        yield from client.send_message(message.channel, 'Начинаю сим для двух целей  %s - %s - %s. Это займет несколько минут' % (character, server, region))
                        subprocess.Popen('python3 sim.py %s %s %s %s %s 2 yes' % (character, server, message.channel.id, escapeAuthor, region), shell=True)
                    elif(run3):
                        print('Starting a 3 target standalone')
                        yield from client.send_message(message.channel, 'Начинаю сим для трёх целей %s - %s - %s. Это займет несколько минут' % (character, server, region))
                        subprocess.Popen('python3 sim.py %s %s %s %s %s 3 yes' % (character, server, message.channel.id, escapeAuthor, region), shell=True)
                    elif(runAll3):
                        print('Starting the 1,2,3 sim run')
                        yield from client.send_message(message.channel, 'Начинаю 3 сима для одной, двух и трёх целей %s - %s - %s. Это займет несколько минут.' % (character, server, region))              
                        subprocess.Popen('python3 sim.py %s %s %s %s %s 1 no' % (character, server, message.channel.id, escapeAuthor, region), shell=True)
                    elif(runStandalone):
                        print('Starting a 1 target standalone')
#                        yield from client.send_message(message.channel, 'Начинаю сим для  %s - %s - %s. Это займёт несколько минут' % (character, server, region))
                        subprocess.Popen('python3 sim.py %s %s %s %s %s 1 yes' % (character, server, message.channel.id, escapeAuthor, region), shell=True)
                    elif(runDPS):
                        print('Starting DPS only')
#                        yield from client.send_message(message.channel, 'Начинаю сим для  %s - %s - %s. Это займет несколько минут' % (character, server, region))          
                        subprocess.Popen('python3 dps.py %s %s %s %s %s' % (character, server, message.channel.id, escapeAuthor, region), shell=True)
                    else:
                        #Failsafe is single sim
                        print('I shouldn\'t be here, but gonna run a single target sim')
#                        yield from client.send_message(message.channel, 'Начинаю сим для %s - %s - %s. Это займет несколько минут' % (character, server, region))
                        subprocess.Popen('python3 sim.py %s %s %s %s %s 1 yes' % (character, server, message.channel. id, escapeAuthor, region), shell=True)
                else:
                    yield from client.send_message(message.channel, '%s: Добро пожаловать отсюда' % author.mention)
            else:
                if (role == 'TANK'):
                    yield from client.send_message(message.channel, '%s: Ты зашел не в тот двор приятель. Ко мне могут обратиться только слуги Н\'Зота' % author.mention)
                elif (role == 'HEALING'):
                    yield from client.send_message(message.channel, '%s: Ты зашел не в тот двор приятель. Ко мне могут обратиться только слуги Н\'Зота' % author.mention)
                else:
                    yield from client.send_message(message.channel, '%s: Ошибка при сканировании %s-%s-%s. Роль не определена. Убедитесь что вы правильно составили запрос \'!sim charactername-servername-region\'.' % (author.mention, character, server, region))
        else:
            yield from client.send_message(message.channel, '%s: Персонаж %s-%s-%s не найден. Убедитесь что вы правильно составили запрос \'!sim charactername-servername-region\'.' % (author.mention, character, server, region))      

client.run(token)
