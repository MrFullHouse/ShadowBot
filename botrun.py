import subprocess
import asyncio

while(True):
    subprocess.call('python3 discordbot.py', shell=True)
    asyncio.sleep(10)
