ShadowBot is a discord bot to assist with simming World of Warcraft.

ShadowBot will run Simcraft for a UNIX environment and output a pawn string, DPS sim results, and link to html simulation file (need apache2 server on bot machine). Currently US and EU regions are supported.

ShadowBot is based off of Silkybot 0.9 (which is configured for Windows), the link to the repo can be found in the fork, or here: https://github.com/troyredfearn/silkybot.

ShadowBot requires BeautifulSoup, Discord.py, Simcraft, a Blizzard API key, and a Discord App turned bot

BeautifulSoup can be found: https://www.crummy.com/software/BeautifulSoup/
Discord.py's github is: https://github.com/Rapptz/discord.py
Simcraft can be downloaded at: http://www.simulationcraft.org/download.html
Simcraft's github can be found at: https://github.com/simulationcraft/simc
Build instructions for simcraft can be found at: https://github.com/simulationcraft/simc/wiki/HowToBuild
(in Ubuntu Server i always use next commands:
git clone https://github.com/simulationcraft/simc
cd engine/
make OPENSSL=1 optimized)
To register for a Blizzard API key, go here: https://dev.battle.net/
To register a Discord app, go here: https://discordapp.com/developers/applications

Further instructions for setting up are on the wiki: https://github.com/gitket/TempleBot/wiki/How-to-set-up-TempleBot-for-the-first-time.

Note to those who use this code:
When updating simcraft version, update the version of simcraft under the !nerd command in discordbot.py so it is up to date

To run the bot, the command is:
python3 botrun.py

To enable DPS estimate along with the pawn string, remove the # on line 58 in sim.py
