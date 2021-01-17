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
import re
import nfl_teams
from nfl_teams import nfl_teams

# Extra Functions
def web_scrape(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    return soup
def capitalize(str):
    str = str.lower()
    first_letter = str[0].upper()
    capitalized_str = f'{first_letter}{str[1:]}'
    return capitalized_str

# Bot Prefix
client = commands.Bot(command_prefix='!')
client.remove_command('help')

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
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send(f'You are on cooldown for {str(error.retry_after)[:3]} seconds!')

# !hello
@client.command(aliases = ['hi'])
async def hello(ctx):
    await ctx.send('Hi!')
    
# !bye
@client.command(aliases = ['goodbye'])
async def bye(ctx):
    await ctx.send('Bye!')

# !help <command>
@client.command()
async def help(ctx, *, command = None):
    if command is None:
        embed = discord.Embed(
            title = 'Commands:',
            description = 'Use `!help [command]` to get more info on a specific command.\n\n**NFL Commands:**\n`!stats <year> <player>`\n\n',
            color = discord.Color.dark_blue()
        )

# !whois <user>
@client.command(aliases = ['user'])
async def whois(ctx, member : discord.Member = None):
    if member is None:
        member = ctx.author
    embed = discord.Embed(title = member.name, description = member.mention, color = discord.Color.dark_blue())
    embed.add_field(name = 'ID', value = member.id , inline = True)
    embed.set_thumbnail(url=member.avatar_url)
    embed.set_footer(icon_url = ctx.author.avatar_url, text = f'Requested By: {ctx.author.name}')
    await ctx.send(embed = embed)

# !botinfo
@client.command()
async def botinfo(ctx):
    embed = discord.Embed(title = 'About NFL Bot:',
                          description = '- NFL Bot is a discord bot for NFL Discord, created by Rishil_Emperor#0001. \n- NFL Bot web-scrapes from [NFL\'s Website](https://https://www.nfl.com/) to collect stats and information.\n- NFL Bot is programmed and coded in Python with the [discord.py](https://github.com/Rapptz/discord.py) API wrapper.\n\n[Bot Invite Link](https://discord.com/api/oauth2/authorize?client_id=792184564034306068&permissions=8&scope=bot) • [Official Discord Server](https://discord.gg/pSgu26fg9R) • [GitHub Page](https://github.com/Rishil-Emperor/NFL-Bot)\n\nCreated by Rishil_Emperor#0001 | Special Thanks to QuaKe#5943',
                          color = discord.Color.dark_blue())
    embed.set_thumbnail(url = client.user.avatar_url)
    await ctx.send(embed=embed)

# !schedule
@client.command()
async def schedule(ctx):
    url = f'https://www.nfl.com/schedules/'
    with concurrent.futures.ThreadPoolExecutor() as pool:
        soup = await asyncio.get_event_loop().run_in_executor(pool, web_scrape, url)
    data = []
    for a in soup.find_all(class_ = 'd3-l-grid--outer d3-l-section-row nfl-o-matchup-group cc_cursor'):
        data.append(a.get_text)
        print(data)

# !info <player>
@client.command()
@commands.cooldown(1, 5, type=commands.BucketType.user)
async def info(ctx, *, searchterm):
    first_embed = discord.Embed(title = 'Loading...', color = discord.Color.dark_blue())
    msg = await ctx.send(embed = first_embed)
    player_name = searchterm.split(' ')
    first_name = player_name[0]
    last_name = player_name[1]
    if searchterm.lower() == 'michael vick':
        first_name = 'Mike'
        last_name = 'Vick'
    url = f'https://www.nfl.com/players/{first_name}-{last_name}/'
    with concurrent.futures.ThreadPoolExecutor() as pool:
        soup = await asyncio.get_event_loop().run_in_executor(pool, web_scrape, url)
    data = []
    data2 = []
    for a in soup.find_all(class_="nfl-c-player-header__title"):
        data.append(a.get_text())
        player_name = data[0]
    for b in soup.find_all(class_="nfl-c-player-header__position"):
        data.append(b.get_text())
        split_position = data[1].split('\n')
        player_position = split_position[1].strip(' ')
    for c in soup.find_all(class_="d3-o-list__item"):
        data.append(c.get_text())
        new_data = [x for x in data if 'Height' in x or 'Weight' in x]
    height_strip = new_data[0].strip('\n')
    height = height_strip.split('\n')
    weight_strip = new_data[1].strip('\n')
    weight = weight_strip.split('\n')
    print(height)
    print(weight)
    final_embed = discord.Embed(
        title = player_name,
        description = f'Position: {player_position}\n{height[0]}: {height[1]}\n{weight[0]}: {weight[1]}',
        color = discord.Color.dark_blue()
    )
    final_embed.set_footer(text = f'Powered by NFL.com | Coded by Rishil_Emperor#0001')
    await msg.edit(embed = final_embed)

# !stats <year> <player>
@client.command()
@commands.cooldown(1, 5, type=commands.BucketType.user)
async def stats(ctx, year, *, searchterm):
    first_embed = discord.Embed(title = 'Loading...', color = discord.Color.dark_blue())
    msg = await ctx.send(embed = first_embed)
    player_name = searchterm.split(' ')
    first_name = player_name[0]
    last_name = player_name[1]
    if searchterm.lower() == 'michael vick':
        first_name = 'Mike'
        last_name = 'Vick'
    url = f'https://www.nfl.com/players/{first_name.lower()}-{last_name.lower()}/stats/'
    with concurrent.futures.ThreadPoolExecutor() as pool:
        soup = await asyncio.get_event_loop().run_in_executor(pool, web_scrape, url)
    data = []
    for a in soup.find_all(class_="d3-o-table--horizontal-scroll"):
        data.append(a.get_text())
        player_stats = data[0]
        new_player_stats = re.sub("[\\n]{2,}", "\\n", player_stats)
        no_line_break_player_stats = new_player_stats.split('\n')[1:]
        categories = []
        final_stats = [x.strip() for x in no_line_break_player_stats]
        nfl_years = [str(x) for x in range(1900, 2100)]
        start_of_stats = None
        for position, x in enumerate(final_stats):
            if x in nfl_years:
                start_of_stats = position
                break
            else:
                categories.append(x)
        if start_of_stats is None:
            error_embed = discord.Embed(title = f'No data was found.', color = discord.Color.dark_blue())
            await msg.edit(embed = error_embed)
            return
        stats_minus_categories = final_stats[start_of_stats:]
        for position, x in enumerate(stats_minus_categories):
            if x in nfl_teams and stats_minus_categories[position-2] == year:
                new_stats = stats_minus_categories[position-2:]
                for position, x in enumerate(new_stats):
                    if x != '2020':
                        if x != new_stats[0] and x in nfl_years:
                            year_stats = new_stats[:position]
                            break
                    else:
                        year_stats = new_stats
                continue
            else:
                pass
        year_stats_no_spaces = [x for x in year_stats if x != '']
        break
    categories[categories.index('YEAR')] = 'Year'
    categories[categories.index('TEAM')] = 'Team'
    categories[categories.index('G')] = 'Games'
    print(categories)
    stats = dict(zip(categories, year_stats_no_spaces))
    print(stats)
    final_embed = discord.Embed(
        title = f'{capitalize(first_name)} {capitalize(last_name)}:',
        description = '\n'.join(f'**{k}**: {v}' for k, v in stats.items()),
        color = discord.Color.dark_blue()
    )
    final_embed.set_footer(text = f'Powered by NFL.com | Coded by Rishil_Emperor#0001')
    await msg.edit(embed=final_embed)

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

# !choice <choices>
@client.command(aliases = ['multiplechoice'])
async def choice(ctx, *, items):
    choices = items.split(',')
    choice = random.choice(choices)
    await ctx.send(f'🤔 | I chose: **{choice}**.')

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
        await ctx.send(f'Please make sure you are inputting two numbers, and make sure that the first number is less than the second number.')

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
    if reason[-1] == '.':
        await ctx.send(f'**{member}** has been warned for *{reason}*')
    else:
        await ctx.send(f'**{member}** has been warned for {reason}.')

# !ping
@client.command()
async def ping(ctx):
    msg = await ctx.send(f'Loading...')
    await asyncio.sleep(0.1)
    await msg.edit(content=f'🏓 | **Pong!** `{round(client.latency * 1000)}ms`')

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

