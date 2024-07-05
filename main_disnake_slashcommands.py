# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Please setup these settings before launching the bot.

# =============[General]=============
token = '' # this is your discord bot token. 
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import disnake
import disnake.ext.commands
from disnake.ext import commands as command
import random
import time
import asyncio
import requests

ltime = time.asctime(time.localtime())
intents = disnake.Intents.all()
client = command.Bot(command_prefix=disnake.ext.commands.when_mentioned, intents=intents)
Client = disnake.Client(intents=intents)
client.remove_command('help')
rule34_base_url = "https://api.rule34.xxx/index.php?page=dapi&s=post&q=index&json=1"
GUILD_IDS = [1134166774657581089]

def json_parse(url):
	try:
		response = requests.get(url)
		response.raise_for_status()  # Raises HTTPError if the HTTP request returned an unsuccessful status code
		response_json = response.json()
		if response_json:
			return response_json[0]['file_url']
	except (requests.exceptions.HTTPError, requests.exceptions.RequestException, ValueError) as e:
		print(f"[ERROR {ltime}]: {e}")
	return None

def json_count(url):
	try:
		response = requests.get(url)
		response.raise_for_status()
		response_json = response.json()
		return len(response_json)
	except (requests.exceptions.HTTPError, requests.exceptions.RequestException, ValueError) as e:
		print(f"[ERROR {ltime}]: {e}")
	return 0

def pidfix(tags):
	url = f"{rule34_base_url}&tags={tags}"
	count = json_count(url)
	return max(count - 1, 0)

def rdl(tags, post_count):
	print(f'[INFO {ltime}]: post_count provided: {post_count}')
	if post_count > 2000:
		post_count = 2000
	if post_count == 0:
		print(f'[INFO {ltime}]: post_count is 0, accommodating for offset overflow bug.') 
	else:
		post_count = random.randint(1, 31)
	print(f'[INFO {ltime}]: post_count after randomizing: {post_count}')
	url = f"{rule34_base_url}&tags={tags}&pid={post_count}"
	file_url = json_parse(url)

	if file_url and 'webm' in file_url:
		if 'sound' not in tags and 'webm' not in tags:
			print(f"[INFO {ltime}]: We got a .webm, user didn't specify sound. Recursing. user tags: {tags}")
			file_url = rdl(tags, pidfix(tags))
	return file_url

async def statuschange():
	while True:
		await client.change_presence(activity=disnake.Game(name='with my pussy'))
		await asyncio.sleep(10)
		await client.change_presence(activity=disnake.Game(name='/help'))
		await asyncio.sleep(10)

@client.event
async def on_ready():
	print(f'[INFO {ltime}]: Logged in as {client.user.name}!')
	await statuschange()
# ================================================================================================================
@client.slash_command(name="porn", description="Polls rule34 for porn following your tags.", guild_ids=GUILD_IDS)
async def porn(inter: disnake.ApplicationCommandInteraction, tag: str):
	tag = tag.replace(" ","_")
	tag = tag.replace(',','')
	tag = tag.replace('(','')
	tag = tag.replace(')','')
	tag = tag.replace("'",'')
	tag += "*"
	print(f'[DEBUG {ltime}]: tag is now {tag}')
	waitone = await inter.channel.send("***:desktop: We're polling Rule34! Please wait a few seconds.***")
	newint = pidfix(tag)
	if newint > 2000:
		newint = 2000
	answer = rdl(tag, newint)
	print(f'[DEBUG {ltime}]: answer is now {answer}')
	if 'mp4' in answer:
			print(f'[DEBUG {ltime}]: video file detected cant send in embed, sending in normal message')
			await waitone.delete()
			return await inter.response.send_message(f'Rule34: {tag}\n{answer}')
	tag = tag.replace('*','')
	tag = tag.replace('_',' ')
	tag = tag.replace(',','')
	tag = tag.replace('(','')
	tag = tag.replace(')','')
	tag = tag.replace("'",'')
	if answer:
		if 'webm' in answer:
			await waitone.delete()
			await inter.response.send_message(answer)
		else:
			embed = disnake.Embed(title=f'Rule34: {tag}', color=inter.author.color)
			embed.set_author(name=f'{inter.author.display_name}', icon_url=f'{inter.author.avatar.url}')
			embed.set_thumbnail(url='https://rule34.paheal.net/themes/rule34v2/rule34_logo_top.png')
			embed.set_image(url=f'{answer}')
			embed.set_footer(text="Pornbot 2.0 - made by jess#3347 and modified by @hotment", icon_url='https://cdn.discordapp.com/avatars/973107233816735754/a_0719060fdd5f311a79d1806132566551.gif?size=128')
			await waitone.delete()
			await inter.response.send_message(embed=embed)
	else:
		await waitone.delete()
		await inter.response.send_message("***:warning: Could not fetch data from Rule34. Please try again later.***")
# ================================================================================================================
@client.slash_command(name="rr", description="Russian roulette. Posts gore images if gun goes off.", guild_ids=GUILD_IDS)
async def rr(inter: disnake.ApplicationCommandInteraction):
	bullet = random.randint(1,6)
	if bullet == 3:
		url = rdl('gore',random.randint(1,100))
		if 'mp4' in url:
			print(f'[DEBUG {ltime}]: video file detected cant send in embed, sending in normal message')
			return await inter.response.send_message(f'CRACK.\n{url}')
		embed = disnake.Embed(title=f'CRACK.')
		embed.set_author(name=f'{inter.author.display_name} - Russian roulette',icon_url=f'{inter.author.avatar.url}')
		embed.set_image(url=url)
		embed.set_footer(text='Pornbot 2.0 - Made by jess#3347 and modified by @hotment')
		await inter.response.send_message(embed=embed)
	if bullet == 6:
		url = rdl('gore',random.randint(1,100))
		if 'mp4' in url:
			print(f'[DEBUG {ltime}]: video file detected cant send in embed, sending in normal message')
			return await inter.response.send_message(f'CRACK.\n{url}')
		embed = disnake.Embed(title=f'CRACK.')
		embed.set_author(name=f'{inter.author.display_name} - Russian roulette',icon_url=f'{inter.author.avatar.url}')
		embed.set_image(url=rdl('gore',random.randint(1,100)))
		embed.set_footer(text='Pornbot 2.0 - Made by jess#3347 and modified by @hotment')
		await inter.response.send_message(embed=embed)
	elif bullet != 3 or bullet != 6:
		await inter.response.send_message('***Click...***')
# ================================================================================================================
@client.slash_command(name="rcoin", description="Flips a coin and posts a nsfw image based on what you get.", guild_ids=GUILD_IDS)
async def rcoin(inter: disnake.ApplicationCommandInteraction):
	side = random.randint(1,100)
	if side == 50 or side > 50:
		url=rdl('blowjob animated',random.randint(1,100))
		if 'mp4' in url:
			print(f'[DEBUG {ltime}]: video file detected cant send in embed, sending in normal message')
			return await inter.response.send_message(f'NSFW Coinflip: Head\n{url}')
		embed = disnake.Embed(title=f'NSFW Coinflip: Heads', color=inter.author.color)
		embed.set_author(name=f'{inter.author.display_name} - NSFW Coinflip',icon_url=f'{inter.author.avatar.url}')
		embed.set_image(url=url)
		print(url)
		embed.set_footer(text='Pornbot 2.0 - Made by jess#3347 and modified by @hotment')
		await inter.send(embed=embed)
	elif side < 50:
		url=rdl('big_ass animated',random.randint(1,100))
		if 'mp4' in url:
			print(f'[DEBUG {ltime}]: video file detected cant send in embed, sending in normal message')
			return await inter.response.send_message(f'NSFW Coinflip: Tails\n{url}')
		embed = disnake.Embed(title=f'NSFW Coinflip: Tails', color=inter.author.color)
		embed.set_author(name=f'{inter.author.display_name} - NSFW Coinflip',icon_url=f'{inter.author.avatar.url}')
		embed.set_image(url=url)
		print(url)
		embed.set_footer(text='Pornbot 2.0 - Made by jess#3347 and modified by @hotment')
		await inter.channel.send(embed=embed)
# ================================================================================================================
@client.slash_command(name="fcoin", description="Flips a coin and posts a nsfw furry image based on what you get.", guild_ids=GUILD_IDS)
async def fcoin(inter: disnake.ApplicationCommandInteraction):
	side = random.randint(1,100)
	if side == 50 or side > 50:
		url=rdl('furry blowjob animated',random.randint(1,100))
		if 'mp4' in url:
			return await inter.response.send_message(f'Furry Coinflip: Heads\n{url}')
		embed = disnake.Embed(title=f'Furry Coinflip: Heads', color=inter.author.color)
		embed.set_author(name=f'{inter.author.display_name} - Furry Coinflip',icon_url=f'{inter.author.avatar.url}')
		embed.set_image(url=url)
		embed.set_footer(text='Pornbot 2.0 - Made by jess#3347 and modified by @hotment')
		await inter.channel.send(embed=embed)
	elif side < 50:
		url=rdl('furry tail animated',random.randint(1,100))
		if 'mp4' in url:
			return await inter.response.send_message(f'Furry Coinflip: Tails\n{url}')
		embed = disnake.Embed(title=f'Furry Coinflip: Tails', color=inter.author.color)
		embed.set_author(name=f'{inter.author.display_name} - Furry Coinflip',icon_url=f'{inter.author.avatar.url}')
		embed.set_image(url=url)
		embed.set_footer(text='Pornbot 2.0 - Made by jess#3347 and modified by @hotment')
		await inter.channel.send(embed=embed)
# ================================================================================================================
@client.slash_command(name="coin", description="Flips a coin.", guild_ids=GUILD_IDS)
async def coin(inter: disnake.ApplicationCommandInteraction):
	side = random.randint(1,100)
	if side == 50 or side > 50:
		await inter.response.send_message('***The coin landed on heads***')
	if side < 50:
		await inter.response.send_message('***The coin landed on tails.***')
# ================================================================================================================
@client.slash_command(name="d6", description="Rolls (a/multiple) 6 sided die.", guild_ids=GUILD_IDS)
async def d6(inter: disnake.ApplicationCommandInteraction, die_amount: int = 1):
	total = 0
	for i in range(die_amount):
		total += random.randint(1,6)
	await inter.response.send_message(f'You rolled a total of {total}') 
# ================================================================================================================
@client.slash_command(name="d8", description="Rolls (a/multiple) 8 sided die.", guild_ids=GUILD_IDS)
async def d8(inter: disnake.ApplicationCommandInteraction, die_amount: int = 1):
	total = 0
	for i in range(die_amount):
		total += random.randint(1,8)
	await inter.response.send_message(f'You rolled a total of {total}') 
# ================================================================================================================
@client.slash_command(name="d10", description="Rolls (a/multiple) 10 sided die.", guild_ids=GUILD_IDS)
async def d10(inter: disnake.ApplicationCommandInteraction, die_amount: int = 1):
	total = 0
	for i in range(die_amount):
		total += random.randint(1,10)
	await inter.response.send_message(f'You rolled a total of {total}') 
# ================================================================================================================
@client.slash_command(name="d12", description="Rolls (a/multiple) 12 sided die.", guild_ids=GUILD_IDS)
async def d12(inter: disnake.ApplicationCommandInteraction, die_amount: int = 1):
	total = 0
	for i in range(die_amount):
		total += random.randint(1,12)
	await inter.response.send_message(f'You rolled a total of {total}') 
# ================================================================================================================
@client.slash_command(name="dc", description="Rolls a custom-sided die", guild_ids=GUILD_IDS)
async def dc(inter: disnake.ApplicationCommandInteraction, sides: int, die_amount: int = 1):
	total = 0
	for i in range(die_amount):
		total += random.randint(1,sides)
	await inter.response.send_message(f'You rolled a total of: {total}')
# ================================================================================================================
@client.slash_command(name="help", description="helps you with the bot usage", guild_ids=GUILD_IDS)
async def help(inter: disnake.ApplicationCommandInteraction):
	embed=disnake.Embed(title="Pornbot help", description="Prefix is &", color=0xff80ff)
	embed.set_author(name=f'{inter.author.display_name}', icon_url=f'{inter.author.avatar.url}')
	embed.add_field(name="'porn [tags]'", value="Polls rule34 for porn following your tags.", inline=False)
	embed.add_field(name="'d6 [dice]'", value="Rolls (a/multiple) 6 sided die. Change [dice] to add several.", inline=False)
	embed.add_field(name="'d8 [dice]'", value="Rolls (a/multiple) 8 sided die, change your [dice] argument to add several.", inline=False)
	embed.add_field(name="'d10 [dice]'", value="Rolls (a/multiple) 10 sided die, change your [dice] argument to add several.", inline=False)
	embed.add_field(name="'d12 [dice]'", value="Rolls (a/multiple) 12 sided die, change your [dice] argument to add several.", inline=False)
	embed.add_field(name="'dc <sides> [dice]'", value="Rolls a custom-sided die, change your <sides> argument to set sides, and your [dice] argument to add more dice.", inline=False)
	embed.add_field(name="'coin'", value="Flips a coin.", inline=False)
	embed.add_field(name="'rcoin'", value="Flips a coin and posts a nsfw image based on what you get.", inline=False)
	embed.add_field(name="'fcoin'", value="Flips a coin and posts a nsfw furry image based on what you get.", inline=False)
	embed.add_field(name="'rr'", value="Russian roulette. Posts gore images if gun goes off.", inline=False)
	embed.add_field(name="'shibe'", value="Posts an image of a Shiba inu. (currently borken)", inline=False)
	embed.add_field(name="'cat'", value="Posts an image of a cat. (currently borken)", inline=False)
	embed.add_field(name="'bird'", value="Posts an image of a bird. (currently borken)", inline=False)
	embed.add_field(name="'suggest'",value="Sends a link to the github to suggest features and improvements aswell as make bug reports.")
	embed.set_footer(text="Pornbot 2.0 - Made by jess#3347 and modified by @hotment",icon_url='https://cdn.discordapp.com/avatars/973107233816735754/a_0719060fdd5f311a79d1806132566551.gif?size=128')
	await inter.response.send_message(embed=embed, ephemeral=True)
# ================================================================================================================
@client.slash_command(name="suggest", description="suggest something ig", guild_ids=GUILD_IDS)
async def suggest(inter: disnake.ApplicationCommandInteraction):
	await inter.response.send_message(f'***If you have a suggestion, make an issue on the github repo: https://github.com/whitetrashyt/r34discordbot/issues***', ephemeral=True)
# ================================================================================================================
@client.slash_command(name="shibe", description="Posts an image of a Shiba inu.", guild_ids=GUILD_IDS)
async def shibe(inter: disnake.ApplicationCommandInteraction):
    return await inter.response.send_message("this command is currently broken and isn't working", ephemeral=True)
    '''r = requests.get('https://shibe.online/api/shibes?count=1')
	y = r.json()
	embed= discord.Embed(title='Have a shibe.',color=0xff80ff)
	embed.set_author(name=f'{inter.author.display_name}',icon_url=f'{inter.author.avatar.url}')
	embed.set_image(url=f'{y[0]}')
	print(f"[INFO {ltime}]: IMG URL IS {y[0]}")
	embed.set_footer(text="Pornbot 2.0 - Made by jess#3347 and modified by @hotment",icon_url='https://cdn.discordapp.com/avatars/973107233816735754/a_0719060fdd5f311a79d1806132566551.gif?size=128')
	await inter.send(embed=embed)'''
# ================================================================================================================
@client.slash_command(name="cat", description="Posts an image of a cat.", guild_ids=GUILD_IDS)
async def cat(inter: disnake.ApplicationCommandInteraction):
    return await inter.response.send_message("this command is currently broken and isn't working", ephemeral=True)
    '''r = requests.get('https://shibe.online/api/cats?count=1')
	y = r.json()
	embed = discord.Embed(title='Have a kitty.',color=0xff80ff)
	embed.set_author(name=f'{inter.author.display_name}',icon_url=f'{inter.author.avatar.url}')
	embed.set_image(url=f'{y[0]}')
	print(f"[INFO {ltime}]: IMG URL IS {y[0]}")
	embed.set_footer(text="Pornbot 2.0 - Made by jess#3347 and modified by @hotment",icon_url='https://cdn.discordapp.com/avatars/973107233816735754/a_0719060fdd5f311a79d1806132566551.gif?size=128')
	await inter.send(embed=embed)'''
# ================================================================================================================
@client.slash_command(name="bird", description="Posts an image of a bird.", guild_ids=GUILD_IDS)
async def bird(inter: disnake.ApplicationCommandInteraction):
    return await inter.response.send_message("this command is currently broken and isn't working", ephemeral=True)
    '''r = requests.get('https://shibe.online/api/birds?count=1')
	y = r.json()
	embed= discord.Embed(title='Have a bird.',color=0xff80ff)
	embed.set_author(name=f'{inter.author.display_name}',icon_url=f'{inter.author.avatar.url}')
	embed.set_image(url=f'{y[0]}')
	print(f"[INFO {ltime}]: IMG URL IS {y[0]}")
	embed.set_footer(text="Pornbot 2.0 - Made by jess#3347 and modified by @hotment",icon_url='https://cdn.discordapp.com/avatars/973107233816735754/a_0719060fdd5f311a79d1806132566551.gif?size=128')
	await inter.send(embed=embed)'''
# ================================================================================================================


client.run(token)
