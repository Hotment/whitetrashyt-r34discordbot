# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Please setup these settings before launching the bot.

# =============[General]=============
token = '' # this is your discord bot token. 
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import discord
from discord.ext import commands as command
import random
import time
import asyncio
import requests

ltime = time.asctime(time.localtime())
intents = discord.Intents.all()
client = command.Bot(command_prefix='&', intents=intents)
Client = discord.Client(intents=intents)
client.remove_command('help')
rule34_base_url = "https://api.rule34.xxx/index.php?page=dapi&s=post&q=index&json=1"

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
        await client.change_presence(activity=discord.Game(name='with my pussy'))
        await asyncio.sleep(10)
        await client.change_presence(activity=discord.Game(name='&help'))
        await asyncio.sleep(10)

@client.event
async def on_ready():
    print(f'[INFO {ltime}]: Logged in as {client.user.name}!')
    await statuschange()
# ================================================================================================================
@client.command()
async def porn(ctx, *args):
    arg = ' '.join(args)
    arg = arg.replace(" ","_")
    arg += "*"
    print(f'[DEBUG {ltime}]: arg is now {arg}')
    waitone = await ctx.send("***:desktop: We're polling Rule34! Please wait a few seconds.***")
    newint = pidfix(arg)
    if newint > 2000:
        newint = 2000
    answer = rdl(arg, newint)
    arg = arg.replace('*','')
    arg = arg.replace('_',' ')
    print(f'[DEBUG {ltime}]: arg is now {arg}')
    if answer:
        if 'webm' in answer:
            await waitone.delete()
            await ctx.send(answer)
        else:
            embed = discord.Embed(title=f'Rule34: {arg}', color=ctx.author.color)
            embed.set_author(name=f'{ctx.author.display_name}', icon_url=f'{ctx.author.avatar.url}')
            embed.set_thumbnail(url='https://rule34.paheal.net/themes/rule34v2/rule34_logo_top.png')
            embed.set_image(url=f'{answer}')
            embed.set_footer(text="Pornbot 2.0 - made by jess#3347", icon_url='https://cdn.discordapp.com/avatars/268211297332625428/e5e43e26d4749c96b48a9465ff564ed2.png?size=128')
            await waitone.delete()
            await ctx.send(embed=embed)
    else:
        await waitone.delete()
        await ctx.send("***:warning: Could not fetch data from Rule34. Please try again later.***")
# ================================================================================================================
@client.command()
async def rr(ctx):
	bullet = random.randint(1,6)
	if bullet == 3:
		embed = discord.Embed(title=f'CRACK.')
		embed.set_author(name=f'{ctx.author.display_name} - Russian roulette',icon_url=f'{ctx.author.avatar.url}')
		embed.set_image(url=rdl('gore',random.randint(1,100)))
		embed.set_footer(text='Pornbot 2.0 - Made by jess#3347')
		await ctx.send(embed=embed)
	if bullet == 6:
		embed = discord.Embed(title=f'CRACK.')
		embed.set_author(name=f'{ctx.author.display_name} - Russian roulette',icon_url=f'{ctx.author.avatar.url}')
		embed.set_image(url=rdl('gore',random.randint(1,100)))
		embed.set_footer(text='Pornbot 2.0 - Made by jess#3347')
		await ctx.send(embed=embed)
	elif bullet != 3 or bullet != 6:
		await ctx.send('***Click...***')
# ================================================================================================================
@client.command()
async def rcoin(ctx):
	side = random.randint(1,100)
	if side == 50 or side > 50:
		url=rdl('blowjob animated',random.randint(1,100))
		if 'mp4' in url:
			await ctx.channel.send('NSFW Coinflip: Head')
			return await ctx.channel.send(url)
		embed = discord.Embed(title=f'NSFW Coinflip: Heads', color=ctx.author.color)
		embed.set_author(name=f'{ctx.author.display_name} - NSFW Coinflip',icon_url=f'{ctx.author.avatar.url}')
		embed.set_image(url=url)
		print(url)
		embed.set_footer(text='Pornbot 2.0 - Made by jess#3347')
		await ctx.send(embed=embed)
	elif side < 50:
		url=rdl('big_ass animated',random.randint(1,100))
		if 'mp4' in url:
			await ctx.channel.send('NSFW Coinflip: Tails')
			return await ctx.channel.send(url)
		embed = discord.Embed(title=f'NSFW Coinflip: Tails', color=ctx.author.color)
		embed.set_author(name=f'{ctx.author.display_name} - NSFW Coinflip',icon_url=f'{ctx.author.avatar.url}')
		embed.set_image(url=url)
		print(url)
		embed.set_footer(text='Pornbot 2.0 - Made by jess#3347')
		await ctx.channel.send(embed=embed)
# ================================================================================================================
@client.command()
async def fcoin(ctx):
	side = random.randint(1,100)
	if side == 50 or side > 50:
		url=rdl('furry blowjob animated',random.randint(1,100))
		if 'mp4' in url:
			await ctx.channel.send('Furry Coinflip: Heads')
			return await ctx.channel.send(url)
		embed = discord.Embed(title=f'Furry Coinflip: Heads', color=ctx.author.color)
		embed.set_author(name=f'{ctx.author.display_name} - Furry Coinflip',icon_url=f'{ctx.author.avatar.url}')
		embed.set_image(url=url)
		embed.set_footer(text='Pornbot 2.0 - Made by jess#3347')
		await ctx.channel.send(embed=embed)
	elif side < 50:
		url=rdl('furry tail animated',random.randint(1,100))
		if 'mp4' in url:
			await ctx.channel.send('Furry Coinflip: Tails')
			return await ctx.channel.send(url)
		embed = discord.Embed(title=f'Furry Coinflip: Tails', color=ctx.author.color)
		embed.set_author(name=f'{ctx.author.display_name} - Furry Coinflip',icon_url=f'{ctx.author.avatar.url}')
		embed.set_image(url=url)
		embed.set_footer(text='Pornbot 2.0 - Made by jess#3347')
		await ctx.channel.send(embed=embed)
# ================================================================================================================
@client.command()
async def coin(ctx):
	side = random.randint(1,100)
	if side == 50 or side > 50:
		await ctx.channel.send('***The coin landed on heads***')
	if side < 50:
		await ctx.channel.send('***The coin landed on tails.***')
# ================================================================================================================
@client.command()
async def d6(ctx,arg=1):
	if arg == '':
		dside = str(random.randint(1,6))
		await ctx.channel.send(f'You rolled:' + ' ' + dside)
	else:
		try:
			aint = int(arg)
		except:
			print(f'Looks like the idiots a user and tried to provide string instead of int.')
			await ctx.channel.send('Hey idiot, send an integer, not text. Example: 6')
		mx = 6 * aint
		total = str(random.randint(1,mx))
			
		await ctx.channel.send(f'You rolled a total of:' + ' ' + total)
# ================================================================================================================
@client.command()
async def d8(ctx,arg=1):
	if arg == '':
		dside = str(random.randint(1,8))
		await ctx.channel.send(f'You rolled:' + ' ' + dside)
	else:
		try:
			aint = int(arg)
		except:
			print(f'Looks like the idiots a user and tried to provide string instead of int.')
			await ctx.channel.send('Hey idiot, send an integer, not text. Example: 6')
		mx = 8 * aint
		total = str(random.randint(1,mx))
			
		await ctx.channel.send(f'You rolled a total of:' + ' ' + total)
# ================================================================================================================
@client.command()
async def d10(ctx,arg=1):
	if arg == '':
		dside = str(random.randint(1,10))
		await ctx.channel.send(f'You rolled:' + ' ' + dside)
	else:
		try:
			aint = int(arg)
		except:
			print(f'Looks like the idiots a user and tried to provide string instead of int.')
			await ctx.channel.send('Hey idiot, send an integer, not text. Example: 6')
		mx = 10 * aint
		total = str(random.randint(1,mx))
		await ctx.send(f'You rolled a total of {total}')
# ================================================================================================================
@client.command()
async def d12(ctx,arg=1):
	if arg == '':
		dside = str(random.randint(1,12))
		await ctx.channel.send(f'You rolled:' + ' ' + dside)
	else:
		try:
			aint = int(arg)
		except:
			print(f'Looks like the idiots a user and tried to provide string instead of int.')
			await ctx.channel.send('Hey idiot, send an integer, not text. Example: 6')
		mx = 12 * aint
		total = str(random.randint(1,mx))
		await ctx.send(f'You rolled a total of {total}') 
# ================================================================================================================
@client.command()
async def dc(ctx,arg1,arg2 = 1):
	
	a = str(arg1)
	if str(arg2) != '':
		b = str(arg2)
	
	print('a is equal to' + a)
	print('b is equal to' + b) # it is really this simple.
	if b == '':
		dside = str(random.randint(1,int(a)))
		await ctx.channel.send(f'You rolled:' + ' ' + dside)
	else:
		mx = int(a) * int(b)
		print('max is:' + str(mx))
		total = str(random.randint(1,mx))
	await ctx.channel.send(f'You rolled a total of:' + ' ' + total)
# ================================================================================================================
@client.command()
async def help(ctx: discord.Message):
	embed=discord.Embed(title="Pornbot help", description="Prefix is &", color=0xff80ff)
	embed.set_author(name=f'{ctx.author.display_name}', icon_url=f'{ctx.author.avatar.url}')
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
	embed.set_footer(text="Pornbot 2.0 - Made by jess#3347",icon_url='https://cdn.discordapp.com/avatars/268211297332625428/e5e43e26d4749c96b48a9465ff564ed2.png?size=128')
	await ctx.send(embed=embed)
# ================================================================================================================
@client.command()
async def suggest(ctx):
	await ctx.channel.send(f'***If you have a suggestion, make an issue on the github repo: https://github.com/whitetrashyt/r34discordbot/issues***')
# ================================================================================================================
@client.command()
async def shibe(ctx):
    return await ctx.channel.send("this command is currently broken and isn't working")
    '''r = requests.get('https://shibe.online/api/shibes?count=1')
	y = r.json()
	embed= discord.Embed(title='Have a shibe.',color=0xff80ff)
	embed.set_author(name=f'{ctx.author.display_name}',icon_url=f'{ctx.author.avatar.url}')
	embed.set_image(url=f'{y[0]}')
	print(f"[INFO {ltime}]: IMG URL IS {y[0]}")
	embed.set_footer(text="Pornbot 2.0 - Made by jess#3347",icon_url='https://cdn.discordapp.com/avatars/268211297332625428/e5e43e26d4749c96b48a9465ff564ed2.png?size=128')
	await ctx.send(embed=embed)'''
# ================================================================================================================
@client.command()
async def cat(ctx):
    return await ctx.channel.send("this command is currently broken and isn't working")
    '''r = requests.get('https://shibe.online/api/cats?count=1')
	y = r.json()
	embed = discord.Embed(title='Have a kitty.',color=0xff80ff)
	embed.set_author(name=f'{ctx.author.display_name}',icon_url=f'{ctx.author.avatar.url}')
	embed.set_image(url=f'{y[0]}')
	print(f"[INFO {ltime}]: IMG URL IS {y[0]}")
	embed.set_footer(text="Pornbot 2.0 - Made by jess#3347",icon_url='https://cdn.discordapp.com/avatars/268211297332625428/e5e43e26d4749c96b48a9465ff564ed2.png?size=128')
	await ctx.send(embed=embed)'''
# ================================================================================================================
@client.command()
async def bird(ctx):
    return await ctx.channel.send("this command is currently broken and isn't working")
    '''r = requests.get('https://shibe.online/api/birds?count=1')
	y = r.json()
	embed= discord.Embed(title='Have a bird.',color=0xff80ff)
	embed.set_author(name=f'{ctx.author.display_name}',icon_url=f'{ctx.author.avatar.url}')
	embed.set_image(url=f'{y[0]}')
	print(f"[INFO {ltime}]: IMG URL IS {y[0]}")
	embed.set_footer(text="Pornbot 2.0 - Made by jess#3347",icon_url='https://cdn.discordapp.com/avatars/268211297332625428/e5e43e26d4749c96b48a9465ff564ed2.png?size=128')
	await ctx.send(embed=embed)'''
# ================================================================================================================


client.run(token)
