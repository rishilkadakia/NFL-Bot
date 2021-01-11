import discord
from discord.ext import commands
import rules
from rules import rules
import asyncio
import requests
from bs4 import BeautifulSoup
import concurrent.futures
import random
import replies
from replies import replies

def web_scrape(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    return soup

# Bot Prefix
client = commands.Bot(command_prefix='!')

# On Run
@client.event
async def on_ready():
    print('Bot is ready.')
    await client.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.playing, name="Rishil_Emperor#0001"), )

# On Error
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send('You do not have permission to perform this command.')

# !hello
@client.command(aliases=['hi'])
async def hello(ctx):
    await ctx.send('Hi!')

# !bye
@client.command(aliases=['goodbye'])
async def bye(ctx):
    await ctx.send('Bye!')

# !stats <player>
@client.command()
async def stats(ctx, *, searchterm):
    player_name = searchterm.split(' ')
    first_name = player_name[0]
    last_name = player_name[1]
    url = f'https://www.nfl.com/players/{first_name.lower()}-{last_name.lower()}/stats/'
    with concurrent.futures.ThreadPoolExecutor() as pool:
        soup = await asyncio.get_event_loop().run_in_executor(pool, web_scrape, url)
    data = []
    for a in soup.find_all(class_="d3-o-table--horizontal-scroll"):
        data.append(a.get_text())
        print(data)

# !rule <number>
@client.command()
async def rule(ctx, *, number):
    await ctx.send(rules[int(number) - 1])

# !coinflip
@client.command(aliases = ['coinflip'])
async def flip(ctx):
    coin = ['Heads', 'Tails']
    await ctx.send(f':coin: | It\'s **{random.choice(coin)}**!')

# !8ball <question>
@client.command(aliases = ['8Ball', '8ball'])
async def fortune(ctx, *, statement):
    reply = random.choice(replies)
    await ctx.send(f'🎱 | {reply}')

# !rps <choice>
@client.command(aliases = ['rockpaperscissors', 'RPS'])
async def rps(ctx, *, choice):
    rps_choices = ['rock', 'paper', 'scissors']
    rps_choice = random.choice(rps_choices)
    if choice.lower() == rps_choice:
        await ctx.send(f'I chose `{rps_choice}` and you chose `{choice.lower()}`. **Tie!**')
    elif choice.lower() == 'rock' and rps_choice == 'scissors' or choice.lower() == 'scissors' and rps_choice == 'paper' or choice.lower() == 'paper' and rps_choice == 'rock':
        await ctx.send(f'I chose `{rps_choice}` and you chose `{choice.lower()}`. **You Win!**')
    elif choice.lower() == 'rock' and rps_choice == 'paper' or choice.lower() == 'paper' and rps_choice == 'scissors' or choice.lower() == 'scissors' and rps_choice == 'rock':
        await ctx.send(f'I chose `{rps_choice}` and you chose `{choice.lower()}`. **I Win!**')
    else:
        await ctx.send(f'Something went wrong. Please make sure your choice is either `rock`, `paper`, or `scissors`.')

# !choosenumber <number 1> <number 2>
@client.command(aliases = ['number'])
async def choosenumber(ctx, num1, *, num2):
    try:
        num_1 = int(num1)
        num_2 = int(num2)
        if num_1 > num_2:
            await ctx.send(f'Please make sure you are inputting two numbers. Make sure that the first number is less than the second number.')
        else:
            await ctx.send(f'Number: **{random.choice(range(num_1, num_2+1))}**')
    except:
        await ctx.send(f'Please make sure you are inputting two numbers. Make sure that the first number is less than the second number.')

# !purge <amount>
@client.command(aliases=['clear'])
async def purge(ctx, amount):
    await ctx.channel.purge(limit=int(amount) + 1)

# !kick <user>
@client.command()
@commands.has_permissions(kick_members = True)
async def kick(ctx, member : discord.Member,*, reason = 'No Reason Provided'):
    await ctx.send(f'{member} has been kicked from NFL Discord for {reason}.')
    await member.kick(reason=reason)

# !ban <user>
@client.command()
@commands.has_permissions(ban_members = True)
async def ban(ctx, member : discord.Member,*, reason = 'No Reason Provided'):
    await ctx.send(f'{member} has been banned from NFL Discord for {reason}.')
    await member.ban(reason=reason)

# !unban <user>
@client.command()
@commands.has_permissions(ban_members = True)
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_disc = member.split('#')
    for banned_entry in banned_users:
        user = banned_entry.user
        if(user.name, user.discriminator) == (member_name, member_disc):
            await ctx.guild.unban(user)
            await ctx.send(f'{member_name} has been unbanned.')
            return

# !mute <user> <time> <unit>
@client.command()
@commands.has_permissions(kick_members=True)
async def mute(ctx, member : discord.Member, duration=0,*, unit = None):
    if not unit or unit.lower() not in ['s', 'm', 'h', 'd']:
        return await ctx.send('Give a correct unit: `s = seconds | m = minutes | h = hours | d = days`.')
    muted_role = ctx.guild.get_role(607034271990939658)
    await ctx.send(f'**{member.mention}** has been muted for *{duration}{unit}*.')
    await member.add_roles(muted_role)
    if unit.lower() == 's':
        wait = 1 * duration
    if unit.lower() == 'm':
        wait = 60 * duration
    if unit.lower() == 'h':
        wait = 3600 * duration
    if unit.lower() == 'd':
        wait = 86400 * duration
    await asyncio.sleep(wait)
    await member.remove_roles(muted_role)
    await ctx.send(f'**{member.mention}** has been unmuted.')

# !unmute <user>
@client.command()
@commands.has_permissions(kick_members=True)
async def unmute(ctx, member : discord.Member):
    muted_role = ctx.guild.get_role(607034271990939658)
    await member.remove_roles(muted_role)
    await ctx.send(f'**{member.mention}** has been unmuted.')

# !warn <user> <reason>
@client.command()
@commands.has_permissions(kick_members=True)
async def warn(ctx, member : discord.Member, *, reason = 'No Reason Provided'):
    await ctx.send(f'**{member}** has been warned for {reason}.')

# !ping
@client.command()
async def ping(ctx):
    latency = str(client.latency * 1000)
    decimal = latency.split('.')
    await ctx.send(f'🏓 | **Pong!** `{decimal[0]}ms`')

# !whois <user>
colors = [discord.Colour.red(), discord.Colour.blue()]
@client.command(aliases = ['user', 'info'])
async def whois(ctx, member : discord.Member = None):
    if member is None:
        member = ctx.author
    embed = discord.Embed(title = member.name, description = member.mention, color = random.choice(colors))
    embed.add_field(name = 'ID', value = member.id , inline = True)
    embed.set_thumbnail(url=member.avatar_url)
    embed.set_footer(icon_url = ctx.author.avatar_url, text = f'Requested By: {ctx.author.name}')
    await ctx.send(embed = embed)

# !calc <number> <operator> <number>
@client.command(aliases=['calculate'])
async def calc(ctx, *, equation):
    try:
        list = equation.split(' ')
        digits1 = 0
        digits2 = 0
        for x in list[0]:
          if x != '.':
            digits1 += 1
          else:
            continue
        for x in list[2]:
          if x != '.':
            digits2 += 1
          else:
            continue
        if digits1 <= 10 and digits2 <= 10:
          if list[1] == '+':
             await ctx.send(f'{list[0]} + {list[2]} = {float(list[0]) + float(list[2])}')
          elif list[1] == '-':
             await ctx.send(f'{list[0]} - {list[2]} = {float(list[0]) - float(list[2])}')
          elif list[1].lower() == 'x' or list[1] == '*':
             await ctx.send(f'{list[0]} x {list[2]} = {float(list[0]) * float(list[2])}')
          elif list[1] == '/':
            await ctx.send(f'{list[0]} / {list[2]} = {float(list[0]) / float(list[2])}')
          else:
              await ctx.send(f'Could not understand; incorrect format. Include a space between number and operator. Please make sure to perform !calc like this: <number> <operator> <number>.\nEx:\n- !calc 4 x 5\n- !calc 3345 + 123\n- !calc 54 / 3')
        else:
            await ctx.send(f'Numbers must only contain 10 or less digits.')
    except:
          await ctx.send(f'Could not understand; incorrect format. Include a space between number and operator. Please make sure to perform !calc like this: <number> <operator> <number>.\nEx:\n- !calc 4 x 5\n- !calc 3345 + 123\n- !calc 54 / 3')

client.run('NzkyMTg0NTY0MDM0MzA2MDY4.X-aBXg.CF8OHklFdCDoOj7ucX1iUPEC7g4')