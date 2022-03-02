from discord.ext import commands
import discord
import asyncio
import keep_alive
import requests
from bs4 import BeautifulSoup
from PIL import Image
import numpy as np
import scipy
import scipy.misc
import scipy.cluster
from replit import db

intents = discord.Intents().all()
client = commands.Bot(command_prefix='!', intents=intents)
name_dict = {'aonkeeper4':'dylan','DerpyChicken86':'henry','greenlemonworm':'lime','fluctuatingworm':'harry','ill_clap_ur_nan':'seb','nebula_beann':'nico','RocksEatSocks':'rachel','blue!':'blue','worm.child':'lime','generic':'johnny','threapster':'toby'}
bads=[]

def get_bads():
    import urllib
    url="https://www.cs.cmu.edu/~biglou/resources/bad-words.txt"
    file = urllib.request.urlopen(url)
    for line in file:
        decoded_line = line.decode("utf-8")
        if decoded_line!="\n":
            bads.append(decoded_line.rstrip("\n"));
    bads.sort(key=len,reverse=True)
get_bads()

@client.event
async def on_ready():
    print('Bot is ready!')

@client.command(help="Makes a message pg")
async def pg(ctx,message_id=None):
    import re
    guild = ctx.message.guild
    my_role = discord.utils.get(guild.roles, name='quotebook')
    bot_role = discord.utils.get(guild.roles, name='bot')
    if not (discord.Permissions(administrator=True) < my_role.permissions or discord.Permissions(administrator=True) < bot_role.permissions):
        await ctx.send('I need the Administrator permission to work.')
        return 
    msg_check = lambda m: m.id != ctx.channel.last_message_id and (not m.content.startswith('!')) and m.author!=client.user
    if message_id is not None:
        msg = await ctx.channel.fetch_message(message_id)
    else:
        msg = discord.utils.find(msg_check, await ctx.channel.history(limit=200).flatten())
    
    pgcontent=msg.content
    for word in bads:
        pgre = re.compile(re.escape(word), re.IGNORECASE)
        pgcontent=pgre.sub('####', pgcontent)
        
    if pgcontent!=msg.content:
        await msg.delete()
        await msg.channel.send("PG cleaned: ("+name_dict.get(msg.author.name, msg.author.display_name)+") "+pgcontent)
    else:
        await msg.channel.send("No need to clean")

async def pp_enlarge(ctx, msg):
    if any(pp in msg.content.lower() for pp in ['pp', 'dick', 'cock', 'willy', 'penis', 'schlong', 'dicc', 'cocc', 'balls', 'weiner']):
        try:
            pp_length = db[msg.author.id]
        except KeyError:
            pp_length = 0
        pp_length += 1
        await ctx.send('8'+'='*pp_length+'D')
        db[msg.author.id] = pp_length
    else:
        await client.process_commands(msg)

async def putSus(ctx):
    if ctx.content=="!whosus" or client.user.id==ctx.author.id:
        return

    if "sus" in ctx.content.lower():
        await ctx.channel.send("https://www.youtube.com/watch?v=0bZ0hkiIKt0")

@client.command(help="Vote in a poll")
async def vote(ctx,v):
    poll_options=[]
    allvotes=[]
    with open("poll","r") as f:
        poll_options=f.readline().rstrip("\n").split(":")[1].split(",")
        allvotes=f.readlines()
    for vote in allvotes:
        if str(ctx.author.id)==vote.split("-")[0]:
            await ctx.channel.send("You have already voted! You chose "+vote.split("-")[1])
            return
    if v in poll_options:
        with open("poll","a") as f:
            f.write("\n"+str(ctx.message.author.id)+"-"+v)
        await ctx.channel.send("Your vote has been recorded!")
    else:
        await ctx.channel.send("'"+v+"' is not a voting option. Options available: "+",".join(poll_options))

@client.command(help="Start a poll with name and options")
async def initpoll(ctx,name,*pollopt):
    if ":" in ctx.message.content or "," in ctx.message.content:
        await ctx.channel.send("Your poll name or options included an invalid character ':' or ','")
    else:
        with open("poll","w") as f:
            f.write(name+":"+",".join(pollopt))
        await ctx.channel.send("Started poll "+name)

@client.command(help="Display info about the current poll")
async def currentpoll(ctx):
    l1=""
    with open("poll","r") as f:
        l1=f.readline().rstrip("\n")
    await ctx.channel.send("Current vote: "+l1.split(":")[0]+"\nOptions:"+l1.split(":")[1])

@client.command(help="Show the results of the poll")
async def pollresults(ctx):
    lines=[]
    with open("poll","r") as f:
        lines=f.readlines()
    await ctx.channel.send("Results for poll "+lines[0].split(":")[0]+":")
    results={x:0 for x in lines[0].split(":")[1].rstrip("\n").split(",")}
    for vote in lines[1:]:
        results[vote.split("-")[1].rstrip("\n")]=results[vote.split("-")[1].rstrip("\n")]+1
    for k in results:
        await ctx.channel.send(k+": "+str(results[k]))



async def incorrectquote(ctx, *, people=None):
    import random
    async with ctx.typing():
        if people is None:
            people = [random.choice(list(name_dict.keys)) for i in range(random.randint(1, 6))]
        else:
            people = people.split(',')
        site = 'https://blockpalettes.com/palette/'+str(random.randint(1, 3300)).zfill(4)
        response = requests.get(site)
        soup = BeautifulSoup(response.content, 'html.parser')

@client.command()
async def regenpp(ctx,p,pp):
    if str(ctx.author.id)=="756092813350928465":
        db[str(p)]=int(pp)
        ctx.reply("okkkkkkk")
    else:
        ctx.reply("lol no")

jacobs=[]
@client.command()
async def dellink(ctx):
    if str(ctx.author.id)=="581747620633116692":
        await jacobs.pop().delete()
    else:
        await ctx.channel.send("Only Jacob can delete his links and images!")

async def censor(ctx):
    if str(ctx.author.id)!="581747620633116692":
        return
    import re
    regex = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
    
    ,re.IGNORECASE)
    if re.match(regex,ctx.content) is not None:
        await ctx.delete()
        jacobs.append(await ctx.channel.send("Jacob sent a link - beware! Message: ||"+ctx.content+"||"))
    if len(ctx.attachments):
        await ctx.delete()
        if len(ctx.content)>0:
            await ctx.channel.send("Jacob sent a message with attachments - beware! Message: ||"+ctx.content+"||")
        else:
            await ctx.channel.send("Jacob sent some attachments - beware!")
        for file in ctx.attachments:
            
            file.filename = f"SPOILER_{file.filename}"
            spoiler = await file.to_file()
            jacobs.append(await ctx.channel.send(file=spoiler))
        

@client.event
async def on_message(msg):
    try:
        await pp_enlarge(msg.channel, msg)
        await putSus(msg)
        await censor(msg)
    except discord.errors.HTTPException as e:
        await handleHTTPErr(e)
    finally:
        await client.process_commands(msg)

@client.command(help='mm beans')
async def bean(ctx):
    bc=0
    with open("beans","r") as f:
        bc=int(f.readline().rstrip("\n"))
    with open("beans","w") as f:
        f.write(str(bc+1))
    await ctx.channel.send("Added 1 bean to the bean pile! The bean count is now "+str(bc+1))
   
@client.command()
async def countdown(ctx):
    import datetime
    await ctx.channel.send("\\:(")
    await ctx.channel.send(str((datetime.datetime(2023,1,8)-datetime.datetime.now()).days)+" days to go")

pg_days=("Musical Monday","Trigonometry Tuesday","PG Wednesday","Circumcision Thursday","Femboy Friday","Sacrificial Saturday","Sussalicious Sunday")
@client.command()
async def day(ctx):
    import datetime
    wkd=datetime.datetime.now().weekday()
    await ctx.channel.send(pg_days[wkd])

susness=(" vented"," killed cyan"," bonked red"," oofed yellow"," sabotaged lights"," is sussy"," sus")
@client.command()
async def whosus(ctx):
    import random
    await ctx.channel.send(random.choice(list(name_dict.values()))+random.choice(list(susness)))

@client.command()
async def active(ctx):
    await ctx.channel.send("Active!")

#@client.command()
async def image(ctx):
    a="ono i broke"
    async with ctx.typing():
        a=await getRandomImage()
    await ctx.channel.send(a)

async def word():
    import random
    chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
    return "".join([random.choice(chars) for i in range(random.randint(3,9))])

async def getRandomImage():
    url = "https://google-search3.p.rapidapi.com/api/v1/images/q="+await word()

    headers = {
        'x-rapidapi-key':"9611c217a2msh2d12af09b1d75d5p189796jsna4d831db24ec",
        'x-rapidapi-host': "google-search3.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers)

    return response.json()["image_results"][0]["image"]["src"]


@client.command(help='Sends last message from channel to #quotebook',aliases=['qb','quote'])
async def quotebook(ctx, message_id=None):
    guild = ctx.message.guild
    my_role = discord.utils.get(guild.roles, name='quotebook')
    bot_role = discord.utils.get(guild.roles, name='bot')
    if not (discord.Permissions(administrator=
                                True) < my_role.permissions or discord.Permissions(administrator=True) < bot_role.permissions):
        await ctx.send('I need the Administrator permission to work.')
        return 
    msg_check = lambda m: m.id != ctx.channel.last_message_id and not m.content.startswith('!')
    if message_id is not None:
        msg = await ctx.channel.fetch_message(message_id)
    else:
        msg = discord.utils.find(msg_check, await ctx.channel.history(limit=200).flatten())
    user_name = name_dict.get(msg.author.name, msg.author.display_name) 
    quotebook = discord.utils.get(guild.channels,name='quotebook')
    await quotebook.send(f'"{msg.content}" - {user_name}')

def block_name_format(url):
    url = url.split('/')[-1][:-4]
    return url.replace('_', ' ').title()

def stitch_palette(*imgs):
    img_width = imgs[0].width
    img_height = imgs[0].height
    dst = Image.new('RGBA', (img_width*3, img_height*2))
    for i, img in enumerate(imgs):
        dst.paste(img, ((i%3)*img_width, (i//3)*img_height))
    dst = dst.resize((192, 128), Image.NEAREST)
    return dst

def get_dominant_colour(img, rgba=False):
    ar = np.asarray(img)
    shape = ar.shape
    ar = ar.reshape(np.product(shape[:2]), shape[2]).astype(float)
    codes, dist = scipy.cluster.vq.kmeans(ar, 5)
    vecs, dist = scipy.cluster.vq.vq(ar, codes)
    counts, bins = np.histogram(vecs, len(codes))
    index_max = np.argmax(counts)
    peak = codes[index_max]
    return [int(c) for c in (peak[:-1] if rgba else peak)]

async def get_palette_file_embed(ctx, block):
    from random import randint, choice
    if block is None:
        site = 'https://blockpalettes.com/palette/'+str(randint(1, 6000)).zfill(4)
    else:
        site = 'https://blockpalettes.com/palettes?block='+block
    try:
        response = requests.get(site)
    except requests.exceptions.ConnectionError:
        await ctx.send('Connection refused')
        return
    soup = BeautifulSoup(response.content, 'html.parser')
    if block is None:
        img_tags = soup.find_all('img', 'block')
        urls = ['https://blockpalettes.com'+img['src'][2:] for img in img_tags][:6]
    else:
        # TODO: fix this so we dont need the loop
        palettes_div = soup.find('div', 'palettes')
        palettes = palettes_div.findChildren("div", {"class": "palette-float"})
        palette_addrs = [palette.find('a') for palette in palettes]
        print(palette_addrs)
        palette_addr = choice(palette_addrs)
        # failed = True
        # protection = 0
        # while failed:
        #     site = palette['href']
        #     print(site)
        #     try:
        #         response = requests.get(site)
        #     except requests.exceptions.ConnectionError:
        #         await ctx.send('Connection refused')
        #         return
        #     except requests.exceptions.MissingSchema:
        #         palette = choice(palettes)
        #         protection += 1
        #         if protection > 100:
        #             await ctx.send("Cannot find that palette")
        #             return
        #     else:
        #         failed = False
        response = requests.get(palette_addr["href"])
        soup = BeautifulSoup(response.content, 'html.parser')
        img_tags = soup.find_all('img', 'block')
        urls = ['https://blockpalettes.com'+img['src'][2:] for img in img_tags][:6]
    
    images = []
    for i, url in enumerate(urls):
        response = requests.get(url)
        with open(f'blocks/image{i}.png', 'wb') as f:
            f.write(response.content)
        images.append(Image.open(f'blocks/image{i}.png'))
    stitched_img = stitch_palette(*images)
    stitched_img.save('palette.png')
    colour = get_dominant_colour(stitched_img, True)
    description = '\n'.join([block_name_format(url) for url in urls])
    embed = discord.Embed(title='Random Block Palette', description=description, colour=discord.Colour.from_rgb(*colour))
    file = discord.File("palette.png", filename="image.png")
    embed.set_image(url='attachment://image.png')
    embed.set_footer(text='Dominant colour: '+'#%02x%02x%02x'%tuple(colour))
    return file, embed
        
@client.command()
async def palette(ctx, block=None):
    async with ctx.typing():
        file, embed = await get_palette_file_embed(ctx, block)
        pass
    await ctx.send(file=file, embed=embed)

@client.command()
async def rank(ctx):
    rankings = ('{0:^40}|{1:^9}\n'+'-'*40+'+---------').format('Name', 'PP Size')
    rankdict=dict(db)
    for k in db.keys():
        rankdict[k]=db[k]
    
    #sort rank dict heremmmmm is also break for some reason hang on fixed it yay
    rankdict={k: v for k, v in sorted(rankdict.items(), key=lambda item: item[1], reverse=True)}

    for k in rankdict.keys():
        try:
            user = ctx.message.guild.get_member(int(k))
            rankings += '\n{0:^40}|{1:^9}'.format(user.display_name, str(rankdict[k]))
        except AttributeError as e:
            print("Raised "+str(e)+" for k: '"+str(k)+"'")
    
    embed = discord.Embed(title='PP Rankings', description=f'```{rankings}```', colour=discord.Colour.blue())
    await ctx.send(embed=embed)

@client.command()
@commands.has_role('furry')
async def clearscores(ctx, _id=None):
    if _id is None:
        for k in db.keys():
            del db[k]
        await ctx.send('Scores cleared! Reminder: no spamming')
    else:
        try:
            del db[_id]
            await ctx.send("EL SUSSY BOY YOU HAVE BEEN CLEARED")
        except KeyError:
            await ctx.send("Invalid id "+str(k))

@client.command()
async def killpp(ctx, _id):
    if str(ctx.author.id)=="756092813350928465":
        try:
            del db[_id]
            await ctx.send("EL SUSSY BOY YOU HAVE BEEN CLEARED")
        except KeyError:
            await ctx.send("Invalid id "+str(_id))
    else:
        ctx.reply("lol no")

@client.command()
async def stop(ctx):
    await client.logout()

keep_alive.keep_alive()
async def handleHTTPErr(e):
    print(e.response.headers["Retry-After"]+" seconds until rate limiting over")

import os
try:
    client.run(os.environ['token'])
except discord.errors.HTTPException as e:
    asyncio.run(handleHTTPErr(e))

